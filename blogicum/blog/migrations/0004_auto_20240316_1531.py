# Generated by Django 3.2.16 on 2024-03-16 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20240312_1937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
