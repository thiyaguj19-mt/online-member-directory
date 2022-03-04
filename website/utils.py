import io
import csv
from pydoc import describe
from .models import *
from django.core.cache import cache
import logging
import datetime
from .email import sendemail
from random import randint
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import Permission, User

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)


def createRegionData(column):
    if len(column) > 0:
        region = None
        regionval = column[0]
        try:
            newCenter = None
            newRegion = None
            region = retrieveFromCache(Region, regionval, "name")
            print("region-val-", region)
            if region == None:
                region = Region(name=column[0])
                region.save()
                newRegion = column[0]
                print("region-name-", region.name)
            else:
                newRegion = region.name
        except Exception as ex:
            print("error in createRegionData: ", ex)
        if region != None:
            created = False
            try:
                _, created = Center.objects.update_or_create(
                    region=region,
                    name=column[1],
                    address=column[2],
                    city=column[3],
                    state=column[4],
                    zip_code=column[5],
                    country=column[6],
                    phone=column[7],
                    website=column[8],
                    latitude=column[9],
                    longitude=column[10],
                    status=column[11],
                    center_type=column[12]
                )
            except Exception as err:
                print(f'Unexpected {err} from createRegionData(), {type(err)}')

            if created:
                newCenter = column[1]
                return {"column2": newCenter, "column1": newRegion}
            else:
                return None


def createMemberData(column):
    if len(column) > 0:
        #print ("column--", column)
        try:

            member = retrieveFromCache(Member, column[3], "email")
            orole = retrieveFromCache(OrgRole, column[13], "name")
            arole = retrieveFromCache(AppRole, column[14], "name")
            region = retrieveFromCache(Region, column[17], "name")
            center = retrieveFromCache(Center, column[18], "name")

            member_status = 0
            if len(column[12]) > 0:
                if column[12] == 'Approved':
                    member_status = 1

            start_date = None
            end_date = None

            # read start and end date from input file then assign the same to member data
            # if user app role is one of an officer role then 2 years will be added
            # if end_date is not provided
            if len(column[15]) > 0:
                start_date = datetime.datetime.strptime(
                    column[15], "%m/%d/%Y").date()
                if len(column[16]) > 0:
                    end_date = datetime.datetime.strptime(
                        column[16], "%m/%d/%Y").date()
                elif arole.name != "Member":
                    end_date = start_date + datetime.timedelta(days=730)

            # Get city from center if not available
            city = None
            if len(column[7]) > 0:
                city = column[7]
            else:
                if len(column[18]) > 0:
                    res = column[18].split("of")
                    city = res[-1]

            created = False
            memobj = None
            if member == None:
                memobj, created = Member.objects.update_or_create(
                    first_name=column[0],
                    last_name=column[1],
                    gender=column[2],
                    email=column[3],
                    phone=column[4],
                    address_1=column[5],
                    address_2=column[6],
                    city=city,
                    state=column[8],
                    zip_code=column[9],
                    country=column[10],
                    age_group=column[11],
                    member_status=member_status,
                    approle=arole,
                    start_date=start_date,
                    end_date=end_date,
                    region=region,
                    center=center,
                )
                if created:
                    memobj.orgrole.add(orole)
                    return {"column1": column}
            else:
                # update region and center_role
                member.region = region
                member.center = center
                member.save()
                # add orgRole
                member.orgrole.add(orole)
        except Exception as ex:
            print("error in createMemberData: ", ex)
            return {"column1": "something went wrong- " + str(ex)}
        return None


def createOrgRole(column):
    if len(column) > 0:
        orgRole = OrgRole(name=column[1], description=column[2])
        orgRole.save()
        return {"column1": column}
    return None


def createQuotes(column):
    if len(column) > 0:
        quotes = Quotes(message=column[1], cite=column[2])
        quotes.save()
        return {"column1": column}
    return None


def uploadCSVFile(csv_file, type):
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    context = []
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        if type == "region":
            region_data = createRegionData(column)
            if region_data != None:
                context.append(region_data)
        elif type == "member":
            member_data = createMemberData(column)
            if member_data != None:
                #print (member_data)
                if member_data not in context:
                    context.append(member_data)
        elif type == "orgRole":
            orgrole_data = createOrgRole(column)
            if orgrole_data != None:
                context.append(orgrole_data)
        elif type == "quotes":
            quotes_data = createQuotes(column)
            if quotes_data != None:
                context.append(quotes_data)
    return context


