# CircularSender

A local web-based school circular distribution tool for sending PDF circulars to large recipient lists using Gmail SMTP accounts.

## Features

- Import recipients from Excel (`.xlsx`, `.xls`) or CSV
- Automatic email-column detection
- Detect and filter by class / grade / section
- Send PDF circulars as attachments
- Support multiple Gmail SMTP accounts
- Batch recipients across configured accounts
- Test Mode
- Scheduled sending
- Live sending progress
- Success and error logs
- CSV log export
- Browser-based account configuration
- Optional Windows system-tray operation
- LAN access from other computers on the same network

## Project Structure

```text
CircularSender/
├── CircularSender.html
├── server.py
├── CircularSender.spec
├── START.bat
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

## Requirements

- Windows 10/11 recommended
- Python 3.10+ recommended
- Gmail account(s)
- Gmail App Password for each SMTP account
- Network access to Gmail SMTP

Install dependencies:

```bash
pip install -r requirements.txt
```

## Gmail Setup

CircularSender uses Gmail SMTP over SSL:

```text
SMTP server: smtp.gmail.com
Port: 465
Security: SMTP SSL
```

Use a Gmail **App Password** rather than your normal Gmail password.

Never publish App Passwords in the repository.

## Running

### START.bat

Double-click `START.bat`. It installs the required packages and starts the server.

### Python

```bash
python server.py
```

Then open:

```text
http://localhost:9090
```

## LAN Access

The server listens on `0.0.0.0:9090`.

From another computer on the same trusted LAN:

```text
http://SERVER-IP:9090
```

Example:

```text
http://192.168.0.100:9090
```

Windows Firewall may need an inbound TCP rule for port `9090`.

## Sending Workflow

1. Start CircularSender.
2. Import the recipient Excel/CSV file.
3. Select the target audience.
4. Upload the PDF circular.
5. Configure the sender display name.
6. Configure Gmail SMTP accounts.
7. Optionally enable Test Mode or Schedule.
8. Start sending.
9. Review progress and logs.
10. Export logs if required.

## Recipient File

The application attempts to detect email and class/grade/section columns. Duplicate email addresses are removed.

The target audience can be `ALL` or a detected class/grade/section value.

## Multiple Gmail Accounts

The current application supports multiple Gmail accounts and uses a batch size of **499 recipients**. Active accounts are rotated batch-by-batch.

## Test Mode

Test Mode uses the primary configured account for the test operation.

## Scheduling

Scheduling is handled in the browser. Keep the CircularSender page open and the server running until the scheduled send starts.

## Logs

Logs are stored in browser `localStorage`. The interface can export successful records, errors, or full logs as CSV.

## Security

- Gmail App Passwords are stored in browser `localStorage`.
- Account configuration can be exported as JSON.
- Never commit exported account JSON files.
- Do not share App Passwords.
- Do not expose port `9090` to the public Internet.
- The current server has no user authentication.
- Run the application only on a trusted network.

## Delivery Status

A successful application response means the SMTP submission operation completed successfully for the batch. It does **not** guarantee final inbox delivery. Bounces, spam filtering, and downstream recipient-server decisions are not currently tracked.

## Building a Windows Executable

Install PyInstaller:

```bash
pip install pyinstaller
```

Build using the included spec:

```bash
pyinstaller CircularSender.spec
```

The executable will be placed in `dist/`.

## API

The Flask server provides:

```text
GET  /
GET  /ping
POST /send
```

## Current Limitations

- Scheduling depends on the browser page remaining open.
- Credentials are stored client-side in `localStorage`.
- No authentication is implemented for the Flask server.
- SMTP submission is not the same as per-recipient delivery confirmation.
- SheetJS is loaded from an external CDN, so the frontend is not completely offline/self-contained.

## License

MIT License. See `LICENSE`.
