import smtplib


class MailMachine:

    def __init__(self, message=list(dict()), email=str()):
        self.raw_text = message
        self.email = email
        self.format_message = self.mail_compose()

    def mail_compose(self):
        format_message = str()

        for report in self.raw_text:
            format_message += ("""{}) Position: {}
            Target Allocation: {}  Real Allocation: {}
            Deviation (%portfolio): {} Deviation (%position): {}
            Transaction: {} {} shares @ {} for {} change in position \n
            """.format(report.get('ticker'), report.get('position'), report.get('target_alloc'),
                       report.get('real_alloc'), report.get('deviation_port'), report.get('deviation_pos'),
                       report.get('transaction'), report.get('amount_change'), report.get('quote'),
                       report.get('position_change')))

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

