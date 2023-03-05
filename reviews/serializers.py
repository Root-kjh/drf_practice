from rest_framework import serializers
from .models import Review, Category, Object

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"