import io
import csv
from .models import Center, Region, Member, OrgRole, AppRole
from django.core.cache import cache
import logging

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

            orole = retrieveFromCache(OrgRole, column[8], "name")
            arole = retrieveFromCache(AppRole, column[9], "name")
            region = retrieveFromCache(Region, column[12], "name")
            center = retrieveFromCache(Center, column[13], "name")
            member = retrieveFromCache(Member, column[3], "email")

            created = False
            memobj = None
            if member == None:
                memobj, created = Member.objects.update_or_create(
                    first_name=column[0],
                    last_name=column[1],
                    gender=column[2],
                    email=column[3],
                    phone=column[4],
                    address=column[5],
                    age=column[6],
                    verified=column[7],
                    approle=arole,
                    start_date=None,
                    end_date=None,
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
