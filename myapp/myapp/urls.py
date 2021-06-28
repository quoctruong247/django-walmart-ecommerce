"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
#home
from home import views
from order import views as OrderView
from django.utils.translation import gettext_lazy as _
urlpatterns = [
    path('selectlanguage', views.selectlanguage, name='selectlanguage'),
    path('selectcurrency', views.selectcurrency, name='selectcurrency'),
    path('savelangcur', views.savelangcur, name='savelangcur'),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('currencies/', include('currencies.urls')),
    path(_('admin/'), admin.site.urls),
    path('', include('home.urls')),
    path('product/', include('product.urls')),
    path('order/', include('order.urls')),
    path('user/', include('user.urls')),
    path('search/', views.search, name='search'),
    path('category/<int:id>/<slug:slug>', views.category, name='category'),
    path('product-detail/<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('shopcart/', OrderView.shopcart, name='shopcart'),
    path('faq/', views.faq, name='faq'),
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
    prefix_default_language=False,
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
