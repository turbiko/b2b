# Generated by Django 4.1.9 on 2023-07-01 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_alter_contact_company_name_alter_contact_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companystuff',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='CompanyStuff',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
