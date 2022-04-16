from threading import Thread
from threading import Event
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage


import sys
import time
import os

import datetime



from jinja2 import Environment, FileSystemLoader
import jinja2
import pymongo

sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..','..', '..', 'API_SourceCode', 'API'))
from helpers import get_articles_within_time


class Notifier():
    def __init__(self):
        # Define parameters here
        self.e = Event()

        self.sender_address = 'bobbytablesatcho@gmail.com'
        self.sender_pass = 'whoneedssecurity'

        self.session = None

        self.thread = Thread(target=self.check_updates)
        self.thread.daemon = True

        self.email_dict

    def get_new_articles(self):
        # end_date = datetime.datetime.now()
        end_date = datetime.datetime(2022, 3, 3, 10, 10)
        start_date = end_date - datetime.timedelta(days=1)


        (result, _, count, locations) = get_articles_within_time(end_date, start_date)

        return result, locations

    def check_updates(self):
        while not self.e.isSet():
            articles, locations = self.get_new_articles()
            new_articles_found = len(articles) > 0

            if (new_articles_found):
                for article in articles:
                    pass

                subscribers = self.get_subscribers(locations)
                self.notify_subscribers(subscribers)

            self.e.wait(60)

    def get_subscribers(self, locations):
        print("Getting subscribers")
        return ['michael.chen0@icloud.com']

    def notify_subscribers(self, subscribers):
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

    def send_email(self, receiver_address, articles=[{'location':'Sydney', 'title':'Sydney is xyz'}]):                
        message = MIMEMultipart()
        message['From'] = self.sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Pandemic article notification'   #The subject line

        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)   
        template = env.get_template('email_format.html')

        mail_content = template.render(articles=articles)
        message.attach(MIMEText(mail_content, 'html'))

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
    # x.start()
    # x.check_updates()
    x.get_new_articles()
    print("Running async")
    # time.sleep(120)

if __name__ == "__main__":
    main()