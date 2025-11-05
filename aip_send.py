import os, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

SENDER_EMAIL = os.getenv("EMAIL_USERNAME")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER, SMTP_PORT = "smtp.gmail.com", 587
RECEIVERS_FILE, IMAGE_PATH = "aip_emails.md", "aip.png"

HTML_BODY = """
<html><body>
<p><img src="cid:embedded_image" style="width:300px;border-radius:10px;"></p>
<p>AIP forum -> <a href="">here</a>link</p>

<p>Google form -> <a href="">here</a>link</p>
</body></html>
"""

with open(RECEIVERS_FILE) as f:
    recipients = [line.strip() for line in f if line.strip()]

if recipients:
    for to_email in recipients:
        msg = MIMEMultipart("related")
        msg["From"], msg["To"], msg["Subject"] = SENDER_EMAIL, to_email, "🎓 AIP"
        alt = MIMEMultipart("alternative")
        msg.attach(alt)
        alt.attach(MIMEText(HTML_BODY, "html"))

        try:
            with open(IMAGE_PATH, "rb") as img:
                mime_img = MIMEImage(img.read())
                mime_img.add_header("Content-ID", "<embedded_image>")
                msg.attach(mime_img)
        except FileNotFoundError:
            pass

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print(f"✅ Sent to {to_email}")
else:
    print("⚠️ No recipients found.")
