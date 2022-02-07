import io
import csv
from .models import Center, Region, Member, OrgRole, AppRole

def createRegionData(column):
    if len(column) > 0:
        region = None
        regionval = column[0]
        try:
            newCenter = None
            newRegion = None
            region = Region.objects.filter(name = regionval).first()
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
                return {"center" : newCenter, "region": newRegion}
            else:
                return None

def createMemberData(column):
    if len(column) > 0:
        try:
            orole = OrgRole.objects.filter(name = column[8]).first()
            arole = AppRole.objects.filter(name = column[9]).first()
            region = Region.objects.filter(name = column[12]).first()
            center = Center.objects.filter(name = column[13]).first()
            member = Member.objects.filter(email = column[3]).first()
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
        except Exception as ex:
            print("error in createMemberData: " , ex)

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
    return context
