from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Blog, Comment, Like
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Blog API")

class RegisterViewSet(viewsets.ViewSet):
    def create(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token':token.key})
        return Response(serializer.errors,status=400)
    

class LoginViewSet(viewsets.ViewSet):
    def create(self,request):
        user = authenticate(username=request.data['username'],password=request.data['password'])
        if user:
            token,_ =Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error':'Invalid credentials'},status=401)
    
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,methods=['post'])
    def like(self,request,pk=None):
        blog = self.get_object()
        Like, created = Like.objects.get_or_create(blog=blog,user=request.user)
        if not created:
            return Response({'detail': 'Already liked'},status=400)
        return Response({'detail':'Liked'},status=200)

    @action(detail=True,methods=['post'])
    def unlike(self,request,pk=None):
        blog = self.get_object()
        deleted, _ = Like.objects.filter(blog=blog,user=request.user).delete()
        if deleted == 0:
            return Response({'detail':'Not liked yet'}, status=400)
        return Response({'detail':'Unliked'}, status=200)

    def retrieve(self,request,*args,**kwargs):
        blog = self.get_object()
        blog_serializer = self.get_serializer(blog)
        latest_comments = Comment.objects.filter(blog=blog).order_by('-created_at')[:5]
        comments_serializer = CommentSerializer(latest_comments, many=True)
        # Combine everything
        data = blog_serializer.data
        data['latest_comments'] = comments_serializer.data
        return Response(data)

class CommentViewSet(viewsets.ModelViewSet):
        serializer_class = CommentSerializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            blog_id = self.request.query_params.get('blog_id')
            if blog_id:
                return Comment.objects.filter(blog__id=blog_id).order_by('-created_at')
            return Comment.objects.all().order_by('-created_at')

        def perform_create(self, serializer):
            serializer.save(user=self.request.user)



            