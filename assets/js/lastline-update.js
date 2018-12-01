/*
 Inspired by Kenrick Beckett
 https://css-tricks.com/jquery-php-chat/
 */

function LogLineUpdater() {
    /*
     Object to watch for updates from any log file and update the the last line
     on the index page.
     Function creates and returns an object.
     */
    var monitor = {};

    monitor.last_line_id = null;
    monitor.updateLastLine = function() {
        $.ajax({
            type: "GET",
            url: 'nextlines',
            data: {
                'monitor_id': 'all',
                'last_line_id': (monitor.last_line_id == null) ? '-1' : monitor.last_line_id,
                'how_many': 'all',
            },
            dataType: "json",


            success: function (response) {

                if (response.status == 'ok') {

                    // Collect just the last lines
                    var last_lines = {};
                    for (var i = 0; i < response.lines.length; i++) {
                        var line = response.lines[i];
                        last_lines[line.monitor_id] = line;
                    }

                    // Iterate latest new log lines
                    for (var monitor_id in last_lines) {
                        var line = last_lines[monitor_id];
                        var lastline_div = '#monitor_' + line.monitor_id + '_lastline';

                        // Update displayed text
                        $(lastline_div).html(line.text);

                        // Highlight text for a short time
                        $(lastline_div).effect("highlight", {}, 1500);

                        // Record line id
                        if (monitor.last_line_id === null || line.line_id > monitor.last_line_id)
                            monitor.last_line_id = line.line_id;
                    }
                }

                // Start a new request to get the next data (long poll)
                monitor.updateLastLine();
            },


            error: function (response) {
                console.log("Request for monitor " + monitor.monitor_id + " FAILED");

                // Start next request
                monitor.updateLastLine();
            }
        });
    }

    return monitor;
}

