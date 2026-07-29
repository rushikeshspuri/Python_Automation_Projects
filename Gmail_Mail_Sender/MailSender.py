#=======================================================
# Program : Simple Gmail Mail Sender
# Author  : Rushikesh Sanjay Puri
# Purpose : Send Mail using Python SMTP
#=======================================================

import smtplib
from email.message import EmailMessage
import schedule
import time
import sys

#-------------------------------------------------------
# Function :        send_mail
# Description :     Sends Email using Gmail SMTP server
#-------------------------------------------------------
def send_mail(sender, app_password, receiver, subject, body):

    msg = EmailMessage()

    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    msg.set_content(body)

    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    smtp.login(sender, app_password)

    smtp.send_message(msg)

    print("Mail Sent Successfully")

    smtp.quit()


#-------------------------------------------------------
# Function :        main
# Description :     Driver Code
#-------------------------------------------------------
def main():

    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage : python3 MailSender.py <receiver_email>")
        return

    sender_email = "rushikeshspuri@gmail.com"

    # Add your Gmail App Password here
    app_password = "--------------"

    # Receiver email from command line
    receiver_email = sys.argv[1]

    subject = "Test mail from Python Script"

    body = """Jay Ganesh...
This mail is sent using Python SMTP.
"""

    # Schedule mail every 1 minute
    schedule.every(1).minutes.do(
        send_mail,
        sender_email,
        app_password,
        receiver_email,
        subject,
        body
    )

    print("Mail scheduler started...")
    print("Mail will be sent every 1 minute.")

    while True:
        schedule.run_pending()
        time.sleep(1)


#-------------------------------------------------------
# Program Entry Point
#-------------------------------------------------------
if __name__ == "__main__":
    main()
```
