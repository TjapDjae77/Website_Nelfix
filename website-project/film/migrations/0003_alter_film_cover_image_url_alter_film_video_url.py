# Generated by Django 5.1 on 2024-08-18 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0002_alter_film_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='cover_image_url',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='film',
            name='video_url',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
