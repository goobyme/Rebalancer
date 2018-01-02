import smtplib

def mailcompose(*args):
    pass


def mailman(message, email):

    smtobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtobj.ehlo()
    smtobj.starttls()
    print('Enter Password')
    smtobj.login(email, input())
    smtobj.sendmail(email, email, message)
    smtobj.quit()
