from django.urls import path
from base.views import user_views as views

urlpatterns = [
    path('', views.get_users, name='users'),

    path('register', views.register_user, name='register'),
    path('login', views.JWTTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('profile', views.get_user_profile, name='user_profile'),
    path('profile/update/', views.update_user_profile, name='update_user_profile'),

    path('update/<int:pk>/', views.update_user, name='update_user'),
    path('<int:pk>', views.get_user_by_id, name='get_user_by_id'),

    path('delete/<int:pk>/', views.delete_user, name='delete_user')
]