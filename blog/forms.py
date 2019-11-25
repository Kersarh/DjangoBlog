from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('text', )

	def __init__(self, *args, **kwargs):
		super(CommentForm, self).__init__(*args, **kwargs)
		# CSS style
		self.fields['text'].widget.attrs.update({
		    'class': 'form-control',
		    'rows': "3"
		})


class UserRegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'email')
