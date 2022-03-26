from django.core.management.base import BaseCommand, CommandError
from website.models import *
import datetime
from swingtime import models as swingtime
from django.contrib.auth.models import User
from decouple import config
from website.email import sendemail
from decouple import config
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

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

    def processdata(self, approvers, members):
        for approver in approvers:
            memberbycenter = []
            approverbycenter = []
            for member in members:
                if member.center.name == approver.center.name:
                    memberbycenter.append(member)
                    if approver not in approverbycenter:
                        approverbycenter.append(approver)
            if len(memberbycenter) > 0:
                self.sendNotificationToTheUser(approverbycenter, memberbycenter)


    def sendNotificationToTheUser(self, approvers, members):
        try:
            html_header = '''<!DOCTYPE html>
            <html>
            <head>
                <style>
                    table {
                        font-family: arial, sans-serif;
                        border-collapse: collapse;
                        width: 100%;
                    }
                    td, th {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                    }
                    tr:nth-child(even) {
                    background-color: #dddddd;
                    }
                </style>
            </head>
            <body>
            Dear Officer(s),<br>
            <br> Following members have been added into Officers App recently. Could you verify their detail and mark their profile verified in the application.<br><br>
            '''

            header = "<table><tr><th>Name</th><th>Email</th><th>Role</th></tr>"

            logging.info("members----" + str(list(members)))

            tableData = ""
            for officer in members:
                tableData += f"<tr><td>{officer.first_name + ' ' + officer.last_name}</td><td>{officer.email}</td><td>{officer.approle}</td></tr>"
            end = "</table>"
            end += '''<br>Thank You,<br>From SSSIO IT Team</h2>'''

            body = html_header + header + tableData + end

            officer_emailAddress = []
            for approver in approvers:
                officer_emailAddress.append(approver.email)
            logging.info("officer_emailAddress--- "  + str(list(officer_emailAddress)))
            if len(officer_emailAddress) > 0:
                sendemail(officer_emailAddress,
                        "New member(s) added to the Officers Portal", body)
        except Exception as err:
            self.stdout.write(self.style.ERROR('sendNotificationToTheUser() throwed an error'))
            print("err-message-", err)

    def handle(self, *args, **options):
        try:
            meta = Metadata.objects.filter(key='email-officers-for-approval').first()
            if meta is not None and bool(meta.value) is True:
                #query region and find out which region which we need to send notification
                region = Region.objects.filter(notification=True)
                app_role = self.getAppRole()
                turnOffNotification = False
                for reg in region:
                    for ar in app_role:
                        #check if there is any approved members in the region
                        if self.getApprovedOfficersByRegion(reg):
                            approver = None
                            v_member = None
                            if ar.name == 'Center Officer':
                                logging.debug("look for unapproved members in " + reg.name)
                                approver = cache.get('getApprovedOfficersByRegion_' + str(reg.id)).filter(approle__name='Center Officer')
                                if approver.count() > 0:
                                    if self.getUnApprovedMembersByRegion(reg):
                                        v_member = cache.get('getUnApprovedMembersByRegion_' + str(reg.id)).filter(approle__name='Member')
                            elif ar.name == 'Regional Officer':
                                logging.debug("look for unapproved center officers in " + reg.name)
                                approver = cache.get('getApprovedOfficersByRegion_' + str(reg.id)).filter(approle__name='Regional Officer')
                                if approver.count() > 0:
                                    if self.getUnApprovedMembersByRegion(reg):
                                        v_member = cache.get('getUnApprovedMembersByRegion_' + str(reg.id)).filter(approle__name='Center Officer')
                            elif ar.name == 'National Officer':
                                logging.debug("look for unapproved region officers in " + reg.name)
                                approver = cache.get('getApprovedOfficersByRegion_' + str(reg.id)).filter(approle__name='National Officer')
                                if approver.count() > 0:
                                    if self.getUnApprovedMembersByRegion(reg):
                                        v_member = cache.get('getUnApprovedMembersByRegion_' + str(reg.id)).filter(approle__name='Regional Officer')
                            if v_member is not None and v_member.count() > 0:
                                if ar.name == 'Center Officer':
                                    self.processdata(approver, v_member)
                                else:
                                    self.sendNotificationToTheUser(approver, v_member)
                            else:
                                turnOffNotification = True
                        else:
                            #email admins that there no approved officers found
                            logging.debug("No admins found for " + reg.name)
            else:
                print('flag email-officers-for-approval is not turned on to send email')
        except Exception as err:
            self.stdout.write(self.style.ERROR('error in sending notification to the officers'))
            print("err-message-", err)