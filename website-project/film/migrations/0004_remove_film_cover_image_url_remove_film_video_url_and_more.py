# Generated by Django 5.1 on 2024-08-20 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0003_alter_film_cover_image_url_alter_film_video_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='cover_image_url',
        ),
        migrations.RemoveField(
            model_name='film',
            name='video_url',
        ),
        migrations.AddField(
            model_name='film',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='film',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]
