from .email import sendemail
import string
import random
from django.core.cache import cache
import logging
from datetime import datetime
from .models import Metadata

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

def authenticateUser(request):
    today = datetime.now().strftime("%d%m%y")
    login_access = request.session.get("login_access", None)
    if login_access is not None:
        logging.debug('login_access--- ' + str(login_access))
        cache_auth_code = cache.get(login_access)
        logging.debug('cache_auth_code--- ' + str(cache_auth_code))
        if cache_auth_code is not None:
            logging.debug('cache_auth_code--- ' + cache_auth_code)
            cache_date = cache.get(cache_auth_code)
            if cache_date is not None:
                logging.debug('cache_date--- ' + cache_date)
                if cache_date == today:
                    return True
    return False

def mailAuthCodetoUser(request, emailaddress):
    auth_code = None
    today = datetime.now().strftime("%d%m%y")
    logging.debug('today: ' + str(today))
    user_key = emailaddress + "_" + today
    logging.debug('user_key: ' + str(user_key))
    if cache.get(user_key):
        auth_code = cache.get(user_key)
        logging.debug('auth_code from cache: ' + str(auth_code))
    else:
        auth_code = ''.join(random.sample(string.digits,6))
        logging.debug('auth_code: ' + str(auth_code))
        cache.set(user_key, auth_code, 14400)
        cache.set(auth_code, today, 14400)
        logging.debug('auth code set in cache: ' + cache.get(user_key))
    if auth_code is not None:
        mailuser(recipient=emailaddress,
            header='Your "Auth Code" from SSSIO Officers Portal',
            authcode=auth_code)

def mailuser(header, authcode, recipient):
    salutation = 'Dear User, <br><br>'
    salutation = salutation + "Please use below 'Auth Code' which is required for Officers portal login:<br><br>"
    footer = "<br><br>Thank You!<br><br>"
    meta = Metadata.objects.get(key='email-common-footer')
    footer = footer + meta.value
    sendemail(to=recipient,
        subject=header,
        body=salutation + authcode + footer)
