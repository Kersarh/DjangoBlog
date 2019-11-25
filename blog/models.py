""" blog models.py """

from django.conf import settings
from django.contrib.auth.models import User
# Для поиска требуется POSTGRESQL!!!
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
# from tinymce.models import HTMLField    # для tinymce
from martor.models import MartorField

# Create your models here.


class BlogTags(models.Model):
	''' Хранения тегов для фильтрации постов'''
	title = models.CharField(max_length=120, verbose_name='Тег')
	slug = models.SlugField(unique=True, verbose_name='slug')
	color = models.CharField(max_length=20,
	                         default='#6c757d',
	                         verbose_name='Фоновый цвет')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return "/tag/%s/" % (self.slug)

	class Meta:
		verbose_name = 'Теги'
		verbose_name_plural = 'Теги'


class Post(models.Model):
	author = models.ForeignKey(
	    settings.AUTH_USER_MODEL,
	    on_delete=models.CASCADE,
	)
	title = models.CharField(max_length=120, verbose_name='Title')
	slug = models.SlugField(unique=True, verbose_name='slug')
	description = models.TextField(default='Description')
	keywords = models.CharField(max_length=120, default='Keywords')
	tags = models.ManyToManyField(BlogTags, blank=True, related_name='Tags')
	img = models.ImageField(upload_to='blog/%Y/%m/%d/',
	                        blank=True,
	                        verbose_name='Images')
	content = MartorField()
	active = models.BooleanField(default=True)
	post_views = models.IntegerField(default=0, verbose_name='Views')
	updated = models.DateTimeField(auto_now=True,
	                               auto_now_add=False,
	                               verbose_name='Updated')
	created = models.DateField(auto_now=False,
	                           auto_now_add=True,
	                           verbose_name='Created')
	sv = SearchVectorField(null=True, editable=False)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return "/post/%s/" % (self.slug)

	class Meta:
		# Для поиска требуется POSTGRESQL!!!
		indexes = [GinIndex(fields=["sv"])]
		ordering = ["-id", "-created"]
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'


class StaticPage(models.Model):
	''' Статичные страницы сайта (О нас, Контакты и тд...) '''
	title = models.CharField(max_length=120, verbose_name='Title')
	slug = models.SlugField(unique=True, verbose_name='slug')
	description = models.TextField(default='Description')
	keywords = models.CharField(max_length=120, default='Keywords')
	content = MartorField()
	active = models.BooleanField(default=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return "/page/%s/" % (self.slug)

	class Meta:
		ordering = ["-id", "-created"]
		verbose_name = 'Страницы'
		verbose_name_plural = 'Страницы'


class Comment(models.Model):
	post = models.ForeignKey(Post,
	                         on_delete=models.CASCADE,
	                         related_name='comments')
	name = models.CharField(max_length=80)
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('created', )
		verbose_name = 'Комментарии'
		verbose_name_plural = 'Комментарии'

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)
