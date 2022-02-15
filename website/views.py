from django.shortcuts import render
from django.http import HttpResponse

from .models import Member,AppRole,OrgRole,Center,Region
from .filters import RoleFilter
from .utils import *
from django.db.models import Q
from django.core.cache import cache
import logging
from .email import sendemail
from .filters import MemberFilter


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

# Create a list for cards


# def index(request):
#     return HttpResponse("Hello World")

#This is the front home page screen view

def home(request):
    message = None
    if request.method == 'POST':
        if request.POST.keys() >= {'emailaddress'}:
            emailaddress = request.POST['emailaddress']
            if len(emailaddress) > 0:
                logging.debug('your email addresss--- ' + emailaddress)
                member = Member.objects.filter(email=emailaddress).first()
                logging.debug('member--- ' + str(member))
                if member == None:
                    message = "Your email is not in our database. Please request for access via Contact Us link"
                else:
                    sendemail(to=emailaddress,
                                subject='Your Auth Code',
                                body="Your Auth Code")
                    return render(request,'home.html',{})
        return render(request,'auth.html',{'message': message})
    #return render(request,'home.html',{})
    return render(request,'home.html',{})


#To import file - Admin Use
def importFile(request):
    return render(request, 'import-page.html',{})

#To export file - Admin Use
def exportFile(request):
    return render(request, 'export-page.html',{})

# #Show All Cards of Region Officers
# def show_regions(request):
#     return render(request, 'show-region.html',{})


#Get all regional officers
def getAllRegionalOfficers(request):
    allRegionalOfficers = Member.objects.filter(approle__name='Regional Officer')
    logging.debug('allRegionalOfficers: ' + str(allRegionalOfficers))
    filterMembers = MemberFilter(request.GET, queryset=allRegionalOfficers)
    allRegionalOfficers = filterMembers.qs

    return render(request, 'regional-officers-page.html',
            {'allRegionalOfficers':  allRegionalOfficers, 'filterMembers' : filterMembers})

#Get all national officers
def getAllNationalOfficers(request):
    if cache.get('allNationalOfficers'):
        allNationalOfficers = cache.get('allNationalOfficers')
    else:
        allNationalOfficers = Member.objects.filter(approle__name='National Officer')
        cache.set('allNationalOfficers', allNationalOfficers)
    logging.debug('allNationalOfficers: ' + str(allNationalOfficers))
    return render(request, 'national-officers-page.html', {'allNationalOfficers': allNationalOfficers})

#Get all center officers
def getAllCenterOfficers(request):
    if cache.get('allCenterOfficers'):
        allCenterOfficers = cache.get('allCenterOfficers')
    else:
        allCenterOfficers = Member.objects.filter(approle__name='Center Officer')
        cache.set('allCenterOfficers', allCenterOfficers)
    logging.debug('allCenterOfficers: ' + str(allCenterOfficers))
    return render(request, 'center-officers-page.html', {'allCenterOfficers':  allCenterOfficers})

#Get regional officers for specific region
def getRegionOfficers(request, regionId):
    logging.debug('regionId: ' + str(regionId))
    if cache.get('regionOfficers'):
        regionOfficers = cache.get('regionOfficers')
    else:
        regionOfficers = Member.objects.filter(approle__name='Regional Officer', region_id=regionId)
        cache.set('regionOfficers', regionOfficers)
    logging.debug('regionOfficers: ' + str(regionOfficers))

    return render(request, 'show-region.html', {'regionOfficers': regionOfficers})


#Get center officers for specific center
def getCenterOfficers(request, centerId):
    if cache.get('centerOfficers'):
        centerOfficers = cache.get('centerOfficers')
    else:
        centerOfficers = Member.objects.filter(approle__name='Center Officer', center_id=centerId)
        cache.set('centerOfficers', centerOfficers)
    logging.debug('centerOfficers: ' + str(centerOfficers))
    return render(request, 'show-center.html', {'centerOfficers': centerOfficers})

#Get all centers of a region - Radhika
def getRegionalCenters(request, regionId):
    if cache.get('centersByRegionId'):
        centersByRegionId = cache.get('centers')
    else:
        # centersByRegionId = Center.objects.get(pk=regionId)
        centersByRegionId = Center.objects.filter(region_id=regionId)

        cache.set('centersByRegionId', centersByRegionId)
    logging.debug('centersByRegionId: ' + str(centersByRegionId))
    return render(request, 'show-regionCenters.html', {'centersByRegionId': centersByRegionId})

#Radhika
def getAllRegions(request):
    region_names = Region.objects.all()
    return render(request,'list-all-regions.html', {'region_names': region_names})

#Radhika
def getallCenters(request):
    center_names = Center.objects.all()
    return render(request,'list-all-centers.html', {'center_names': center_names})

#Radhika - but didn't use it.
def showCenters(request, centerId):
    show_center = Center.objects.get(pk=centerId)
    return render(request,'list-centerNames.html', {'show_center': show_center})

# Search By Member-Names
def search_members(request):
    if request.method == "POST":
        searched =  request.POST['searched']
        print('searched-----', searched)
        members = Member.objects.filter(
            Q(first_name__contains=searched)
            | Q(last_name__contains=searched)
            | Q(orgrole__name__contains=searched)
            | Q(region__name__contains=searched)
            | Q(approle__name__contains=searched)).distinct()
        # role_info = MemberInfo.objects.filter(Q(roleDesc__description__icontains =searched))
        # Asset.objects.filter( project__name__contains="Foo" )
        # members = MemberInfo.objects.filter(firstName__contains=searched)
        logging.debug('members: ' + str(members))
        return render(request, 'search-members.html', {'searched':searched, 'members': members })
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

def role_filter_list(request):


    filtered_persons = RoleFilter(request.GET, queryset=Member.objects.all())

    context = {'filtered_persons':filtered_persons}
    return render(request,'filter-list.html', context)


# Write a view for the

# def role_filter_list(request):
#     role_list = Member.objects.all()
#     role_filter = RoleFilter(request.GET, queryset=role_list)
#     return render(request, 'filter-list.html', {'role_filter': role_filter})
