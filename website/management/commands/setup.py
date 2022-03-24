from django.core.management.base import BaseCommand, CommandError
from website.models import *
import datetime
from swingtime import models as swingtime
from django.contrib.auth.models import User
from decouple import config

class Command(BaseCommand):
    help = 'setup environment'

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.WARNING('create swingtime event...'))
            st = swingtime.EventType.objects.count()
            if st > 0:
                self.stdout.write(self.style.NOTICE('swingtime event already exist...'))
            else:
                et = swingtime.EventType.objects.create(abbr='e1', label='SSSIO event')
                self.stdout.write(self.style.SUCCESS('Created SSSIO event'))

            self.stdout.write(self.style.WARNING('create metadata...'))

            key = 'smtp-from-email'
            value = config('EMAIL_HOST_USER', '')
            metadata = Metadata.objects.filter(key=key).first()
            if metadata is None:
                Metadata.objects.create(key=key, value=value)
                self.stdout.write(self.style.SUCCESS('successfully added ' + key +' key in metadata'))

            key = 'email-officers-for-approval'
            value = False
            metadata = Metadata.objects.filter(key=key).first()
            if metadata is None:
                Metadata.objects.create(key=key, value=value)
                self.stdout.write(self.style.SUCCESS('successfully added ' + key +' key in metadata'))

            key = 'email-common-footer'
            value = 'For any assistance please contact SSSIO Officers Portal via Contact Us link on the website'
            metadata = Metadata.objects.filter(key=key).first()
            if metadata is None:
                Metadata.objects.create(key=key, value=value)
                self.stdout.write(self.style.SUCCESS('successfully added ' + key +' key in metadata'))

            key = 'contact-msg-header'
            value = '''Officer's App - You have received a message'''
            metadata = Metadata.objects.filter(key=key).first()
            if metadata is None:
                Metadata.objects.create(key=key, value=value)
                self.stdout.write(self.style.SUCCESS('successfully added ' + key +' key in metadata'))

            key = 'contact-email'
            value = config('contact-email', '')
            metadata = Metadata.objects.filter(key=key).first()
            if metadata is None:
                Metadata.objects.create(key=key, value=value)
                self.stdout.write(self.style.SUCCESS('successfully added ' + key +' key in metadata'))


            self.stdout.write(self.style.WARNING('create superuser...'))
            admin_name = config("ADMIN_NAME", "admin")
            admin_password = config("ADMIN_PASS", None)
            if admin_password is not None:
                user = User.objects.filter(username=admin_name).first()
                if user is None:
                    User.objects.create_superuser(admin_name, 'admin@example.com', admin_password)
                    self.stdout.write(self.style.SUCCESS('created admin user...'))
                else:
                    self.stdout.write(self.style.NOTICE('admin user already exist'))
            else:
                self.stdout.write(self.style.NOTICE('ADMIN_PASS not supplied hence skipping admin user creation'))


            self.stdout.write(self.style.WARNING('create app roles...'))
            
            name='Member'
            level='L1'
            approle = AppRole.objects.filter(name=name).first()
            if approle is None:
                AppRole.objects.create(name=name, level=level)
                self.stdout.write(self.style.SUCCESS('Added '+ name+ ' entry in AppRole...'))

            name='Center Officer'
            level='L2'
            approle = AppRole.objects.filter(name=name).first()
            if approle is None:
                AppRole.objects.create(name=name, level=level)
                self.stdout.write(self.style.SUCCESS('Added '+ name+ ' entry in AppRole...'))

            name='Regional Officer'
            level='L3'
            approle = AppRole.objects.filter(name=name).first()
            if approle is None:
                AppRole.objects.create(name=name, level=level)
                self.stdout.write(self.style.SUCCESS('Added '+ name+ ' entry in AppRole...'))

            name='National Officer'
            level='L4'
            approle = AppRole.objects.filter(name=name).first()
            if approle is None:
                AppRole.objects.create(name=name, level=level)
                self.stdout.write(self.style.SUCCESS('Added '+ name+ ' entry in AppRole...'))

        except Exception as err:
            self.stdout.write(self.style.ERROR('error creating the data'))
            print("err-message-", err)