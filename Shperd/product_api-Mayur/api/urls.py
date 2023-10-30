from django.urls import path
from . import views
from .views import filter_product_by_type

urlpatterns = [
    path('', views.productApiOverview, name='Product-api-overview'),

    path('product-list/', views.showAll, name='List of all products'),
    path('product-details/<int:id>/', views.product_detail, name='Details of particular product'),
    path('create-product/', views.create_product, name='Create a product'),
    path('update-product/<int:id>/', views.update_product, name='Update a product'),
    path('delete-product/<int:id>/',views.delete_product, name='Delete the product'),

    path('table/', views.get_table_products, name='Get the products for table'),

    path('products/by_type/<str:product_type>/', views.filter_product_by_type, name='Filter product by product type with Pagination'),
    path('products/by-tags', views.filter_products_by_tags, name='Filter Product by multiple/single tags with Pagination'),
]