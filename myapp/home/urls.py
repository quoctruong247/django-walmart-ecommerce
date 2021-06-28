from django.urls import path
from .views import *
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path('', index, name='home'),
    path(_('about/'), about, name='about'),
    path(_('contact/'), contact, name='contact'),
]