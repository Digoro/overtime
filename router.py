from datetime import datetime, timedelta
from flask import Response
from flask import Flask
from flask import json
from flask import render_template
from flask import request
from flask import send_from_directory
import computer

app = Flask(__name__, static_folder='static')


@app.route('/<path:path>')
def send_js(path):
    return send_from_directory(app.static_folder, path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/overtimes')
def overtimes():
    return render_template('gsdb.html', page_key='overtimes')


@app.route('/comments')
def comments():
    return render_template('gsdb.html', page_key='comments')


@app.route('/rest/api/1/overtimes')
def rest_api_1_overtimes():
    start, end = get_init_date()
    users = computer.Computer().getOvetimes(start, end)
    return Response(response=json.dumps(users), status=200, mimetype="application/json")


@app.route('/rest/api/1/comments')
def rest_api_1_comments():
    start, end = get_init_date()
    users = computer.Computer().getComments(start, end)
    return Response(response=json.dumps(users), status=200, mimetype="application/json")


@app.route('/rest/api/1/overtimes/search', methods=['POST'])
def rest_api_1_overtimes_search():
    start, end = get_date()
    users = computer.Computer().getOvetimes(start, end)
    return Response(response=json.dumps(users), status=200, mimetype="application/json")


@app.route('/rest/api/1/comments/search', methods=['POST'])
def rest_api_1_comments_search():
    start, end = get_date()
    users = computer.Computer().getComments(start, end)
    return Response(response=json.dumps(users), status=200, mimetype="application/json")


@app.route('/test')
def rest_api_1_image():
    return Response(response=open('wurihan.png', 'wb'), status=200)



def get_init_date():
    end = datetime.today()
    start = end - timedelta(1)
    return start, end


def get_date():
    start = datetime(day('s_y'), day('s_m'), day('s_d'))
    end = datetime(day('e_y'), day('e_m'), day('e_d'))
    return start, end


def day(ele):
    post = request.get_json()
    return int(post.get(ele))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
