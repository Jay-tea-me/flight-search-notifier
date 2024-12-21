import pprint
import requests

class DataManager:
    def __init__(self, url):
        self.url = url

    def fetch(self):
        print(self.url)
        response = requests.get(url=self.url)
        response.raise_for_status()
        pprint.pp(response.json())
        return response.json()

    def update_iata_code(self, body, id):
        response = requests.put(url=f'{self.url}/{id}',
                     json=body)
        print("update_iata_code")
        print("-"*10)
        print(response.status_code)
        print(response.text)
        print("-" * 10)



