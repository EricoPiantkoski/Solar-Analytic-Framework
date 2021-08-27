try:
    import urequests as requests
except:
    import requests

def get_simple(url):
    r = requests.get(url)
    return r

def get_params(url, p):
    r = requests.get(url, params = p)
    return r

def post(url, data):
    r = requests.post(url, json=data)
    return r

endpoint = "http://127.0.0.1:5000/f-data"

data = { 
    'id_esp' : 1,
    'date_log': '31/08/2021',
    'data':{
        'spent': 4,
        'gain': 5,
        'prediction': 5
    }
}



# data = { 
#     'id_data': 1234,
#     'content':{
#         'id_esp': 1,
#         'date_log': '27/08/2021',
#         'data':{
#             'spent': 4,
#             'gain': 5,
#             'prediction': 5
#         }
#     }
# }

#   "language": "Python$",
#   "framework": "Flask"#,
#   "website": "Scotch",
#   "version_info": {
#     "python": "3.9.0",
#     "flask": "1.1.2"
#   },
#   "examples": ["query", "form", "json"],
#   "boolean_test": True

#response = get_simple(endget)
#response = post("http://127.0.0.1:5000/req?esp-id=1", data)
response = post(endpoint, data)

# print(response.url)
#print(response.text)
print(response.json())