# Generated by Django 5.1 on 2024-08-21 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0005_alter_film_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]