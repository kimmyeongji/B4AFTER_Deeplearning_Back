from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from post.models import Post, Image, Comment
from post.serializers import (
    PostSerializer, PostDetailSerializer, PostCreateSerializer, PostUpdateSerializer,
    ImageSerializer, ImageCreateSerializer,
    CommentSerializer, CommentCreateSerializer
)

class UploadView(APIView):
    def post(self, request):
        serializer = ImageCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            # 이미지 변환 함수
            # serializer.save(after_image=request.image)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageView(APIView):
    def get(self, request, image_id):
        image = get_object_or_404(Image, id=image_id)
        serializer = ImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, image_id):
        image = get_object_or_404(Image, id=image_id)
        serializer = ImageCreateSerializer(image, data=request.data)
        if request.user == image.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('권한이 없습니다', serializer.errors, status=status.HTTP_403_FORBIDDEN)

class PostView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    def get(self, request, post_id):
        post = get_object_or_404(Post,  id=post_id)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.user:
            serializer = PostUpdateSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('권한이 없습니다', status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없습니다', status=status.HTTP_403_FORBIDDEN)

class CommentView(APIView):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentDetailView(APIView):
    def put(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('권한이 없습니다', status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없습니다', status=status.HTTP_403_FORBIDDEN)

class LikeView(APIView):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response('좋아요를 취소했습니다', status=status.HTTP_204_NO_CONTENT)
        else:
            post.likes.add(request.user)
            return Response('좋아요를 했습니다', status=status.HTTP_201_CREATED)