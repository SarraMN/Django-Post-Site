
from django.shortcuts import render, get_object_or_404,redirect
from .models import Post,Like
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import CommentForm
from taggit.models import Tag
from django.core.paginator import Paginator
from django.db.models import Count
@login_required
def post_list(request):
    tag_name = request.GET.get('tag')  # Get the tag from the query parameters
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)  # Filter for published posts
    liked_posts = Like.objects.filter(user=request.user).values_list('post', flat=True)  # Get liked posts by the user

    # Filter posts by tag if a tag name is provided
    if tag_name:
        tag = Tag.objects.filter(name__iexact=tag_name).first()  # Case-insensitive search for the tag
        if tag:
            posts = posts.filter(tags=tag)

    posts = posts.annotate(
        num_comments=Count('comments'),
        num_likes=Count('likes'),
        num_shares=Count('shares')
    )

    # Pagination
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the posts for the current page

    return render(request, 'blog/list.html', {
        'posts': page_obj,
        'liked_posts': liked_posts,
        'tag_name': tag_name,
    })

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user  # Assign the current user as the author
            new_comment.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })

@login_required
def user_posts(request):
    tag_name = request.GET.get('tag')  # Get the tag from the query parameters
    posts = Post.objects.filter(author=request.user)

    # Filter posts by tag if a tag name is provided
    if tag_name:
        tag = Tag.objects.filter(name__iexact=tag_name).first()  # Case-insensitive search for the tag
        if tag:
            posts = posts.filter(tags=tag)

    # Paginate the posts
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')  # Get the page number from query parameters
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/user_posts.html', {'page_obj': page_obj})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the logged-in user as the author
            post.save()
            form.save_m2m()
            return redirect('blog:user_posts')  # Redirect to the user's posts page
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)  # Ensure only the author can edit
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:user_posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)  # Ensure only the author can delete
    if request.method == "POST":
        post.delete()
        return redirect('blog:user_posts')
    return render(request, 'blog/delete_post_confirm.html', {'post': post})

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)   
   # Check if the user has already liked the post
    existing_like = Like.objects.filter(post=post, user=request.user).first()
    
    if existing_like:
        # If the user has liked the post, remove the like (dislike action)
        existing_like.delete()
    else:
        # If the user hasn't liked the post, create a new like
        Like.objects.create(post=post, user=request.user)
    
    return redirect('blog:post_list')  # Redirect back to the post list page

def share_post_via_email(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        recipient_email = request.POST.get('email')

        # Get the current user who is sharing the post
        current_user = request.user

        # Construct the email subject and body
        subject = f"Check out this blog post: {post.title}"
        body = f"Hi, \n\n{current_user.username} wanted to share this blog post with you:\n\n{post.title}\n\n{post.body}\n\n"
        body += f"Shared by: {current_user.username}\n\n"
        body += f"Read more at: {request.build_absolute_uri(post.get_absolute_url())}"

        # Send the email
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER, 
            [recipient_email], 
            fail_silently=False,
        )

        # Redirect back to the blog list page after sending the email
        return redirect('blog:post_list')

    return redirect('blog:post_list')  # If not POST, just redirect to the post list

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # Ensure the author is set
            comment.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/detail.html', {'post': post, 'form': form})