from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

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
    esp_id = request.args.get('esp-id')
    date_req = request.args.get('date')
    #print(response)

    try:
        if int(esp_id) == response['id']:
            if str(date_req) == response['date_log'][0:5]:
                return response
        else:
            raise RuntimeError("Request not understood")
    except NameError:
        return 'No data yet'
    

@app.route('/f-data', methods=['POST', 'OPTIONS'])
def receive_data():
    global id
    global datelog #dd/mm/yyyy
    global spent #wh/m2
    global gain #wh/m2
    global response #to-json

    if request.method == "OPTIONS": # CORS prefligh
        return _build_cors_prelight_response()
    elif request.method == "POST":
        request_data = request.get_json()
        response = {
            'id': request_data['id'],
            'date_log': request_data['date_log'],
            'data':{
                'spent': request_data['data']['spent'],
                'gain': request_data['data']['gain'],
                'prediction': request_data['data']['prediction']
            }
        }
        atribute_data(response) 
        
        return _corsify_actual_response(jsonify(response))

    else:
        raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))


def atribute_data(response):
    id = response['id']
    datelog = response['date_log']
    spent = response['data']['spent']
    gain = response['data']['gain']

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(debug=True)