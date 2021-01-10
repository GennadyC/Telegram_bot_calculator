import smtplib


class MailConnection():
    def __init__(self, smtp, port, username, password):
        self.smtp = smtp
        self.port = port
        self.username = username
        self.password = password
        self.smtpObj = None
        self.mail_connection()

    def mail_connection(self):
        self.smtpObj = smtplib.SMTP(self.smtp, self.port)
        self.smtpObj.starttls()
        self.smtpObj.login(self.username, self.password)

    def send_mail(self, to, message):
        self.smtpObj.sendmail(self.username, to, message)

    def close_connection(self):
        self.smtpObj.quit()