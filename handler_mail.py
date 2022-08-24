import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
import random
import consts


def id_generator(size=6, chars=string.ascii_uppercase + string.digits) -> str:
    """Create new random str"""
    return ''.join(random.choice(chars) for _ in range(size))


def send_mail_reset(mail: str, username: str):
    """Send new password to mail"""
    msg = MIMEMultipart('alternative')

    msg['Subject'] = "Reset password - My-Health"
    msg['From'] = consts.SENDER_MAIL
    msg['To'] = mail

    password = id_generator()

    # Create the body of the message (a plain-text and an HTML version).
    html = """\
    <html>
    <head></head>
    <body>
        <p>Hi {0} from My-Health<br>
         Your new password is: {1}
        </p>
    </body>
    </html>
    """

    txt = html.format(username, password)

    # Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(txt, 'html')
    msg.attach(part2)

    # Send the message via SMTP server
    server = smtplib.SMTP(consts.SMTP_SERVER, 587)
    server.ehlo()
    server.starttls()
    server.login(consts.SENDER_MAIL, consts.SENDER_PASSWORD)
    server.sendmail(consts.SENDER_MAIL, [mail], msg.as_string())
    server.close()

    return password
