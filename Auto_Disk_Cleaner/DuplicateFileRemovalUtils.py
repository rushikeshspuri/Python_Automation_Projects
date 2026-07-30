#============================================================================
# Module  : DuplicateFileRemovalUtils
# Author  : Rushikesh Sanjay Puri
# Purpose : Contains all user-defined functions used by Auto_Disk_Cleaner.py
#============================================================================

#----------------------------------------------------------------------------
# Importing required Libraries
#----------------------------------------------------------------------------

import hashlib
import os
import datetime
import smtplib
from email.message import EmailMessage

#----------------------------------------------------------------------------
# Function :    DeleteEmpty
# input    :    Name of Directory, open log file object
# Purpose  :    Cleans up empty files, writes details into the log file
#----------------------------------------------------------------------------
def DeleteEmpty(DirectoryPath,fobj):
    Border = '-'*50

    Ret = os.path.exists(DirectoryPath)
    if Ret == False:
        fobj.write(f"Error : There is no such directory with name {DirectoryPath}.\n")
        return

    Ret = os.path.isdir(DirectoryPath)
    if Ret == False:
        fobj.write(f"Error : {DirectoryPath} is not a directory.\n")
        return

    fobj.write(Border+"\n")
    fobj.write("Empty File Cleanup Section\n")
    fobj.write(Border+"\n\n")

    TotalFiles = 0
    EmptyFiles = 0

    for FolderName, SubFolder, FileName in os.walk(DirectoryPath):
        for fName in FileName:
            TotalFiles += 1
            try:
                fName = os.path.join(FolderName,fName)
                fobj.write(f"{fName} : {os.path.getsize(fName)} bytes\n")

                if os.path.getsize(fName) == 0:
                    EmptyFiles += 1
                    os.remove(fName)
                    fobj.write(f"Deleted empty files : {fName}\n")

            except OSError as e:
                fobj.write(f"Error processing {fName} : {e}\n")

    fobj.write(Border+"\n")
    fobj.write(f"Total Files Scanned : {TotalFiles}\n")
    fobj.write(f"Empty Files Found & Deleted : {EmptyFiles}\n")
    fobj.write(Border+"\n\n")

#----------------------------------------------------------------------------
# Function :    CalculateCheckSum
# input    :    Name of file
# Purpose  :    returns the MD5 checksum
#----------------------------------------------------------------------------
def CalculateCheckSum(FileName):
    try:
        fobj = open(FileName,'rb')
        hobj = hashlib.md5()

        Buffer = fobj.read(1024)
        while len(Buffer) > 0:
            hobj.update(Buffer)
            Buffer = fobj.read(1024)

        fobj.close()
        return hobj.hexdigest()

    except OSError as e:
        return None

#----------------------------------------------------------------------------
# Function :    FindDuplicate
# input    :    Name of Directory, open log file object
# Purpose  :    returns dict of {checksum : [file paths]}
#----------------------------------------------------------------------------
def FindDuplicate(DirectoryPath,fobj):
    Ret = os.path.exists(DirectoryPath)
    if Ret == False:
        fobj.write(f"Error : There is no such directory with name {DirectoryPath}.\n")
        return None
    
    Ret = os.path.isdir(DirectoryPath)
    if Ret == False:
        fobj.write(f"Error : {DirectoryPath} is not a directory.\n")
        return None

    Duplicate = {}
    TotalFiles = 0

    for FolderName, SubFolder, FileName in os.walk(DirectoryPath):
        for fName in FileName:
            fName = os.path.join(FolderName,fName)

            if not os.path.isfile(fName):
                continue
            if not os.access(fName, os.R_OK):
                fobj.write(f"Error : Cannot read file {fName} (permission denied)\n")
                continue

            TotalFiles += 1

            CheckSum = CalculateCheckSum(fName)

            if CheckSum is None:
                fobj.write(f"Error : Could not calculate checksum for {fName}\n")
                continue

            if CheckSum in Duplicate:
                Duplicate[CheckSum].append(fName)
            else:
                Duplicate[CheckSum] = [fName]

    return Duplicate, TotalFiles

#----------------------------------------------------------------------------
# Function :    DeleteDuplicate
# input    :    Name of Directory, open log file object
# Purpose  :    Deletes duplicate files, writes details into log file
#               returns (TotalFiles, TotalDuplicatesFound, TotalDeleted)
#----------------------------------------------------------------------------
def DeleteDuplicate(DirectoryPath,fobj):
    Border = "-"*50

    Result = FindDuplicate(DirectoryPath, fobj)
    if Result is None:
        return 0,0,0

    MyDict ,TotalFiles = Result

    fobj.write(Border+"\n")
    fobj.write("Duplicate File Remove Section\n")
    fobj.write(Border+"\n")

    DuplicateGroups = list(filter(lambda x : len(x) > 1, MyDict.values()))

    Count = 0
    TotalDeleted = 0
    TotalFound = sum(len(group) - 1 for group in DuplicateGroups)

    for value in DuplicateGroups:
        fobj.write(f"Kept   : {value[0]}\n")

        for subvalues in value:
            Count += 1
            if Count > 1:
                try:
                    os.remove(subvalues)
                    TotalDeleted += 1
                    fobj.write(f"Deleted successfully : {subvalues}\n")
                except OSError as e:
                    fobj.write(f"Error deleting {subvalues} : {e}\n")
        Count = 0

    fobj.write(Border+"\n")
    fobj.write(f"Total Files Scanned : {TotalFiles}\n")
    fobj.write(f"Total Duplicate Files Found : {TotalFound}\n")
    fobj.write(f"Total Duplicate Files Deleted : {TotalDeleted}\n")
    fobj.write(Border+"\n\n")

    return TotalFiles, TotalFound, TotalDeleted

#----------------------------------------------------------------------------
# Function :    SendMail
# input    :    sender, app_password, receiver, subject, body, attachment path
# Purpose  :    Sends email using Gmail SMTP server, attaches log file
#----------------------------------------------------------------------------
def SendMail(sender,app_password,receiver,subject,body,AttachmentPath = None):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"]   = receiver
    msg["Subject"] = subject
    msg.set_content(body)

    if AttachmentPath and os.path.exists(AttachmentPath):
        with open(AttachmentPath,'rb') as f:
            FileData = f.read()
            FileName = os.path.basename(AttachmentPath)
            msg.add_attachment(FileData, maintype="application", subtype="octet-stream", filename=FileName)

    try:
        smtp = smtplib.SMTP_SSL("smtp.gmail.com",465)
        smtp.login(sender,app_password)
        smtp.send_message(msg)
        smtp.quit()
        return True, "Mail sent successfullly"

    except Exception as e:
        return False, f"Failed to send mail : {e}" 