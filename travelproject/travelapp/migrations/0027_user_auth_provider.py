# Generated by Django 4.0.3 on 2022-05-16 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelapp', '0026_news_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auth_provider',
            field=models.CharField(default='default', max_length=255),
        ),
    ]
