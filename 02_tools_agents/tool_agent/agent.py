from google.adk.agents.llm_agent import Agent
# from google.adk.tools import google_search
import requests
def get_coordinates(city:str):
    """
    Get the latitude and longitude of city.

    Args:
    city :Name of city.

    Returns:
    A dictionary containing latitude,longitude and city name.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name":city,
        "count":1,
        "language":"en",
        "format":"json",
    }
    resopnse = requests.get(url,params=params,timeout=10)
    resopnse.raise_for_status()

    data = resopnse.json()
    if not data.get('results'):
        return{
            "status":"error",
            "message":f"Could not find coordinates for {city}."
        }
    location = data['results'][0]

    return{
        "status":"success",
        "city":location["name"],
        "country":location.get("country"),
        "latitude":location["latitude"],
        "longitude":location["longitude"],
    }


def get_weather(latitude:float,longitude:float,unit:str='celcius')->dict:
    """
    Get current weather for a location.

    Args: 
          latitude: Latitude of location.
          longitude:Longitude of the location.
          unit: Temperature unit, either celsius or fahrenheite.

          Returns: 
                Current weather information.

    """
    url = 'https://api.open-meteo.com/v1/forecast'

    temperature_unit=(
        "fahrenheite"
        if unit.lower() == "fahrenheit"
        else "celsius"
    )

    params = {
        "latitude":latitude,
        "longitude":longitude,
        "current":",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
        ]),
        "temperature_unit":temperature_unit,
        "wind_speed_unit":"kmh",
        "timezone":"auto",
    }
    response = requests.get(url,params=params,timeout=10)
    response.raise_for_status()

    data = response.json()
    return {
        "status":"success",
        "location":{
            "latitude":latitude,
            "longitude":longitude
        },
        "current":data["current"],
        "unit":data["current_units"],
    } 


root_agent = Agent(
    model='gemini-3.5-flash',
    name='weather_agent',
    description='An assistant that provides current weather information.',
    instruction="""
You are a helpful weather assistant.

    When the user asks about the current weather:

    1. Identify the city from the user's question.
    2. Use get_coordinates to find the city's latitude and longitude.
    3. Use get_weather with those coordinates.
    4. Explain the current weather clearly.
    5. Do not invent weather information.
    6. If the user specifies Fahrenheit, use Fahrenheit.
       Otherwise use Celsius.

    For questions unrelated to weather, answer normally.
     """,
    tools=[get_weather],
)
