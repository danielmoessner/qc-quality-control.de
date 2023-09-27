from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.conf import settings
from django import forms

from .models import Category
from .models import Product
from .models import File

import os


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    company = forms.CharField()
    phone = forms.CharField()
    message = forms.CharField()

    def clean_message(self):
        message = self.cleaned_data['message']
        message = strip_tags(message)
        return message


class NotesForm(forms.Form):
    notes = forms.CharField()


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['parent', 'name', 'sub']
        fields += ['slug', 'icon']

    def clean(self):
        parent = self.cleaned_data['parent']
        icon = self.cleaned_data['icon']
        if parent and parent.products_m2m.exists():
            raise ValidationError('The parent category contains products.')
        if not parent and not icon:
            raise ValidationError('Every category without a parent needs to contain an icon.')
        if icon:
            # hard coded kinda bad i know
            icon_path = os.path.join(settings.APPS_DIR, 'files/dist/img', icon)
            if not os.path.exists(icon_path):
                raise ValidationError('Icon path does not exist.')


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['categories', 'image', 'name', 'sub', 'description']
        fields += ['slug', 'deletion_mark', 'image_mark', 'category_mark', 'text_mark', 'notes_mark']

    def clean(self):
        categories = self.cleaned_data['categories']
        for category in categories:
            if not category.is_bottom():
                raise ValidationError('One or more of the categories is not a bottom category.')


class FilesAdminForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['categories', 'file', 'name', 'sub', 'description']
        fields += ['slug']

    def clean(self):
        categories = self.cleaned_data['categories']
        for category in categories:
            if not category.is_bottom():
                raise ValidationError('One or more of the categories is not a bottom category.')