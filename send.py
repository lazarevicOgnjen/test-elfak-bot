import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

courses = {
    "bp": {"subject": "🎓 Baze podataka", "forum": "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=4&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=", "attachment": "bp.png"},
    "dmat": {"subject": "🎓 Diskretna matematika", "forum": "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=97&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=", "attachment": "dmat.png"},
    "sp": {"subject": "🎓 Strukture podataka", "forum": "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=9&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=", "attachment": "sp.png"},
    "pj": {"subject": "🎓 Programski jezici", "forum": "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=11&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=", "attachment": "pj.png"},
    "oopj": {"subject": "🎓 Objektno orijentisano projektovanje", "forum": "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=62&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=", "attachment": "oopj.png"},
    "lp": {"subject": "🎓 Logičko projektovanje", "forum": "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=41&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=", "attachment": "lp.png"},
    "oop": {"subject": "🎓 Objektno orijentisano programiranje", "forum": "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=45&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=", "attachment": "oop.png"},
    "aor1": {"subject": "🎓 Arhitektura i organizacija računara 1", "forum": "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=139&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2020&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=", "attachment": "aor1.png"},
    "aip": {"subject": "🎓 Algoritmi i programiranje", "forum": "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=3&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=", "attachment": "aip.png"},
    "uur": {"subject": "🎓 Uvod u računarstvo", "forum": "https://cs.elfak.ni.ac.rs/nastava/mod/forum/search.php?id=2&words=&phrase=&notwords=&fullwords=&timefromrestrict=1&fromday=1&frommonth=1&fromyear=2023&fromhour=0&fromminute=0&hfromday=0&hfrommonth=0&hfromyear=0&hfromhour=0&hfromminute=0&htoday=1&htomonth=1&htoyear=1&htohour=1&htominute=1&forumid=&subject=&user=", "attachment": "uur.png"},
    "sip": {"subject": "🎓 SIP", "forum": "https://sip.elfak.ni.ac.rs/", "attachment": "sip.png"}
}

EMAIL_USERNAME = os.environ['EMAIL_USERNAME']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

def send_email(to_emails, subject, html_body, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USERNAME
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html'))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', f"<{os.path.basename(attachment_path).split('.')[0]}_image>")
            msg.attach(img)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)

for course, info in courses.items():
    changed = os.environ.get(f"{course}_changed", "false")
    email_file = f"{course}_emails.md"

    if changed == "true" and os.path.exists(email_file):
        with open(email_file) as f:
            to_emails = [line.strip() for line in f if line.strip()]

        if not to_emails:
            print(f"No emails for {course}, skipping.")
            continue

        html_body = f"""
        <html>
          <body>
            <img src="cid:{course}_image" alt="{course} Screenshot" style="max-width:100%; border:1px solid #ccc;">
            <p>Check the course page for details: <a href="{info['forum']}">{info['subject']} Forum</a></p>
            <p><small>
              🔔 <strong>Manage your notifications:</strong>
              <a href="https://forms.gle/2XaMVYxLjiVikKCw5" style="color:#666; text-decoration:underline;">Form link</a>
            </small></p>
          </body>
        </html>
        """
        print(f"Sending {course} email to: {', '.join(to_emails)}")
        send_email(to_emails, info['subject'], html_body, info['attachment'])
