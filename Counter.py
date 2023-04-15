import json
from datetime import datetime


class Counter:
    _path: str
    _data: dict

    def __init__(self, path: str):
        self._path = path
        self._data = {
            "max_id": "0",
            "counter": dict()
        }

    def _read_data(self):
        with open(self._path, "r") as f:
            return json.load(f)

    def _save_data(self):
        with open(self._path, "w") as f:
            json.dump(self._data, f)

    def add_visit(self, id, date: datetime):
        self._data = self._read_data()

        date_str = date.strftime("%d/%m/%Y, %H:%M:%S")

        if id in self._data["counter"]:
            self._data["counter"][id].append(date_str)
        else:
            self._data["counter"][id] = []
            self._data["counter"][id].append(date_str)
        if int(id) > int(self._data["max_id"]):
            self._data["max_id"] = id

        self._save_data()

    def generate_new_id(self):
        return str(int(self._data["max_id"])+1)

    def _check_day(self, curr_date, year, month=None, day=None):
        if month and day:
            return (year == curr_date.year and
                    month == curr_date.month and
                    day == curr_date.day)
        if month:
            return (year == curr_date.year and
                    month == curr_date.month)
        return year == curr_date.year

    def get_stat_by_date(self, is_unique, year=None, month=None, day=None, **kwargs):
        result = {
            "visits": 0,
            "visitors": []
        }
        data = self._read_data()
        for user_id, dates in data["counter"].items():
            for date in dates:
                curr_date = datetime.strptime(date, "%d/%m/%Y, %H:%M:%S")
                if self._check_day(curr_date, year, month, day) or kwargs["all"]:
                    result["visits"] += 1
                    result["visitors"].append(f"{user_id} {date}")
                    if is_unique == "unique":
                        break
        return result

