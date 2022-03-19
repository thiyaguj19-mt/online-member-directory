import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import Member, AppRole, OrgRole, Center, Region, Quotes, Metadata
from django.core import serializers
from django.http import JsonResponse
from website import email
from .filters import MemberFilter
from .utils import *
from django.core.cache import cache
import logging
from .auth import *
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.models import Permission, User
from django.shortcuts import get_object_or_404


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

# this new code for authenticate user using
# OOTB user authentication data model


def home(request):

    try:
        print("request.user.is_authenticated--- ",
              request.user.is_authenticated)
        if request.user.is_authenticated:
            quote_message = random_quote()
            return render(request, 'home.html', {'quote': quote_message})
            print("request.user--- ", request.user)
            return render(request, 'home.html', {})
        if request.method == 'POST':
            if request.POST.keys() >= {'emailaddress'}:
                emailaddress = request.POST['emailaddress']
                context = generateAuthCode(request, emailaddress)
                return render(request, 'auth.html', context)
            elif request.POST.keys() >= {'authcode', 'email'}:
                emailaddress = request.POST['email']
                context = authenticateUser(request, emailaddress)
                if context == True:
                    setupAppPermissions(request, emailaddress)
                    return render(request, 'home.html', {})
                else:
                    return render(request, 'auth.html', context)
    except Exception as err:
        print(f'Unexpected {err} from home(), {type(err)}')
        raise
    return render(request, 'auth.html', {})

# To import file - Admin Use


def importFile(request):
    if request.user.is_authenticated:
        return render(request, 'import-page.html', {})
    else:
        return render(request, 'auth.html', {})

# To export file - Admin Use


def exportFile(request):
    if request.user.is_authenticated:
        return render(request, 'export-page.html', {})
    else:
        return render(request, 'auth.html', {})

#Show the USA-Regions Map
def getUSARegionsMap(request):
    return render(request, 'region-map.html', {}) 


# Get all regional officers
def getAllRegionalOfficers(request):
    if request.user.is_authenticated:
        gridcheckflag = request.GET.get('gridcheckflag')
        user = User.objects.filter(username=request.user).first()
        if user.has_perm('website.is_national_officer'):
            officers_data = Member.objects.filter(
                approle__name='Regional Officer')
        else:
            member = Member.objects.filter(email=request.user).first()
            officers_data = Member.objects.filter(
                approle__name='Regional Officer', region=member.region, center__status='Active')
        filterMembers = MemberFilter(request.GET, queryset=officers_data)
        officers_data = filterMembers.qs
        page_obj = Paginator(officers_data, 12)
        page = request.GET.get('page')
        officers_data = page_obj.get_page(page)
        context = {}
        # get regions
        member_regions = getAllRegions()
        # get organization roles
        member_orgroles = getAllOrgRoles()
        # get app_roles
        member_approles = getAllAppRoles()
        if gridcheckflag is not None:
            context = {'officers_data': officers_data,
                       'officer_header': 'Regional Officers',
                       'filterMembers': filterMembers,
                       'gridcheckflag': gridcheckflag}
        else:
            context = {'officers_data': officers_data,
                       'officer_header': 'Regional Officers',
                       'filterMembers': filterMembers}
        context['member_regions'] = member_regions
        context['member_orgroles'] = member_orgroles
        context['member_approles'] = member_approles
        return render(request, 'show-officers.html', context)
    else:
        return render(request, 'auth.html', {})

# Get all national officers


