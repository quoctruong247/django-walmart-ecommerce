from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm, TextInput


class Language(models.Model):
    name= models.CharField(max_length=20)
    code= models.CharField(max_length=5)
    status=models.BooleanField()
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


llist = Language.objects.filter(status=True)
list1 = []
for rs in llist:
    list1.append((rs.code,rs.name))
langlist = (list1)


# Create your models here.
class Setting(models.Model):
    STATUS = (
        ('True','On'),
        ('False','Off')
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField()
    keyword = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    smtpserver = models.CharField(blank=True, max_length=20)
    smtpemail = models.CharField(blank=True, max_length=20)
    smtppassword = models.CharField(blank=True, max_length=10)
    smtpport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to="icon")
    facebook = models.CharField(blank=True, max_length=50)
    istagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contactus = RichTextUploadingField(blank=True)
    reference = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SettingLang(models.Model):
    langlist = (
        ('en', 'English'),
        ('vi', 'Vietnam')
    )
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE) #many to one relation with Category
    lang =  models.CharField(max_length=6, choices=langlist)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    aboutus = RichTextUploadingField(blank=True)
    contactus = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    STATUS = (
        ('New','New'),
        ('Read','Read'),
        ('Closed','Closed')
    )

    name = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.TextField(blank=True, max_length=255)
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placdholder': 'Name & surname'}),
            'email': TextInput(attrs={'class': 'input', 'placdholder': 'Email address'}),
            'subject': TextInput(attrs={'class': 'input', 'placdholder': 'Subject'}),
            'message': TextInput(attrs={'class': 'input', 'placdholder': 'Your message', 'rows': '5'}),
        }


class FAQ(models.Model):
    STATUS = (
        ('True', 'On'),
        ('False', 'Off'),
    )
    # langlist = (
    #     ('en', 'English'),
    #     ('vi', 'Vietnam')
    # )
    lang =  models.CharField(max_length=6, choices=langlist, blank=True, null=True)
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()
    status=models.CharField(max_length=10, choices=STATUS)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Language(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=5)
    status = models.BooleanField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


