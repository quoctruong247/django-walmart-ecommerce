from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.utils.safestring import mark_safe
from home.models import Language
from currencies.models import Currency


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    image = models.ImageField(blank=True, upload_to='user')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_decription = 'Image'