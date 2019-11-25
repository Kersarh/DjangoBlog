from django.contrib.sitemaps import Sitemap

from .models import Post, StaticPage


class PostSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.9

	def items(self):
		return Post.objects.filter(active=True)

	def lastmod(self, obj):
		return obj.updated


class StaticPageSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.9

	def items(self):
		return StaticPage.objects.filter(active=True)

	def lastmod(self, obj):
		return obj.updated
