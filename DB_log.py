from datetime import datetime
from peewee import PeeweeException
from loader import Req
from typing import Iterable, Optional


def write_req(req_id: int, in_user_id: int, req_time: datetime, in_command: str, in_city: str, in_hotels: str) -> bool:
    try:
        Req.create(
                    request_id=req_id, user_id=in_user_id, request_time=req_time, command=in_command,
                    city=in_city, hotels=in_hotels
        )
        return True

    except PeeweeException:
        return False


def get_history(in_user_id: int) -> Optional[Iterable]:
    res = dict()
    try:
        records = Req.select().where(Req.user_id == in_user_id).order_by(Req.request_time)
        for record in records:
            date = datetime.strftime(record.request_time, '%d-%m-%Y %H:%M:%S')  # record.request_time
            command = record.command
            city = record.city
            hotels = record.hotels.split(';')[:-1]
            res[date] = [command, city, hotels]
        return res
    except PeeweeException:
        return None
