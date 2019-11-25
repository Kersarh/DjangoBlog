from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import DetailView, FormView, ListView

from blog.models import BlogTags, Post, StaticPage

from .forms import CommentForm, UserRegistrationForm


class ListAll(ListView):
	""" Return all posts """
	model = Post
	paginate_by = 5
	template_name = 'blog/partial/list.html'

	def get_queryset(self):
		list_filter = Post.objects.filter(active=1)
		return list_filter


class DetailPost(DetailView):
	model = Post
	template_name = 'blog/partial/detail.html'

	def get(self, request, *args, **kwargs):
		# Счетчик просмотров
		self.object = self.get_object()
		self.object.post_views += 1
		self.object.save()
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

	def get_context_data(self, **kwargs):
		# Отобразить форму
		context = super(DetailPost, self).get_context_data(**kwargs)
		context['comment_form'] = CommentForm()
		# Фильтр для коментов
		context['comments'] = self.object.comments.filter(active=True)
		return context

	def post(self, request, **kwargs):
		# Обработка формы
		self.object = self.get_object()
		context = super(DetailPost, self).get_context_data(**kwargs)
		context['comment_form'] = CommentForm()
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = self.object    # Поле post привязываем к текущему комментарию
			new_comment.name = self.request.user    # Поле name привязываем к текущему пользователю
			new_comment.save()
			return HttpResponseRedirect(self.object.get_absolute_url())
		else:
			comment_form = CommentForm()
			return self.render_to_response(context)


def static_pages(request, slug=None):
	""" Static Pages """
	page = get_object_or_404(StaticPage.objects.filter(slug=slug))
	return render(request, "blog/partial/static_page.html", {'object': page})


class ListTags(ListView):
	""" Список тегов """
	model = BlogTags
	paginate_by = 5
	template_name = 'blog/partial/list.html'

	def get_queryset(self):
		idd = self.kwargs['slug']    # site.com/tag/1/
		# idd = self.request.GET.get("slug", 2)  # site.com/tag/?id=1
		q = Post.objects.filter(tags__slug=idd)
		if not q:
			self.template_name = "blog/partial/not_found.html"
			return ["Not Found Tags!"]
		elif q:
			return q


class Search(ListView):
	""" Для поиска требуется POSTGRES!!!
		Если не используется удалить!
	"""
	model = Post
	paginate_by = 10
	template_name = 'blog/partial/search.html'

	def get_queryset(self):
		queryset = super(Search, self).get_queryset()
		q = self.request.GET.get("q")
		if q:
			vector = SearchVector('title',
			                      'content',
			                      raw=True,
			                      fields=('title'))
			vector_trgm = TrigramSimilarity(
			    'title', q, raw=True, fields=('title')) + TrigramSimilarity(
			        'content', q, raw=True, fields=('content'))
			a = queryset.annotate(search=vector).order_by('title').filter(
			    search=q) or queryset.annotate(similarity=vector_trgm).filter(
			        similarity__gt=0.1).order_by('title')
			if not a:    # Если НЕ найдено
				self.template_name = "blog/partial/not_found.html"
				return ["Not Found!"]
			else:    # если НАЙДЕНО
				return a
		elif not q:    # Если ПУСТОЙ запрос
			self.template_name = "blog/partial/not_found.html"
			return ["Empty Search String."]

	def get_context_data(self, **kwargs):
		""" Добавляет в контекст параметр q из Get запроса
		Необходим для корректной работы пагинации в поиске """
		context = super().get_context_data(**kwargs)
		context['q'] = self.request.GET.get('q', 2)
		return context


# РЕГИСТРАЦИЯ
class RegisterFormView(FormView):
	form_class = UserRegistrationForm
	success_url = "/accounts/register_done/"
	template_name = "registration/register.html"

	def form_valid(self, form):
		listing = form.save(commit=False)
		listing.name = self.request.user
		listing.save()
		# Вызываем метод базового класса
		return super(RegisterFormView, self).form_valid(form)


def regdone(request):
	return render(request, "registration/registerdone.html")
