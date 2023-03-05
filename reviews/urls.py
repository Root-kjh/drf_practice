from .views import CategoryViewSet, ObjectViewSet, ReviewViewSet
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'objects', ObjectViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
