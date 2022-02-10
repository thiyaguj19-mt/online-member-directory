from .email import sendemail
import string
import random
from django.core.cache import cache
import logging
from datetime import datetime
from .models import Metadata

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

def mailAuthCodetoUser(request, emailaddress):
    auth_code = None
    host_name = request.META.get('HOSTNAME')
    logging.debug('host_name: ' + str(host_name))
    today = datetime.now().strftime("%d%m%y")
    logging.debug('today: ' + str(today))
    user_key = emailaddress + "_" + host_name + "_" + today
    logging.debug('user_key: ' + str(user_key))
    for meta in request.META:
        logging.debug('meta: ' + str(meta))
        logging.debug('value: ' + request.META.get('meta'))
    if cache.get(user_key):
        auth_code = cache.get(user_key)
        logging.debug('auth_code from cache: ' + str(auth_code))
    else:
        auth_code = ''.join(random.sample(string.digits,6))
        logging.debug('auth_code: ' + str(auth_code))
        cache.set(user_key, auth_code, 14400)
        logging.debug('auth code in cache: ' + str(today))
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
