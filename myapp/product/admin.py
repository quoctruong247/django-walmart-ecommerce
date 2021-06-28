import admin_thumbnails
from django.contrib import admin
from .models import *
from mptt.admin import DraggableMPTTAdmin


class CategoryLangInline(admin.TabularInline):
    model = CategoryLang
    extra = 1
    show_change_link = True
    prepopulated_fields = {'slug': ('title',)}


# Register your models here.
class CategoryAdmin1(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug':('title',)}
    inlines = [CategoryLangInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at', 'image_tag']


class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True

@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image','title','image_thumbnail']


class ProductLangInline(admin.TabularInline):
    model = ProductLang
    extra = 1
    show_change_link = True
    prepopulated_fields = {'slug': ('title',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created_at', 'image_tag']
    inlines = [ProductImageInline,ProductVariantsInline,ProductLangInline]
    readonly_fields = ('image_tag',)
    prepopulated_fields = {'slug':('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'rate', 'ip', 'user', 'product',  'created_at']
    readonly_fields = ('subject', 'comment', 'rate', 'ip', 'user', 'product')


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code','color_tag']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','code']


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','size','price','quantity','image_tag']


class ProductLangugaeAdmin(admin.ModelAdmin):
    list_display = ['title','lang','slug']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['lang']


class CategoryLangugaeAdmin(admin.ModelAdmin):
    list_display = ['title','lang','slug']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['lang']


admin.site.site_header = "E-commerce - Admin Tutorial Dashboard"
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin1)
admin.site.register(Product, ProductAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Variants,VariantsAdmin)
admin.site.register(ProductLang,ProductLangugaeAdmin)
admin.site.register(CategoryLang,CategoryLangugaeAdmin)

