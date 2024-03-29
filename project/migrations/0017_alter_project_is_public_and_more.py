# Generated by Django 4.1.9 on 2023-07-24 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('project', '0016_alter_project_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='is_public',
            field=models.BooleanField(default=False, help_text='if True - acessible for all visitors'),
        ),
        migrations.AlterField(
            model_name='project',
            name='representative_image',
            field=models.ForeignKey(blank=True, help_text='picture of the representative of the project', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
