from django.shortcuts import render
from django.http import HttpResponse
from .models import Member,AppRole,OrgRole,Center,Region
from .utils import *
from django.db.models import Q


# def index(request):
#     return HttpResponse("Hello World")

#This is the front home page screen view

def home(request):
    return render(request,'home.html',{})


#To import file - Admin Use
def importFile(request):
    return render(request, 'import-page.html',{})

#To export file - Admin Use
def exportFile(request):
    return render(request, 'export-page.html',{})

# Search By Member-Names
def search_members(request):
    if request.method == "POST":
        searched =  request.POST['searched']

        members = Member.objects.filter(Q(first_name__contains=searched) | Q(last_name__contains=searched) | Q(orgrole__name__contains=searched) | Q(approle__name__contains=searched))
        # role_info = MemberInfo.objects.filter(Q(roleDesc__description__icontains =searched))
        # Asset.objects.filter( project__name__contains="Foo" )
        # members = MemberInfo.objects.filter(firstName__contains=searched)
        return render(request, 'search-members.html', {'searched':searched, 'members': members})
    else:
        return render(request, 'search-members.html', {})

def uploadRegion(request):

    regiondata = {}
    if request.method == "POST":
        print("request.FILES ", request.FILES)
        csv_file = request.FILES['file']
        print(csv_file)
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            message = 'THIS IS NOT A CSV FILE'
        else:
            regiondata = uploadCSVFile(csv_file, "Region")
    return render(request, 'import-page.html', {"regiondata": regiondata})
