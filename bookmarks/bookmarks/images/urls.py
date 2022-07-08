from django.urls import path
from .views import image_create, image_detail, image_like, image_list, image_ranking


app_name = 'images'

urlpatterns = [
    path('create/', image_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', image_detail, name='detail'),
    path('like/', image_like, name='like'),
    path('ranking/', image_ranking, name='create'),
    path('', image_list, name='list'),
]