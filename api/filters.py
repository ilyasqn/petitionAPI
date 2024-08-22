import django_filters
from .models import Petition

class PetitionFilter(django_filters.FilterSet):
    class Meta:
        model = Petition
        fields = {
            'title': ['icontains'],
            'pub_date': ['exact', 'gte', 'lte'],
        }