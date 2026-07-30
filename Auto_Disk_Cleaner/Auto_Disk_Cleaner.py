#============================================================================
# Program : Auto Disk Cleaner.
# Author  : Rushikesh Sanjay Puri
# Purpose : Scans a directory, removes duplicate & empty files on a schedule,
#           logs everything, and emails the log file.
# Date    : 30/07/2026
#============================================================================

import os
import sys
import schedule
import time
import datetime

from DuplicateFileRemovalUtils import DeleteEmpty, DeleteDuplicate, SendMail

#----------------------------------------------------------------------------
# Function :    RunCleaner
# Purpose  :    Wrapper that runs both cleaning tasks, writes log, sends mail
#----------------------------------------------------------------------------
def RunCleaner(DirectoryPath, IntervalMinutes, UserEmail, SenderEmail, AppPassword):
    Border = "-"*50

    now = datetime.datetime.now()
    time_stamp = now.strftime("%d_%m_%Y_%H_%M_%S")
    LogFileName = os.path.join("DiskCleanerLog", f"DuplicateRemoveLog_{time_stamp}.log")

    StartTime = datetime.datetime.now()

    try:
        fobj = open(LogFileName,'w')
    except OSError as e:
        return   

    fobj.write(Border+"\n")
    fobj.write("Auto Disk Cleaner - Log\n")
    fobj.write(Border+"\n\n")
    fobj.write(f"Starting time of scanning : {StartTime.strftime('%d %B %Y, %I:%M:%S %p')}\n")
    fobj.write(f"Directory to scan : {DirectoryPath}\n\n")

    # Empty files cleanup 
    DeleteEmpty(DirectoryPath, fobj)

    # Duplicate file removal
    TotalFiles, TotalFound, TotalDeleted = DeleteDuplicate(DirectoryPath, fobj)

    CompletionTime = datetime.datetime.now()
    fobj.write(f"Completion time of scanning : {CompletionTime.strftime('%d %B %Y, %I:%M:%S %p')}\n")
    fobj.close()

    # Send mail
    EmailBody = f"""Jay Ganesh,

The Auto Disk Cleaner operation has been completed successfully.

Operation Statistics:

Starting time of scanning: {StartTime.strftime('%d %B %Y, %I:%M:%S %p')}
Completion time of scanning: {CompletionTime.strftime('%d %B %Y, %I:%M:%S %p')}
Directory scanned: {DirectoryPath}
Total number of files scanned: {TotalFiles}
Total number of duplicate files found: {TotalFound}
Total number of duplicate files deleted: {TotalDeleted}

Please find the detailed log file attached to this email.

Regards,
Rushikesh Puri
"""

    Success, MailStatus = SendMail(SenderEmail, AppPassword, UserEmail,
                                    "Duplicate File Removal Automation - Log Report",
                                    EmailBody, AttachmentPath=LogFileName)

    with open(LogFileName, 'a') as fobj:
        fobj.write(f"Email delivery status : {MailStatus}\n")
        fobj.write(Border+"\n")
#----------------------------------------------------------------------------
# Function :    IsValidEmail
# Purpose  :    Very basic email format validation
#----------------------------------------------------------------------------
def IsValidEmail(email):
    return "@" in email and "." in email.split("@")[-1]

#----------------------------------------------------------------------------
# Function :        main
# Description :     Driver Code
#----------------------------------------------------------------------------
def main():
    Border = "-"*50

    SenderEmail = "rushikeshspuri@gmail.com" # TODO: put your Gmail here
    AppPassword = "--------------"   # TODO: put your Gmail App Password here

    if len(sys.argv) == 2:
        if(sys.argv[1] in ("--h", "--H", "--help")):
            print("Auto Disk Cleaner Automation")
            print()
            print("This script scans a directory, identifies duplicate files using")
            print("checksums, deletes duplicate files, creates a log file, and sends")
            print("the log file through email.")
            print()
            print("Usage:")
            print("    python Auto_Disk_Cleaner.py <DirectoryPath> <IntervalInMinutes> <ReceiverEmail>")
            print()
            print("Example:")
            print("    python Auto_Disk_Cleaner.py  E:/Data/Demo 50 --------@gmail.com")
            return

        elif(sys.argv[1] in ("--u", "--U", "--usage")):
            print("Usage:")
            print("    python Auto_Disk_Cleaner.py <AbsoluteDirectoryPath> <TimeIntervalInMinutes> <ReceiverEmailAddress>")
            return

        else:
            print("Invalid argument. Please use --h or --u for more information.")
            return

    elif len(sys.argv) == 4:
        TargetDirectory = sys.argv[1]
        MinutesStr = sys.argv[2]
        UserEmail = sys.argv[3]

        # Directory validation
        if not os.path.isabs(TargetDirectory):
            print("Error : Directory path must be absolute.")
            return
        if not os.path.exists(TargetDirectory):
            print(f"Error : Directory '{TargetDirectory}' does not exist.")
            return
        if not os.path.isdir(TargetDirectory):
            print(f"Error : '{TargetDirectory}' is not a directory.")
            return
        if not os.access(TargetDirectory, os.R_OK):
            print(f"Error : No read permission for '{TargetDirectory}'.")
            return

         # Time interval validation
        if not MinutesStr.isdigit() or int(MinutesStr) <= 0:
            print(f"Error : Invalid interval '{MinutesStr}'. Must be a positive integer (minutes).")
            return
        IntervalMinutes = int(MinutesStr)

        
         # Email validation
        if not IsValidEmail(UserEmail):
            print(f"Error : Invalid email address '{UserEmail}'.")
            return

        # Creates log Directory
        os.makedirs("DiskCleanerLog", exist_ok=True)
        print(f"{Border}\nAuto Disk Cleaner SCRIPT\n{Border}")
        print(f"Scheduler started — will run every {IntervalMinutes} minute(s). Press Ctrl+C to stop.")


          # Run once immediately
        RunCleaner(TargetDirectory, IntervalMinutes, UserEmail, SenderEmail, AppPassword)

        # Schedule repeating runs
        schedule.every(IntervalMinutes).minutes.do(
            RunCleaner, TargetDirectory, IntervalMinutes, UserEmail, SenderEmail, AppPassword
        )

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nScheduler stopped by user.")

    else:
        print("Invalid number of arguments.")
        print("Please use --h or --u for more information.")


    print(Border)
    print(" Thank You for using Auto Disk Cleaner ")
    print(Border)

#-------------------------------------------------------
# Program Entry Point
#-------------------------------------------------------
if __name__ == "__main__":
    main()
