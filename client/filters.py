from django.db.models import Q
import django_filters

from client.models import Client


class UserSearchFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='client_search', label="Search")

    class Meta:
        model = Client
        fields = ['q']

    def client_search(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(email__icontains=value)
            | Q(alternative_email__icontains=value) | Q(main_phone__icontains=value) | Q(alternative_phone__icontains=value)
        )