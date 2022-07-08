from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import mail
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from . import forms
from . import models
from app import settings
from taggit.models import Tag


def post_list(request, tag_slug=None):
    '''
        Пагинция на основе функции и класса Paginator

        Внутри 'blog/post/list.html' в 'pagination.html' указать page=posts
    '''
    object_list = models.Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in = [tag])
    paginator = Paginator(object_list, 6)
    page = request.GET.get("page")

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/post/list.html',  {
        'page': page,
        'posts': posts,
        'tag': tag
    })




def post_detail(reqeust, year, month, day, post):
    '''
        Вывод нужного поста
    '''
    post = get_object_or_404(models.Post, slug=post, status='published',
                            publish__year=year, publish__month=month, 
                            publish__day=day)
    # Список активных комментариев для этой статьи
    comments = post.comments.filter(active=True)
    comment_form = forms.CommentForm()
    new_comment = None
    if reqeust.method == 'POST':
        # Пользователь отправил комментарий
        comment_form = forms.CommentForm(data=reqeust.POST)
        if comment_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в БД
            new_comment = comment_form.save(commit=False)
            # Привязываем комментарий к текущей статье
            new_comment.post = post
            # Сохраняем комментарий в БД
            new_comment.save()
        else:
            comment_form = forms.CommentForm()
    # формирование списка похожих статей.
    # post_tags_ids = post.tags.values_list('id', flat=True)
    # similar_posts = models.Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by("-same_tags", '-published')[:4]
    # аналог
    similar_posts = post.tags.similar_objects()
    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts
    }
    return render(reqeust, 'blog/post/detail.html', context)


def post_share(request, post_id):
    '''
        Поиск определенной статьи и отправка по e-mail
    '''
    # Получение статьи по id
    post = get_object_or_404(models.Post, id=post_id, status='published')
    sent = False
    form = forms.EmailPostForm()
    if request.method == 'POST':
        # форма была отправлена на сохранение
        form = forms.EmailPostForm(request.POST)
        if form.is_valid():
            # все поля формы прошли валидацию
            cd = form.cleaned_data
            # отправка электронной почты
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading " {}"'.format(cd["name"], 
                                                                    cd["email"], 
                                                                    post.title)
            message = 'Read "{}" at {}\n\n{}\' comments: {}'.format(
                                                                    post.title,
                                                                    post_url,
                                                                    cd["name"],
                                                                    cd["comments"]
            ) 
            mail.send_mail(subject,message, settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
        else:
            form = forms.EmailPostForm()
    return render(request, 'blog/post/share.html',{
        'post': post,
        'form': form,
        'sent': sent
    })



def post_search(request):
    '''
        https://docs.djangoproject.com/en/4.0/ref/contrib/postgres/search/
        Поиск с приоритетом одного поля над другим
    '''
    form = forms.SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = models.Post.objects.annotate(
                rank=SearchRank(search_vector,search_query)).filter(
                    rank__gte=0.3
                ).order_by('-rank')
    return render(request, 'blog/post/search.html', {
        'form':form,
        'query':query,
        'results': results
    })


# class PostList(ListView):
#     '''
#         Пагинация на основе класса ListView 
#
#         Внутри 'blog/post/list.html' в 'pagination.html' указать page=page_obj
#     '''
#     template_name = 'blog/post/list.html'
#     context_object_name ='posts'
#     paginate_by = 3
#     queryset = models.Post.published.all()


# def post_search(request):
#     ''' 
#         https://docs.djangoproject.com/en/4.0/ref/contrib/postgres/search/
#         Поиск по вектору (только для postgreSQL)
#     '''
#     form = forms.SearchForm()
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = forms.SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = models.Post.objects.annotate(
#             search=SearchVector('title', 'body'),
#             ).filter(search=query)
#     return render(request, 'blog/post/search.html', {
#         'form': form,
#         'query': query,
#         'results': results
#     })


# def post_search(request):
#     '''
#         https://docs.djangoproject.com/en/4.0/ref/contrib/postgres/search/
#         Поиск с применение ранжирования 
#     '''
#     form = forms.SearchForm()
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = forms.SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
#             search_query = SearchQuery(query)
#             results = models.Post.objects.annotate(
#                     search=search_vector,
#                     rank=SearchRank(search_vector, search_query)
#                 ).filter(
#                         search=search_query
#                     ).order_by('-rank')
#     return render(request, 'blog/post/search.html', {
#         'form':form,
#         'query':query,
#         'results': results
#     })