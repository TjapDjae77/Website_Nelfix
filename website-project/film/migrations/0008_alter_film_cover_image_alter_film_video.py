# Generated by Django 5.1 on 2024-08-22 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0007_alter_film_cover_image_alter_film_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='film',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]
