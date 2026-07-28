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
    path('checkout/', views.checkout, name='checkout'),
    path('order/summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('orders/', views.my_orders, name='my_orders'),
    path('store-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('store-admin/products/', views.admin_products, name='admin_products'),
    path('store-admin/products/new/', views.admin_new_product, name='admin_new_product'),
    path('store-admin/products/<int:product_id>/edit/', views.admin_edit_product, name='admin_edit_product'),
    path('store-admin/products/<int:product_id>/delete/', views.admin_delete_product, name='admin_delete_product'),
    path('store-admin/orders/', views.admin_orders, name='admin_orders'),
    path('store-admin/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
]

