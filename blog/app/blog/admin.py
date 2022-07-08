from tabnanny import verbose
from django.contrib import admin
from django import forms

from . import models

from taggit.models import Tag
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class PostAdminForm(forms.ModelForm):
    '''
        Форма для таблетки "CKEditor"
    '''
    body = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = models.Post
        fields = '__all__'
        
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display =('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body') 
    form = PostAdminForm
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields =('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    save_as = True


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    '''
        Админка комментариев
    '''
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
    