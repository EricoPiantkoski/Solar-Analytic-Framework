from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
import requests

app = Flask(__name__)
cors = CORS(app)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
@cross_origin()
def index():
    return "apitest"


@app.route('/req', methods=['GET'])
def get_data():
    #if key doesn't exist, return none
    date_req = request.args.get('date')
    esp_id = request.args.get('esp-id')

    try:
        if date_req == response[date_req]['date_log']:
            if esp_id == str(response[date_req]['id_esp']):
                return response[date_req]
            else:
                raise RuntimeError("Request not understood")
    except NameError:
        return 'No data yet'


@app.route('/req/getall', methods=['GET'])
def get_alldata():
    return response


@app.route('/f-data', methods=['POST', 'OPTIONS'])
def receive_data():
    global response #to-json
    try:
        if response:
            flag = 1
    except NameError:
        flag = 0

    if request.method == "OPTIONS": # CORS prefligh
        return _build_cors_prelight_response()
    elif request.method == "POST":
        request_data = json.loads(request.get_json())

        if flag == 0:
            response = {
                request_data['date_log']:{
                    'id_esp': request_data['id_esp'],
                    'date_log': request_data['date_log'],
                    'data':{
                        'spent': key_verify('spent', request_data['data'], request_data),
                        'gain': key_verify('gain', request_data['data'], request_data),
                        'prediction': key_verify('prediction', request_data['data'], request_data)
                    }
                }
            }
           

        else:
            response[request_data['date_log']] = {
                'id_esp': request_data['id_esp'],
                'date_log': request_data['date_log'],
                'data':{
                    #'spent': request_data['data']['spent'],
                    'spent': key_verify('spent', request_data['data'], request_data),
                    'gain': key_verify('gain', request_data['data'], request_data),
                    'prediction': key_verify('prediction', request_data['data'], request_data)
                }
            }
            
        return _corsify_actual_response(jsonify(response))

    else:
        raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))


def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def key_verify(key, req_in, req):
    if key in req_in:
        return req_in[key]
    else:
        end = 'https://gaes.pythonanywhere.com/req?date='+req['date_log']+'&esp-id='+str(req['id_esp'])
        try:
            resp = requests.get(end).json()
            if resp['data'][key] != 0:
                return resp['data'][key]
            else:
                return 0
        except:
            return 0
       

if __name__ == "__main__":
    app.run(debug=False)