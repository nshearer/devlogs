import json

from ..monitors.CommandMonitor import CommandStateError

def execute_command(request, server, assets):
    '''
    User requests that a command be executed

    Expected GET parameters (in GET body I believe):
        monitor_id      = The monitor ID representing the command to be executed

    '''

    # Request parameters
    try:
        monitor_id = int(request['monitor_id'])
    except ValueError:
        return json.dumps({
            'status': 'error',
            'msg': "Invalid monitor ID: " + str(monitor_id)
        })
    except KeyError:
        return json.dumps({
            'status': 'error',
            'msg': "Monitor ID is required",
        })

    # Determine which object we want to query for new data
    try:
        command_monitor = server.monitors[monitor_id]
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'msg': "Invalid monitor ID: " + str(e)
        })

    # Request execution
    try:
        command_monitor.start_command()
    except CommandStateError as e:
        return json.dumps({
            'status': 'error',
            'msg': "Can't start the command now: " + str(e)
        })

    # Return success
    return json.dumps({
        'status': 'ok',
    })

