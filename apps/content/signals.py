from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Category
from .models import Product
from .models import File


@receiver(post_delete, sender=Category)
@receiver(post_save, sender=Category)
def category_saved(sender, instance, **kwargs):
    for c in Category.objects.all():
        c.invalidate_cache()


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def product_saved(sender, instance, **kwargs):
    for c in Category.objects.all():
        c.invalidate_cache()


@receiver(post_save, sender=File)
@receiver(post_delete, sender=File)
def product_saved(sender, instance, **kwargs):
    for c in Category.objects.all():
        c.invalidate_cache()
