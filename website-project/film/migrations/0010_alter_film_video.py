# Generated by Django 5.1 on 2024-08-22 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0009_alter_film_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='video',
            field=models.FileField(upload_to='videos/'),
        ),
    ]