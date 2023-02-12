

import requests
API_KEY = "590694425933fdbfe10eb5695c3a51bc"
ip_request = requests.get('https://get.geojs.io/v1/ip.json')
my_ip = ip_request.json()['ip']
geo_request = requests.get(f'https://get.geojs.io/v1/ip/geo/{my_ip}.json')
geo_data = geo_request.json()
latitude =  geo_data["latitude"]
longitude = geo_data["longitude"]
print(latitude, longitude)
request_url  = "https://api.openweathermap.org/data/3.0/onecall?lat="+latitude+"&lon="+longitude+"&appid=590694425933fdbfe10eb5695c3a51bc"
response = requests.get(request_url).json()
print(response)
