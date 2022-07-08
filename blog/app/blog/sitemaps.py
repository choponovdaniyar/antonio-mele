from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSiteMap(Sitemap):
    '''
        Карта постов

        priority - частота  
        lastmod - последнее обновление
        items - посты 
    '''
    changefreq = 'weekly'
    priority = 0.1
    def items(self):
        return Post.published.all()
    def lastmod(self, obj):
        return obj.update