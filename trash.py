import requests

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

json_data = {
    'title': 'string',
    'description': 'string',
    'image': 'string',
    'price': 500000,
}

response = requests.post('http://127.0.0.1:15000/product/create', headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{\n  "title": "string",\n  "description": "string",\n  "image": "string",\n  "price": 0\n}'
#response = requests.post('http://127.0.0.1:15000/product/create', headers=headers, data=data)