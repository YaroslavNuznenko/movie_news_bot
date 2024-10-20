import requests

BASE_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "TieTimeBot/1.0"


def nominatim_search_geolocation(q):
    params = {"q": q, "format": "json", "limit": 1}
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(BASE_URL, params=params, headers=headers)

    if response.status_code != 200:
        return

    data = response.json()

    if len(data) == 0:
        return

    location = data[0]
    return {
        "lat": location["lat"],
        "lon": location["lon"],
    }
