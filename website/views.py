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

# #Show All Cards of Region Officers
# def show_regions(request):
#     return render(request, 'show-region.html',{})


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
                loadeddata = ""
                loadeddata = uploadCSVFile(csv_file, importType)

            emailOfficersForApprovalMetaData = Metadata.objects.get(
                key='email-officers-for-approval')
            if emailOfficersForApprovalMetaData.value:
                emailOfficersForApproval(importType)

            # print(loadeddata, "loadeddata")
            if len(loadeddata) == 0:
                return render(request, 'import-page.html', {"message": message})
            else:
                return render(request, 'import-page.html', {"loadeddata": loadeddata})
        else:
            return render(request, 'import-page.html', {})
    else:
        return render(request, 'auth.html', {})


def emailOfficersForApproval(importType):
    if importType == "member":
        # Querying member Table to get all Unique Regions Ids
        uniqueRegionsQuerySet = Member.objects.values(
            'region_id').distinct()

        uniqueCentersQuerySet = Member.objects.values(
            'center_id').distinct()

        uniqueRegionIds, uniqueCenterIds = set([]), set([])
        for regionObject in uniqueRegionsQuerySet:
            if regionObject['region_id']:
                uniqueRegionIds.add(regionObject['region_id'])

        for centerObject in uniqueCentersQuerySet:
            if centerObject['center_id']:
                uniqueCenterIds.add(centerObject['center_id'])

        officers = Member.objects.filter(
            region_id__in=list(uniqueRegionIds)).exclude(approle__name='member')

        officers_list, regionOfficers, centerOfficersInRegion = [], {}, {}
        for officer in officers:
            officerObj = {
                "first_name":  officer.first_name,
                "last_name": officer.last_name,
                "email": officer.email,
                "appRole": officer.approle.name,
                "region_id": officer.region_id,
                "center_id": officer.center_id,
                "member_status": officer.member_status,
                "region": officer.region,
                "center": officer.center
            }
            officers_list.append(officerObj)

            if officerObj["region_id"] not in regionOfficers:
                regionOfficers[officerObj["region_id"]] = []
            if officerObj["region_id"] not in centerOfficersInRegion:
                centerOfficersInRegion[officerObj["region_id"]] = [
                ]

            if officerObj["appRole"] == "Regional Officer":
                regionOfficers[officerObj["region_id"]].append(
                    officerObj)
            if officerObj["appRole"] == "Center Officer":
                centerOfficersInRegion[officerObj["region_id"]].append(
                    officerObj)

        emailUnApprovedCenterOfficers(
            regionOfficers, centerOfficersInRegion)


def emailUnApprovedCenterOfficers(regionOfficers, centerOfficersInRegion):
    try:
        for regionId, officers in centerOfficersInRegion.items():
            unApprovedCenterofficersByRegion = []
            for officer in officers:
                if officer["member_status"] == 0:
                    unApprovedCenterofficersByRegion.append(officer)

            if len(regionOfficers[regionId]) > 0 and len(unApprovedCenterofficersByRegion) > 0:
                regionalOfficerEmails = []
                for regionalOfficer in regionOfficers[regionId]:
                    if regionalOfficer["member_status"] == 1 and regionalOfficer["email"] not in regionalOfficerEmails:
                        regionalOfficerEmails.append(
                            regionalOfficer["email"])

                html_header = '''<!DOCTYPE html><html><head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><h2>
                \n Dear Regional Officer(s),
                \n Following Center Officers have been imported in Officers App. Could you verify their details and set their status to Approved.
                \n Thank You,
                \n From SSSIO IT Team</h2>'''

                header = "<table><tr><th>Name</th><th>Email</th><th>Role</th></tr>"

                tableData = ""
                for officer in unApprovedCenterofficersByRegion:
                    tableData += f"<tr><td>{officer['first_name'] + ' ' +officer['last_name']}</td><td>{officer['email']}</td><td>{officer['appRole']}</td></tr>"
                end = "</table>"

                body = html_header + header + tableData + end

                if len(regionalOfficerEmails) > 0:
                    sendemail(regionalOfficerEmails,
                              "List of Unapproved Center Officers", body)
    except:
        logging.error("Error while Sending email to Officers")


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
