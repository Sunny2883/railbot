"""additional tools used by langchain agent is here
these tools use api and call them to retrieve information"""

import os
from datetime import date
import dotenv
import requests
from langchain.tools import StructuredTool

dotenv.load_dotenv()
rapidapi_api_key = os.getenv("X-RapidAPI-Key")

today = date.today()
formatted_date = today.strftime("%Y-%m-%d")


# api tools
def get_station(query: str):
    """Returns a list of stations that match or have similar type code to the queried station"""
    url = "https://irctc1.p.rapidapi.com/api/v1/searchStation"

    querystring = {"query": query}

    headers = {
        "X-RapidAPI-Key": rapidapi_api_key,
        "X-RapidAPI-Host": "irctc1.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring, timeout=20)

    response = response.json()

    if response["status"] is True and response["message"] == "Success":
        return response["data"]
    return {"message": "no data found"}


def get_train(query: int):
    """Returns train details provivded train number"""
    url = "https://irctc1.p.rapidapi.com/api/v1/searchTrain"

    querystring = {"query": query}

    headers = {
        "X-RapidAPI-Key": rapidapi_api_key,
        "X-RapidAPI-Host": "irctc1.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring, timeout=20)

    response = response.json()

    if response["status"] is True and response["message"] == "Success":
        return response["data"]
    return {"message": "no data found"}


def get_train_between_stations(
    src: str, dst: str, date_of_journey: str = formatted_date
):
    """Returns list of trains running between two stations on a given date"""
    url = "https://irctc1.p.rapidapi.com/api/v3/trainBetweenStations"

    querystring = {
        "fromStationCode": src,
        "toStationCode": dst,
        "dateOfJourney": date_of_journey,
    }

    headers = {
        "X-RapidAPI-Key": rapidapi_api_key,
        "X-RapidAPI-Host": "irctc1.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring, timeout=20)

    response = response.json()
    print(response["status"], response["message"])
    if response["status"] is True and response["message"] == "Success":
        return response["data"]
    return {"message": "no data found"}


def get_train_live_status(train_no: str, day: str = "1"):
    """Returns trains live status given train number and day no of the journey"""
    url = "https://irctc1.p.rapidapi.com/api/v1/liveTrainStatus"

    querystring = {"trainNo": train_no, "startDay": day}

    headers = {
        "X-RapidAPI-Key": rapidapi_api_key,
        "X-RapidAPI-Host": "irctc1.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring, timeout=20)

    response = response.json()

    if response["status"] is True and response["message"] == "Success":
        return response["data"]
    return {"message": "no data found"}


#
get_station_info = StructuredTool.from_function(
    func=get_station,
    name="get_station_info",
    description="Returns a list of stations that match or have similar type code to the queried station. takes one argument: station code in string format",
)

get_train_info = StructuredTool.from_function(
    func=get_train,
    name="get_train_info",
    description="Returns train details for provivded train number. takes one argument: train number in integer or number format",
)

get_train_between_stations_info = StructuredTool.from_function(
    func=get_train_between_stations,
    name="get_train_between_stations_info",
    description="Returns list of trains running between two stations on a given date. takes three arguments: source station in string format, destination station in string format, date of journey in string format(YYYY-MM-DD). if date is not specified, don't pass date argument",
)

get_train_live_status_info = StructuredTool.from_function(
    func=get_train_live_status,
    name="get_train_live_status_info",
    description="Returns trains live status for given train number and day no of the journey. takes two arguments: train number in string format and day number in string format. if day not provided then leave it or pass '1'.",
)

extra_tools = [
    get_train_info,
    get_station_info,
    get_train_between_stations_info,
    get_train_live_status_info,
]
