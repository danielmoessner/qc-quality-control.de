# Generated by Django 2.2.4 on 2019-09-02 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
