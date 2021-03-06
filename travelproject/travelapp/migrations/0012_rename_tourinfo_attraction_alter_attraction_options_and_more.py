# Generated by Django 4.0.3 on 2022-05-02 08:44

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travelapp', '0011_remove_imagetour_tour_info_imagetour_tour_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TourInfo',
            new_name='Attraction',
        ),
        migrations.AlterModelOptions(
            name='attraction',
            options={},
        ),
        migrations.RemoveField(
            model_name='tour',
            name='tour_info',
        ),
        migrations.AddField(
            model_name='tour',
            name='attraction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tours', to='travelapp.attraction'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='note',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
