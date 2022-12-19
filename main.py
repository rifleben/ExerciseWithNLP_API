import requests
from datetime import datetime
import os

BEAR_TOKEN = os.environ.get("BEAR_TOKEN")
SHEETY_API = os.environ.get("SHEETY_API_WK")
APP_ID = os.environ.get("NUT_APP_ID")
API_KEY = os.environ.get("NUT_API_KEY")
API_SITE = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_input = input("Enter exercises in natural text: ")

params = {"query": exercise_input,
          "gender": "male",
          "weight_kg": 65,
          "height_cm": 170.18,
          "age": 25
          }

response = requests.post(url=API_SITE, json=params, headers={"x-app-id": APP_ID, "x-app-key": API_KEY})
result = response.json()


today = datetime.now().strftime("%d/%m/%Y")
now = datetime.now().strftime("%X")

for exer in result["exercises"]:
    sheet_input = {
        "workout": {
            "date": today,
            "time": now,
            "exercise": exer["name"].title(),
            "duration": exer["duration_min"],
            "calories": exer["nf_calories"]
        }
    }

    sheet_response = requests.post(url=SHEETY_API, json=sheet_input, headers={"Authorization": f"Bearer {BEAR_TOKEN}"})
    print(sheet_response.text)
    print("Successfully added to Google Sheet")
