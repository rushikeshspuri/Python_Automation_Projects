#============================================================================
# Program : PlatformPulse
# Project : PlatformPulse
# Author  : Rushikesh Puri
# Purpose : Automated System Monitoring Platform
#============================================================================

import PlatformPulseUtils
import schedule
import time
import sys
import os


#----------------------------------------------------------------------------
# Function : create_system_report
# Purpose  : Generate, save and email PlatformPulse report
#----------------------------------------------------------------------------

def create_system_report(sender, receiver, app_password):

    log_directory = "PlatformPulseLogs"

    # Generate complete system report
    report = PlatformPulseUtils.generate_system_report()

    # Save report
    filepath = PlatformPulseUtils.save_report(
        report,
        log_directory
    )

    if filepath:

        print(f"Report saved : {filepath}")

    else:

        print("Failed to save report.")
        return

    # Send report through email
    success, message = PlatformPulseUtils.send_report_email(
        sender,
        app_password,
        receiver,
        "PlatformPulse System Report",
        "Attached is the latest PlatformPulse system monitoring report.",
        filepath
    )

    print(message)


#----------------------------------------------------------------------------
# Function : main
# Purpose  : Start PlatformPulse monitoring scheduler
#----------------------------------------------------------------------------

def main():

    #------------------------------------------------------------
    # Check command-line arguments
    #------------------------------------------------------------

    if len(sys.argv) not in (4, 5):

        print(
            "Usage : python3 PlatformPulse.py "
            "<interval> <sender> <receiver> [process_name]"
        )

        print(
            "Example : python3 PlatformPulse.py "
            "10 sender@gmail.com receiver@gmail.com"
        )

        print(
            "Example : python3 PlatformPulse.py "
            "10 sender@gmail.com receiver@gmail.com chrome"
        )

        return


    #------------------------------------------------------------
    # Get monitoring interval
    #------------------------------------------------------------

    try:

        time_interval = int(sys.argv[1])

    except ValueError:

        print("Error : Time interval must be an integer.")
        return


    if time_interval <= 0:

        print("Error : Time interval must be greater than 0.")
        return


    #------------------------------------------------------------
    # Get email information
    #------------------------------------------------------------

    sender = sys.argv[2]
    receiver = sys.argv[3]


    #------------------------------------------------------------
    # Optional process name
    #------------------------------------------------------------

    process_name = None

    if len(sys.argv) == 5:

        process_name = sys.argv[4]


    #------------------------------------------------------------
    # Gmail App Password
    #------------------------------------------------------------

    # TODO : Replace this with your Gmail App Password
    app_password = "YOUR_APP_PASSWORD"

    if not app_password:

        print("Error : app_password is not specified.")
        return


    #------------------------------------------------------------
    # Create log directory
    #------------------------------------------------------------

    log_directory = "PlatformPulseLogs"

    if not os.path.exists(log_directory):

        os.makedirs(log_directory)


    #------------------------------------------------------------
    # Display PlatformPulse information
    #------------------------------------------------------------

    print("=" * 70)
    print("                    PlatformPulse")
    print("          Automated System Monitoring Platform")
    print("=" * 70)

    print(f"\nReport interval : {time_interval} minute(s)")
    print(f"Sender          : {sender}")
    print(f"Receiver        : {receiver}")


    if process_name:

        print(f"Process search  : {process_name}")

    else:

        print("Process search  : Not specified")


    #------------------------------------------------------------
    # Search for process if process name was provided
    #------------------------------------------------------------

    if process_name:

        print("\nSearching for requested process...")

        PlatformPulseUtils.find_process_by_name(
            process_name
        )


    #------------------------------------------------------------
    # Generate first report immediately
    #------------------------------------------------------------

    print("\nGenerating initial report...")

    create_system_report(
        sender,
        receiver,
        app_password
    )


    #------------------------------------------------------------
    # Schedule future reports
    #------------------------------------------------------------

    schedule.every(time_interval).minutes.do(
        create_system_report,
        sender,
        receiver,
        app_password
    )


    print("\nMonitoring started...")
    print("Press Ctrl+C to stop.")


    #------------------------------------------------------------
    # Keep scheduler running
    #------------------------------------------------------------

    while True:

        schedule.run_pending()

        time.sleep(1)


#----------------------------------------------------------------------------
# Program Entry Point
#----------------------------------------------------------------------------

if __name__ == "__main__":

    main()