from django.contrib import admin

from .models import Category
from .models import Product
from .models import File
from .forms import CategoryAdminForm
from .forms import ProductAdminForm


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    fieldsets = (
        (None, {
           'fields': ('parent', 'name', 'sub')
        }),
        ('Advanced options', {
            'fields': ('slug', 'icon'),
        }),
    )


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    fieldsets = (
        (None, {
           'fields': ('categories', 'image', 'name', 'sub', 'description')
        }),
        ('Advanced options', {
            'fields': ('slug', 'deletion_mark', 'image_mark', 'category_mark', 'text_mark', 'notes_mark'),
        }),
    )


class FileAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    fieldsets = (
        (None, {
           'fields': ('categories', 'file', 'name', 'sub', 'description')
        }),
        ('Advanced options', {
            'fields': ('slug',),
        }),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(File, FileAdmin)
