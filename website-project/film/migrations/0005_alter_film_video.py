# Generated by Django 5.1 on 2024-08-20 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0004_remove_film_cover_image_url_remove_film_video_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='video',
            field=models.FileField(upload_to='videos/'),
        ),
    ]