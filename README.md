# CircularSender

A lightweight, self-hosted bulk email dispatcher designed for distributing school circulars as PDF attachments.

CircularSender provides a browser-based interface for importing recipient lists from Excel/CSV files, selecting a target audience, attaching a PDF circular, configuring Gmail SMTP accounts, and dispatching emails in batches with live progress and detailed logs.

## Features

* 📊 Import recipients from `.xlsx`, `.xls`, or `.csv`
* 🔎 Automatically detect email columns
* 🧹 Remove duplicate email addresses
* 🎯 Filter recipients by Class, Grade, or Section
* 📄 Attach PDF circulars
* 📝 Automatically use the PDF filename as the initial subject
* 📧 Support multiple Gmail SMTP accounts
* 🔐 Gmail App Password authentication
* 📦 Split large recipient lists into batches
* 🧪 Test Mode for sending to the primary account before a real dispatch
* ⏰ Schedule a dispatch for a specified time
* 📈 Live sending progress
* 📟 Live activity output
* ❌ Cancellation support
* 📋 Persistent dispatch logs
* 🔍 Filter logs by success or error
* 📤 Export success, error, or complete logs as CSV
* ⚙️ Import/export Gmail account configuration
* 🖥️ Local Flask server
* 🌐 LAN access from other computers
* 🔔 Windows system-tray integration
* 🚀 Optional PyInstaller executable build

## How It Works

```text
Excel / CSV
     │
     ▼
CircularSender Web Interface
     │
     ├── Select email columns
     ├── Remove duplicates
     ├── Select class / section
     ├── Select PDF circular
     ├── Set subject
     └── Configure sender accounts
     │
     ▼
Recipient Batching
     │
     ▼
Local Flask Backend
     │
     ▼
Gmail SMTP
     │
     ▼
Recipients
```

The frontend runs in the browser while the Python backend handles SMTP authentication and email delivery.

## Project Structure

```text
CircularSender/
│
├── CircularSender.html      # Web interface
├── server.py                # Flask + Gmail SMTP backend
├── CircularSender.spec      # PyInstaller build configuration
├── START.bat                # Windows development/startup script
├── requirements.txt         # Python dependencies
├── README.md                # Documentation
├── .gitignore               # Git exclusions
└── LICENSE                  # Optional license
```

## Requirements

### Windows

* Windows 10/11
* Python 3.x
* Internet connection
* Gmail account(s) with App Passwords enabled

### Python packages

```bash
pip install -r requirements.txt
```

Required packages:

```text
Flask
flask-cors
pystray
Pillow
```

## Gmail Configuration

CircularSender uses Gmail SMTP with an App Password.

Each configured account contains:

* Gmail address
* Gmail App Password
* Sender display name

The application uses:

```text
SMTP Server: smtp.gmail.com
SMTP Port: 465
Security: SSL
```

Do not use your normal Gmail password.

Use a Gmail App Password where supported by your Google account.

## Running the Application

### Option 1 — START.bat

On Windows, run:

```text
START.bat
```

The script starts the local Flask server and opens the application.

The application is available at:

```text
http://localhost:9090
```

### Option 2 — Python

