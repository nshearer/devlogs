import json
from ..monitors.SourceMonitorThread import NoNewLines

TIMEOUT_SEC=15.0

def nextline_view(request, server, assets):
    '''
    Wait for new lines to be detected

    Note: run with auto-lock disabled.  This view will aquire lock as needed.
    This allows it to not hold the lock while waioting for new data
    '''

    # Request parameters
    monitor_id = int(request['monitor_id'])
    last_line_id = int(request['last_line_id'])

    # Find monitor
    with server.lock:
        try:
            monitor = server.monitors[monitor_id]
        except Exception as e:
            return json.dumps({
                'status': 'error',
                'msg': str(e)
            })

    # Request next line
    if last_line_id == -1:
        last_line_id = None
    try:
        last_line = monitor.wait_new_line_available(last_line_id, TIMEOUT_SEC)[-1]
    except NoNewLines:
        last_line = None

    # Return no data
    if last_line is None:
        return json.dumps({
            'status': 'nodata',
            'msg': 'no new data',
        })

    # Encapsulate response
    return json.dumps({
        'status': 'ok',
        'text': last_line.txt,
        'line_id': last_line.line_id,
    })

