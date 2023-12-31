# Generated by Django 2.2.4 on 2019-09-04 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190904_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='shown_in_footer_legal',
            field=models.BooleanField(default=False, help_text='Should a link to the page in the footer be displayed?', verbose_name='Shown in the footer section legal'),
            preserve_default=False,
        ),
    ]
