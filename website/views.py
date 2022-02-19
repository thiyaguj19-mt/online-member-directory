from django.shortcuts import render
from django.http import HttpResponse
from .models import Member,AppRole,OrgRole,Center,Region
from .filters import MemberFilter
from .utils import *
from django.db.models import Q
from django.core.cache import cache
import logging
from .auth import *
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.models import Permission, User
from django.shortcuts import get_object_or_404

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

#this new code for authenticate user using
#OOTB user authentication data model
def home(request):

    try:
        print("request.user.is_authenticated--- ", request.user.is_authenticated)
        if request.user.is_authenticated:
            return render(request,'home.html', {})
        if request.method == 'POST':
            if request.POST.keys() >= {'emailaddress'}:
                emailaddress = request.POST['emailaddress']
                context = generateAuthCode(request, emailaddress)
                return render(request, 'auth.html', context)
            elif request.POST.keys() >= { 'authcode', 'email' }:
                emailaddress = request.POST['email']
                context = authenticateUser(request, emailaddress)
                if context == True:
                    setupAppPermissions(request, emailaddress)
                    return render(request,'home.html',{})
                else:
                    return render(request, 'auth.html', context)
    except Exception as err:
        print(f'Unexpected {err} from home(), {type(err)}')
        raise
    return render(request,'auth.html',{})

#To import file - Admin Use
def importFile(request):
    if request.user.is_authenticated:
        return render(request, 'import-page.html',{})
    else:
        return render(request,'auth.html',{})

#To export file - Admin Use
def exportFile(request):
    if request.user.is_authenticated:
        return render(request, 'export-page.html',{})
    else:
        return render(request,'auth.html',{})

# #Show All Cards of Region Officers
# def show_regions(request):
#     return render(request, 'show-region.html',{})


#Get all regional officers
def getAllRegionalOfficers(request):
    if request.user.is_authenticated:
        gridcheckflag = request.GET.get('gridcheckflag')
        user = User.objects.filter(username=request.user).first()
        if user.has_perm('website.is_national_officer'):
            officers_data = Member.objects.filter(approle__name='Regional Officer')
        else:
            member = Member.objects.filter(email=request.user).first()
            officers_data = Member.objects.filter(approle__name='Regional Officer',region=member.region)
        filterMembers = MemberFilter(request.GET, queryset=officers_data)
        officers_data = filterMembers.qs
        page_obj = Paginator(officers_data, 12)
        page = request.GET.get('page')
        officers_data = page_obj.get_page(page)
        context = {}
        if gridcheckflag is not None:
            context = {'officers_data':officers_data,
                    'officer_header':'Regional Officers',
                    'filterMembers':filterMembers,
                    'gridcheckflag': gridcheckflag}
        else:
            context = {'officers_data':officers_data,
                    'officer_header':'Regional Officers',
                    'filterMembers':filterMembers}
        return render(request,'show-officers.html', context)
    else:
        return render(request,'auth.html',{})

#Get all national officers
def getAllNationalOfficers(request):
    if request.user.is_authenticated:
        gridcheckflag = request.GET.get('gridcheckflag')
        officers_data = Member.objects.filter(approle__name='National Officer')
        logging.debug('allNationalOfficers: ' + str(officers_data))
        filterMembers = MemberFilter(request.GET, queryset=officers_data)
        officers_data = filterMembers.qs
        page_obj = Paginator(officers_data, 12)
        page = request.GET.get('page')
        officers_data = page_obj.get_page(page)
        #return render(request, 'national-officers-page.html', {'allNationalOfficers': allNationalOfficers, 'filterMembers' : filterMembers})
        context = {}
        if gridcheckflag is not None:
            context = {'officers_data':officers_data,
                    'officer_header':'National Officers',
                    'filterMembers':filterMembers,
                    'gridcheckflag': gridcheckflag}
        else:
            context = {'officers_data':officers_data,
                    'officer_header':'National Officers',
                    'filterMembers':filterMembers}
        return render(request,'show-officers.html', context)
    else:
        return render(request,'auth.html',{})

