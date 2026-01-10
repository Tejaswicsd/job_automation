import os
import feedparser
import yagmail
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER = os.getenv("RECEIVER_EMAIL")

RSS_FEEDS = {
    "Indeed": "https://www.indeed.com/rss?q=entry+level+data+analyst",
    "Wellfound": "https://angel.co/jobs.rss?keywords=data%20analyst"
}

def fetch_jobs():
    jobs = []

    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            jobs.append(
                f"{entry.title}\n{entry.link}\nSource: {source}\n"
            )

    send_email(jobs)

def send_email(jobs):
    if not jobs:
        body = "No new Data Analyst jobs found today."
    else:
        body = "📊 Entry-Level Data Analyst Jobs\n\n"
        body += "\n".join(jobs)

    yag = yagmail.SMTP(EMAIL, PASSWORD)
    yag.send(
        to=RECEIVER,
        subject=f"📊 Daily Job Alerts – {datetime.now().strftime('%d %b %Y')}",
        contents=body
    )

if __name__ == "__main__":
    fetch_jobs()
