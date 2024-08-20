from django.contrib.auth.models import User
from django.db import models
from film.models import Film

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
    films = models.ManyToManyField(Film, blank=True, related_name='purchased_by')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def add_balance(self, increment):
        self.balance += increment
        self.save()

    def purchase_film(self, film):
        if self.balance >= film.price:
            self.films.add(film)
            self.balance -= film.price
            self.save()
            return True
        return False