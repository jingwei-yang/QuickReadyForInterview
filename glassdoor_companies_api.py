import requests

url = "http://api.glassdoor.com/api/api.htm?t.p=29781&t.k=jQdxv7dRxPc&userip=0.0.0.0&useragent=Chrome&format=json&v=1&action=employers&q=Google"
response = requests.get(url)
response_dict = response.json()

return 