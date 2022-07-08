from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from common.decorators import ajax_required, is_ajax
from actions.utils import create_action

from .forms import ImageCreateForm, Image
from django.conf import settings

import redis


r =  redis.StrictRedis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    db=settings.REDIS_DB
)

@login_required
def image_create(request):
    if request.method == 'POST':
        # Форма отправлена
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # Данные формы валидны
            cd = form.cleaned_data

            new_item = form.save(commit=False)
                        
            # Добавляем пользователя на страницу сохраненного изображения.
            print(request.user)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarklet image', new_item)

            messages.success(request, 'Image added successfully')

            # Перенаправляем пользвателя на страницу сохраненного изображения
            return redirect(new_item.get_absolute_url())
    else:
        # Заполняем форму данными из GET - запроса.
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # Увеличиваем общее количество просмотров на 1
    total_views = r.incr('image:{}:views'.format(image.id))
    # Увеличиваем рейтинг картинки на 1.
    r.zincrby('image_ranking', image.id, 1)
    return render(
        request, 
        'images/image/detail.html',
        {
            'section': 'images',
            'image': image,
            'total_views': total_views
        }
    )


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    print(image_id, action)

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)  
                create_action(request.user, "likes", image)
            else:
                image.users_like.remove(request.user)
        except Exception as e:
            print(e)
    return JsonResponse({'status':'ok'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Если переданная страница не является числом, возвращаем первую
        images = paginator.page(1)
    except EmptyPage:
        if is_ajax(request):
            # Если получили AJAX-запрос с номером страницы, большим, чем их количество, возвращаем пустую страниц
            return HttpResponse('')

    if is_ajax(request):
        return render(request, 'images/image/list_ajax.html',{
            'section': 'images',
            'images': images
        })
    return render(request, 'images/image/list.html',{
        'section': 'images',
        'images': images
    })


@login_required
def image_ranking(request):
    # Получаем набор рейтинга картинок.
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # Получаем отсортированный список самых популярных картинок.
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(
        request,
        'images/image/ranking.html',
        {
            'section': 'images',
            'most_viewed': most_viewed
        }
    )