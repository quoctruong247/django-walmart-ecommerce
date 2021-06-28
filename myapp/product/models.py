from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, Count
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.forms import ModelForm, TextInput
from home.models import Language


# Create your models here.
class ModelClass:
    ## content = models.TextField()
    content = RichTextUploadingField()


class Category(MPTTModel):
    STATUS = (
        ('True', 'On'),
        ('False', 'Off')
    )

    parent = TreeForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=False, unique=True)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to="category")
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs = {'slug':self.slug})

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Product(models.Model):
    STATUS = (
        ('True', 'On'),
        ('False', 'Off')
    )
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=False, unique=True)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    detail = RichTextUploadingField(blank=True)
    image = models.ImageField(blank=True, upload_to="category")
    price = models.FloatField()
    amount = models.IntegerField()
    minamount = models.IntegerField()
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug':self.slug})

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))    
    image_tag.short_decription = 'Image'

    def avaregereview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(avarage=Avg('rate'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank = True, upload_to="product")

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'On'),
        ('False', 'Off')
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']


class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)

    def __str__(self):
        return self.name


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""

llist= Language.objects.all()
list1=[]
for rs in llist:
    list1.append((rs.code,rs.name))
langlist= (list1)


class ProductLang(models.Model):
    # langlist = (
    #     ('en', 'English'),
    #     ('vi', 'Vietnam')
    # )
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #many to one relation with Category
    lang =  models.CharField(max_length=6, choices=langlist)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    slug = models.SlugField(null=False, unique=True)
    detail=RichTextUploadingField()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class CategoryLang(models.Model):
    # langlist = (
    #     ('en', 'English'),
    #     ('vi', 'Vietnam')
    # )
    category = models.ForeignKey(Category, related_name='categorylangs', on_delete=models.CASCADE) #many to one relation with Category
    lang =  models.CharField(max_length=6, choices=langlist)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    slug = models.SlugField(null=False, unique=True)
    description = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


