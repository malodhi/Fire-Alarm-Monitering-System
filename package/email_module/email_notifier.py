import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
from getpass import getpass


class EmailNotifier(object):
    def __init__(self,
                 recipient_file: str = "../email_module/recipient_emails.txt",
                 host_ip: str='192.168.146.38', host_port='5000'):
        self.img_file = '' 
        self.smoke_qty = int(-1)
        self.recipient_file = recipient_file
        self.host_ip = host_ip
        self.host_port = host_port
        self.sender_address = "s6509106860073@email.kmutnb.ac.th"

    def _get_sender_pass(self):
        password = getpass(f"Please enter password for email: {self.sender_address}\n"
                           f"Password: ")
        return password
        
    def send_emails(self, smoke_qty: float, img_file: str = ''):
        self.smoke_qty = smoke_qty
        self.img_file = Path(img_file)
        if not self.img_file.exists():
            raise Exception("Image file not found.")
        password = self._get_sender_pass()
        msg = "Mansoor97." # self.generate_msg()
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            # smtp.set_debuglevel(1)
            smtp.starttls()
            smtp.login(self.sender_address, password)
            for recipient_email in self._read_recipient_data(self.recipient_file):
                smtp.sendmail(self.sender_address, recipient_email, msg.as_string())

    def generate_msg(self, recipient_email: str = ''):
        msg = MIMEMultipart('related')
        msg["Subject"] = "FIRE WARNING"
        msg["From"] = self.sender_address
        msg["To"] = recipient_email if recipient_email else None
        image_id = 'image_id_1'
        body = self._generate_body()
        msg.attach(MIMEText(self._generate_html(body, image_id), 'html'))
        with open(self.img_file.as_posix(), 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', f'<{image_id}>')
            msg.attach(img)
        return msg

    def _generate_body(self):
        return f'<b>DEAR ALL, <br><br>' \
               f'ACCORDING TO PM2.5 SMOKE SENSOR, THE SMOKE LEVEL IS :   \t\t{str(self.smoke_qty)} <br><br>' \
               f'IF YOU ARE ON UNIVERSITY NETWORK, YOU CAN MONITOR IT LIVE. <br>' \
               f'CLICK <a href="http://{self.host_ip}:{self.host_port}/">HERE</a> TO VIEW.</p>' \
               f'<br><br> BEST REGARDS, <br><br></b>'

    @staticmethod
    def _generate_html(body, image_id):
        return f"""\
        <html>
          <body>
            <p>{body}</p>
            <img src="cid:{image_id}">
          </body>
        </html>
        """

    @staticmethod
    def _read_recipient_data(file):
        file = Path(file)
        if not file.exists() or not file.is_file():
            raise Exception("Recipient emails file not found.")
        f = open(file.as_posix(), "r")
        emails = f.read().strip().split("\n")
        emails = [email.strip() for email in emails]
        return emails


if __name__ == '__main__':
    email_handler = EmailNotifier()
    email_handler.send_emails(smoke_qty=50, 
                              img_file="image_1682321440.9615016.png")
    print("Email Send !")
