import requests
import json
#varables= url, prams, readings, hottest_first, s ,
def get_wbgt_data():#data of weather import
    #Fetches the latest WBGT readings from data.gov.sg.
    url = "https://api-open.data.gov.sg/v2/real-time/api/weather"
    params = {"api": "wbgt"}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status() # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
#sorter
wbgt_data = get_wbgt_data()
readings = wbgt_data["data"]["records"][0]["item"]["readings"]

hottest_first = sorted(readings, key=lambda s: float(s["wbgt"]), reverse=True)

print(f"temperature    heatstress    station")#heading
for s in hottest_first:#sorted data
    print(f'{s["wbgt"]:>5}  |  {s["heatStress"]:<9}  |  {s["station"]["name"]}')

