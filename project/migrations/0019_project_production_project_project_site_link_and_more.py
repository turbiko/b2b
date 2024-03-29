# Generated by Django 4.1.9 on 2023-09-03 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0018_delete_filestofolder'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='production',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Production'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_site_link',
            field=models.URLField(blank=True, null=True, verbose_name='Project site link'),
        ),
        migrations.AddField(
            model_name='project',
            name='running_time_minutes',
            field=models.IntegerField(blank=True, null=True, verbose_name='Running time'),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Status'),
        ),
    ]
