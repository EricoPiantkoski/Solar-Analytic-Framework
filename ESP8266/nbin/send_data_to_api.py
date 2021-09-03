# send_data_to_api.py
try:
    import urequests as requests
except:
    import requests
import ujson as json

endpoint = "https://gaes.pythonanywhere.com/f-data"
consum_data =  [[-25.0, 300.0, -25.0, 600.0, '25/08/2021'], [-25.0, 200.0, -25.0, 500.0, '26/08/2021'], [-25.0, 1000.0, -25.0, 7000.0, '27/08/2021'], [-25.0, 8000.0, -25.0, 700.0, '28/08/2021'], [-25.0, 500.0, -25.0, 600.0, '29/08/2021'], [-25.0, 900.0, -25.0, 500.0, '30/08/2021'], [-25.0, 700.0, -25.0, 700.0, '31/08/2021'], [-25.0, 1200.0, -25.0, 800.0, '01/09/2021'], [-25.0, 400.0, -25.0, 600.0, '02/09/2021']]
# for cdata in consum_data:
#     data = { 
#             'id_esp' : 1,
#             'date_log': cdata[4],
#             'data':{
#                 'spent': cdata[1],
#                 'gain': cdata[3]
#             }
#         }    
#         # print('dict data: ', data)
#     post_data = ujson.dumps(data)
#     response = requests.post(endpoint, headers = {'content-type': 'application/json'}, json = post_data).json()
#     #print(data)
#     print('consum_data response cdata: ', response.text)

data = { 
    'id_esp' : 1,
    'date_log': '25/08/2021',
    'data':{
        'spent': 300.0,
        'gain': 600.0
    }
}  
post_data = json.dumps(data)
print(post_data)
response = requests.post(endpoint, json = post_data)
print(response.text)