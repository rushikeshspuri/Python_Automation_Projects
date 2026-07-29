# 📧 Gmail Mail Sender

A Python automation project that sends emails using Gmail's SMTP server. This project demonstrates how to automate email delivery with Python using the `smtplib` module, the `email` package, and the `schedule` library.

---

## 📌 Overview

The **Gmail Mail Sender** is a simple SMTP-based automation tool developed in Python. It establishes a secure connection with Gmail's SMTP server, authenticates using a Gmail App Password, composes an email, and sends it to a recipient.

The script also supports **scheduled email delivery**, allowing emails to be sent automatically at fixed intervals without manual intervention.

This project is useful for learning:

* SMTP (Simple Mail Transfer Protocol)
* Email automation using Python
* Gmail App Password authentication
* Task scheduling
* Command-line arguments
* Python functions and modular programming

---

## ✨ Features

* Send emails securely using Gmail SMTP.
* Uses SSL encryption for secure communication.
* Supports Gmail App Password authentication.
* Accepts the receiver's email address through command-line arguments.
* Sends emails automatically at scheduled intervals.
* Customizable subject and message body.
* Simple and beginner-friendly implementation.

---

## 🛠 Technologies Used

* Python 3
* smtplib
* email.message
* schedule
* sys
* time

---

## 📁 Project Structure

```text
Gmail_Mail_Sender/
│
├── MailSender.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Requirements

Install the required package before running the project.

```bash
pip install schedule
```

---

## 🔐 Gmail App Password

This project uses **Gmail App Password Authentication** instead of your Gmail account password.

Before running the program:

1. Enable **2-Step Verification** on your Google Account.
2. Generate an **App Password**.
3. Replace the placeholder inside the script:

```python
app_password = "YOUR_APP_PASSWORD"
```

> **Important:** Never upload your real App Password to GitHub.

---

## ▶️ How to Run

Run the script by providing the receiver's email address as a command-line argument.

```bash
python MailSender.py receiver@example.com
```

Example:

```bash
python MailSender.py johndoe@gmail.com
```

---

## ⚙️ Working

The program performs the following steps:

1. Reads the receiver's email from the command line.
2. Creates an email using the `EmailMessage` class.
3. Connects securely to Gmail's SMTP server.
4. Authenticates using the sender's email and App Password.
5. Sends the email to the specified receiver.
6. Executes automatically at the configured schedule interval.
7. Closes the SMTP connection.

---

## 📨 Email Details

The generated email contains:

* Sender Email
* Receiver Email
* Subject
* Custom Message Body

These values can easily be modified inside the script.

---

## ⏰ Scheduling

The project uses the **schedule** library to automate email delivery.

Example:

```python
schedule.every(1).minutes.do(send_mail,
                              sender_email,
                              app_password,
                              receiver_email,
                              subject,
                              body)
```

The interval can be changed according to your requirements.

Examples:

```python
schedule.every(10).seconds.do(...)

schedule.every(5).minutes.do(...)

schedule.every().hour.do(...)

schedule.every().day.at("09:00").do(...)
```

---

## 📚 Concepts Covered

This project demonstrates the following Python concepts:

* Functions
* Modules
* SMTP Protocol
* SSL Connection
* Email Automation
* Command-Line Arguments
* Scheduling Tasks
* String Formatting (f-strings)
* Infinite Loops
* Secure Authentication

---

## 🚀 Future Improvements

Some enhancements that can be added to this project include:

* HTML email support
* Email attachments
* Multiple recipients
* CC and BCC support
* Exception handling
* Logging system
* Reading email details from a configuration file
* Environment variable support for credentials
* Command-line options for subject and message
* Email templates

---

## ⚠️ Note

For security reasons, never store your real Gmail App Password inside the source code or commit it to a public repository. Use environment variables or a secure configuration file whenever possible.

---

## 👨‍💻 Author

**Rushikesh Sanjay Puri**

Python Automation Project
