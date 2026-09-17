"""
CircularSender — server.py
Click the tray icon to stop the server.
"""
import smtplib, base64, os, sys, threading, webbrowser, time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formataddr
from email import encoders
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import socket

# ── Tray icon ──
try:
    import pystray
    from PIL import Image, ImageDraw
    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False

app = Flask(__name__)
CORS(app)

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'CircularSender.html')

@app.route('/ping')
def ping():
    return jsonify({"ok": True})

@app.route('/send', methods=['POST'])
def send():
    data        = request.get_json(force=True)
    email       = data.get('email', '').strip()
    password    = data.get('password', '').strip()
    sender_name = data.get('sender_name', '').strip()
    subject     = data.get('subject', '(No Subject)')
    recipients  = data.get('recipients', [])
    pdf_b64     = data.get('pdfBase64', '')
    pdf_name    = data.get('pdfName', 'circular.pdf')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400
    if not recipients:
        return jsonify({"error": "No recipients"}), 400

    try:
        msg = MIMEMultipart()
        display = formataddr((sender_name, email)) if sender_name else email
        msg["From"]     = display
        msg["Reply-To"] = display
        msg["To"]       = email
        msg["Subject"]  = subject
        msg.attach(MIMEText("", "plain"))

        if pdf_b64:
            part = MIMEBase("application", "pdf")
            part.set_payload(base64.b64decode(pdf_b64))
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="{pdf_name}"')
            msg.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email, password)
            smtp.sendmail(email, recipients, msg.as_string())

        print(f"[OK]  {len(recipients)} emails sent via {email}")
        return jsonify({"ok": True, "sent": len(recipients)})

    except smtplib.SMTPAuthenticationError:
        print(f"[ERR] Auth failed for {email}")
        return jsonify({"error": f"Authentication failed for {email}. Check your App Password."}), 401
    except Exception as e:
        print(f"[ERR] {e}")
        return jsonify({"error": str(e)}), 500

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def make_tray_icon():
    """Draw a simple envelope icon for the tray."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Blue background circle
    d.ellipse([0, 0, 63, 63], fill=(79, 142, 247, 255))
    # Envelope body
    d.rectangle([12, 22, 52, 44], fill="white")
    # Envelope flap (V shape)
    d.polygon([12, 22, 32, 36, 52, 22], fill=(180, 210, 255))
    return img

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://localhost:9090")

def start_flask():
    app.run(host='0.0.0.0', port=9090, debug=False, use_reloader=False)

def run_tray(local_ip):
    if not HAS_TRAY:
        # No tray support — just run flask with a console
        start_flask()
        return

    icon_image = make_tray_icon()

    def on_open(icon, item):
        webbrowser.open("http://localhost:9090")

    def on_quit(icon, item):
        icon.stop()
        os._exit(0)

    menu = pystray.Menu(
        pystray.MenuItem("Open CircularSender", on_open, default=True),
        pystray.MenuItem(f"Running on port 9090", None, enabled=False),
        pystray.MenuItem(f"LAN: {local_ip}:9090", None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Stop Server & Quit", on_quit),
    )

    icon = pystray.Icon("CircularSender", icon_image, "CircularSender ✉", menu)

    # Flask runs in background thread, tray runs on main thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    icon.run()

if __name__ == '__main__':
    local_ip = get_local_ip()
    print("=" * 50)
    print("  CircularSender — Running!")
    print(f"  This PC:   http://localhost:9090")
    print(f"  Other PCs: http://{local_ip}:9090")
    print("  Right-click tray icon to stop.")
    print("=" * 50)

    threading.Thread(target=open_browser, daemon=True).start()
    run_tray(local_ip)
