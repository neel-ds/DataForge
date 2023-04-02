import requests as req
import json

params = {
  "Suburb": "askldjfkj",
  "Address": "skljdfskldjf",
  "Rooms": 3,
  "Type": "h",
  "Method": "S",
  "SellerG": "Biggin",
  "Date": "29304",
  "Distance": 11.2,
  "Postcode": 3186.0,
  "Bedroom2": 3.0,
  "Bathroom": 2.0,
  "Car": 1.0,
  "Landsize": 354.0,
  "BuildingArea": 143.0, 
  "YearBuilt": 1910.0,
  "CouncilArea": "Yarra",
  "Lattitude": -37.8916, 
  "Longtitude": 145.0017,
  "Regionname": "Southern Metropolitan",
  "PropertyCount": 10579.0
}

json_data = json.dumps(params)

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

url = 'http://127.0.0.1:5000/deploy'

response = req.post(url, data=json_data, headers=headers)

print(response.text)
