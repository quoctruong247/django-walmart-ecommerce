from django.contrib import admin
from .models import *


# Register your models here.
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'address', 'phone', 'status']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'ip', 'status']
    readonly_fields = ('name', 'email', 'subject', 'message', 'ip')
    list_filter = ['status']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer','ordernumber','lang','status']
    list_filter = ['status','lang']


class LanguagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'code','status']
    list_filter = ['status']


class SettingLangAdmin(admin.ModelAdmin):
    list_display = ['title', 'keywords','description','lang']
    list_filter = ['lang']


admin.site.register(Setting, SettingAdmin)
admin.site.register(SettingLang,SettingLangAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(FAQ,FAQAdmin)
admin.site.register(Language,LanguagesAdmin)