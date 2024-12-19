
from django.shortcuts import render, get_object_or_404,redirect
from .models import Post,Like
from django.contrib.auth.decorators import login_required
from .forms import PostForm

@login_required
def post_list(request):
    posts = Post.objects.all()
    #posts = Post.objects.filter(publish=2024)
    return render(request, 'blog/list.html', {'posts': posts})

@login_required
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/detail.html', {'post': post})

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Check if the user has already liked the post
    if not Like.objects.filter(post=post, user=request.user).exists():
        Like.objects.create(post=post, user=request.user)
    return redirect('blog:post_list')  # Redirect back to the post list page

@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/user_posts.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the logged-in user as the author
            post.save()
            return redirect('blog:user_posts')  # Redirect to the user's posts page
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})