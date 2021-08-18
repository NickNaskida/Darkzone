import django_filters

from .models import ThreadPosts

from datetime import timedelta, date
from dateutil.relativedelta import *

prefix_choices = (
	('', 'Prefix: No Prefix'),
	('Post', 'Prefix: Post'),
	('Question', 'Prefix: Question'),
	)

order_choices = (
	('Ascending', 'Order: Ascending'),
	('Descending', 'Order: Descending'),
)

date_choices = (
	('', 'All/Don\'t Sort'),
	('today', 'Today'),
	('yesterday', 'Yesterday'),
	('last_week', 'Last Week'),
	('last_month', 'Last Month'),
)


class post_filter(django_filters.FilterSet):
	date_filter = django_filters.ChoiceFilter(field_name='post_date', choices=date_choices, empty_label='Sort By Date', label='', method='filter_by_date')
	order_filter = django_filters.ChoiceFilter(field_name='post_date', choices=order_choices, empty_label=None, label='', method='filter_by_order')
	prefix_filter = django_filters.ChoiceFilter(field_name='post_prefix', choices=prefix_choices, empty_label='Prefix: Any/No Prefix', label='')


	'''def __init__(self, *args, **kwargs):
					self.user = kwargs.pop('request', None)
					super(post_filter, self).__init__(*args, **kwargs)'''

		
	class Meta:
		model = ThreadPosts
		fields = []

	def filter_by_order(self, queryset, name, value):
		if value == 'Ascending':
			return queryset
		else:
			return queryset.order_by('-post_date')

	def filter_by_date(self, queryset, name, value):
		if value == 'today':
			return queryset.filter(post_date__date=date.today())
		elif value == 'yesterday':
			return queryset.filter(post_date__date=date.today()-timedelta(days=1))
		elif value == 'last_week':
			return queryset.filter(post_date__gte=date.today()-timedelta(days=7))
		elif value == 'last_month':
			return queryset.filter(post_date__gte=date.today()-relativedelta(months=+1))					