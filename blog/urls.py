from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('my-posts/', views.user_posts, name='user_posts'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:id>/', views.edit_post, name='edit_post'),  # Edit post route
    path('delete/<int:id>/', views.delete_post, name='delete_post'),  # Delete post route
    path('share/<int:post_id>/', views.share_post_via_email, name='share_post_via_email'),
]