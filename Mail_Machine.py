import smtplib


class MailMachine:

    def __init__(self, message, email):
        self.message = message
        self.email = email
        self.format_message = self.mailcompose(message)

    def mailcompose(self):
        format_message = self.message
        # TODO add message writer to MailMachine
        return format_message

    def mailman(self):

        smtobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtobj.ehlo()
        smtobj.starttls()
        print('Enter Password')
        smtobj.login(self.email, input())
        smtobj.sendmail(self.email, self.email, self.mailcompose())
        print('Mail sent to {}'.format(self.email))
        smtobj.quit()

