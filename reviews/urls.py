from .views import CategoryViewSet, ItemViewSet, ReviewViewSet
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'items', ItemViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
