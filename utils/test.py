import requests as req
import json

def test(params):      
  json_data = json.dumps(params)

  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

  url = 'http://127.0.0.1:5000/deploy'

  response = req.post(url, data=json_data, headers=headers)

  print(response.text)  
  return response.text