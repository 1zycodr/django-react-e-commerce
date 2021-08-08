from django.urls import path
from base.views import product_views as views

urlpatterns = [
    path('', views.get_products, name='products'),
    path('<str:pk>/', views.get_product, name='product'),
    path('create', views.create_product, name='create_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('update/<int:pk>', views.update_product, name='update_product'),
]
