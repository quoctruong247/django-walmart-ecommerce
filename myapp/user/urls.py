from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_form, name='login'),
    path('signup/', signup_form, name='signup'),
    path('logout/', logout_form, name='logout'),
    path('userprofile/', userprofile_form, name='userprofile'),

    path('update/', user_update, name='user_update'),
    path('password/', user_password, name='user_password'),
    path('orders/', user_orders, name='user_orders'),
    path('orders_product/', user_order_product, name='user_order_product'),
    path('orderdetail/<int:id>', user_orderdetail, name='user_orderdetail'),
    path('order_product_detail/<int:id>/<int:oid>', user_order_product_detail, name='user_order_product_detail'),
    path('comments/', user_comments, name='user_comments'),
    path('deletecomment/<int:id>', user_deletecomment, name='user_deletecomment'),
]