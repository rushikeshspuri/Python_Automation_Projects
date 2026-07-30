# 🚀 PlatformPulse

> **An Automated System Monitoring Platform built with Python**

PlatformPulse is a Python-based system monitoring application that periodically collects system information, generates detailed monitoring reports, stores them as timestamped log files, and can automatically send those reports via email. The project separates monitoring logic into a reusable utility module while the main program handles scheduling and report generation.

---

## 📌 Features

* 🖥️ Monitor CPU usage and frequency
* 💾 Monitor memory (RAM) usage
* 🌐 Monitor network statistics
* ⚙️ Display all running processes
* 📄 Generate formatted system reports
* 📝 Save reports as timestamped log files
* 📧 Send reports automatically via Gmail SMTP
* ⏰ Schedule monitoring at user-defined intervals

---

## 📂 Project Structure

```text
PlatformPulse/
│
├── PlatformPulse.py              # Main application
├── PlatformPulseUtils.py         # Utility functions
├── PlatformPulseLogs/            # Generated reports
└── README.md
```

---

## 🛠️ Technologies Used

* Python 3
* psutil
* schedule
* smtplib
* email.message
* os
* datetime

---

## 📊 What PlatformPulse Monitors

### CPU Statistics

* CPU Usage
* CPU Count
* CPU Frequency

### Memory Statistics

* Total RAM
* Used RAM
* Available RAM
* Memory Usage Percentage

### Network Statistics

* Bytes Sent
* Bytes Received
* Packets Sent
* Packets Received

### Running Processes

* Process ID (PID)
* Process Name
* Username
* CPU Usage
* Memory Usage

These monitoring functions are implemented in the reusable utility module (`PlatformPulseUtils.py`).

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/PlatformPulse.git

cd PlatformPulse
```

Install the required dependencies:

```bash
pip install psutil schedule
```

---

## ▶️ Usage

Run the application:

```bash
python PlatformPulse.py <interval> <sender_email> <receiver_email>
```

Example:

```bash
python PlatformPulse.py 10 sender@gmail.com receiver@gmail.com
```

Where:

* `interval` → Monitoring interval in minutes
* `sender_email` → Gmail account used to send reports
* `receiver_email` → Email address that receives reports

---

## 📧 Email Configuration

PlatformPulse sends reports using **Gmail SMTP**.

Before running the application, open **`PlatformPulse.py`** and locate the following line:

```
# TODO : Add your mail password here
app_password = "YOUR_GMAIL_APP_PASSWORD"

```

Replace `"YOUR_GMAIL_APP_PASSWORD"` with your **Google App Password**.

> **Note:** You must generate a Google App Password if you have Two-Factor Authentication (2FA) enabled on your Gmail account. Regular Gmail passwords will not work.

After updating the App Password, run the program normally:

```
python PlatformPulse.py <interval> <sender_email> <receiver_email>

```

**Example:**

```
python PlatformPulse.py 10 sender@gmail.com receiver@gmail.com

```

> **Important:** Since the App Password is stored directly in the source code, do **not** share your password or upload it publicly. If you plan to publish this project on GitHub, replace the password with a placeholder (for example, `"YOUR_GMAIL_APP_PASSWORD"`) before pushing the code.

---

## 📄 Sample Report

```text
======================================================
                PLATFORMPULSE REPORT
======================================================

CPU STATISTICS
--------------
CPU Usage        : 18.40 %
CPU Count        : 8
CPU Frequency    : 2500.00 MHz

MEMORY STATISTICS
-----------------
Total RAM        : 16.00 GB
Used RAM         : 7.21 GB
Available RAM    : 8.79 GB

NETWORK STATISTICS
------------------
Data Sent        : 512.33 MB
Data Received    : 1234.61 MB

RUNNING PROCESSES
-----------------
PID      Process Name        Username      CPU %    Memory %
```

---

## 🔄 How It Works

```text
Start Program
      │
      ▼
Read Command-Line Arguments
      │
      ▼
Collect CPU, RAM, Network & Process Data
      │
      ▼
Generate Monitoring Report
      │
      ▼
Save Report as Timestamped Log
      │
      ▼
Email Report (Optional)
      │
      ▼
Wait for Scheduled Interval
      │
      ▼
Repeat
```

---

## 📸 Future Improvements

* GUI Dashboard
* Real-time graphs
* Disk usage monitoring
* Multi-platform notifications
* PDF report generation
* Database storage
* Docker support
* REST API integration
* Web dashboard using Flask or Django

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request

---

## 👨‍💻 Author

**Rushikesh Puri**

If you found this project useful, consider giving it a ⭐ on GitHub.

---

## 📜 License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute it for educational and personal projects.
