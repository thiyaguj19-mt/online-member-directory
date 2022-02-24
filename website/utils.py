import io
import csv
from .models import Center, Region, Member, OrgRole, AppRole, Metadata
from django.core.cache import cache
import logging
import datetime
from .email import sendemail

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

def createRegionData(column):
    if len(column) > 0:
        region = None
        regionval = column[0]
        try:
            newCenter = None
            newRegion = None
            region = retrieveFromCache(Region, regionval, "name")
            if region == None:
                region = Region(name=column[0])
                region.save()
                newRegion = column[0]
            else:
                newRegion = region.name
        except Exception as ex:
            print("error in createRegionData: " , ex)
        if region != None:
            _, created = Center.objects.update_or_create(
                region=region,
                name=column[1]
            )
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
            end_date= None

            #startdate_str = retrieveFromCache(Member, column[15], "start_date")
            #dt_obj = datetime.datetime.strptime(startdate_str, '%Y/%m/%d')
            #formatted_date = datetime.datetime.strftime(dt_obj, "%m/%d/%Y")
            #start_date = formatted_date
            #end_date = datetime.datetime.strftime(dt_obj + datetime.timedelta(days=730), "%m/%d/%Y")

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

def getHelp(request):
    context = {}
    if request.method == 'GET':
        metadata = Metadata.objects.filter(key__contains='contact-header-line').first()
        context = {'metadata' : metadata.value}
    elif request.method == 'POST':
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
                    + "<td>Phone</td>"
                    + "<td>" + request.POST.get('phone') + "</td>"
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
    return context
