from django.contrib.auth.models import User
from django.db import models
from film.models import Film

# Create your models here.

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