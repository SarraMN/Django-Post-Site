from django.shortcuts import render, get_object_or_404,redirect
from .models import Post,Like

def post_list(request):
    posts = Post.objects.all()
    #posts = Post.objects.filter(publish=2024)
    return render(request, 'blog/list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/detail.html', {'post': post})

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Check if the user has already liked the post
    if not Like.objects.filter(post=post, user=request.user).exists():
        Like.objects.create(post=post, user=request.user)
    return redirect('blog:post_list')  # Redirect back to the post list page