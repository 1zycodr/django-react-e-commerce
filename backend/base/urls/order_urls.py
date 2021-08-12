from django.urls import path
from base.views import order_views as views

urlpatterns = [
    path('add/', views.add_order_items, name='add_order_items'),
    path('<int:pk>/deliver', views.update_order_to_delivered, name='update_order_to_delivered'),
    path('myorders/', views.get_user_orders, name='get_user_orders'),
    path('', views.get_orders, name='get_orders'),
    path('<int:pk>', views.get_order_by_id, name='get_order_by_id'),
    path('<int:pk>/pay/', views.update_order_to_paid, name='update_order_to_paid'),
]