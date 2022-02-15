from django.contrib.auth.models import User
import django_filters
from .models import Member

# Declaring filters of Model Member

class MemberFilter(django_filters.FilterSet):

    class Meta:
        model = Member
        #fields = "__all__"
        fields = ['orgrole', 'member_status', 'region', 'center']
