# Generated by Django 4.1.9 on 2023-07-23 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0015_newspage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['date'], 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
    ]
