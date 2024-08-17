from django.db import models

# Create your models here.
class Film(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    director = models.CharField(max_length=80)
    release_year = models.PositiveIntegerField()
    genre = models.JSONField(default=list)
    price = models.IntegerField()
    duration = models.DurationField()
    video_url = models.URLField(blank=True, null=True)
    cover_image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title