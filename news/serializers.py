from rest_framework import serializers

from .models import News, Comment


class NewsSerializer(serializers.ModelSerializer):
    post_username = serializers.ReadOnlyField()
    get_status = serializers.ReadOnlyField()

    class Meta:
        model = News
        fields = "__all__"
        read_only_fields = ['user', ]


class CommentSerializer(serializers.ModelSerializer):
    post_username = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['author', 'news']
