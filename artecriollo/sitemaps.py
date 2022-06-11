from django.contrib.sitemaps import Sitemap # Importamos la clase Sitemap
from shop.models import Category # Importamos nuestro modelo

from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['contact', 'about', 'privacy','terms','help']

    def location(self, item):
        return reverse(item)


# class CategorySitemap(Sitemap):
#     changefreq = 'weekly'
#     priority = 0.5

#     def items(self):
#         return Category.objects.filter(active=True)

#     def lastmod(self, obj):
#         return obj.cre