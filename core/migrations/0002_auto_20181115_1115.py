# Generated by Django 2.1.3 on 2018-11-15 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='department_images',
            new_name='picture',
        ),
    ]