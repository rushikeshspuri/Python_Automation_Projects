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
def send_mail(sender,app_password,reciever,subject,body):
    msg = EmailMessage()

    msg["From"] = sender
    msg["To"] = reciever
    msg["Subject"] = subject

    msg.set_content(body)

    smtp = smtplib.SMTP_SSL("smtp.gmail.com",465)

    smtp.login(sender,app_password)

    smtp.send_message(msg)

    print("Mail Sent Successfull")

    smtp.quit()

#-------------------------------------------------------
# Function :        main
# Description :     Driver Code
#-------------------------------------------------------
def main():
    sender_email   = "rushikeshspuri@gmail.com"

    # Add your mail app Password here
    app_password   = "--------------"

    # Add reciever mail id using Command line arguments
    reciever_email = sys.argv[1]

    subject = "Test mail from Python Script"

    body = f"""Jay Ganesh...
"""
    if len(sys.argv) != 2:
        print("Usage : python3 MailSender.py <receiver_email>")
        return

    schedule.every(1).minutes.do(send_mail,sender_email,app_password,reciever_email,subject,body)

    while True:
        schedule.run_pending()
        time.sleep(1)

#-------------------------------------------------------
# Program Entry Point
#-------------------------------------------------------
if __name__ == "__main__":
    main()