def getAllNationalOfficers(request):
    if request.user.is_authenticated:
        gridcheckflag = request.GET.get('gridcheckflag')
        officers_data = Member.objects.filter(
            approle__name='National Officer', center__status='Active')
        logging.debug('allNationalOfficers: ' + str(officers_data))
        filterMembers = MemberFilter(request.GET, queryset=officers_data)
        officers_data = filterMembers.qs
        page_obj = Paginator(officers_data, 12)
        page = request.GET.get('page')
        officers_data = page_obj.get_page(page)
        # return render(request, 'national-officers-page.html', {'allNationalOfficers': allNationalOfficers, 'filterMembers' : filterMembers})
        context = {}
        # get regions
        member_regions = getAllRegions()
        # get organization roles
        member_orgroles = getAllOrgRoles()
        # get app_roles
        member_approles = getAllAppRoles()
        if gridcheckflag is not None:
            context = {'officers_data': officers_data,
                       'officer_header': 'National Officers',
                       'filterMembers': filterMembers,
                       'gridcheckflag': gridcheckflag}
        else:
            context = {'officers_data': officers_data,
                       'officer_header': 'National Officers',
                       'filterMembers': filterMembers}
        context['member_regions'] = member_regions
        context['member_orgroles'] = member_orgroles
        context['member_approles'] = member_approles
        return render(request, 'show-officers.html', context)
    else:
        return render(request, 'auth.html', {})

# Get all center officers


def getAllCenterOfficers(request):
    if request.user.is_authenticated:
        gridcheckflag = request.GET.get('gridcheckflag')
        user = User.objects.filter(username=request.user).first()
        if user.has_perm('website.is_national_officer'):
            officers_data = Member.objects.filter(
                approle__name='Center Officer', center__status='Active')
        elif user.has_perm('website.is_regional_officer'):
            member = Member.objects.filter(email=request.user).first()
            officers_data = Member.objects.filter(
                approle__name='Center Officer', region=member.region, center__status='Active')
        else:
            member = Member.objects.filter(email=request.user).first()
            officers_data = Member.objects.filter(
                approle__name='Center Officer', center=member.center, center__status='Active')
        logging.debug('officers_data: ' + str(officers_data))
        filterMembers = MemberFilter(request.GET, queryset=officers_data)
        officers_data = filterMembers.qs
        page_obj = Paginator(officers_data, 12)
        page = request.GET.get('page')
        officers_data = page_obj.get_page(page)
        context = {}
        # get regions
        member_regions = getAllRegions()
        # get organization roles
        member_orgroles = getAllOrgRoles()
        # get app_roles
        member_approles = getAllAppRoles()
        if gridcheckflag is not None:
            context = {'officers_data': officers_data,
                       'officer_header': 'Center Officers',
                       'filterMembers': filterMembers,
                       'gridcheckflag': gridcheckflag}
        else:
            context = {'officers_data': officers_data,
                       'officer_header': 'Center Officers',
                       'filterMembers': filterMembers}
        context['member_orgroles'] = member_orgroles
        context['member_regions'] = member_regions
        context['member_approles'] = member_approles
        return render(request, 'show-officers.html', context)
    else:
        return render(request, 'auth.html', {})

# Get regional officers for specific region


def getRegionOfficers(request, regionId):
    regionOfficers = Member.objects.filter(
        approle__name='Regional Officer', region_id=regionId, center__status='Active')
    logging.debug('regionOfficers: ' + str(regionOfficers))
    regionName = ''
    if len(regionOfficers) > 0:
        regionName = regionOfficers[0].region.name
    return render(request, 'display-region.html', {'regionOfficers': regionOfficers, 'regionId': regionId, 'regionName': regionName})


# Get center officers for specific center
def getCenterOfficers(request, centerId):
    centerOfficers = Member.objects.filter(
        approle__name='Center Officer', center_id=centerId, center__status='Active')
    logging.debug('centerOfficers: ' + str(centerOfficers))
    regionName = ''
    if len(centerOfficers) > 0:
        regionName = centerOfficers[0].region.name
    return render(request, 'display-center.html', {'centerId': centerId, 'centerOfficers': centerOfficers, 'regionName': regionName})

# Get all centers of a region


def getRegionalCenters(request, regionId):
    centersByRegionId = Center.objects.filter(
        region_id=regionId, status='Active')
    logging.debug('centersByRegionId: ' + str(centersByRegionId))

# Search By Member-Names


