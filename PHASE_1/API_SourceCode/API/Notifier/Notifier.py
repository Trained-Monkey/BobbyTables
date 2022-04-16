from threading import Thread
from threading import Event
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

class Notifier():
    def __init__(self):
        # Define parameters here
        self.e = Event()

        self.sender_address = 'bobbytablesatcho@gmail.com'
        self.sender_pass = 'whoneedssecurity'

        self.session = None

        self.thread = Thread(target=self.check_updates)
        self.thread.daemon = True

    def get_new_articles(self):
        return [1]

    def check_updates(self):
        while not self.e.isSet():
            articles = self.get_new_articles()
            new_articles_found = len(articles) > 0

            if (new_articles_found):
                subscribers = self.get_subscribers()
                self.notify_subscribers(subscribers)

            self.e.wait(60)

    def get_subscribers(self):
        print("Getting subscribers from the db")
        return ['lifasog470@aikusy.com']

    def notify_subscribers(self, subscribers):
        print("Sending email to subscribers")

        self.session = smtplib.SMTP('smtp.gmail.com', 587) 
        self.session.starttls() 
        self.session.login(self.sender_address, self.sender_pass)

        for subscriber in subscribers:
            self.send_email(subscriber)

        self.session.quit()

    def start(self):
        self.thread.start()

    def end(self):
        print("Terminating")
        self.e.set()

    def send_email(self, receiver_address):                
        message = MIMEMultipart()
        message['From'] = self.sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Pandemic article notification'   #The subject line

        mail_content = "We received a new article on the country you subscribed to"
        message.attach(MIMEText(mail_content, 'plain'))
        text = message.as_string()
        self.session.sendmail(self.sender_address, receiver_address, text)

    def __del__(self):
        print("Destructor called shutting down")
        if (self.thread.is_alive()):
            self.end()
            self.thread.join()
            print("Successfully joined")

def main():
    x = Notifier()
    x.start()
    print("Running async")
    time.sleep(120)

if __name__ == "__main__":
    main()