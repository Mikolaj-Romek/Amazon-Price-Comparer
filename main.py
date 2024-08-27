from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
import os

headers = {
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Upgrade-Insecure-Requests': '1',
}

response = requests.get("https://www.amazon.pl/Ragnar%C3%B6k-PEGI-uncut-niemieckie-opakowanie/dp/B0B6G74TF3/ref=sr_1_3?crid=2VSJ7HD13D3TW&dib=eyJ2IjoiMSJ9.bBZZz4jkID6M5kXB5EGHqvZUMUitqPIIre6ZeGyjACj0-3kg_zK-YpxfSg_Vm2Nv7ziewYSM4xGilTjuxcpdhKnpglUvStWlaSUsup804yx5z2UCX7bQ33rZtn3o680pUGpd9pLpsqNy39Xby_z7EvINs8nfxt8a_n4L7tMNiaeS-OAJ7uU15A_jf7cC9kGWLHWh9zJL3rOBiwDiJeVeWhqcDZ04vVJocbuwTHfEVfTpz8DrlUxsLNExW3jnVJ66Ora92M_fQRsy4HZVwIebxzYcJutG2TnCwIRl-IuvkD0.Fr--c2Ql-ACZ5yFWH7CvqKKkF04Me7_dqZuYFIgks6Y&dib_tag=se&keywords=god+of+war+ragnar%C3%B6k+ps5&qid=1724777265&sprefix=god+of+war+ra%2Caps%2C101&sr=8-3", headers=headers)

soup = BeautifulSoup(response.content, "lxml")
price = soup.find(class_="a-offscreen").get_text()

price_without_zl = price.split("zł")[0]
price = price_without_zl.split(",")
price_without_zl = ".".join(price)
price_float = float(price_without_zl)
print(price_float)

subject = "Buy god of war"
body = f"Buy god of war, the price is: {price_float:.2f} zł"
sender = os.getenv("SENDER_EMAIL")
recipients = [os.getenv("RECIPIENT_EMAIL")]
password = os.getenv("EMAIL_PASSWORD")


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

if price_float < 200:
    send_email(subject, body, sender, recipients, password)
