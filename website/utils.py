import io
import csv
from .models import *
from django.core.cache import cache
import logging
import datetime
from .email import sendemail
from random import randint
from django.http import HttpResponse

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
            print("error in createRegionData: " , ex)
        if region != None:
            created = False
            try:
                _, created = Center.objects.update_or_create(
                    region=region,
                    name=column[1],
                    address = column[2],
                    city = column[3],
                    state = column[4],
                    zip_code = column[5],
                    country = column[6],
                    phone = column[7],
                    website = column[8],
                    latitude = column[9],
                    longitude = column[10],
                    status=column[11],
                    center_type=column[12]
                )
            except Exception as err:
                print(f'Unexpected {err} from createRegionData(), {type(err)}')

            if created:
                newCenter = column[1]
                return {"column2" : newCenter, "column1": newRegion}
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

            member_status=0
            if len(column[12]) > 0:
                if column[12] == 'Approved':
                    member_status = 1

            start_date = None
            end_date = None

            #read start and end date from input file then assign the same to member data
            #if user app role is one of an officer role then 2 years will be added
            #if end_date is not provided
            if len(column[15]) > 0:
                start_date = datetime.datetime.strptime(column[15], "%m/%d/%Y").date()
                if len(column[16]) > 0:
                    end_date = datetime.datetime.strptime(column[16], "%m/%d/%Y").date()
                elif arole.name != "Member":
                    end_date = start_date + datetime.timedelta(days=730)

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
                    city=column[7],
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
                    return {"column1" : column}
            else:
                #update region and center_role
                member.region = region
                member.center = center
                member.save()
                #add orgRole
                member.orgrole.add(orole)
        except Exception as ex:
            print("error in createMemberData: " , ex)
            return {"column1" : "something went wrong- " + str(ex)}
        return None

def uploadCSVFile(csv_file, type):
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    context = []
    loopindex = 0
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        if loopindex == 0:
            loopindex += 1
            continue
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
                result = obj.objects.filter(name = columnval).first()
            else:
                result = obj.objects.filter(email = columnval).first()
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
        metadata = Metadata.objects.filter(key__contains='contact-header-line').first()
        context = {'metadata' : metadata.value}
    elif request.method == 'POST':
        if request.POST.keys() >= { 'fullname', 'email', 'subject', 'message' }:
            path = 'contactus.html'
            msgheader = Metadata.objects.get(key='contact-msg-header')
            contactaddress = Metadata.objects.get(key='contact-email')
            messagebody = "".join("<table>"
                        + "<tr style='background-color: #f2f2f2;'>"
                        + "<td>Full Name</td>"
                        + "<td>" + request.POST.get('fullname') + "</td>"
                        + "</tr>"
                        + "<tr style='background-color: #f2f2f2;'>"
                        + "<td>Email</td>"
                        + "<td>" + request.POST.get('email') + "</td>"
                        + "</tr>"
                        + "<tr style='background-color: #f2f2f2;'>"
                        + "<td>Subject</td>"
                        + "<td>" + request.POST.get('subject') + "</td>"
                        + "</tr>"
                        + "<tr style='background-color: #f2f2f2;'>"
                        + "<td>Message</td>"
                        + "<td>" + request.POST.get('message') + "</td>"
                        + "</tr>"
                        + "</table>")
            sendemail(contactaddress.value, msgheader.value, messagebody)
        else:
            return HttpResponse('Something went wrong. Please try again later.')
    return context
