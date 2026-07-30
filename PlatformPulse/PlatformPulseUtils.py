#============================================================================
# Module  : PlatformPulseUtils
# Project : PlatformPulse
# Author  : Rushikesh Puri
# Purpose : Contains all user-defined functions used by PlatformPulse scripts
#============================================================================

import psutil
import os
import datetime
import smtplib
from email.message import EmailMessage

# ------------------------------------------------------------
# Function : get_running_processes
# Purpose  : Collect information about running processes
# ------------------------------------------------------------
def get_running_processes():

    processes = []

    for process in psutil.process_iter(
        ['pid', 'name', 'username', 'memory_percent']
    ):

        try:

            pid = process.info['pid']
            name = process.info['name']
            username = process.info['username']

            cpu_usage = process.cpu_percent(interval=0.1)
            memory_usage = process.info['memory_percent']

            processes.append({
                "pid": pid,
                "name": name,
                "username": username,
                "cpu": cpu_usage,
                "memory": memory_usage
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return processes
# ------------------------------------------------------------
# Function : find_process_by_name
# Purpose  : Search for a running process by its name
# ------------------------------------------------------------
def find_process_by_name(process_name):
    found = False

    print("-"*120)
    print(f"              PROCESS SEARCH : {process_name}")
    print("-"*120)

    print(f"{'PID':<10}{'Process Name':<30}{'Username':<30}{'CPU %':<15}{'Memory %':<15}")

    for process in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):

        try:
            current_name = process.info['name']

            if current_name and current_name.lower() == process_name.lower():

                pid = process.info['pid']
                username = process.info['username']
                cpu_usage = process.info['cpu_percent']
                memory_usage = process.info['memory_percent']

                print(f"{pid:<10}{current_name:<30}{username:<30}{cpu_usage:<15}{memory_usage:<15.2f}")

                found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if not found:
        print(f"Process '{process_name}' is not running.")

    print("-" * 120)


#----------------------------------------------------------------------------
# Function : get_cpu_statistics
# Purpose  : Collect system-wide CPU information
#----------------------------------------------------------------------------
def get_cpu_statistics():

    cpu_usage = psutil.cpu_percent(interval= 1)
    cpu_count = psutil.cpu_count()
    cpu_frequency = psutil.cpu_freq()

    return{
        "usage" : cpu_usage,
        "count" : cpu_count,
        "frequency" : cpu_frequency
    }


#----------------------------------------------------------------------------
# Function : get_memory_statistics
# Purpose  : Collect system-wide RAM information
#----------------------------------------------------------------------------
def get_memory_statistics():
    memory = psutil.virtual_memory()

    return{
        "total" : memory.total,
        "available" : memory.available,
        "used" : memory.used,
        "percentage" : memory.percent
    }

#----------------------------------------------------------------------------
# Function : get_network_statistics
# Purpose  : Collect system-wide network statistics
#----------------------------------------------------------------------------
def get_network_statistics():

    network = psutil.net_io_counters()

    return {
        "bytes_sent": network.bytes_sent,
        "bytes_received": network.bytes_recv,
        "packets_sent": network.packets_sent,
        "packets_received": network.packets_recv
    }

#----------------------------------------------------------------------------
# Function : generate_system_report
# Purpose  : Generate a complete system monitoring report
#----------------------------------------------------------------------------
def generate_system_report():

    cpu_info = get_cpu_statistics()
    memory_info = get_memory_statistics()
    network_info = get_network_statistics()
    processes = get_running_processes()

    total_memory_gb = memory_info['total'] / (1024 ** 3)
    used_memory_gb = memory_info['used'] / (1024 ** 3)
    available_memory_gb = memory_info['available'] / (1024 ** 3)

    sent_mb = network_info['bytes_sent'] / (1024 ** 2)
    received_mb = network_info['bytes_received'] / (1024 ** 2)

    report = ""

    report += "=" * 70 + "\n"
    report += "                    PLATFORMPULSE REPORT\n"
    report += "=" * 70 + "\n\n"

    # CPU information
    report += "-" * 70 + "\n"
    report += "                    CPU STATISTICS\n"
    report += "-" * 70 + "\n"

    report += f"CPU Usage       : {cpu_info['usage']:.2f} %\n"
    report += f"CPU Count       : {cpu_info['count']}\n"

    if cpu_info['frequency']:
        report += (
            f"CPU Frequency   : "
            f"{cpu_info['frequency'].current:.2f} MHz\n"
        )

    # Memory information
    report += "\n"
    report += "-" * 70 + "\n"
    report += "                    MEMORY STATISTICS\n"
    report += "-" * 70 + "\n"

    report += f"Total RAM       : {total_memory_gb:.2f} GB\n"
    report += f"Used RAM        : {used_memory_gb:.2f} GB\n"
    report += f"Available RAM   : {available_memory_gb:.2f} GB\n"
    report += f"Memory Usage    : {memory_info['percentage']:.2f} %\n"

    # Network information
    report += "\n"
    report += "-" * 70 + "\n"
    report += "                    NETWORK STATISTICS\n"
    report += "-" * 70 + "\n"

    report += f"Data Sent       : {sent_mb:.2f} MB\n"
    report += f"Data Received   : {received_mb:.2f} MB\n"
    report += f"Packets Sent    : {network_info['packets_sent']}\n"
    report += f"Packets Received: {network_info['packets_received']}\n"

    report += "\n"
    report += "=" * 70 + "\n"

    # Process information

    report += "\n"
    report += "-" * 100 + "\n"
    report += "                    RUNNING PROCESSES\n"
    report += "-" * 100 + "\n"

    report += (
        f"{'PID':<10}"
        f"{'Process Name':<30}"
        f"{'Username':<30}"
        f"{'CPU %':<15}"
        f"{'Memory %':<15}\n"
    )

    report += "-" * 100 + "\n"

    for process in processes:

        report += (
            f"{process['pid']:<10}"
            f"{str(process['name']):<30}"
            f"{str(process['username']):<30}"
            f"{process['cpu']:<15.2f}"
            f"{process['memory']:<15.2f}\n"
        )

    return report

# ------------------------------------------------------------
# Function : save_report
# Purpose  : Save generated report into a log file
# ------------------------------------------------------------
def save_report(report, directory):
    try:
        if not os.path.isdir(directory):
            os.makedirs(directory)

        time_stamp = datetime.datetime.now()

        file_name = time_stamp.strftime("PlatformPulse_%Y%m%d_%H%M%S.log")

        filepath = os.path.join(directory,file_name)

        with open (filepath,'w') as file:
            file.write(report)

        return filepath

    except OSError as error:
        print(f"Unable to save report : {error}")
        return None

#----------------------------------------------------------------------------
# Function : def send_report_email(...)
# Purpose  : Send PlatformPulse report through Gmail SMTP
#----------------------------------------------------------------------------
def send_report_email(sender,app_password,receiver,subject,body,attachment_path=None):

    msg = EmailMessage()

    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    msg.set_content(body)

   
    # Attach report file if provided
    if attachment_path and os.path.exists(attachment_path):

        with open(attachment_path, 'rb') as file:

            FileData = file.read()
            FileName = os.path.basename(attachment_path)

            msg.add_attachment(
                FileData,
                maintype="application",
                subtype="octet-stream",
                filename=FileName
            )

    # Send mail using Gmail SMTP
    try:

        smtp = smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        )

        smtp.login(
            sender,
            app_password
        )

        smtp.send_message(msg)

        smtp.quit()

        return True, "Mail sent successfully"

    except Exception as error:

        return False, f"Failed to send mail : {error}"