import os
import requests
from constants import  *

class FlightSearch:
    def __init__(self, url):
        self._api_key = os.environ[AMADEUS_API_KEY]
        self._api_secret = os.environ[AMADEUS_SECRET]
        self.url = url
        token = self._get_token()
        self.headers = {
            'authorization': f"Bearer {token}",
            'accept': 'application/json'
        }

    def _get_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=FLIGHT_SEARCH_TOKEN_ENDPOINT, headers=header, data=body)
        print(response.json())
        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']

    def iato_code(self, location):
        param_config = {
            'keyword': location,
        }
        end_point = "/reference-data/locations/cities"
        response_json = self.get(end_point, param_config, "iato_code")
        return response_json['data'][0][IATA_CODE]

    def get_flights(self, origin_city_code, destination_city_code, from_date, to_date):
        param_config = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_date.strftime("%Y-%m-%d"),
            "returnDate": to_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": 5
        }
        end_point = "/shopping/flight-offers"
        response_json = self.get(end_point, param_config, calling_func_name = "get_flights")
        return response_json

    def get(self, end_point, params, calling_func_name):
        print(calling_func_name)
        print("-" * 10)
        url = self.url + end_point
        response = requests.get(url=url, headers=self.headers, params=params)
        response.raise_for_status()
        json_response = response.json()
        print(json_response)
        print("-" * 10)
        return  json_response

