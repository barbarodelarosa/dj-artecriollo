from core.forms import AuthAdminForm
from artecriollo.sitemaps import AuctionSitemap, CategoryShopSitemap, LotterySitemap, ProductSitemap, StaticViewSitemap
from django.contrib import admin
from django.urls import path, re_path

from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from core import views

from django.views import i18n
from django.conf.urls import handler404, handler500, handler403
from django.views.generic import RedirectView, TemplateView
from django.contrib.sitemaps import views as views_sitemap
from django.views.decorators.cache import cache_page


sitemaps = {
    'static': StaticViewSitemap,
    'category-shop': CategoryShopSitemap,
    'products':ProductSitemap,
    'lotteries':LotterySitemap,
    'auctions':AuctionSitemap,
}
admin.autodiscover()
admin.site.login_form = AuthAdminForm
admin.site.login_template = 'account/admin/login.html'

urlpatterns = [

 



    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('affiliate/', include('affiliate.urls')),
    path('subasta/', include('auction.urls')),
    path('lottery/', include('lottery.urls')),
    path('', views.HomeView.as_view(), name='home'),
    path('contacto/', views.ContactView.as_view(), name='contact'),
    path('shop/', include('shop.urls', namespace='shop')),
    # path('utils/', include('utils.urls', namespace='utils')),
    # path('user/', include('authy.urls', namespace='user')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('profile-user/', include('profile.urls', namespace='profile')),
  
    path('newsletters/', include('newsletters.urls', namespace='newsletters')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('page/<slug>/', views.PageDetailView.as_view(), name='page-detail'),
    path('download/', views.downloadFile, name='download'),
    path('download1/', views.GithubAvatarDownloadView.as_view(), name='download1'),
    path('jsi18n/', i18n.JavaScriptCatalog.as_view(), name='jsi18n'),
    path('u/<str:shortened_part>', views.redirect_url_view, name='redirect-url-short'),
    # path('', RedirectView.as_view(pattern_name='home'), name='redirect-register'),
    path('', include('pwa.urls')),
  
    
    path('sitemap.xml', views_sitemap.index, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', views_sitemap.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),


    



]

# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.views.static import serve as mediaserve
urlpatterns += [
        path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$', mediaserve, {'document_root': settings.MEDIA_ROOT}),
        # path(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$', mediaserve, {'document_root': settings.STATIC_ROOT}),
    ]

#Necesario para los statics del admin


handler404 = views.pag_404_not_found
handler500 = views.pag_500_error_server
handler403 = views.pag_403_forbidden