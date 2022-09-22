from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('news', views.NewsViewSet, basename='news')
router.register('comment', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('news/<int:news_id>/<str:status_slug>/', views.PostNewsStatus.as_view()),
    path('news/<int:news_id>/comment/<int:pk>/<str:status_slug>/', views.PostCommentStatus.as_view()),
]
