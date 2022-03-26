from django.core.management.base import BaseCommand, CommandError
from website.models import *
import datetime
from swingtime import models as swingtime
from django.contrib.auth.models import User
from decouple import config
from website.email import sendemail

class Command(BaseCommand):
    help = 'notify officers'

    def getApprovedOfficersByRegion(self, region):
        a_member = cache.get("getApprovedOfficersByRegion_" + str(region.id))
        if a_member is None:
            a_member = Member.objects.filter(member_status=1, region__name=region.name).exclude(approle__name='member')
            cache.set("getApprovedOfficersByRegion_" + str(region.id), a_member)
        if a_member.count() > 0:
            return True
        else:
            return False

    def getUnApprovedMembersByRegion(self, region):
        u_member = cache.get("getUnApprovedMembersByRegion_" + str(region.id))
        if u_member is None:
            u_member = Member.objects.filter(member_status=0, region__name=region.name)
            cache.set("getUnApprovedMembersByRegion_" + str(region.id), u_member)
        if u_member.count() > 0:
            return True
        else:
            return False

    def getAppRole(self):
        app_role = cache.get('app_role_batch')
        if app_role is None:
            app_role = AppRole.objects.exclude(name='Member')
            cache.set('app_role_batch', app_role)
        return app_role

    def handle(self, *args, **options):
        try:
            #query region and find out which region which we need to send notification
            region = Region.objects.filter(notification=True)
            app_role = self.getAppRole()
            print(app_role)
            for reg in region:
                for ar in app_role:
                    #check if there is any approved members in the region
                    if self.getApprovedOfficersByRegion(reg):
                        officer = None
                        if ar.name == 'Center Officer':
                            officer = cache.get('getApprovedOfficersByRegion_' + str(reg.id)).filter(approle__name='Center Officer')
                            print(ar.name, " " ,officer)
                        elif ar.name == 'Regional Officer':
                            officer = cache.get('getApprovedOfficersByRegion_' + str(reg.id)).filter(approle__name='Regional Officer')
                        elif ar.name == 'National Officer':
                            officer = cache.get('getApprovedOfficersByRegion_' + str(reg.id)).filter(approle__name='National Officer')
                        print("officer.... " , officer.count())
                        #find all unapproved member in the current region
                        #0 means unapproved and 1 means approved
                        if self.getUnApprovedMembersByRegion(reg):
                            u_member = cache.get('getApprovedOfficersByRegion_' + str(reg.id))
                            print('u_member ', u_member)
                        else:
                            #since no unapproved member found. region notification will set to false
                            reg.update(notification=False)
                    else:
                        #email admins that there no approved officers found
                        print("No admins found for " , reg.name)
        except Exception as err:
            self.stdout.write(self.style.ERROR('error in sending notification to the officers'))
            print("err-message-", err)