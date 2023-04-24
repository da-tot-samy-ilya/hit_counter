import json
from datetime import datetime


class HitCounter:
    def __init__(self, path: str):
        self._path = path
        self.default_value = {
            "max_id": "0",
            "counter": dict()
        }
        self._data = self.default_value
        self._save_data()

    def clear_data(self):
        with open(self._path, "w") as f:
            json.dump(self.default_value, f)
        self._data = self.default_value

    def _read_data(self):
        with open(self._path, "r") as f:
            return json.load(f)

    def _save_data(self):
        with open(self._path, "w") as f:
            json.dump(self._data, f)

    def add_visit(self, user_id, date: datetime, visitor_ip):
        self._data = self._read_data()

        date_str = date.strftime("%d/%m/%Y, %H:%M:%S")

        count_data = {"date": date_str, "ip": visitor_ip}

        if user_id in self._data["counter"]:
            self._data["counter"][user_id].append(count_data)
        else:
            self._data["counter"][user_id] = []
            self._data["counter"][user_id].append(count_data)
        if int(user_id) > int(self._data["max_id"]):
            self._data["max_id"] = user_id

        self._save_data()

    def generate_new_id(self):
        return str(int(self._data["max_id"])+1)

    @staticmethod
    def _check_day(curr_date, year, month=None, day=None):
        if month and day:
            return all([year == curr_date.year, month == curr_date.month, day == curr_date.day])
        if month:
            return all([year == curr_date.year, month == curr_date.month])
        return year == curr_date.year

    def get_stat_by_date(self, is_unique, year=None, month=None, day=None, all_stat=False):
        result = {
            "visits": 0,
            "visitors": []
        }
        data = self._read_data()
        for user_id, count_datas in data["counter"].items():
            for count_data in count_datas:
                curr_date = datetime.strptime(count_data["date"], "%d/%m/%Y, %H:%M:%S")
                if self._check_day(curr_date, year, month, day) or all_stat:
                    result["visits"] += 1
                    result["visitors"].append({"id": user_id,
                                               "date": count_data["date"],
                                               "IP": count_data["ip"]})
                    if is_unique == "unique":
                        break
        return result
