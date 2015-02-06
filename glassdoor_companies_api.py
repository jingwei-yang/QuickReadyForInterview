import requests

url = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=29781&t.k=jQdxv7dRxPc&action=employers&q=Google&userip=0.0.0.0&useragent=Chrome/%2F4.0"
user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'}
response  = requests.get(url, headers = user_agent).json()

print response