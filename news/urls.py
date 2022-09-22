from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('news', views.NewsViewSet, basename='news')
router.register('statuses', views.StatusViewSet, basename='statuses')

urlpatterns = [
    path('', include(router.urls)),
    path('news/<int:news_id>/comments/', views.CommentListCreateAPIView.as_view()),
    path('news/<int:news_id>/comments/<int:id>/', views.CommentRetrieveUpdateDestroyAPIView.as_view()),
    path('news/<int:news_id>/<str:slug>/', views.PostNewsStatus.as_view()),
    path('news/<int:news_id>/comment/<int:comment_id>/<str:slug>/', views.PostCommentStatus.as_view()),
]
