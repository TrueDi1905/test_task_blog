from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from posts.forms import PostForm
from posts.models import Follow, Post, ReadPost
from posts.systems import send

User = get_user_model()


def index(request):
    if request.user.is_anonymous:
        return redirect(reverse('login'))
    follow = Post.objects.filter(author__following__user=request.user)
    users = User.objects.exclude(username=request.user)
    paginator = Paginator(follow, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {"page": page,
                                          'paginator': paginator,
                                          'users': users})


def blog(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'author': author,
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'blog.html', context=context)


@csrf_exempt
@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            follows = Follow.objects.filter(author=request.user)
            for follow in follows:
                send(follow.user, request.user)
            return redirect('posts:news')
        return render(request, "new_post.html", {'form': form})
    form = PostForm()
    return render(request, "new_post.html", {'form': form})


def blog_follow(request, username):
    follow_user = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=request.user,
                                   author=follow_user)
    if follow or request.user.username == username:
        return redirect(reverse('posts:news'))
    else:
        follow_objects = Follow.objects.create(user=request.user,
                                               author=follow_user)
        follow_objects.save()
    return redirect(reverse('posts:news'))


def blog_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(author=author, user=request.user)
    ReadPost.objects.filter(post__author=author,
                            reader=request.user).delete()
    follow.delete()
    return redirect(reverse('posts:news'))


def read_post(request, id):
    post = get_object_or_404(Post, id=id)
    read = ReadPost.objects.filter(reader=request.user, post=post)
    if read:
        return redirect(reverse('posts:news'))
    ReadPost.objects.create(post=post, reader=request.user)
    return redirect(reverse('posts:news'))
