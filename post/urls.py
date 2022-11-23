from django.urls import path
from post.views import (
    PostView, PostDetailView, 
    UploadView, ImageView, 
    CommentView, CommentDetailView, 
    LikeView
)

urlpatterns = [
    path('', PostView.as_view(), name="main_view"),
    path('upload/', UploadView.as_view(), name="post_create_view"),
    path('upload/<int:image_id>/', ImageView.as_view(), name="image_view"),
    path('<int:post_id>/', PostDetailView.as_view(), name="post_detail_view"),
    path('<int:post_id>/like/', LikeView.as_view(), name="like_view"),
    path('<int:post_id>/comment/', CommentView.as_view(), name="comment_view"),
    path('<int:post_id>/comment/<int:comment_id>/', CommentDetailView.as_view(), name="comment_detail_view"),
]
