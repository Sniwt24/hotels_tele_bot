from typing import Optional
from datetime import datetime


class Headers:
    def __init__(self) -> None:
        self.user_id: Optional[int] = None
        self.command_id: Optional[int] = None
        self.command_date: Optional[datetime] = None
        self.command: Optional[str] = None
        self.city: Optional[str] = None
        self.hotels_count: Optional[int] = None
        self.min_price: Optional[float] = None
        self.max_price: Optional[float] = None
        self.min_dist: Optional[float] = None
        self.max_dist: Optional[float] = None
        self.need_photo: Optional[bool] = None
        self.photo_count: Optional[int] = None
        self.ch_in: Optional[str] = None
        self.ch_out: Optional[str] = None

    def __str__(self) -> str:
        return 'City: {}; \nHotels count: {};\nMin price: {};\nMax price: {};\nMin distance from city center: {}' \
               '\nMax distance from city center: {};\nNeed photo: {}'.format(
                self.city, self.hotels_count, self.min_price, self.max_price,
                self.min_dist, self.max_dist, self.need_photo
                )
