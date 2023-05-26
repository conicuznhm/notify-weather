import os
import json
import time 
from helper import get_weather_data, send_line_notify
from dotenv import load_dotenv

def read_config(json_path: str) -> dict:
    """
    Read config file (JSON) and return a dictionary with the config values
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Config file not found ar {json_path}")

    with open(json_path,"r") as json_file:
        json_config: dict = json.load(json_file)

    return json_config
    # TODO: implement this function
    # raise NotImplementedError()


if __name__ == "__main__":
    # read config file (JSON) and call load_dotenv function
    json_path = "config.json"
    json_config: dict = read_config(json_path)
    load_dotenv() #to load data from .env

    #get config values
    time_sleep = json_config.get("time_sleep", 60*60)
    # TODO: add exit case if there is any error

    # line_notify_token = json_config.get("line_notify_token","")
    # weather_access_key = json_config.get("weather_access_key","")

    # get line and weather access key from dotenv
    line_notify_token = os.environ.get("line_notify_token","")
    weather_access_key = os.environ.get("weather_access_key","")

    # get lat and lon from config.json
    lat = json_config.get("lat","13.7450255")
    lon = json_config.get("lon","100.5209932")

    if weather_access_key=="":
        raise ValueError("Weather access key is empty")
    if line_notify_token=="":
        raise ValueError("line token is empty")

    while True:
        # raise NotImplementedError()
        # TODO: get weather data from OpenWeatherMap API
        print('getting weather data')
        request_data = get_weather_data(weather_access_key, lat, lon)

        # if request_data.status_code == 200:
        #     weather_data:dict = request_data.json()
        #     weather_condition = weather_data['weather'][0]['main']

        if request_data.status_code != 200:
            time.sleep(int(time_sleep))
            continue

        # parse json to dict
        weather_data:dict = request_data.json() 

        # get data to variable
        weather_condition = weather_data['weather'][0]['main']
        temperature = weather_data["main"]["temp"]
        location_name = weather_data["name"]

        print('check condition')
        
        if weather_condition != "":
            print('constructing message')
            message = f'hello ope\nAt location: {location_name}\nThe current weather is: {weather_condition}\nThe current temperature is: {temperature}'
            print(f"send line notify: {message}")
            send_line_notify(access_token=line_notify_token,message=message)

        # if weather is Clouds set message to notify location, weather condition, temperature
        # if weather_condition == 'Clouds':
        #     print('constructing message')
        #     message = f'hello ope\nAt location: {location_name}\nthe current weather is: {weather_condition}\nthe temperature is: {temperature}'
        #     print(f"send line notify: {message}")
        #     send_line_notify(access_token=line_notify_token,message=message)

        # if weather_condition != 'Clouds':
        #     pass
        # weather_data:dict = request_data.json()
        # weather_condition = weather_data['weather'][0]['main']

        # add time sleep ex. 1 hour
        time.sleep(time_sleep) #unit: second

