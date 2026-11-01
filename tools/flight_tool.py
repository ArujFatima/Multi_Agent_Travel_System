import os
import requests
from dotenv import load_dotenv  

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv("AviationStack_API_Key")

def search_flights(query):
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": API_KEY,
        "limit": 5,  # Limit the number of results
    }
    response = requests.get(url, params=params)
    data = response.json()  
    
    flights = []
    
    if "data" in data:
        for flight in data["data"][:5]:
            airline = flight.get("airline", {}).get("name", "Unknown Airline")
            departure_airport = flight.get("departure", {}).get("airport", "Unknown Departure Airport")
            arrival_airport = flight.get("arrival", {}).get("airport", "Unknown Arrival Airport")
            flight_number = flight.get("flight", {}).get("number", "Unknown Flight Number")
            
            flights.append(
                f"""
                Airline: {airline}
                Flight Number: {flight_number}
                Departure Airport: {departure_airport}
                Arrival Airport: {arrival_airport}
                                
                """)
    return "\n".join(flights)