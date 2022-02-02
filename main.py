import requests
from datetime import datetime
from decouple import config

user_input = input("Tell me which exercise you did: ")
today = datetime.today()
today_str = today.strftime("%d/%m/%Y")
time = datetime.now()
time_str = time.strftime("%H:%M:%S")

# Nutritionix API
nu_api_id = config('NU_API_ID')
nu_api_key = config('NU_API_KEY')
nu_api_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
nu_api_header = {
    "x-app-id": nu_api_id,
    "x-app-key": nu_api_key,
    "Content-Type": "application/json"
}
nu_api_body = {
    "query": user_input
}
exercise_response = requests.post(nu_api_endpoint, headers=nu_api_header, json=nu_api_body)
exercise_data = exercise_response.json()['exercises']

# Sheety API
# Query key must be the singular of spreadsheet name
sh_api_endpoint = config('SH_API_ENDPOINT')
sh_api_header = {
    "Content-Type": "application/json"
}
for exercise in exercise_data:
    sh_api_body = {
        "workout": {
            "date": today_str,
            "time": time_str,
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories']
        }
    }
    sheet_response = requests.post(sh_api_endpoint, headers=sh_api_header, json=sh_api_body)
    sheet_response.raise_for_status()
