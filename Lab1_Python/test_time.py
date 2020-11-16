import requests
import json

url = 'http://127.0.0.1:8080'

print('POST:\n************************************************************************************\n')
data = {'time_zone_1': 'Asia/Tomsk', 'type': 'time'}
print('TIME:\t\t' + requests.post(url=url, data = json.dumps(data)).text)

data = {'time_zone_1': 'Asia/Tomsk', 'type': 'date'}
print('DATE:\t\t' + requests.post(url=url, data = json.dumps(data)).text)

data = {'time_zone_1': 'Asia/Tomsk','time_zone_2': 'Asia/Tokyo', 'type': 'difference'}
print('DIFFERENCE:\t' + requests.post(url=url, data = json.dumps(data)).text)

data = {'time_zone_1': 'Asia/Tomsk','time_zone_2': 'Europe/Moscow', 'type': 'difference'}
print('DIFFERENCE:\t' + requests.post(url=url, data = json.dumps(data)).text)

print('\n************************************************************************************\n')

data = {'time_zone_1': 'Asia/Tomsk', 'type': 'time'}
print('NOT JSON DATE:\t\t\t' + requests.post(url=url, data=data).text)

data = {'time_zone_1': 'Asia/Tomsk'}
print('NO ATTR "type":\t\t\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'type': 'time'}
print('NO ATTR "time_zone_1":\t' + requests.post(url=url, data = json.dumps(data)).text)

data = {'time_zone_1': 'Asia/Tomsk', 'type': 'tme'}
print('ERROR ATTR "type":\t\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'time_zone_1': 'Asia/Toms', 'type': 'time'}
print('ERROR ATTR "time_zone_1":' + requests.post(url=url, data=json.dumps(data)).text)

print('\n************************************************************************************\n')

data = {'time_zone_1': 'Europe/Moscow', 'time_zone_2': 'Europe/Moscow', 'type': 'difference'}
print('TWO IDENTICAL OBJECTS:\t\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'type': 'difference'}
print('NO ATTRS "time_zone_1/2":\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'time_zone_1': 'Europe/Moscow', 'type': 'difference'}
print('NO ATTR "time_zone_2":\t\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'time_zone_2': 'Europe/Moscow', 'type': 'difference'}
print('NO ATTR "time_zone_1":\t\t' + requests.post(url=url, data=json.dumps(data)).text)

print('\n************************************************************************************')