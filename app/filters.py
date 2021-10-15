import django_filters
from . models import Project, Agent, Invoice


class ProjectsFilter(django_filters.FilterSet):
	class Meta:
		model = Project
		fields = ['title', 'date_added',]

class AgentFilter(django_filters.FilterSet):
	class Meta:
		model = Agent
		fields = ['ssdc_number', 'project']

class InvoiceFilter(django_filters.FilterSet):
	class Meta:
		model = Invoice
		fields = ['project', 'status', 'due_date']