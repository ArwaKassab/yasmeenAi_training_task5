import django_filters
from projects.models import Task
from django_filters import rest_framework as filters

class TaskFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    due_date = filters.DateFilter(field_name='due_date')
    project = filters.NumberFilter(field_name='project__id')
    assigned_to = filters.NumberFilter(field_name='assigned_to__id')

    class Meta:
        model = Task
        fields = ['status', 'due_date', 'project', 'assigned_to']
