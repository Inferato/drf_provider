from rest_framework import serializers
from .models import Post
from comments.serializers import CommentSerializer

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'comments']
