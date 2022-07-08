from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf.urls.static import static

from . import settings
from blog import sitemaps

sitemaps_ = {
    'posts':  sitemaps.PostSiteMap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('blog.urls', namespace="blog")),
    
    # таблетка CKEditor 
    path(r'^ckeditor/', include('ckeditor_uploader.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps_},
        name='django.contrib.sitemaps.views.sitemap')
]
