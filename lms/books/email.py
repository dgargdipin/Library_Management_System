from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
def sendMail(to,name,book):
    message = Mail(
        from_email='oarzpo+ete5dgnbnh4a4@sharklasers.com',
        to_emails=to,
        subject='Book Overdue',
        html_content='Dear {},\n The book named {} you issued is overdue, kindly return it.'.format(name,book))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("sada")
        print(e)



        