""" Sidebar tags """

from django import template

from blog.models import BlogTags

register = template.Library()


@register.inclusion_tag(
    'blog/partial/sidebar_tags.html'
)    # регистрируем тег и подключаем шаблон lastnews_tpl.html
def sidebar_tags():
	spisok = BlogTags.objects.all(
	)    # можно передавать не только строки, но и сложные объекты типа выборки из базы данных
	return {'sidebar_tags': spisok}
