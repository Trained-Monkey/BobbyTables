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
from helpers import get_articles_within_time, get_subscribed


class Notifier():
    def __init__(self):
        # Define parameters here
        self.e = Event()

        self.sender_address = 'bobbytablesatcho@gmail.com'
        self.sender_pass = 'whoneedssecurity'

        self.session = None

        self.thread = Thread(target=self.check_updates)
        self.thread.daemon = True

        # self.email_dict

    def get_new_articles(self):
        end_date = datetime.datetime.now()
        # Uncomment the line below to get actual data
        end_date = datetime.datetime(2022, 3, 3, 10, 10)
        start_date = end_date - datetime.timedelta(days=1)

        (result, _, count, locations) = get_articles_within_time(end_date, start_date)

        return locations

    def check_updates(self):
        while not self.e.isSet():
            articles = self.get_new_articles()
            new_articles_found = len(articles) > 0

            # Dict of users we're going to notify about this
            to_be_notified = dict()

            if (new_articles_found):
                for location_pair in articles:
                    locations = location_pair[0]
                    article = location_pair[1]

                    subscribers = self.get_subscribers(locations)

                    for subscriber in subscribers:
                        articles_sent = to_be_notified.get(subscriber, [])
                        articles_sent.append(article)
                        to_be_notified[subscriber] = articles_sent

                self.notify_subscribers(to_be_notified)

            # Wait a whole day
            # seconds * minutes * hours
            self.e.wait(60 * 60 * 24)

    def get_subscribers(self, locations):
        print("Getting subscribers")

        return get_subscribed(locations)

    def notify_subscribers(self, subscribers):
        self.session = smtplib.SMTP('smtp.gmail.com', 587) 
        self.session.starttls() 
        self.session.login(self.sender_address, self.sender_pass)

        for subscriber in subscribers.keys():
            self.send_email(subscriber, subscribers[subscriber])

        self.session.quit()

    def start(self):
        self.thread.start()

    def end(self):
        self.e.set()

    def send_email(self, receiver_address, articles=[{'location':'Sydney', 'title':'Sydney is xyz'}]):                
        message = MIMEMultipart()
        message['From'] = self.sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Pandemic article notification'   #The subject line

        file_loader = FileSystemLoader('Notifier/templates')
        env = Environment(loader=file_loader)   
        template = env.get_template('email_format.html')

        mail_content = template.render(articles=articles)
        message.attach(MIMEText(mail_content, 'html'))

        text = message.as_string()
        self.session.sendmail(self.sender_address, receiver_address, text)

    def __del__(self):
        if (self.thread.is_alive()):
            self.end()

def main():
    x = Notifier()
    x.start()
    time.sleep(120)
    x.end()

if __name__ == "__main__":
    main()