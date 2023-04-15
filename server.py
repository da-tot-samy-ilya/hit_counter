from flask import Flask, render_template, request, make_response
from Counter import Counter
from datetime import datetime, timedelta

app = Flask(__name__)
c = Counter("data.json")

COOKIES_LIFE_LIMIT = 365 * 10


@app.route("/")
def index():
    visitor_cookie = request.cookies.get('visitor_id')
    id_to_response = visitor_cookie
    if visitor_cookie:
        response_content = "Hello again, your id: " + id_to_response
    else:
        id_to_response = c.generate_new_id()
        response_content = "You are in first time here, your id: " + id_to_response

    expiration_date = datetime.now() + timedelta(days=COOKIES_LIFE_LIMIT)
    expiration_date_string = expiration_date.strftime('%a, %d %b %Y %H:%M:%S GMT')

    c.add_visit(id_to_response, datetime.now())
    response = make_response(render_template("index.html", content=response_content))
    response.set_cookie('visitor_id', id_to_response, expires=expiration_date_string)
    return response


@app.route('/api/counter/not_unique/<string:all>')
def counter_not_unique_all(all):
    return c.get_stat_by_date("not_unique", all=True)


@app.route('/api/counter/unique/<string:all>')
def counter_unique_all(all):
    return c.get_stat_by_date("unique", all=True)


@app.route('/api/counter/not_unique/<int:year>/<int:month>/<int:day>')
@app.route('/api/counter/not_unique/<int:year>/<int:month>')
@app.route('/api/counter/not_unique/<int:year>')
def counter_not_unique(year=0, month=0, day=0):
    if month and day:
        return c.get_stat_by_date("not_unique", year, month, day)
    if month:
        return c.get_stat_by_date("not_unique", year, month)
    return c.get_stat_by_date("not_unique", year)


@app.route('/api/counter/unique/<int:year>/<int:month>/<int:day>')
@app.route('/api/counter/unique/<int:year>/<int:month>')
@app.route('/api/counter/unique/<int:year>')
def counter_unique(year, month=0, day=0):
    if month and day:
        return c.get_stat_by_date("unique", year, month, day)
    if month:
        return c.get_stat_by_date("unique", year, month)
    return c.get_stat_by_date("unique", year)


if __name__ == '__main__':
    app.run(debug=True)
