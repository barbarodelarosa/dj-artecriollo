from auction.models import Auction
from lottery.models import Lottery
from django.contrib.sitemaps import Sitemap # Importamos la clase Sitemap
from shop.models import Category, Product # Importamos nuestro modelo
from core.models import Page
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'


    def items(self):
        return Page.objects.filter(active=True)

    # def location(self, item):
    #     return reverse(item)


class CategoryShopSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Category.objects.filter(active=True)

class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.1

    def items(self):
        return Product.objects.filter(active=True, aprobated=True, for_auction=False, for_lottery=False)

class LotterySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.2

    def items(self):
        return Lottery.objects.filter(active=True, aprobated=True)
class AuctionSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.3

    def items(self):
        return Auction.objects.filter(active=True, aprobated=True)