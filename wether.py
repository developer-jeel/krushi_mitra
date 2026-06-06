import requests

api_key = "cda9b54ada6d720cbc78948d2e86b4d8"

user_input = input("Enter the city name: ")

wather_url = f"http://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={api_key}"

response = requests.get(wather_url)
print(response.json())