"""
Templates app URL configuration.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeTemplateViewSet

router = DefaultRouter()
router.register(r'', ResumeTemplateViewSet, basename='template')

urlpatterns = [
    path('', include(router.urls)),
]
