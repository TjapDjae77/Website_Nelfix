from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class PostModel(models.Model):
#     judul   = models.CharField(max_length = 100)
#     body    = models.TextField()
#     author  = models.CharField(max_length = 100)

#     LIST_CATEGORY = (
#         ('Jurnal', 'jurnal'),
#         ('Berita', 'berita'),
#         ('Gosip', 'gosip'),
#     )

#     category= models.CharField(
#         max_length= 100,
#         choices = LIST_CATEGORY,
#         default='jurnal',
#     )

#     def __str__(self) -> str:
#         return "{}. {}".format(self.id, self.judul)

# class Movie(models.Model):
#     title = models.CharField(max_length=150)
#     description = models.TextField()
#     director = models.CharField(max_length=80)
#     release_year = models.PositiveIntegerField()
#     genre = models.JSONField(default=list)
#     price = models.IntegerField()
#     duration = models.PositiveIntegerField(help_text="Duration in seconds")
#     video_url = models.URLField(blank=True, null=True)
#     cover_image_url = models.URLField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self) -> str:
#         return self.title
    
# class CustomUser(AbstractUser):
#     balance = models.IntegerField()
#     bio = models.TextField(max_length=500, blank=True)

#     groups = models.ManyToManyField(
#         Group,
#         related_name='customuser_set',
#         blank=True,
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#         verbose_name='groups',
#     )

#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='customuser_set',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions',
#     )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'