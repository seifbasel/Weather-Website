from django.shortcuts import render
import datetime
import httpx
from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def index(request):
    api_key = OPENWEATHER_API_KEY
    current_weather_url = (
        "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    )

    if request.method == "POST":
        city1 = request.POST["city1"]
        city2 = request.POST.get("city2", None)

        weather_data1 = fetch_weather(
            city1, api_key, current_weather_url
        )

        if city2:
            weather_data2 = fetch_weather(
                city2, api_key, current_weather_url
            )
        else:
            weather_data2 = None

        context = {
            "weather_data1": weather_data1,
            "weather_data2": weather_data2,
        }

        return render(request, "weather_app/index.html", context)

    return render(request, "weather_app/index.html")


def fetch_weather(city, api_key, current_weather_url):
    try:
        with httpx.Client() as client:
            response = client.get(current_weather_url.format(city, api_key)).json()

            if "coord" in response and "weather" in response:
                weather_data = {
                    "city": city,
                    "temperature": int(round(response["main"]["temp"] - 273.15, 2)),
                    "feels_like": int(round(response["main"]["feels_like"] - 273.15, 2)),
                    "humidity": response["main"]["humidity"],
                    "pressure": response["main"]["pressure"],
                    "wind_speed": response["wind"]["speed"],
                    "description": response["weather"][0]["description"],
                    "icon": response["weather"][0]["icon"],
                    "last_updated": datetime.datetime.utcfromtimestamp(
                        response["dt"]
                    ).strftime("%Y-%m-%d %H:%M UTC"),
                }

                return weather_data
            else:
                print("Incomplete data in current weather API response.")
                return None, None

    except httpx.RequestError as e:
        print(f"HTTPX request failed: {e}")
        return None, None
