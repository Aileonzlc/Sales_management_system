import pprint
import requests

payload = {
    'username': 'zlc',
    'action': 'list_customer',
}
# get方法时，使用params=payload
response = requests.get('http://127.0.0.1/api/mgr/customers',
                         params=payload)

pprint.pprint(response.json())
