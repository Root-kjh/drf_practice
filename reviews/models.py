from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    context = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.name
    