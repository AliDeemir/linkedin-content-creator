from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    path('generate-posts', views.GeneratePostsView.as_view(), name='generate-posts'),
    path('verify-api-key', views.verify_api_key, name='verify_api_key'),
    path('', include(router.urls)),
] 