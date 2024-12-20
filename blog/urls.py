from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('my-posts/', views.user_posts, name='user_posts'),  # New route for user-specific posts
    path('create/', views.create_post, name='create_post'),
    path('share/<int:post_id>/', views.share_post_via_email, name='share_post_via_email'),
]