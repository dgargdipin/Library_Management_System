
def emailsend(email_data):
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    message = Mail(
        from_email='oarzpo+ete5dgnbnh4a4@sharklasers.com',
        to_emails=email_data['email'],
        subject='Notice for Book Due',
        html_content='Dear {},\nYour book {} is due at the library. Please return soon.'.format(email_data['name'],email_data['book_name']))

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)