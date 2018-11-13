

import json

def nextline_view(request, server, assets):
    '''
    Wait for new lines to be detected

    Note: run with auto-lock disabled.  This view will aquire lock as needed.
    This allows it to not hold the lock while waioting for new data
    '''

    # Find monitor
    with server.lock:
        try:
            monitor = server.monitors[int(request['monitor_id'])]
        except Exception as e:
            return json.dumps({
                'status': 'error',
                'msg': str(e)
            })

    last_line = monitor.last_line
    if last_line is None:
        return json.dumps({
            'status': 'error',
            'msg': 'no data',
        })

    return json.dumps({
        'status': 'ok',
        'text': last_line.txt,
        'line_id': last_line.line_id,
    })

