import requests
from requests.exceptions import ConnectTimeout, ReadTimeout
from typing import Optional, Iterable, Tuple


def location_search(city: str, api_key: str) -> Optional[int]:
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city}
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': api_key
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
    except (ConnectTimeout, ReadTimeout):
        return None
    code = response.status_code
    if code == 200:
        loc_dict = response.json()
        return int(loc_dict["suggestions"][0]["entities"][0]["destinationId"])
    else:
        return None


def properties_list(destination_id: int, api_key: str, ch_in: str, ch_out: str, sort: str = "PRICE",
                    page: int = 1, p_size: int = 25) -> Optional[Tuple[dict, Optional[int]]]:
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": destination_id, "pageNumber": str(page), "pageSize": p_size, "checkIn": ch_in,
                   "checkOut": ch_out, "adults1": "1", "sortOrder": sort}
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': api_key
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
    except (ConnectTimeout, ReadTimeout):
        return None
    code = response.status_code
    if code == 200:
        prop_dict = response.json()
        next_page = prop_dict["data"]["body"]["searchResults"]["pagination"].get("nextPageNumber")
        return prop_dict["data"]["body"]["searchResults"]["results"], next_page
    else:

        return None


def get_photo(hotel_id: int, api_key: str, photos: int) -> Iterable[str]:
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': api_key
    }
    res = []
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
    except (ConnectTimeout, ReadTimeout):
        return res
    photo_dict = response.json()
    for i_photo in range(photos):
        if len(photo_dict['hotelImages']) > i_photo:
            url = photo_dict['hotelImages'][i_photo]['baseUrl'].format(
                                                    size=photo_dict['hotelImages'][i_photo]['sizes'][0]['suffix'])
            res.append(url)
    return res
