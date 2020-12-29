import pyrebase
import webbrowser
import requests
from bs4 import BeautifulSoup
import schedule
import time
import smtplib
import gettext

config = {
    "apiKey": "AIzaSyC5PuJj7QcRNIjIeI32EczKTaVa6mhuVyg",
    "authDomain": "flipkart-price-tracker.firebaseapp.com",
    "databaseURL": "https://flipkart-price-tracker-default-rtdb.firebaseio.com",
    "projectId": "flipkart-price-tracker",
    "storageBucket": "flipkart-price-tracker.appspot.com",
    "messagingSenderId": "1044509919052",
    "appId": "1:1044509919052:web:bf45df6c22986e8f1031e9",
    "measurementId": "G-RESS01LCH6"
}

headers = {
    'user-agent': 'Mozilla/5.0 (X11Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

firebase = pyrebase.initialize_app(config)

db = firebase.database()


def get_amazon_price(amazon_url):
    org_amazon_page = requests.get(amazon_url, headers=headers)
    soup = BeautifulSoup(org_amazon_page.content, 'html.parser')
    try:
        org_amazon_price = soup.find(id="priceblock_ourprice").get_text()
        org_amazon_price = float(org_amazon_price[1:])
        return org_amazon_price
    except:
        return start()


def get_flipkart_price(flipkart_url):
    org_flipkart_page = requests.get(flipkart_url, headers=headers)
    soup = BeautifulSoup(org_flipkart_page.content, 'html.parser')
    try:
        org_flipkart_price = soup.find(
            "div", {"class": "_30jeq3 _16Jk6d"}).get_text()
        org_flipkart_price = float(org_flipkart_price[1:].replace(',', ''))
        return org_flipkart_price
    except:
        return start()


def check_prices(amazon_url, flipkart_url, budget_price, mail_id):

    org_amazon_price = get_amazon_price(amazon_url)
    org_flipkart_price = get_flipkart_price(flipkart_url)
    price_list = {}
    price_list['amazon_price'], price_list['flipkart_price'] = org_amazon_price, org_flipkart_price
    if min(price_list.values()) is not None and budget_price is not None:
        if min(price_list.values()) <= float(budget_price):
            if price_list['amazon_price'] < price_list['flipkart_price']:
                message = f"Amazon has the best deal with Rs.{org_amazon_price}"
                sendmail(mail_id, message, amazon_url)
                return delete_record(mail_id)
            elif price_list['flipkart_price'] < price_list['amazon_price']:
                message = f"Flipkart has the best deal with Rs.{org_flipkart_price}"
                sendmail(mail_id, message, flipkart_url)
                return delete_record(mail_id)
            elif price_list['amazon_price'] == price_list["flipkart_price"]:
                message = f"Both has the same price at Rs.{org_amazon_price}"
                sendmail(mail_id, message, 'Amazon link - ' +
                         amazon_url+'\n'+'Flipkart link - '+flipkart_url)
                return delete_record(mail_id)
    else:
        return


def delete_record(mail_id):
    db.child("Users").child(mail_id.strip(".com")).remove()
    print("deleted")


def sendmail(mail_id, message, URL):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('poobalan12100@gmail.com', 'Poobalan1210/')
    subject = 'Hey! Price fell down'
    body = message+'\n'+'Check the link ->' + URL

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail('poobalan12100@gmail.com', mail_id, msg)

    print('Email Sent')

    server.quit()


def start():

    user = db.child("Users").get()

    if user.val() is None:
        print("sleeping")
        time.sleep(30)
        return

    for use in user.each():
        if use is None:
            return start()
        data = {}
        subdb = db.child("Users").child(use.key()).get()
        for key in subdb.each():
            if key.val() is None:
                time.sleep(60)
            data[key.key()] = key.val()
        check_prices(data['amazon_url'],
                     data['flipkart_url'], data['budget_price'], data['mailid'])


schedule.every(60).seconds.do(start)
while True:
    schedule.run_pending()
    time.sleep(1)
    start()
