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
            a_member = Member.objects.filter(member_status=1, region__name=region.name).exclude(approle__name='Member')
            cache.set("getApprovedOfficersByRegion_" + str(region.id), a_member)
        if a_member.count() > 0:
            return True
        else:
            return False


    def getUnApprovedAllRegionalOfficer(self):
        u_member = cache.get("getUnApprovedAllRegionalOfficer")
        if u_member is None:
            u_member = Member.objects.filter(member_status=0, approle__name='Regional Officer')
            cache.set("getUnApprovedAllRegionalOfficer", u_member)
        if u_member.count() > 0:
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

    def processdata(self, region, approvers, members):
        for approver in approvers:
            memberbycenter = []
            approverbycenter = []
            for member in members:
                if member.center.name == approver.center.name:
                    memberbycenter.append(member)
                    if approver not in approverbycenter:
                        approverbycenter.append(approver)
            if len(memberbycenter) > 0:
                self.sendNotificationToTheUser(region, approverbycenter, memberbycenter)


    def sendNotificationToTheUser(self, region, approvers, members):
        try:
            saluation = Metadata.objects.filter(key='email-officer-salution').first().value
            print('saluation---', saluation)
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
            '''

            html_header = html_header + 'Dear ' + saluation + '<br><br>'
            msg_body = Metadata.objects.filter(key='email-officer-msgbody').first().value
            video_link = Metadata.objects.filter(key='video-link').first().value
            html_header = html_header + msg_body + ' <a href="' + video_link + '" target="_blank" />Click Here</a>' + '<br><br>'

            header = "<table><tr><th>Name</th><th>Email</th><th>Role</th></tr>"

            logging.info("members----" + str(list(members)))

            tableData = ""
            for officer in members:
                tableData += f"<tr><td>{officer.first_name + ' ' + officer.last_name}</td><td>{officer.email}</td><td>{officer.approle}</td></tr>"
            end = "</table>"
            end += '''<br>Thank You,<br>From SSSIO IT Team</h2>'''

            body = html_header + header + tableData + end

            print('body....', body)

            officer_emailAddress = []
            for approver in approvers:
                officer_emailAddress.append(approver.email)
            logging.info("officer_emailAddress--- "  + str(list(officer_emailAddress)))
            if len(officer_emailAddress) > 0:
                sendemail(officer_emailAddress,
                        "New member(s) added to the Officers Portal", body)
                if config("local", False):
                    print('region notification will remain True since its local env')
                else:
                    region.notification=False
                    region.save()
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
                index = 1
                for reg in region:
                    for ar in app_role:
                        #check if there is any approved members in the region
                        if self.getApprovedOfficersByRegion(reg):
                            approver = None
                            v_member = None
                            print ("ar.name--> ", ar.name)
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
                            elif index == 1 and ar.name == 'National Officer':
                                index = index + 1
                                logging.debug("look for unapproved region officers ")
                                #approver = cache.get('getApprovedOfficersByRegion_' + str(reg.id)).filter(approle__name='National Officer')
                                approver = Member.objects.filter(member_status=1, approle__name='National Officer')
                                if approver.count() > 0:
                                    if self.getUnApprovedAllRegionalOfficer():
                                        v_member = cache.get('getUnApprovedAllRegionalOfficer')
                            if v_member is not None and v_member.count() > 0:
                                if ar.name == 'Center Officer':
                                    self.processdata(reg, approver, v_member)
                                else:
                                    self.sendNotificationToTheUser(reg, approver, v_member)
                        else:
                            #email admins that there no approved officers found
                            logging.debug("No admins found for " + reg.name)
            else:
                print('flag email-officers-for-approval is not turned on to send email')
        except Exception as err:
            self.stdout.write(self.style.ERROR('error in sending notification to the officers'))
            print("err-message-", err)