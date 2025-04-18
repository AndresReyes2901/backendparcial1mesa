from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, client_report_view, top_products_report_view

router = DefaultRouter()
router.register(r'', ProductViewSet)

urlpatterns = [

    path('reports/client/', client_report_view, name='client-report'),
    path('reports/top-products/', top_products_report_view, name='top-products-report'),
    path('', include(router.urls)),
]