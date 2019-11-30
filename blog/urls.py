""" urls.py Настройки роутера для проекта """

from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from blog.sitemaps import PostSitemap, StaticPageSitemap

from . import views

SITEMAPS = {
    "posts": PostSitemap,
    "static": StaticPageSitemap,
}

urlpatterns = [
    path("", views.ListAll.as_view(), name='home'),
    path('post/<slug:slug>/', views.DetailPost.as_view(), name='detail'),
    path("tag/<slug:slug>/", views.ListTags.as_view(), name='tags'),
    path("page/<slug:slug>/", views.static_pages, name='static_page'),
    path("search/", views.Search.as_view(), name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.RegisterFormView.as_view()),
    path('accounts/register_done/', views.regdone),
    path('robots.txt', views.robots),
    path("sitemap.xml",
         sitemap, {'sitemaps': SITEMAPS},
         name='django.contrib.sitemaps.views.sitemap'),
]
