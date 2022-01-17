import re
from typing import Optional, Tuple


def is_float(val: str) -> bool:
    pattern = re.compile(r'\d*\.?\d+')
    res = re.match(pattern, val)
    if res:
        return res.group() == val
    return False


def check_date(date_str: str) -> Optional[Tuple[str, str, str]]:
    pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    res = re.match(pattern, date_str)
    if res:
        if res.group() == date_str:
            year = int(res.group()[:4])
            month = int(res.group()[5:7])
            day = int(res.group()[8:])
            big_month = (1, 3, 5, 7, 8, 10, 12)

            if year < 1 or year > 9999:
                return None

            if year % 4 != 0:
                leap_year = False
            elif year % 100 != 0:
                leap_year = True
            elif year % 400 == 0:
                leap_year = True
            else:
                leap_year = False

            if month < 0 or month > 12:
                return None
            if day < 0:
                return None

            if month == 2:
                if leap_year:
                    if day > 29:
                        return None
                else:
                    if day > 28:
                        return None
            if (month not in big_month) and (day < 0 or day > 30):
                return None
            if (month in big_month) and (day < 0 or day > 31):
                return None

            return res.group()[:4], res.group()[5:7], res.group()[8:]
    return None
