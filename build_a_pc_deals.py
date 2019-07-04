#! usr/bin/env python3
import praw
from twilio.rest import Client
import time
import test

monitor_list = []


def text(monitor):
    account_sid = test.TWILIO_ACCOUNT_SID
    auth_token = test.TWILIO_SECRET
    client = Client(account_sid, auth_token)
    body_m = monitor.title
    body_m += " " + monitor.url

    message = client.messages.create(
        body=body_m,
        from_=test.FROM_NUMBER,
        to=test.TO_NUMBER

    )


def add_monitor(monitor):
    global monitor_list
    if monitor.id not in monitor_list:
        monitor_list.append(monitor.id)
        text(monitor)
        if len(monitor_list) >= 10:
            monitor_list.pop(0)

def main():
    reddit = praw.Reddit(client_id=test.REDDIT_CLIENT_ID, client_secret=test.REDDIT_CLIENT_SECRET,
                         user_agent=test.REDDIT_SUB, username=test.REDDIT_USERNAME,
                         password=test.REDDIT_PASSWORD)

    subreddit = reddit.subreddit('buildapcsales')

    new_submissions = subreddit.new(limit=10)

    for submission_ in new_submissions:
        submission = submission_.title.split()
        if submission[0].lower() == '[monitor]':
            add_monitor(submission_)


if __name__ == '__main__':
    try:
        while True:
            main()
            time.sleep(10)
            print("running")
    except KeyboardInterrupt:
        print("Terminating Program")
