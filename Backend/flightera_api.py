import requests

url = "https://flightera-flight-data.p.rapidapi.com/flight/info"

querystring = {"flnr": "LHRDFW"}

headers = {
    "x-rapidapi-key": "88f9d9b041msh3846bee977479c3p1cab7bjsn44f51f32e68b",
    "x-rapidapi-host": "flightera-flight-data.p.rapidapi.com",
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
