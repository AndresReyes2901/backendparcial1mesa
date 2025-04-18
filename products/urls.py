from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, simple_client_report_view, simple_top_products_report_view
)

router = DefaultRouter()
router.register(r'', ProductViewSet)

urlpatterns = [

    path('simple-reports/client/', simple_client_report_view, name='simple-client-report'),
    path('simple-reports/top-products/', simple_top_products_report_view, name='simple-top-products-report'),


    path('', include(router.urls)),
]