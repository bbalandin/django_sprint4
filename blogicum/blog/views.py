from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
from django.http import Http404
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import PostForm


def index(request):
    # Адрес шаблона сохранён в переменную, это не обязательно, но удобно.
    template_name = 'blog/index.html'
    # дополнить условие
    post_list = Post.objects.select_related('category').filter(
        is_published=True, category__is_published=True,
        pub_date__lte=timezone.now()).order_by(
            '-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    # Третьим аргументом в render() передаём словарь context:
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    post_list = get_object_or_404(
        Post.objects.select_related('category').filter(
            is_published=True,
            category__is_published=True, pub_date__lt=timezone.now()),
        pk=post_id
    )
    return render(request, template_name, {'post': post_list})


def category_posts(request, category_name):
    template_name = 'blog/category.html'
    category_cur = Category.objects.get(slug__exact=category_name)
    if not category_cur.is_published:
        raise Http404('Ошибка')
    post_list = Post.objects.select_related('category').filter(
        category__is_published=True, category=category_cur, is_published=True,
        pub_date__lte=timezone.now())
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category_cur.title,
               'page_obj': page_obj}
    return render(request, template_name, context)


def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    template_name = 'blog/create.html'
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, template_name, context)


# def edit_post(request, post_id):
#     instance = get_object_or_404(Post, pk=post_id)
#     form = PostForm(request.POST or None, instance=instance)
#     context = {'form': form}
#     # Сохраняем данные, полученные из формы, и отправляем ответ:
#     if form.is_valid():
#         form.save()
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context)

def profile(request, username):
    # заглушка
    pass
