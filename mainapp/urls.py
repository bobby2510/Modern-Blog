from django.urls import path
from mainapp.views import (
    CreatePost,
    PostDetail,
    DelatePost,
    EditPostView,
    EditPostSave,
    UpvoteView,
    DownvoteView,
    CommentView
)
from mainapp.views_helper import (
    CommentDisplayView,
    CommentEditView,
    CommentDeleteView,
    CommentUpvoteView,
    CommentDownvoteView,
)

app_name='mainapp'
urlpatterns=[
    path('new/',CreatePost,name='newpost'),
    path('<int:id>/',PostDetail,name='post-detail'),
    path('<int:id>/delete/',DelatePost,name='post-delete'),
    path('<int:id>/edit/',EditPostView,name='post-edit'),
    path('<int:id>/edit/save/',EditPostSave,name='post-edit-save'),
    path('<int:id>/upvote/',UpvoteView,name='post-upvote'),
    path('<int:id>/downvote/',DownvoteView,name='post-downvote'),
    path('<int:id>/comment/',CommentView,name='post-comment'),
    path('<int:id>/comment/<int:c_id>/',CommentDisplayView,name='post-comment-view'),
    path('<int:id>/comment/<int:c_id>/save/',CommentEditView,name='post-comment-edit'),
    path('<int:id>/comment/<int:c_id>/delete/',CommentDeleteView,name='post-comment-delete'),
    path('<int:id>/comment/<int:c_id>/downvote/',CommentDownvoteView,name='post-comment-downvote'),
    path('<int:id>/comment/<int:c_id>/upvote/',CommentUpvoteView,name='post-comment-upvote'),
    
]