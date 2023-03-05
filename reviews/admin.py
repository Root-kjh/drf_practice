from django.contrib import admin

from .models import Category, Object, Review

admin.site.register(Category)
admin.site.register(Object)
admin.site.register(Review)