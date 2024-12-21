import datetime
import os

from data_manager import DataManager
from flight_data import find_cheapest_flight
from flight_search import FlightSearch
from notification_manager import NotificationManager
from constants import *


def new_price_body(city, iata_code, lowest_price, id):
    return {
        "price": {
            'city': city,
                'iataCode': iata_code,
                'lowestPrice': lowest_price,
                'id': id
                  }
    }


def update_iata_codes(sheet_data, flight_search, data_manager):
    global row
    for row in sheet_data[PRICES]:
        iata_code = row[IATA_CODE]
        id = row[ID]
        if len(iata_code) > 0:
            continue
        city = row[CITY]
        iata_code = flight_search.iato_code(city)
        body = new_price_body(city, iata_code, row[LOWEST_PRICE], id)
        data_manager.update_iata_code(body=body, id=id)


def get_all_flight_data(flight_search, from_days, destination_iata_code):
    all_flight_data = []
    origin_iata_code = 'LON'
    for from_date in from_days:
        to_date = from_date + datetime.timedelta(days=7)
        flight_data = flight_search.get_flights(origin_iata_code, destination_iata_code, from_date, to_date)
        all_flight_data.append(flight_data)
    return all_flight_data

def main():
    data_manager = DataManager(url=os.environ[SHEETY_API_URL])
    sheet_data = data_manager.fetch()
    flight_search = FlightSearch(url=FLIGHT_SEARCH_URL)

    update_iata_codes(sheet_data, flight_search, data_manager)

    from_days = [datetime.datetime.now() + datetime.timedelta(days=day) for day in range(1, DAYS_TO_SEARCH + 1)]
    notification_manager = NotificationManager()
    for row in sheet_data[PRICES]:
        destination_iata_code = row[IATA_CODE]
        all_flight_data = get_all_flight_data(flight_search, from_days, destination_iata_code)
        cheapest_flight = find_cheapest_flight(all_flight_data)
        if type(cheapest_flight.price) is not float or float(row[LOWEST_PRICE]) > cheapest_flight.price:
            continue
        message = f"Low price alert! Only £{cheapest_flight.price} to fly " + \
                  f"from {cheapest_flight.origin} to {cheapest_flight.destination}, " + \
                  f"on {cheapest_flight.departure_date} until {cheapest_flight.return_date}."
        notification_manager.send_sms(message)

if __name__ == '__main__':
    main()