#Get all center officers
def getAllCenterOfficers(request):
    if request.user.is_authenticated:
        gridcheckflag = request.GET.get('gridcheckflag')
        user = User.objects.filter(username=request.user).first()
        if user.has_perm('website.is_national_officer'):
            officers_data = Member.objects.filter(approle__name='Center Officer')
        else:
            member = Member.objects.filter(email=request.user).first()
            officers_data = Member.objects.filter(approle__name='Center Officer', region=member.region)
        logging.debug('officers_data: ' + str(officers_data))
        filterMembers = MemberFilter(request.GET, queryset=officers_data)
        officers_data = filterMembers.qs
        page_obj = Paginator(officers_data, 12)
        page = request.GET.get('page')
        officers_data = page_obj.get_page(page)
        #return render(request, 'center-officers-page.html', {'allCenterOfficers':  allCenterOfficers,'filterMembers' : filterMembers})
        context = {}
        if gridcheckflag is not None:
            context = {'officers_data':officers_data,
                    'officer_header':'Center Officers',
                    'filterMembers':filterMembers,
                    'gridcheckflag': gridcheckflag}
        else:
            context = {'officers_data':officers_data,
                    'officer_header':'Center Officers',
                    'filterMembers':filterMembers}
        return render(request,'show-officers.html', context)
    else:
        return render(request,'auth.html',{})

#Get regional officers for specific region
def getRegionOfficers(request, regionId):
    regionOfficers = Member.objects.filter(approle__name='Regional Officer', region_id=regionId)
    logging.debug('regionOfficers: ' + str(regionOfficers))
    return render(request, 'display-region.html', {'regionOfficers': regionOfficers, 'regionId': regionId})


#Get center officers for specific center
def getCenterOfficers(request, centerId):
    centerOfficers = Member.objects.filter(approle__name='Center Officer', center_id=centerId)
    logging.debug('centerOfficers: ' + str(centerOfficers))
    return render(request, 'display-center.html', {'centerId': centerId, 'centerOfficers': centerOfficers})

#Get all centers of a region
def getRegionalCenters(request, regionId):
    centersByRegionId = Center.objects.filter(region_id=regionId)
    logging.debug('centersByRegionId: ' + str(centersByRegionId))

# Search By Member-Names
def search_members(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            searched =  request.POST['searched']

            members = Member.objects.filter(
                Q(first_name__contains=searched)
                | Q(last_name__contains=searched)
                | Q(region__name__contains=searched)
                | Q(orgrole__name__contains=searched)
                | Q(approle__name__contains=searched)).distinct()
            # role_info = MemberInfo.objects.filter(Q(roleDesc__description__icontains =searched))
            # Asset.objects.filter( project__name__contains="Foo" )
            # members = MemberInfo.objects.filter(firstName__contains=searched)
            logging.debug('members: ' + str(members))
            return render(request, 'search-members.html', {'searched':searched, 'members': members})
        else:
            return render(request, 'search-members.html', {})
    else:
        return render(request,'auth.html',{})

def uploadFile(request):

    if request.user.is_authenticated:
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
    else:
        return render(request,'auth.html',{})

def displayRegionCenters(request, regionId):
    centersByRegionId = Center.objects.filter(region_id=regionId)    
    logging.debug('centersByRegionId' + str(centersByRegionId))
    return render(request, 'display-all-centers.html', {'regionId': regionId, 'centersByRegionId': centersByRegionId})

def contactus(request):
    context = {}
    path = 'contactus.html'
    if request.method == 'POST':
        getHelp(request)
        path = 'ack.html'
    else:
        context = getHelp(request)
    return render(request, path, context)

def getMembersForCenter(request, centerId):
    membersForCenter = Member.objects.filter(center_id=centerId)
    logging.debug('membersForCenter' + str(membersForCenter))
    return render(request, 'display-all-members.html', {'centerId': centerId, 'membersForCenter': membersForCenter})