from decouple import config
import logging
import smtplib
from email.message import EmailMessage
from .models import Metadata

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

def sendemail(to, subject, body):

    EMAIL_PORT = config('EMAIL_PORT')
    EMAIL_HOST_NAME = config('EMAIL_HOST_NAME')
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

    if len(EMAIL_PORT) > 0 and len(EMAIL_HOST_NAME) > 0 \
        and len(EMAIL_HOST_USER) > 0 and len(EMAIL_HOST_PASSWORD) > 0:
        try:
            is_local = config("local", False)
            #if you are working in local environment then set is_local = False to test email feature
            #is_local = False
            if is_local:
                logging.info('email feature is turned off in local environment')
            else:
                smtp_server = smtplib.SMTP_SSL(EMAIL_HOST_NAME, EMAIL_PORT)
                smtp_server.ehlo()
                smtp_server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                msg = EmailMessage()
                msg.set_content(body, subtype='html')
                msg['Subject'] = subject
                #msg['From'] = self.FROM_ADDRESS
                meta = Metadata.objects.get(key='smtp-from-email')
                msg['From'] = meta.value
                #print("from_address" , msg['From'])
                msg['To'] = to
                smtp_server.send_message(msg)
                smtp_server.close()
        except Exception as ex:
            print ("Something went wrong.",ex)
    else:
        logger.critical('email env variables are not configured. Unable to send email at this time.')
