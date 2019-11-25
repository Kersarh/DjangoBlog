from django.contrib import admin

from .models import BlogTags, Comment, Post, StaticPage

# Register your models here.
# Для отображения нашей модели статьи в админ панели отредактируем файл \blog\admin.py, где
# list_display — поля, отображающиеся в списке статей;
# list_display_links — поля, являющиеся ссылками для подробного просмотра полей статьи;
# list_editable — поля, доступные для редактирования сразу из просмотра списка всех статей;
# list_filter — фильтры в правой части страницы;
# search_fields — поля по которым осуществляется поиск.


class PostModelAdmin(admin.ModelAdmin):
	list_display = [
	    "id", "title", "updated", "created", "post_views", 'active'
	]
	list_display_links = ["id", "title"]
	list_editable = []
	list_filter = ["updated", "created"]
	search_fields = ["title", "content"]
	# Для автозаполнения на основе заголовка
	prepopulated_fields = {"slug": ("title", )}

	class Meta:
		model = Post


admin.site.register(Post, PostModelAdmin)


class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'post', 'created', 'active')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('name', 'body')


admin.site.register(Comment, CommentAdmin)


class StaticPageAdmin(admin.ModelAdmin):
	list_display = ["id", "title", "updated", "created"]
	list_display_links = ["id", "title"]
	list_editable = []
	list_filter = ["updated", "created"]
	search_fields = ["title", "content"]
	prepopulated_fields = {"slug": ("title", )}

	class Meta:
		model = StaticPage


admin.site.register(StaticPage, StaticPageAdmin)


class TagsAdmin(admin.ModelAdmin):
	list_display = ["id", "title", "slug"]
	list_display_links = ["id", "title"]
	list_editable = []
	search_fields = ["title"]
	prepopulated_fields = {"slug": ("title", )}

	class Meta:
		model = BlogTags


admin.site.register(BlogTags, TagsAdmin)
