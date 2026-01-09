import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import yagmail
from datetime import datetime

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER = os.getenv("RECEIVER_EMAIL")

SEARCH_QUERY = "entry level data analyst jobs top startups"

def search_jobs():
    url = f"https://www.google.com/search?q={SEARCH_QUERY.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for a in soup.select("a"):
        href = a.get("href")
        if href and "http" in href and ("job" in href or "career" in href):
            links.append(href)

    links = list(set(links))[:10]

    send_email(links)

def send_email(links):
    if not links:
        body = "No job listings found today."
    else:
        body = "Top Entry-Level Data Analyst Jobs:\n\n"
        for i, link in enumerate(links, 1):
            body += f"{i}. {link}\n"

    yag = yagmail.SMTP(EMAIL, PASSWORD)
    yag.send(
        to=RECEIVER,
        subject=f"📊 Daily Data Analyst Jobs – {datetime.now().strftime('%d %b %Y')}",
        contents=body
    )

if __name__ == "__main__":
    search_jobs()
