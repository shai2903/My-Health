import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
import random

ME = "somemail"


def id_generator(size=6, chars=string.ascii_uppercase + string.digits) -> str:
    """create new random str"""
    return ''.join(random.choice(chars) for _ in range(size))


def send_mail_reset(mail: str, username: str):
    """send new password to mail"""
    msg = MIMEMultipart('alternative')

    msg['Subject'] = "Reset password - My-Health"
    msg['From'] = ME
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

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("somemail", "somepass")
    server.sendmail(ME, [mail], msg.as_string())
    server.close()

    return password
