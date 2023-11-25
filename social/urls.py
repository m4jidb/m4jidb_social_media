from django.urls import path
from . import views


app_name = 'social'

urlpatterns = [
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/detail/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/add_comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('post/list/', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),
]