Install dependencies:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python server.py
```

Open:

```text
http://localhost:9090
```

## LAN Access

The Flask server listens on:

```text
0.0.0.0:9090
```

This allows the application to be accessed from another computer on the same LAN.

For example:

```text
http://192.168.1.100:9090
```

Replace the IP address with the IP address of the computer running CircularSender.

Windows Firewall must allow inbound TCP traffic on port `9090` if other computers need access.

## Sending a Circular

### 1. Import the recipient list

Upload an Excel or CSV file.

CircularSender attempts to detect columns containing email addresses.

For example:

```text
Name              Email                    Class
---------------------------------------------------
John              john@example.com         8A
Sarah             sarah@example.com        8A
David             david@example.com        8B
```

### 2. Select the audience

Choose:

```text
ALL — All recipients
```

or a detected class/grade/section.

### 3. Select the PDF

Upload the school circular PDF.

The filename is automatically used as the initial email subject.

### 4. Configure the sender

Add one or more Gmail accounts in the **Gmail Accounts** tab.

Each account can have its own sender display name.

### 5. Test

Enable:

```text
Test Mode
```

This sends a test email to the primary configured Gmail account rather than the complete recipient list.

### 6. Send

Click:

```text
START SENDING
```

The recipient list is divided into batches and processed sequentially.

## Recipient Batching

The current frontend uses a batch size of:

```text
499 recipients
```

Batches are assigned to configured accounts sequentially.

For example:

```text
Batch 1 → Account 1
Batch 2 → Account 2
Batch 3 → Account 3
Batch 4 → Account 4
Batch 5 → Account 1
```

Only accounts containing both an email address and password are considered active.

## Scheduling

The Send Settings section provides a scheduling option.

When enabled, the browser waits until the selected time before beginning the dispatch.

Keep the browser/application running while waiting for the scheduled send.

## Logs

CircularSender records dispatch information locally in browser storage.

The Logs section provides:

* All dispatches
* Successful batches
* Failed batches
* Individual recipient lists
* Success/error filtering
* CSV export

Available exports:

```text
Success Log
Error Log
Full Log
```

## Account Configuration

Account settings are stored in browser `localStorage`.

The application also provides:

```text
Export JSON
Import JSON
```

for transferring account configuration between browser installations.

### Security Warning

Account configuration contains Gmail App Passwords.

Do **not** commit exported account JSON files to Git.

Do not upload real credentials to GitHub.

If an account configuration has been exposed publicly, revoke the affected App Password and create a new one.

## Building a Windows Executable

The repository includes:

```text
CircularSender.spec
```

for PyInstaller.

A typical build command is:

```bash
pyinstaller CircularSender.spec
```

The generated executable will be placed in the PyInstaller output directory.

Before building, make sure the `.spec` file references the local project `server.py` rather than a machine-specific absolute path.

## Architecture

### Frontend

```text
CircularSender.html
```

The frontend handles:

* UI
* Excel parsing
* Recipient filtering
* Duplicate removal
* PDF loading
* Account configuration
* Scheduling
* Batch management
* Progress display
* Local logs

SheetJS is used in the browser to process Excel files.

### Backend

```text
server.py
```

The backend provides a small Flask API.

Endpoints:

```text
GET  /
GET  /ping
POST /send
```

`/` serves the CircularSender interface.

`/ping` is used to determine whether the local backend is running.

`/send` receives the email account, recipients, subject and PDF data and sends the message through Gmail SMTP.

## Important Limitations

This project is intended as a lightweight internal tool rather than a full enterprise mail delivery platform.

Current implementation characteristics include:

* Gmail SMTP is used for delivery.
* Scheduling is performed by the browser.
* Account settings are stored in browser `localStorage`.
* Dispatch logs are stored in browser `localStorage`.
* LAN access depends on Windows Firewall/network configuration.
* The frontend loads some resources from external CDNs.
* Delivery status represents successful SMTP submission, not confirmation that the recipient actually opened or received the message.
* A failed batch is currently treated as failed for the recipients in that batch.
* The application should remain running during scheduled operations.

## Security Considerations

CircularSender handles sensitive information including:

* Gmail addresses
* Gmail App Passwords
* Recipient email addresses
* School circular documents
* Dispatch history

For internal deployment:

* Restrict LAN access to trusted networks.
* Do not expose port `9090` directly to the public Internet.
* Do not commit credentials or exported account JSON files.
* Use Gmail App Passwords rather than normal account passwords.
* Protect the Windows computer hosting the application.
* Consider moving credential storage to a secure encrypted mechanism for production use.

## Development

Clone the repository:

```bash
git clone https://github.com/<your-username>/circular-sender.git
cd circular-sender
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python server.py
```

Then open:

```text
http://localhost:9090
```

## License

Choose a license appropriate for your intended distribution.

If this is primarily an internal school IT project, you may also keep the repository private and omit a public license.

---

**CircularSender**
Lightweight school circular distribution through Gmail SMTP.
