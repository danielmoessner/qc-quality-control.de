from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.db import models
from django.conf import settings

from cache_memoize import cache_memoize
from random import randint
import os


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=400)
    sub = models.CharField(max_length=200, blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['slug']

    def __str__(self):
        return self.slug.replace('-', ' ')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.set_slug(commit=False)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def is_bottom(self):
        if self.children.exists():
            return False
        return True

    def set_slug(self, slug=None, commit=False):
        if slug:
            self.slug = slug
        else:
            self.slug = slugify(self.get_parent_names())
            if Category.objects.filter(slug=self.slug).exists():
                self.slug = randint(1, 100000)
        if commit:
            self.save()

    def get_children(self):
        children = self.children.all()
        for c in children:
            children = children | c.get_children()
        return children

    def get_parents(self):
        parent = self.parent
        if parent:
            parents_query = Category.objects.filter(pk=self.parent.pk) | parent.get_parents()
        else:
            parents_query = Category.objects.none()
        return parents_query

    @cache_memoize(60 * 60 * 24)
    def get_bottom(self):
        children = self.children.all()
        bottom_query = Category.objects.none()
        if children.exists():
            for c in children:
                bottom_query = bottom_query | c.get_bottom()
        else:
            bottom_query = Category.objects.filter(pk=self.pk)
        return bottom_query

    @cache_memoize(60 * 60 * 24)
    def get_products(self):
        products = self.products_m2m.all()
        for c in self.children.all():
            products = products | c.get_products()
        return products

    @cache_memoize(60 * 60 * 24)
    def get_files(self):
        files = self.files_m2m.all()
        for c in self.children.all():
            files = files | c.get_files()
        return files

    def get_parent_names(self):
        if not self.parent:
            return self.name
        else:
            return self.parent.get_parent_names() + ' > ' + self.name

    def invalidate_cache(self):
        self.get_bottom.invalidate(self)
        self.get_products.invalidate(self)
        self.get_files.invalidate(self)
        self.get_children_html.invalidate(self)

    @cache_memoize(60 * 60 * 24)
    def get_children_html(self):
        children = list(self.children.all())
        name = self.name
        slug = self.slug
        if not children:
            href = reverse_lazy('content:products', args=[slug])
            html = '<li class="list-item"><a href="{}" class="list-link">{}</a></li>'\
                .format(href, name)
        else:
            href = '#{}'.format(slug)
            content = ''.join([c.get_children_html() for c in children])
            html = '<li class="list-item"><a href="{}" data-toggle="collapse" aria-expanded="false" ' \
                   'class="dropdown-toggle list-link">{}</a><ul class="collapse list" id="{}">{}</ul></li>'\
                .format(href, name, slug, content)
        return html


class File(models.Model):
    categories = models.ManyToManyField(Category, related_name='files_m2m')
    file = models.FileField(upload_to='products/files/')
    name = models.CharField(max_length=200)
    sub = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=400, blank=True)
    
    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.set_slug(commit=False)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def get_filename(self):
        return os.path.basename(self.file.name)

    def set_slug(self, slug=None, commit=False):
        if slug:
            self.slug = slug
        else:
            self.slug = slugify(self.name)
            if File.objects.filter(slug=self.slug).exists():
                self.slug = randint(1, 100000)
        if commit:
            self.save()
            

class Product(models.Model):
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    categories = models.ManyToManyField(Category, related_name='products_m2m')
    image = models.ImageField(upload_to='products/')
    name = models.CharField(max_length=200)
    sub = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=400, blank=True)
    # custom
    deletion_mark = models.BooleanField(default=False, blank=True, null=True)
    image_mark = models.BooleanField(default=False, blank=True, null=True)
    category_mark = models.BooleanField(default=False, blank=True, null=True)
    text_mark = models.BooleanField(default=False, blank=True, null=True)
    notes_mark = models.CharField(max_length=1000, default='', blank=True, null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.set_slug(commit=False)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def set_deletion_mark(self):
        self.deletion_mark = not self.deletion_mark
        self.save()

    def set_image_update_mark(self):
        self.image_mark = not self.image_mark
        self.save()

    def set_category_upate_mark(self):
        self.category_mark = not self.category_mark
        self.save()

    def set_text_update_mark(self):
        self.text_mark = not self.text_mark
        self.save()

    def set_notes_mark(self, text):
        self.notes_mark = text
        self.save()

    def set_slug(self, slug=None, commit=False):
        if slug:
            self.slug = slug
        else:
            self.slug = slugify(self.name)
            if Product.objects.filter(slug=self.slug).exists():
                self.slug = randint(1, 100000)
        if commit:
            self.save()
