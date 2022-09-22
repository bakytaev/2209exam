from django.db import models
from django.db.models import Count

from account.models import Author


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.__class__.__name__} from {self.author} at {self.updated}'

    @property
    def post_username(self):
        return self.author.user.username


class News(Post):
    title = models.CharField(max_length=100, help_text='news title')
    content = models.TextField(help_text='news content')

    def get_status(self):
        statuses = NewsStatus.objects.filter(news=self).values('status__name').annotate(count=Count('status'))
        result = {}
        for i in statuses:
            result[i['status__name']] = i['count']
        return result

    def __str__(self):
        return f'{self.title} from {self.user.username} at {self.updated}'


class Comment(Post):
    text = models.CharField(max_length=255)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def get_status(self):
        statuses = CommentStatus.objects.filter(comment=self).values('status__name').annotate(count=Count('status'))
        result = {}
        for i in statuses:
            result[i['status__name']] = i['count']
        return result

    def __str__(self):
        return self.text


class Status(models.Model):
    slug = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class NewsStatus(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('author', 'news')


class CommentStatus(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('author', 'comment')


# class DoNewsStatus(models.Model):
#     news = models.ForeignKey(News, on_delete=models.CASCADE)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     status = models.ForeignKey(NewsStatus, on_delete=models.CASCADE, null=True, blank=True)
#
#     class Meta:
#         unique_together = ('author', 'news')
#
#     def __str__(self):
#         return f'{self.news} - {self.author.username} - {self.status.name}'
#
#
# class DoCommentStatus(models.Model):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     status = models.ForeignKey(CommentStatus, on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = ('author', 'comment')
#
#     def __str__(self):
#         return f'{self.comment} - {self.author.username} - {self.status.name}'
