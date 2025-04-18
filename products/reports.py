from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from orders.models import Order, OrderItem
from datetime import datetime, timedelta
import os


if os.environ.get('DJANGO_SKIP_PANDAS', '') != 'true':
    import pandas as pd
    import io
    from xhtml2pdf import pisa
    from django.template.loader import get_template
    from django.http import HttpResponse
else:

    class MockPD:
        def DataFrame(self, *args, **kwargs): pass
        def ExcelWriter(self, *args, **kwargs): return type('obj', (object,), {'__enter__': lambda s: s, '__exit__': lambda s, *a, **k: None})
    pd = MockPD()
    io = type('io', (), {'BytesIO': type('BytesIO', (), {'seek': lambda s, *a: None, 'read': lambda s: b''})})
    pisa = type('pisa', (), {'CreatePDF': lambda *a, **k: type('PisaStatus', (), {'err': False})()})
    def get_template(template_src):
        return type('Template', (), {'render': lambda s, ctx: ''})
    HttpResponse = lambda *args, **kwargs: None


def generate_client_report(client_id, start_date=None, end_date=None):

    orders = Order.objects.filter(user_id=client_id)

    if start_date:
        orders = orders.filter(created_at__gte=start_date)
    if end_date:
        orders = orders.filter(created_at__lte=end_date)


    orders_data = []
    for order in orders:
        items = OrderItem.objects.filter(order=order)
        orders_data.append({
            'id': order.id,
            'date': order.created_at,
            'total': order.total,
            'status': order.status,
            'items': [
                {
                    'product': item.product.name,
                    'price': item.price,
                    'quantity': item.quantity,
                    'subtotal': item.price * item.quantity
                } for item in items
            ]
        })

    return {
        'client_id': client_id,
        'start_date': start_date,
        'end_date': end_date,
        'orders': orders_data,
        'total_spent': sum(order['total'] for order in orders_data)
    }


def generate_top_products_report(start_date=None, end_date=None, limit=10):

    query = OrderItem.objects.values('product__id', 'product__name')

    if start_date:
        query = query.filter(order__created_at__gte=start_date)
    if end_date:
        query = query.filter(order__created_at__lte=end_date)


    top_products = query.annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_sold')[:limit]

    return {
        'start_date': start_date,
        'end_date': end_date,
        'top_products': list(top_products)
    }


def export_to_excel(data, report_type):

    buffer = io.BytesIO()

    if report_type == 'client':

        orders_df = pd.DataFrame([
            {
                'Orden ID': order['id'],
                'Fecha': order['date'],
                'Total': order['total'],
                'Estado': order['status']
            } for order in data['orders']
        ])


        items_data = []
        for order in data['orders']:
            for item in order['items']:
                items_data.append({
                    'Orden ID': order['id'],
                    'Producto': item['product'],
                    'Precio': item['price'],
                    'Cantidad': item['quantity'],
                    'Subtotal': item['subtotal']
                })
        items_df = pd.DataFrame(items_data)


        with pd.ExcelWriter(buffer) as writer:
            orders_df.to_excel(writer, sheet_name='Órdenes', index=False)
            items_df.to_excel(writer, sheet_name='Detalles', index=False)

    elif report_type == 'top_products':

        df = pd.DataFrame(data['top_products'])
        df.columns = ['ID Producto', 'Nombre', 'Cantidad Vendida', 'Ingreso Total']
        df.to_excel(buffer, index=False)

    buffer.seek(0)
    return buffer


def render_to_pdf(template_src, context_dict):

    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()


    pisa_status = pisa.CreatePDF(html, dest=result)

    if pisa_status.err:
        return None

    result.seek(0)
    return result