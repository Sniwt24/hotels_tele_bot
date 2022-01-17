from typing import Dict, Optional
import finder_api
import re


def low_price(city: str, api_key: str, count: int, photos: int, ch_in: str, ch_out: str) -> Optional[Dict]:
    dest_id = finder_api.location_search(city=city, api_key=api_key)
    if dest_id is not None:
        hotels_dict, next_page = finder_api.properties_list(destination_id=dest_id, api_key=api_key, ch_in=ch_in,
                                                            ch_out=ch_out, p_size=count)
    else:
        hotels_dict = None
    res = dict()
    num = 1
    if hotels_dict is not None and dest_id is not None:
        for hotel in hotels_dict:
            addr = ''
            for item in hotel['address']:
                if isinstance(hotel['address'][item], str):
                    addr += ' {value}; '.format(value=hotel['address'][item])
            res[num] = dict(id=hotel['id'], name=hotel['name'], address=addr, dist=hotel['landmarks'][0]['distance'],
                            price=hotel['ratePlan']['price']['exactCurrent'],
                            photos_url=finder_api.get_photo(hotel_id=hotel['id'], api_key=api_key, photos=photos))
            num += 1
        return res
    else:
        return None


def high_price(city: str, api_key: str, count: int, photos: int, ch_in: str, ch_out: str) -> Optional[Dict]:
    dest_id = finder_api.location_search(city=city, api_key=api_key)
    if dest_id is not None:
        hotels_dict, next_page = finder_api.properties_list(destination_id=dest_id, api_key=api_key, ch_in=ch_in,
                                                            ch_out=ch_out, sort='PRICE_HIGHEST_FIRST', p_size=count)
    else:
        hotels_dict = None
    res = dict()
    num = 1
    if hotels_dict is not None and dest_id is not None:
        for hotel in hotels_dict:
            addr = ''
            for item in hotel['address']:
                if isinstance(hotel['address'][item], str):
                    addr += ' {value}; '.format(value=hotel['address'][item])
            res[num] = dict(id=hotel['id'], name=hotel['name'], address=addr, dist=hotel['landmarks'][0]['distance'],
                            price=hotel['ratePlan']['price']['exactCurrent'],
                            photos_url=finder_api.get_photo(hotel_id=hotel['id'], api_key=api_key, photos=photos))
            num += 1
        return res
    else:
        return None


def best_deal(city: str, api_key: str, count: int, photos: int, ch_in: str, ch_out: str, min_price: float,
              max_price: float, min_dist: float, max_dist: float):
    dest_id = finder_api.location_search(city=city, api_key=api_key)
    if dest_id is not None:
        hotels_dict, next_page = finder_api.properties_list(destination_id=dest_id, api_key=api_key, ch_in=ch_in,
                                                            ch_out=ch_out, sort='DISTANCE_FROM_LANDMARK',)
    else:
        hotels_dict = None
    res = dict()
    num = 1
    if hotels_dict is not None and dest_id is not None:
        while num <= count:
            for hotel in hotels_dict:
                pattern = re.compile(r'\d*\.?\d+')
                dist_from_center = float(re.match(pattern, hotel['landmarks'][0]['distance']).group())
                if ((dist_from_center >= min_dist) and (dist_from_center <= max_dist)) and \
                        ((hotel['ratePlan']['price']['exactCurrent'] >= min_price) and
                         (hotel['ratePlan']['price']['exactCurrent'] <= max_price)):
                    addr = ''
                    for item in hotel['address']:
                        if isinstance(hotel['address'][item], str):
                            addr += ' {value}; '.format(value=hotel['address'][item])
                    res[num] = dict(id=hotel['id'], name=hotel['name'], address=addr, dist=hotel['landmarks'][0]['distance'],
                                    price=hotel['ratePlan']['price']['exactCurrent'],
                                    photos_url=finder_api.get_photo(hotel_id=hotel['id'], api_key=api_key, photos=photos))
                    num += 1
                if (dist_from_center > max_dist) or (num > count):
                    return res
            if next_page is not None:
                hotels_dict, next_page = finder_api.properties_list(destination_id=dest_id, api_key=api_key,
                                                                    ch_in=ch_in,
                                                                    ch_out=ch_out, sort='DISTANCE_FROM_LANDMARK',
                                                                    page=next_page)
                if hotels_dict is None:
                    return res
        return res
    else:
        return None


def history():
    pass
