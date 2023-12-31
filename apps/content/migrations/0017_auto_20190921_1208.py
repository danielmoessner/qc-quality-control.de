# Generated by Django 2.2.4 on 2019-09-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0016_auto_20190918_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category_mark',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='deletion_mark',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_mark',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='notes_mark',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='text_mark',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
