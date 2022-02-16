from django.contrib.auth.models import User
import django_filters
from .models import Member

# Declaring filters of Model Member

class MemberFilter(django_filters.FilterSet):

    first_name = django_filters.CharFilter(lookup_expr='icontains')
    #last_name = django_filters.CharFilter(lookup_expr='icontains')
    center__name = django_filters.CharFilter(lookup_expr='icontains')
    orgrole__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Member
        #fields = "__all__"
        fields = ['first_name', 'age_group', 'member_status', 'region']
