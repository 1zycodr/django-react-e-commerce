from django.urls import path
from base.views import product_views as views

urlpatterns = [
    path('', views.get_products, name='products'),
    path('<int:pk>/', views.get_product, name='get_product'),
    path('<int:pk>/reviews/', views.create_product_review, name='create_product_review'),
    path('create', views.create_product, name='create_product'),
    path('top', views.get_top_products, name='get_top_products'),
    path('upload', views.upload_image, name='upload_image'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('update/<int:pk>', views.update_product, name='update_product'),
]
