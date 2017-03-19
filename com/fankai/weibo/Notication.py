import smtplib
from email.message import EmailMessage
import imghdr
import sys, threading
import logging

logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

mail_host = "smtp.126.com"
mail_user = '....'
mail_passwd = '.....'
my_email = '....'


def send_email_impl(subject, content, files=None, To=my_email):
    if files is None:
        files = []
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = mail_user
    msg['To'] = To

    for file in files:
        with open(file, 'rb') as fp:
            img_data = fp.read()
        msg.add_attachment(img_data, maintype='image', subtype=imghdr.what(None, img_data), filename=file)

    with smtplib.SMTP() as smtp:
        try:
            smtp.connect(mail_host)
            smtp.login(mail_user, mail_passwd)
            smtp.send_message(msg, mail_user, To)
            logging.info("send email success.subject:%s", msg['Subject'])
        except:
            logging.error('send email exception:%s', sys.exc_info()[0])


def send_email(subject, content, files=None, To=my_email):
    thread = threading.Thread(target=send_email_impl(subject, content, files, To))
    thread.start()


if __name__ == "__main__":
    send_email("测试", "来自Python")
