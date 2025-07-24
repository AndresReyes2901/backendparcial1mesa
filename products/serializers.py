from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    related_products_info = serializers.SerializerMethodField(read_only=True)
    #añadir el campo de imagen
    #img_url = serializers.SerializerMethodField(read_only=True)  # Añadimos el campo de imagen
    # Obtener la URL de la imagen
    #img_url = serializers.URLField(source='img_url', read_only=True)  # Asegúrate de incluir el campo `img_url`
    img_url = serializers.URLField(read_only=True)  # Ya no es necesario `source='img_url'`

    class Meta:
        model = Product
        fields = '__all__'

    def get_related_products_info(self, obj):

        return [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'final_price': product.final_price
            } for product in obj.related_products.filter(
                is_active=True, is_available=True
            )[:3]
        ]

#agregar el get_img_url method para obtener la URL de la imagen
    # Esto es útil si estás usando un campo ImageField o FileField en tu modelo Product
