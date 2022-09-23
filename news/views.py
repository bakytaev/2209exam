from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .permissions import IsAuthorPermission, IsAdminPermission
from .models import News, Comment, Status, NewsStatus, CommentStatus
from .serializers import NewsSerializer, CommentSerializer, StatusSerializer


class NewsViewSet(ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    def get_queryset(self):
        queryset = self.queryset
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author__username=author)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(text__icontains=search)
        return queryset


# class CommentViewSet(ModelViewSet):
#     serializer_class = CommentSerializer
#     queryset = Comment.objects.all()
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [CommentPermission, ]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        return self.queryset.filter(news_id=self.kwargs['news_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            news_id=self.kwargs['news_id']
        )


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def get_object(self):
        obj = get_object_or_404(self.queryset, id=self.kwargs['id'])
        self.check_object_permissions(self.request, obj)
        return obj


class StatusViewSet(ModelViewSet):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminPermission, ]


class PostNewsStatus(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def get(self, request, news_id, slug):
        news = get_object_or_404(News, id=news_id)
        this_status = get_object_or_404(Status, slug=slug)
        try:
            like_dislike = NewsStatus.objects.create(news=news, author=request.user.author, status=this_status)
        except IntegrityError:
            like_dislike = NewsStatus.objects.get(news=news, author=request.user.author)
            if like_dislike.status == this_status:
                like_dislike.status = None
                data = {'delete': f'{request.user.username} deleted status of the news {news_id}'}
            else:
                like_dislike.status = this_status
            like_dislike.save()
            data = {"error": f"news {news_id} has changed status by {request.user.username}"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"message": f"news {news_id} got status from {request.user.username}"}
            return Response(data, status=status.HTTP_201_CREATED)


class PostCommentStatus(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def get(self, request, news_id, comment_id, slug):
        news = get_object_or_404(News, id=news_id)
        comment = get_object_or_404(Comment, id=comment_id)
        this_status = get_object_or_404(Status, slug=slug)
        try:
            like_dislike = CommentStatus.objects.create(comment=comment, user=request.user.author, status=this_status)
        except IntegrityError:
            like_dislike = CommentStatus.objects.get(comment=comment, user=request.user)
            if like_dislike.status == this_status:
                like_dislike.status = None
            else:
                like_dislike.status = this_status
                data = {"message": f"comment {comment.text} - to news - {news.title} - \
                got {like_dislike.status.slug} from {request.user.username}"}
            like_dislike.save()
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"message": f"comment {comment_id} got status from {request.user.username}"}
            return Response(data, status=status.HTTP_201_CREATED)