def retrieveFromCache(obj, columnval, field):

    result = None
    try:
        logging.debug('columnval: ' + columnval)
        if cache.get(columnval):
            result = cache.get(columnval)
            logging.debug('result from cache: ' + str(columnval))
        else:
            logging.debug('field: ' + field)
            if field == "name":
                result = obj.objects.filter(name=columnval).first()
            else:
                result = obj.objects.filter(email=columnval).first()
                logging.debug('result from database: ' + str(result))
            #print("region---from..db....." , region)
            cache.set(columnval, result)
    except Exception as ex:
        print("error from retrieveFromCache - " + str(ex))
    #print("retrieveFromCache-result, " , result)
    return result


def random_quote():
    random_quote = None
    quotes_count = 0
    if cache.get("random_quote"):
        random_quote = cache.get("random_quote")
        quotes_count = cache.get("quotes_count")
    else:
        quotes_count = Quotes.objects.count()
        if quotes_count > 0:
            random_quote = Quotes.objects.all()[randint(0, quotes_count - 1)]
            cache.set("quotes_count", quotes_count)
            cache.set("random_quote", random_quote)
    return random_quote


def getAllAppRoles():
    mem_appRoles = None
    if cache.get("mem_appRoles"):
        mem_appRoles = cache.get("mem_appRoles")
    else:
        mem_appRoles = AppRole.objects.all()
        cache.set("mem_appRoles", mem_appRoles)
    return mem_appRoles


def getAllOrgRoles():
    mem_roles = None
    if cache.get("member_orgroles"):
        mem_roles = cache.get("member_orgroles")
    else:
        mem_roles = OrgRole.objects.all()
        cache.set("member_orgroles", mem_roles)
    return mem_roles


def getAllRegions():
    mem_regions = None
    if cache.get("member_regions"):
        mem_regions = cache.get("member_regions")
    else:
        mem_regions = Region.objects.all()
        cache.set("member_regions", mem_regions)
    return mem_regions


def getHelp(request):
    context = {}
    if request.method == 'GET':
        metadata = Metadata.objects.filter(
            key__contains='contact-header-line').first()
        context = {'metadata': metadata.value}
    elif request.method == 'POST':
        if request.POST.keys() >= {'fullname', 'email', 'subject', 'message'}:
            path = 'contactus.html'
            msgheader = Metadata.objects.get(key='contact-msg-header')
            contactaddress = Metadata.objects.get(key='contact-email')
            messagebody = "".join("<table>"
                                  + "<tr style='background-color: #f2f2f2;'>"
                                  + "<td>Full Name</td>"
                                  + "<td>" +
                                  request.POST.get('fullname') + "</td>"
                                  + "</tr>"
                                  + "<tr style='background-color: #f2f2f2;'>"
                                  + "<td>Email</td>"
                                  + "<td>" +
                                  request.POST.get('email') + "</td>"
                                  + "</tr>"
                                  + "<tr style='background-color: #f2f2f2;'>"
                                  + "<td>Subject</td>"
                                  + "<td>" +
                                  request.POST.get('subject') + "</td>"
                                  + "</tr>"
                                  + "<tr style='background-color: #f2f2f2;'>"
                                  + "<td>Message</td>"
                                  + "<td>" +
                                  request.POST.get('message') + "</td>"
                                  + "</tr>"
                                  + "</table>")
            sendemail(contactaddress.value, msgheader.value, messagebody)
        else:
            return HttpResponse('Something went wrong. Please try again later.')
    return context


def filtered_search_data(request, searched):
    members = None
    try:
        user = User.objects.filter(username=request.user).first()
        print("who is that? ", user)
        member = Member.objects.filter(email=request.user).first()
        print("user.is_staff----", user.is_staff)
        if user.is_staff == False:
            regionId = member.region.id
            centerId = member.center.id
        if user.is_staff or user.has_perm('website.is_national_officer') == True:
            print("is_national_officer----")
            members = Member.objects.filter(
                Q(first_name__contains=searched)
                | Q(last_name__contains=searched)
                | Q(region__name__contains=searched)
                | Q(orgrole__name__contains=searched)
                | Q(approle__name__contains=searched),
                center__status='Active').distinct()
        elif user.has_perm('website.is_regional_officer') == True:
            print("is_regional_officer----")
            members = Member.objects.filter(
                Q(first_name__contains=searched)
                | Q(last_name__contains=searched)
                | Q(region__name__contains=searched)
                | Q(orgrole__name__contains=searched)
                | Q(approle__name__contains=searched), center__status='Active', region=regionId).distinct()
        elif user.has_perm('website.is_central_officer') == True:
            print("is_central_officer----")
            members = Member.objects.filter(
                Q(first_name__contains=searched)
                | Q(last_name__contains=searched)
                | Q(region__name__contains=searched)
                | Q(orgrole__name__contains=searched)
                | Q(approle__name__contains=searched), center__status='Active', center=centerId).distinct()
    except Exception as err:
        print("error in filtered_search_data---", err)
    return members


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
