from django.contrib.auth.models import User
import django_filters
from .models import Member
#Declaring filters of Model Member

class RoleFilter(django_filters.FilterSet):

    #Filter based on approle, region and center
   
    class Meta:

        model = Member
        fields = ['first_name', 'last_name', 'gender']
