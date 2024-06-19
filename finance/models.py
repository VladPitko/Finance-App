from django.contrib.auth.models import User
from django.db import models
from django.template.defaulttags import now


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True)


    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Budget(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f'{self.description} - {self.amount}'


class Tag(models.Model):
    name = models.CharField(max_length=50)
    transactions = models.ManyToManyField(Transaction, related_name='tags')

    def __str__(self):
        return self.name
