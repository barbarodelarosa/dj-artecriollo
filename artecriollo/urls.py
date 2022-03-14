from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from core import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.HomeView.as_view(), name='home'),
    path('contacto/', views.ContactView.as_view(), name='contact'),
    path('acerca-de/', views.AboutView.as_view(), name='about'),
    path('politica-privacidad/', views.PrivacyView.as_view(), name='privacy'),
    path('terminos-condiciones/', views.TermsView.as_view(), name='terms'),
    path('ayuda/', views.HelpView.as_view(), name='help'),
    path('shop/', include('shop.urls', namespace='shop')),
    # path('user/', include('authy.urls', namespace='user')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('profile-user/', include('profile.urls', namespace='profile')),
  
    path('newsletters/', include('newsletters.urls', namespace='newsletters')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('page/<slug>/', views.PageDetailView.as_view(), name='page-detail'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

