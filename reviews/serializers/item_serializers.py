from rest_framework import serializers

from ..models import Item
from .review_serializers import ReviewSerializer

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ItemDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Item
        fields = "__all__"