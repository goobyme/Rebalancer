import smtplib


class MailMachine:

    def __init__(self, message, email):
        self.raw_text = message
        self.email = email
        self.format_message = self.mail_compose()

    def mail_compose(self):
        format_message = self.raw_text
        # TODO add message writer to MailMachine
        return format_message

    def send(self):

        smtobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtobj.ehlo()
        smtobj.starttls()
        print('Enter Password')
        smtobj.login(self.email, input())
        smtobj.sendmail(self.email, self.email, self.format_message)
        print('Mail sent to {}'.format(self.email))
        smtobj.quit()

