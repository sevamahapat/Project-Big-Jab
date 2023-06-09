# file : vaccine.py
# Authors : dsanmukh, dishantv, jgala, rkacheri, smahapat
# Purpose : Fetches vaccination slot location data from getvax api

# imported by: covid_main.py

import requests
from datetime import datetime
from datetime import timedelta

def get_vaccination_slots(state):
    url = "https://getmyvax.org/api/edge/locations?state="
    response = requests.get(url+state)

    slots = response.json()
    locations = []

    for data in slots["data"]:
        if data["availability"].get("available","NO") == "YES":
            continue
        updated_date = datetime.strptime(data["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ")

        # if updated date is today or yesterday (because of 12am issues), append the location
        if updated_date.date() == datetime.today().date() or updated_date.date() == (datetime.today().date() - timedelta(days=1)) :
            address = str(data['address_lines'][0]).title()
            locations.append(address + ", " + data["city"])
    return locations

if __name__ == '__main__':
    locations = get_vaccination_slots('NY')
    for loc in locations:
        print(loc)