from django import forms
from django.utils.text import slugify

from .models import Categories, CategoryThreads, ThreadPosts, PostReplys

from ckeditor_uploader.widgets import CKEditorUploadingWidget


choices1 = (
	('Public', 'Public'),
	('Private', 'Private')
	)

choices2 = (
	('Question', 'Question'),
	('Post', 'Post')
	)
		
class AddCategoryForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['category_name'].label = 'Category Name'
		self.fields['category_description'].label = 'Category Description (Optional)'

	class Meta:
		model = Categories
		fields = ['category_name', 'category_description']


class AddCategoryThreadForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['category'].empty_label = None
		self.fields['category'].widget.attrs['required'] = True
		self.fields['category'].widget.attrs.update({'size': '5'})

		self.fields['category_thread_name'].label = 'Thread Name'
		self.fields['category_thread_description'].label = 'Thread Description (Optional)'
		self.fields['category_thread_type'].label = 'Thread Type'
		self.fields['category_thread_icon'].label = 'Thread Icon'

	class Meta:
		model = CategoryThreads
		fields = ['category', 'category_thread_name',  'category_thread_type', 'category_thread_icon', 'category_thread_description', 'category_thread_slug']		

		widgets = {
			'category_thread_type': forms.Select(choices=choices1),
			'category_thread_slug': forms.HiddenInput(),
		}

		help_texts = {
            'category_thread_icon': '<a href="https://fontawesome.com/v5.15/icons/" target="_blank">Get icons here</a>',
        }



class AddPostForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['post_prefix'].empty_label = None
		self.fields['post_slug'].label = 'Post slug/url'
		self.fields['post_body'].widget.attrs['required'] = True
		self.fields['post_tags'].widget.attrs.update({'data-role': 'tagsinput', 'name': 'tags'})
		self.fields['post_tags'].help_text = "Enter tag name and hit enter."

	class Meta:
		model = ThreadPosts
		fields = ['author', 'thread', 'post_title', 'post_slug', 'post_prefix', 'post_tags', 'post_date', 'post_body', 'post_status']

		widgets = {
			'post_prefix': forms.Select(choices=choices2),
			'post_body': CKEditorUploadingWidget(),
			'author': forms.HiddenInput(),
			'thread': forms.HiddenInput(),
			'post_date': forms.HiddenInput(),
			'post_status': forms.HiddenInput(),
		}


class AddReplyForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['reply_body'].label = ''

	class Meta:
		model = PostReplys
		fields = ['post', 'reply_author', 'reply_date', 'reply_body']

		widgets = {
			'reply_body': CKEditorUploadingWidget(),
			'post': forms.HiddenInput(),
			'reply_author': forms.HiddenInput(),
			'reply_date': forms.HiddenInput(),
		}


class RemoveForm(forms.Form):
	remove_reason = forms.CharField(max_length=300, help_text='Write clearly why is this post removed. Also warn him that he will be banned if such case repeats.')		

		



	
					

	
	