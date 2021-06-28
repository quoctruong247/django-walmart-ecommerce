from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('addtoshopcart/<int:id>', addtoshopcart, name='addtoshopcart'),
    path('deletefromecart/<int:id>', deletefromecart, name='deletefromcart'),
    path('checkout/', checkout, name='checkout'),
    path('orderproduct/', orderproduct, name='orderproduct'),
]