from django.shortcuts import render
from django.http import HttpResponse
from .models import Member,AppRole,OrgRole,Center,Region
from .utils import *
from django.db.models import Q
from django.core.cache import cache
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

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

#Show Region Officers with Center Info
# def show_regions(request):
#     return render(request, 'show-region.html',{})

#Get all regional officers
def getAllRegionalOfficers(request):
    allRegionalOfficers = Member.objects.filter(approle__name='Regional Officer')
    logging.debug('allRegionalOfficers: ' + str(allRegionalOfficers))

#Get all national officers
def getAllNationalOfficers(request):
    allNationalOfficers = Member.objects.filter(approle__name='National Officer')
    logging.debug('allNationalOfficers: ' + str(allNationalOfficers))

#Get all center officers
def getAllCenterOfficers(request):
    allCenterOfficers = Member.objects.filter(approle__name='Center Officer')
    logging.debug('allCenterOfficers: ' + str(allCenterOfficers))

#Get regional officers for specific region
def getRegionOfficers(request, regionId):
    logging.debug('regionId: ' + str(regionId))
    regionOfficers = Member.objects.filter(approle__name='Regional Officer', region_id=regionId)
    logging.debug('regionOfficers: ' + str(regionOfficers))
    return render(request, 'show-region.html', {'regionOfficers': regionOfficers})

#Get centre officers for specific center
def getCenterOfficers(request, centerName):
    centerOfficers = Member.objects.filter(approle__name='Center Officer', center__name=centerName)
    logging.debug('centerOfficers: ' + str(centerOfficers))

# Search By Member-Names
def search_members(request):
    if request.method == "POST":
        searched =  request.POST['searched']

        members = Member.objects.filter(
            Q(first_name__contains=searched)
            | Q(last_name__contains=searched)
            | Q(orgrole__name__contains=searched)
            | Q(approle__name__contains=searched)).distinct()
        # role_info = MemberInfo.objects.filter(Q(roleDesc__description__icontains =searched))
        # Asset.objects.filter( project__name__contains="Foo" )
        # members = MemberInfo.objects.filter(firstName__contains=searched)
        logging.debug('members: ' + str(members))
        return render(request, 'search-members.html', {'searched':searched, 'members': members})
    else:
        return render(request, 'search-members.html', {})

def uploadFile(request):

    csv_file = None
    message = "All are up to date"
    importType = None
    if request.method == "POST":
        importType = request.POST.get('importType')
        try:
            csv_file = request.FILES['file']
        except Exception as ex:
            message = str(ex)
            return render(request, 'import-page.html', {"message" : "upload failed. check your input file."})
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            message = 'Please upload a CSV file'
            return render(request, 'import-page.html', {"message" : message})
        else:
            loadeddata = ""
            loadeddata = uploadCSVFile(csv_file, importType)
            #print(loadeddata, "loadeddata")
            if len(loadeddata) == 0:
                return render(request, 'import-page.html', {"message" : message})
            else:
                return render(request, 'import-page.html', {"loadeddata": loadeddata})
    else:
        return render(request, 'import-page.html',{})
