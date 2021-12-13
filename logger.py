# Logger Module.

# Author: EJacobsen
# Date: 10/1/2021

import smtplib
import logging
import os
import json
from config import EMAIL, GMAIL_API_KEY


#my_dir = os.path.dirname(__file__)
my_dir = os.path.dirname(os.path.abspath(__file__))
logPath = os.path.join(my_dir, 'log.log')


# Format email body.
def FormatEmail(job):
    status = job.status
    contract = job.txnTo
    sender = job.txnFrom
    method = job.txnMethodName

    msg = str('STATUS: ' + status + '\n' + 'CONTRACT: ' + contract + '\n' + 'SENDER: ' + sender + '\n' + 'METHOD: ' + method)
    return msg


# Send email.
def SendEmail(subject, body):
    sender = 'eljacobsen12@gmail.com'
    password = GMAIL_API_KEY

    try:
        msg = 'Subject: {}\n\n{}'.format(subject, body)
        smtp =  smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(sender, password)
        smtp.sendmail(sender, EMAIL, msg=msg)
        smtp.quit()
        WriteToLog('info', "Email sent successfully.")
    except smtplib.SMTPException:
        WriteToLog('error', "Email failed to send. SMTP exception.")


# Write to log file.
def WriteToLog(type, msg):
    global logPath
    logging.basicConfig(filename=logPath, format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO)
    if type == 'debug':
        logging.debug(msg)
    elif type == 'info':
        logging.info(msg)
    elif type == 'warning':
        logging.warning(msg)
    elif type == 'error':
        logging.error(msg)
        SendEmail('silopete117@protonmail.com', 'Error Occurred', "Error Occurred: {}".format(msg))
    else:
        logging.log(msg)


# Update JSON file.
def LoadJsonFile(filename):
    global my_dir
    path = os.path.join(my_dir, filename)
    f = open(path, 'r')
    WriteToLog('info', "Successfully loaded json")
    return json.load(f)