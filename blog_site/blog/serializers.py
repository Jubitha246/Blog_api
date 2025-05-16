from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog,Comment,Like

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password']
        
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class BlogSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'
    
    def get_likes_count(self,obj):
        return Like.objects.filter(blog=obj).count()

    def get_comments_count(self,obj):
        return Comment.objects.filter(blog=obj).count()
    
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Like
        fields = '__all__'


