from .models import Post
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Category, Comments
from django.http import Http404
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .forms import CommentsForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from users.forms import CreationForm, EditUserForm


User = get_user_model()


def index(request):
    template_name = 'blog/index.html'
    post_list = Post.objects.select_related('category').filter(
        is_published=True, category__is_published=True,
        pub_date__lte=timezone.now()).order_by(
            '-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(Post, pk=post_id)
    is_published = (post.is_published
                    and post.category.is_published
                    and post.pub_date <= timezone.now())
    is_author = request.user.is_authenticated and post.author == request.user
    if not (is_published or is_author):
        raise Http404("Пост не найден")
    comments = post.comments.all()
    form = CommentsForm()
    return render(request, template_name, {
        'post': post,
        'form': form,
        'comments': comments
    })


def category_posts(request, category_name):
    template_name = 'blog/category.html'
    category_cur = Category.objects.get(slug__exact=category_name)
    if not category_cur.is_published:
        raise Http404('Ошибка')
    post_list = Post.objects.select_related('category').filter(
        category__is_published=True, category=category_cur, is_published=True,
        pub_date__lte=timezone.now()).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category_cur.title,
               'page_obj': page_obj}
    return render(request, template_name, context)


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    template_name = 'blog/create.html'
    context = {'form': form}
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, template_name, context)


def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not request.user.is_authenticated or post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None,
                        instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)
    template_name = 'blog/create.html'
    context = {'form': form, 'post': post}
    return render(request, template_name, context)


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not request.user.is_authenticated or post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    form = PostForm(instance=post)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def add_comment(request, post_id):
    instance = get_object_or_404(Post, pk=post_id)
    form = CommentsForm(request.POST)
    if form.is_valid():
        comments = form.save(commit=False)
        comments.author = request.user
        comments.post = instance
        comments.save()
        return redirect('blog:post_detail', post_id=post_id)
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    if comment.author != request.user:
        raise Http404("У вас нет прав для редактирования этого комментария.")
    form = CommentsForm(request.POST or None, instance=comment)
    context = {'form': form, 'comment': comment}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    if comment.author != request.user:
        raise Http404("У вас нет прав для удаления этого комментария.")
    context = {'comment': comment}
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', context)


def profile(request, username):
    cur_profile = get_object_or_404(User, username=username)
    page_obj = None
    if request.user.is_authenticated:
        post_list = Post.objects.filter(
            author_id=cur_profile.id).order_by(
            '-pub_date')
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    template = 'blog/profile.html'
    context = {
        'page_obj': page_obj,
        'profile': cur_profile,
    }
    return render(request, template, context)


def edit_profile(request):
    cur_profile = get_object_or_404(User, username=request.user)
    form = EditUserForm(request.POST or None, instance=cur_profile)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:index')
    return render(request, 'blog/user.html', context)
