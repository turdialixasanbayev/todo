from django_filters import rest_framework as filters

from .models import ToDo


class ToDoFilter(filters.FilterSet):
    priority = filters.ChoiceFilter(choices=ToDo.Priority.choices)

    class Meta:
        model = ToDo
        fields = ['priority']
