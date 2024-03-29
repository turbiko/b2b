# Generated by Django 4.1.9 on 2023-06-30 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_remove_contact_company_name_remove_contact_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='company_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='contacts.company'),
        ),
        migrations.AddField(
            model_name='contact',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
