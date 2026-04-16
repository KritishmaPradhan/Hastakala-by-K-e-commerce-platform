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
    path('wishlist/', views.wishlist_page, name='wishlist'),
    path('api/wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
    path('api/wishlist/check/<int:product_id>/', views.check_wishlist, name='check_wishlist'),
    path('cart/', views.cart_page, name='cart'),
    path('api/cart/add/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('api/cart/update/', views.update_cart_item, name='update_cart_item'),
    path('api/cart/info/', views.get_cart_info, name='get_cart_info'),
]

