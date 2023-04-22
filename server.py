from flask import Flask, render_template, request, make_response
from HitCounter import HitCounter
from datetime import datetime, timedelta

app = Flask(__name__)
counter = HitCounter("data.json")

COOKIES_LIFE_LIMIT = 365 * 10


def get_stat(is_unique: str, year: int, month: int, day: int):
    if month and day:
        return counter.get_stat_by_date(is_unique, year, month, day)
    if month:
        return counter.get_stat_by_date(is_unique, year, month)
    return counter.get_stat_by_date(is_unique, year)


@app.route("/")
def index():
    visitor_cookie = request.cookies.get('visitor_id')
    visitor_ip = request.remote_addr
    id_to_response = visitor_cookie
    if visitor_cookie:
        response_content = "Hello again, your id: " + id_to_response
    else:
        id_to_response = counter.generate_new_id()
        response_content = "You are in first time here, your id: " + id_to_response

    expiration_date = datetime.now() + timedelta(days=COOKIES_LIFE_LIMIT)
    expiration_date_string = expiration_date.strftime('%a, %d %b %Y %H:%M:%S GMT')

    counter.add_visit(id_to_response, datetime.now(), visitor_ip)
    response = make_response(render_template("index.html", content=response_content))
    response.set_cookie('visitor_id', id_to_response, expires=expiration_date_string)
    return response


@app.route('/api/counter/not_unique/<string:all>')
def counter_not_unique_all(all):
    return counter.get_stat_by_date("not_unique", all_stat=True)


@app.route('/api/counter/unique/<string:all>')
def counter_unique_all(all):
    return counter.get_stat_by_date("unique", all_stat=True)


@app.route('/api/counter/not_unique/<int:year>/<int:month>/<int:day>')
@app.route('/api/counter/not_unique/<int:year>/<int:month>')
@app.route('/api/counter/not_unique/<int:year>')
def counter_not_unique(year=0, month=0, day=0):
    return get_stat("not_unique", year, month, day)


@app.route('/api/counter/unique/<int:year>/<int:month>/<int:day>')
@app.route('/api/counter/unique/<int:year>/<int:month>')
@app.route('/api/counter/unique/<int:year>')
def counter_unique(year, month=0, day=0):
    return get_stat("unique", year, month, day)


if __name__ == '__main__':
    app.run(debug=True)
