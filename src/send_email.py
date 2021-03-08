import smtplib
import ssl
import config

# Below gmail works.
# Must set "Allow insecure apps" to true
#EMAIL_FROM = 'throwawayz5432@gmail.com'
#EMAIL_TO = 'throwawayz5432@gmail.com'
#SMTP_HOST = 'smtp.gmail.com'
#SMTP_PORT = 587
#password = "" #01

# Below works.
# Must generate an app password
#EMAIL_FROM = 'mzborowski@yahoo.com'
#EMAIL_TO = 'mzborowski@yahoo.com'
#SMTP_HOST = 'smtp.mail.yahoo.com'
#SMTP_PORT = 587
#yahoo_app_password = 'wogbwdgopawfwjcz' # for homelab
#password = yahoo_app_password

# AWS SES

EMAIL_FROM = 'dcabot@mzborowski.com'
EMAIL_TO = 'mzborowski@yahoo.com'
SMTP_HOST = 'email-smtp.us-east-1.amazonaws.com'
SMTP_PORT = 587
# SES smtp credentials. IAM user is zeebrow
ses_username = 'AKIASXTXBRBGFMOMG3UF'
ses_password = 'BHSSPWvTvriP7222ubhn2tmYTWVHBrknWJxJEelWyn/U'

def email(msg,
        email_to='mzborowski@yahoo.com',
        email_from='dcabot@mzborowski.com',
        smtp_host='email-smtp.us-east-1.amazonaws.com',
        smtp_port=587,
        ses_username='AKIASXTXBRBGFMOMG3UF',
        ses_password='BHSSPWvTvriP7222ubhn2tmYTWVHBrknWJxJEelWyn/U'):
    
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(ses_username, ses_password)
        print("Logged in. Sending message...")
        server.sendmail(email_from, email_to, msg)
        print("Message sent.")

    except Exception as e:
        print(e)
    finally:
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

