import smtplib
import ssl
from dca_config import config
from dca_config import SecretsManager as sm
import logging

logger = logging.getLogger(__name__)
send_email_notifications = True
# AWS SES
secrets = sm.SecretsManager()
EMAIL_FROM = 'dcabot@mzborowski.com'
EMAIL_TO = 'mzborowski@yahoo.com'
SMTP_HOST = 'email-smtp.us-east-1.amazonaws.com'
SMTP_PORT = 587
# SES smtp credentials. IAM user is zeebrow
ses_username = secrets.smtp_username
ses_password = secrets.smtp_password
def email(msg,
        email_to=EMAIL_TO,
        email_from=EMAIL_FROM,
        smtp_host=SMTP_HOST,
        smtp_port=SMTP_PORT,
        ses_username=ses_username,
        ses_password=ses_password):

    if (not send_email_notifications):
        logger.info(f"Stopped email from being sent (_is_test = {_is_test}, send_email_notifications = {send_email_notifications}")
        return

    try:
        logger.debug("Attempting to conect to server...")
        context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(ses_username, ses_password)
        logger.debug("Logged in. Sending message...")
        server.sendmail(email_from, email_to, msg)
        logger.debug("Message sent.")

    except Exception as e:
        logger.error("There was an error sending email notification.")
        logger.error(e)
    finally:
        logging.debug("Closing connection to server.")
        server.quit()


if __name__ == '__main__':
    context = ssl.create_default_context()
    msg = """
Subject: yello

This is a test message from homelab python script.
"""

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(ses_username, ses_password)
        print("Logged in. Sending message...")
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg)
        print("Message sent.")

    except Exception as e:
        print(e)
    finally:
        server.quit()

