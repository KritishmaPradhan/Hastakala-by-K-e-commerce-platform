from django.urls import path
from . import views

app_name = 'hasta_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('api/carousel/', views.api_carousel_items, name='api_carousel'),
]
