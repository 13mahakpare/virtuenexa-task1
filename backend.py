import requests
import os

API_KEY = "2fc97d34f9b284803ee1c2d25ec32903"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
HISTORY_FILE = "history.txt"

def get_weather(city):
    """Fetch live weather data for the given city."""
    try:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            weather_info = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
            }
            return weather_info
        else:
            return {"error": data["message"]}
    except Exception as e:
        return {"error": str(e)}

def save_history(city):
    """Save only city names in history.txt"""
    try:
        cities = get_saved_cities()
        if city not in cities:  # Avoid duplicate entries
            with open(HISTORY_FILE, "a") as file:
                file.write(f"{city}\n")
    except Exception as e:
        print(f"Error saving history: {e}")

def get_saved_cities():
    """Retrieve saved city names only."""
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as file:
            pass  # Create empty file if not found

    try:
        with open(HISTORY_FILE, "r") as file:
            cities = file.readlines()
        return [city.strip() for city in cities if city.strip()]  # Remove empty lines
    except Exception as e:
        print(f"Error reading history file: {e}")
        return []