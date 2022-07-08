from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

import markdown

from .. import models


register = template.Library()


@register.simple_tag
def total_posts():
    '''
        Простой тег для вывода кол-во опубликованных постов
    '''
    return models.Post.published.count()


@register.simple_tag    
def get_most_commented_posts(count=5):
    '''
        Простой тег для вывода кол-ва комментов
    '''
    return models.Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    '''
        Сложный тег для вывода последних постов
    '''
    latest_posts = models.Post.published.all().order_by('-publish')[:count]
    print(latest_posts)
    return {"latest_posts": latest_posts}

@register.filter(name="markdown")
def markdown_format(text):
    '''
        Фильтр для подключение markdown к тексту
    '''
    return mark_safe(markdown.markdown(text))

@register.filter(name="div")
def div(list,int):
    return int