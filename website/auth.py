from .email import sendemail
import string
import random
from django.core.cache import cache
import logging
from datetime import datetime
from .models import Member, Metadata
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission, User
from decouple import config

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
today = datetime.now().strftime("%d%m%y")

def setupAppPermissions(request, emailaddress):
    try:
        user = User.objects.filter(username=emailaddress).first()
        member = Member.objects.filter(email=emailaddress).first()
        if user is not None:
            if member.approle.name == 'Center Officer':
                permission = Permission.objects.filter(codename='is_central_officer').first()
                print("permission-- ", permission)
                if user.has_perm('website.is_central_officer') != True:
                    user.user_permissions.add(permission)
                    print("added permission-- ")
            elif member.approle.name == 'Regional Officer':
                permission = Permission.objects.filter(codename='is_regional_officer').first()
                if user.has_perm('website.is_regional_officer') != True:
                    user.user_permissions.add(permission)
            elif member.approle.name == 'National Officer':
                permission = Permission.objects.filter(codename='is_national_officer').first()
                if user.has_perm('website.is_national_officer') != True:
                    user.user_permissions.add(permission)
            logging.debug("before authenticate")
            #user = authenticate(request, username=member.email, password=member.email)
            logging.debug("before login..")
            if request.user.is_authenticated != True:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            logging.debug("after login")
    except Exception as err:
        print(f'Unexpected {err} from setupAppPermissions(), {type(err)}')
        raise

def getAuthCodeFromCache(emailaddress):
    user_key = emailaddress + "_" + today
    if cache.get(user_key):
        auth_code = cache.get(user_key)
        return auth_code
    else:
        return None

def generateAuthCode(request, emailaddress):
    try:
        member = None
        if emailaddress is not None:
            member = Member.objects.filter(email=emailaddress).first()
        context = None
        if member is not None:
            auth_code = getAuthCodeFromCache(emailaddress)
            if auth_code is None:
                auth_code = ''.join(random.sample(string.digits,6))
                #logging.debug('auth_code: ' + str(auth_code))
                user_key = emailaddress + "_" + today
                cache.set(user_key, auth_code)
            if config("local", False):
                logging.debug('auth_code--- ' + str(auth_code))
            logging.debug('call a make to mailuser()')
            mailuser(recipient=emailaddress,
                header='Your "Auth Code" from SSSIO Officers Portal',
                authcode=auth_code)
            logging.debug('sent email to the user')
            context = {
                "issued" : True,
                "email" : emailaddress,
                "message" : "Please enter the auth code sent to your email (make sure to check your spam folder)"
            }
        else:
            message = "Your email is not in our database. Please request for access via Contact Us link"
            context = {'message': message}
        return context
    except Exception as err:
        print(f'Unexpected {err} from generateAuthCode(), {type(err)}')
        raise

def authenticateUser(request, emailaddress):
    try:
        authcode = request.POST['authcode']
        if authcode is not None:
            user_key = emailaddress + "_" + today
            cache_authcode = getAuthCodeFromCache(emailaddress)
            if authcode == cache_authcode:
                user = User.objects.filter(username=emailaddress)
                if len(user) == 0:
                    user = User.objects.create_user(emailaddress, emailaddress, emailaddress)
                return True
            else:
                context = {
                    "issued" : True,
                    "email" : emailaddress,
                    "message" : "Auth Code didn't match. Please try typing the 'Auth Code' number and click authenticate button"
                }
                return context
    except Exception as err:
        print(f'Unexpected {err} from authenticateUser(), {type(err)}')
        raise

def mailuser(header, authcode, recipient):
    try:
        salutation = 'Dear User, <br><br>'
        salutation = salutation + "Please use below 'Auth Code' which is required for Officers portal login:<br><br>"
        footer = "<br><br>Thank You!<br><br>"
        meta = Metadata.objects.get(key='email-common-footer')
        footer = footer + meta.value
        sendemail(to=recipient,
            subject=header,
            body=salutation + authcode + footer)
    except Exception as err:
        print(f'Unexpected {err} from mailuser(), {type(err)}')
        raise
