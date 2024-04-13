from django.urls import path
from .views import *

urlpatterns =[
    path('',index_view , name='index_url'),
    path('account/',account_view , name='account_url'),
    path('about/',about_view , name='about_url'),
    path('blog/',blog_view , name='blog_url'),
    path('blog-single/<int:pk>/',blog_single_view , name='blog_single_url'),
    path('cart/',cart_view , name='cart_url'),
    path('checkout/',checkout_view , name='checkout_url'),
    path('contact/',contact_view , name='contact_url'),
    path('create_contact_us/', create_contact_us, name='create_contact_us_url'),
    path('product-single/<int:pk>/', product_single, name='product_single_url'),
    path('shop/', shop_view, name='shop_url'),
    path('create_order/', create_order, name='create_order_url'),
    path('remove_cart_product/<int:pk>/<int:id>/', remove_cart_product, name='remove_cart_product_url'),
    path('add_basket_form/<int:pk>/', add_basket_form, name='add_basket_form_url'),
    path('add_basket/<int:pk>/', add_basket, name='add_basket_url'),
    path('update_cart/<int:pk>/', update_cart, name='update_cart_url'),
    path('create_comment/<int:pk>/', create_comment, name='create_comment_url'),
    path('login/', login_view, name='login_url'),
    path('edit_profile/', edit_profile, name='edit_profile_url'),
    path('edit_password_user/', edit_password_user, name='edit_password_user_url'),
    path('sing-up/', sing_up_view, name='sing_up_url'),
    path('logout/', user_logout, name='logout_url'),


]