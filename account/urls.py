from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('author', views.AuthorViewSet, basename='author')


urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('token/', obtain_auth_token),
    path('', include('rest_framework.urls')),
    path('', include(router.urls)),
]
