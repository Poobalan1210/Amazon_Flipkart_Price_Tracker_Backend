import requests
from bs4 import BeautifulSoup
import schedule
import time
import smtplib

headers = {
    'user-agent': 'Mozilla/5.0 (X11Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

amazon_url = "https://www.amazon.in/Logitech-M235-Wireless-Mouse-Grey/dp/B004IO5BMQ/ref=sr_1_3?dchild=1&keywords=logitech+m235&qid=1609294717&sr=8-3"
#res = requests.get(url, headers=headers)
#soup = BeautifulSoup(res.text, 'html.parser')

org_amazon_page = requests.get(amazon_url, headers=headers)
soup = BeautifulSoup(org_amazon_page.content, 'html.parser')
# print(soup(soup.find(id="priceblock_ourprice")))
org_amazon_price = soup.find(id="priceblock_ourprice").getText()
org_amazon_price = float(org_amazon_price[1:])
print(org_amazon_price)

flipkart_url = "https://www.flipkart.com/logitech-m235-wireless-optical-mouse/p/itmf945ezsm9uggf?pid=ACCCZHJZGQAWCNHY&lid=LSTACCCZHJZGQAWCNHYH7N58K&marketplace=FLIPKART&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=37d9ec0f-7384-4747-8424-3aa5fcca9d77.ACCCZHJZGQAWCNHY.SEARCH&ssid=vy7h0e8fsw0000001609295013958&qH=2d778ad48ed829b3"
org_flipkart_page = requests.get(flipkart_url, headers=headers)
soup = BeautifulSoup(org_flipkart_page.content, 'html.parser')
# print(soup.find(
# "div", {"class": "_30jeq3 _16Jk6d"}))
org_flipkart_price = soup.find(
    "div", {"class": "_30jeq3 _16Jk6d"}).getText()
print(org_flipkart_price)
org_flipkart_price = float(org_flipkart_price[1:].replace(',', ''))
print(org_flipkart_price)
