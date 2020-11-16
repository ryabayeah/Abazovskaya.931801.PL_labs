import json
from paste import reloader
from paste.httpserver import serve
from pytz import timezone
from datetime import datetime
from tzlocal import get_localzone


def check_data(time_zone,received_data):
    received_type = received_data['type']
    try:
        time_zone = received_data[time_zone]
        try:
            time_zone = timezone(time_zone)
        except:
            return None, b'Could not found time zone.'
    except KeyError:
        if received_type == 'time' or received_type == 'date':
            time_zone = get_localzone()
        else:
            return None, bytes('Could not find attr name "{}"'.format(time_zone), encoding='utf-8')
    return time_zone,None

def time_app(environ,start_response):
    status = '200 OK'  # HTTP Status
    headers = [('Content-type', 'text/plain')]  # HTTP Headers

    print(environ['REQUEST_METHOD'])

    if environ['REQUEST_METHOD'] == 'POST':
        received_data = environ['wsgi.input'].read().decode('utf-8')

        try:
            received_data = json.loads(received_data)
        except json.JSONDecodeError:
            start_response(status, headers)
            return [b'Incorrect data.']

        try:
            received_type = received_data['type']
        except KeyError:
            start_response(status, headers)
            return [b'Could not found argument "type".']

        if received_type == 'time':

             time_zone_1, error = check_data('time_zone_1', received_data)
             if error:
                 start_response(status, headers)
                 return [error]

             out = json.dumps(
                {
                    'time': datetime.now(tz=time_zone_1).time().isoformat(),
                    'tz': str(time_zone_1)
                 }
             )

        elif received_type == 'date':

            time_zone_1, error = check_data('time_zone_1', received_data)
            if error:
                start_response(status, headers)
                return [error]

            out = json.dumps(
                {
                    'date':datetime.now(tz=time_zone_1).date().isoformat(),
                    'tz': str(time_zone_1)
                }
            )

        elif received_type == 'difference':

            time_zone_1, error = check_data('time_zone_1', received_data)
            if error:
                start_response(status, headers)
                return [error]

            time_zone_2, error = check_data('time_zone_2', received_data)
            if error:
                start_response(status, headers)
                return [error]

            fist_tz = datetime.now(tz=time_zone_1).utcoffset()
            second_tz = datetime.now(tz=time_zone_2).utcoffset()
            find_the_greatest = lambda x, y: str(x-y) if x >= y else '-' + str(y - x)

            out = json.dumps(
                {
                    'First time zone': str(received_data['time_zone_1']),
                    'Second time zone': str(received_data['time_zone_2']),
                    'Difference:': find_the_greatest(fist_tz, second_tz)
                 }
            )
        else:
            out = 'No such type'
        start_response(status, headers)
        return [bytes(out, encoding='utf-8')]


    else:
        set_timezone = environ['PATH_INFO'][1:]

        try:
            tm = timezone(set_timezone)
        except:
            start_response(status, headers)
            time_zone = datetime.now().time()
            return [bytes(
                'Time in '+ str(get_localzone()) +
                ' is ' + str(datetime.now(tz=get_localzone()).strftime('%H:%M:%S %Z')),
                encoding='utf-8'),
                b'\nWrite time zone in url']

    start_response(status, headers)

    return [bytes('Time in '+ str(timezone(set_timezone)) +
                  ' is ' + str(datetime.now(tz=tm).strftime('%H:%M:%S %Z')),
                  encoding='utf-8')]

if __name__ == '__main__':
    reloader.install()
    serve(time_app)
