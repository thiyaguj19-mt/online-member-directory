import io
import csv
from .models import Center, Region

def createRegionData(column):
    if len(column) > 0:
        region = None
        regionval = column[0]
        try:
            newCenter = None
            newRegion = None
            print("regionval---" , regionval)
            region = Region.objects.filter(name = regionval).first()
            print("region---" , region)
            if region == None:
                region = Region(name=column[0])
                region.save()
                newRegion = column[0]
            else:
                newRegion = region.name
            print("newRegion---" , newRegion)
        except Exception as ex:
            print("error in createRegionData: " , ex)
        print("value of region---" , region)
        if region != None:
            _, created = Center.objects.update_or_create(
                region=region,
                name=column[1]
            )
            print("value of created---" , created)
            if created:
                newCenter = column[1]
                return {"center" : newCenter, "region": newRegion}
            else:
                return None

def uploadCSVFile(csv_file, type):
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    context = []
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        if type == "Region":
            region_data = createRegionData(column)
            print("value of region_data---" , region_data)
            if region_data != None:
                context.append(region_data)
    return context
