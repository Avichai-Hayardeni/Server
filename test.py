import requests

url = "http://localhost:8000/send_message"
data = {"date": "2022-04-01 03:01:00", "author_id": 0, "addressee_id": 2, "type": 0, "data": "hallo"}
x = requests.post(url=url , data = data)
print(x.text)
