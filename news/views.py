from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .permissions import IsAuthorPermission, CommentPermission


from .models import News, Comment, NewsStatus, CommentStatus
from .serializers import NewsSerializer, CommentSerializer


class NewsViewSet(ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user__username=user)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(text__icontains=search)
        return queryset


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [CommentPermission, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostNewsStatus(APIView):
    def get(self, request, news_id, status_slug):
        news = get_object_or_404(News, id=news_id)
        news_status = get_object_or_404(NewsStatus, slug=status_slug)
        try:
            like_dislike = NewsStatus.objects.create(news=news, user=request.user, status=news_status)
        except IntegrityError:
            like_dislike = NewsStatus.objects.get(news=news, user=request.user)
            if like_dislike.status == news_status:
                like_dislike.status = None
            else:
                like_dislike.status = news_status
            like_dislike.save()
            data = {"error": f"news {news_id} has changed status by {request.user.username}"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"message": f"news {news_id} got status from {request.user.username}"}
            return Response(data, status=status.HTTP_201_CREATED)


class PostCommentStatus(APIView):
    def get(self, request, comment_id, status_slug):
        comment = get_object_or_404(Comment, id=comment_id)
        comment_status = get_object_or_404(CommentStatus, slug=status_slug)
        try:
            like_dislike = CommentStatus.objects.create(comment=comment, user=request.user, status=comment_status)
        except IntegrityError:
            like_dislike = CommentStatus.objects.get(comment=comment, user=request.user)
            like_dislike.status = comment_status
            like_dislike.save()
            data = {"error": f"comment {comment_id} has changed status by {request.user.username}"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"message": f"comment {comment_id} got status from {request.user.username}"}
            return Response(data, status=status.HTTP_201_CREATED)
