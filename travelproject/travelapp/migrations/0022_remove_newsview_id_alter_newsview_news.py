# Generated by Django 4.0.3 on 2022-05-12 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travelapp', '0021_newsview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsview',
            name='id',
        ),
        migrations.AlterField(
            model_name='newsview',
            name='news',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='travelapp.news'),
        ),
    ]
