# Generated by Django 4.1.9 on 2023-06-30 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_alter_contact_staff_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='email',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='featured_image',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='second_name',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='staff_name',
        ),
    ]