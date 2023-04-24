from server import app, counter
from datetime import datetime
import json

data_file_path = "data.json"


class TestSuccessResponse:

    def setup(self):
        app.testing = True
        self.client = app.test_client()

    def test_on_home(self):
        response = self.client.get("/")
        assert response.status_code == 200

    def test_on_api_unique_all(self):
        response = self.client.get("/api/counter/unique/all")
        assert response.status_code == 200

    def test_on_api_not_unique_all(self):
        response = self.client.get("/api/counter/not_unique/all")
        assert response.status_code == 200

    def test_on_api_not_unique_year(self):
        response = self.client.get("/api/counter/not_unique/2023")
        assert response.status_code == 200

    def tes_on_api_not_unique_year_month(self):
        response = self.client.get("/api/counter/not_unique/2023/04")
        assert response.status_code == 200

    def test_on_api_not_unique_year_month_day(self):
        response = self.client.get("/api/counter/not_unique/2023/04/22")
        assert response.status_code == 200

    def test_on_api_unique_year(self):
        response = self.client.get("/api/counter/unique/2023")
        assert response.status_code == 200

    def test_on_api_unique_year_month(self):
        response = self.client.get("/api/counter/unique/2023/04")
        assert response.status_code == 200

    def test_on_api_unique_year_month_day(self):
        response = self.client.get("/api/counter/unique/2023/04/22")
        assert response.status_code == 200


class TestRequestStatistics:
    def setup(self):
        app.testing = True
        self.clients_count = 5
        self.clients = []
        for i in range(self.clients_count):
            self.clients.append(app.test_client())
        counter.clear_data()

    def test_one_request(self):
        self.clients[0].get("/")
        with open(data_file_path, "r") as f:
            data = json.load(f)
            assert data == {'counter': {'1': [{'date': datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                                               'ip': '127.0.0.1'}]}, 'max_id': '1'}

    def test_many_clients_one_requests(self):
        for i in range(self.clients_count):
            self.clients[i].get("/")

        with open(data_file_path, "r") as f:
            curr_data = json.load(f)

        assert curr_data["max_id"] == str(self.clients_count)

        for _, data in curr_data["counter"].items():
            assert data[0]["date"] == datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            assert data[0]["ip"] == "127.0.0.1"

    def test_many_requests_one_client(self):
        for i in range(self.clients_count):
            self.clients[0].get("/")

        with open(data_file_path, "r") as f:
            curr_data = json.load(f)

        assert curr_data["max_id"] == "1"

        for _, datas in curr_data["counter"].items():
            for data in datas:
                assert data["date"] == datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                assert data["ip"] == "127.0.0.1"
