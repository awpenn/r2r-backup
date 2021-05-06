from dotenv import load_dotenv
import smtplib, ssl
import datetime
import os

port = 465  # For SSL

load_dotenv()

password = os.getenv('ALERT_EMAIL_PASS')
email = os.getenv('ALERT_EMAIL')
reciever = os.getenv('EMAIL_DEST')


def main( ):
# Create a secure SSL context
    context = ssl.create_default_context( )

    date = datetime.date.today( )
    time = datetime.datetime.now( ).strftime("%H:%M:%S")

    message = f"""\
        Subject: SCP Failure

        SCP backup of 165.123.11.7 to sciget failed at { date }-{ time }. Check remote storage."""
    
    with smtplib.SMTP_SSL( "smtp.gmail.com", port, context=context ) as server:
        server.login( email, password )
        print('sending error email')
        server.sendmail( email, reciever, message )

if __name__ == '__main__':
    main()

