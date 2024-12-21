class FlightData:
    def __init__(self,
                 price,
                 origin,
                 destination,
                 departure_date,
                 return_date,
                 ):
        self.price = price
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.return_date = return_date



def find_cheapest_flight(all_flights_data):
    if all_flights_data is None or not all_flights_data:
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")
    flights_data = []
    for f in all_flights_data:
        for offer in f["data"]:
            flights_data.append(offer)
    min_flight_price_index = -1
    lowest_price = float("inf")
    for f_ind in range(len(flights_data)):
        flight_price = float(flights_data[f_ind]["price"]["grandTotal"])
        if flight_price < lowest_price:
            min_flight_price_index = f_ind
            lowest_price = flight_price

    if min_flight_price_index == -1:
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    cheapest_flight = flights_data[min_flight_price_index]
    return FlightData(
        price=float(cheapest_flight["price"]["grandTotal"]),
        origin=cheapest_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"],
        destination=cheapest_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"],
        departure_date=cheapest_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0],
        return_date=cheapest_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
    )