def search_members(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            searched = request.POST['searched']
            members = filtered_search_data(request, searched)
            logging.debug('members: ' + str(members))
            return render(request, 'search-members.html', {'searched': searched, 'members': members})
        else:
            return render(request, 'search-members.html', {})
    else:
        return render(request, 'auth.html', {})


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
                return render(request, 'import-page.html', {"message": "upload failed. check your input file."})
            # let's check if it is a csv file
            if not csv_file.name.endswith('.csv'):
                message = 'Please upload a CSV file'
                return render(request, 'import-page.html', {"message": message})
            else:
                member = Member.objects.filter(email=request.user).first()
                membercenter = member.center
                memberregion = member.region
                canupload = False
                allowall = False
                print(membercenter)
                print(memberregion)
                if importType == "region":
                    if request.user.has_perm('website.is_regional_officer') is not True and\
                       request.user.has_perm('website.is_national_officer') is not True:
                        message = 'Only Regional or National officers have permissions to upload region data.'
                        return render(request, 'import-results.html', {"message": message})
                    else:
                        canupload = True
                elif importType == "member":
                    if request.user.has_perm('website.is_regional_officer') is not True and \
                       request.user.has_perm('website.is_central_officer') is not True and \
                       request.user.has_perm('website.is_national_officer') is not True:
                        message = 'Only Center, Regional or National officers have permissions to upload member data.'
                        return render(request, 'import-results.html', {"message": message})
                    else:
                        canupload = True

            loadeddata = ""
            allowall = request.user.has_perm('website.is_national_officer')

            if canupload is True:
                loadeddata = uploadCSVFile(csv_file, importType,membercenter,memberregion,allowall)

            emailOfficersForApprovalMetaData = get_object_or_404(Metadata, key='email-officers-for-approval')
            if emailOfficersForApprovalMetaData.value:
                emailOfficersForApproval(importType)

            #print(loadeddata, "loadeddata")
            if len(loadeddata) == 0:
                return render(request, 'import-results.html', {"message": message})
            else:
                if loadeddata.__contains__("Error"):
                    message = 'The file you are trying to upload is not valid for the selected option - ' + importType
                    return render(request, 'import-results.html', {"message": message})
                else:
                    return render(request, 'import-results.html', {"loadeddata": loadeddata})
        else:
            return render(request, 'import-page.html', {})
    else:
        return render(request, 'auth.html', {})

def displayRegionCenters(request, regionId):
    centersByRegionId = Center.objects.filter(
        region_id=regionId, status='Active')
    logging.debug('centersByRegionId' + str(centersByRegionId))
    regionName = ''
    if len(centersByRegionId) > 0:
        regionName = centersByRegionId[0].region.name
    return render(request, 'display-all-centers.html', {'regionId': regionId, 'centersByRegionId': centersByRegionId, 'regionName': regionName})


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


def getMemberData(request):
    if request.headers.keys() >= {'Emailid'}:
        emailId = request.headers['Emailid']
        if len(emailId) > 0:
            memberdata = Member.objects.filter(email=emailId)
            return JsonResponse(serializers.serialize('json', memberdata), safe=False)
    else:
        return None


def updateMemberProfile(request):
    data = json.loads(request.body)
    if len(data) > 0:
        emailid = data['emailaddr']
        first_name = data['first_name']
        last_name = data['last_name']
        orglist = data['orgrole']
        #age_group = data['agegroup']
        approle = data['approle']
        if emailid is not None:
            member = Member.objects.filter(email=emailid)
            member.update(first_name=first_name,
                          last_name=last_name,
                          approle=approle)
            if len(orglist) > 0:
                member = member.first()
                allroles = OrgRole.objects.all()
                for orgRole in allroles:
                    for orole in orglist:
                        if int(orgRole.id) == int(orole):
                            member.orgrole.add(orgRole)
                    if str(orgRole.id) not in orglist:
                        member.orgrole.remove(orgRole)
        return JsonResponse({"message": "Record successfully updated."}, safe=False)


def updateMemberStatus(request):
    data = json.loads(request.body)
    if len(data) > 0:
        print("data----", data)
        emailid = data['emailaddr']
        member_status = data['member_status']
        if emailid is not None:
            memberdata = Member.objects.filter(
                email=emailid).update(member_status=member_status)
        return JsonResponse({"message": "Record successfully updated."}, safe=False)
