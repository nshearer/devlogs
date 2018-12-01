/*
 Inspired by Kenrick Beckett
 https://css-tricks.com/jquery-php-chat/
 */

function MonitorMenuActivity() {
    /*
     Flash menu links to show activity on the monitors
     */
    var monitor = {};

    monitor.last_line_id = null;
    monitor.checkForActivity = function() {
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

                    // Flash monitor links
                    var flashed = [];
                    for (var i = 0; i < response.lines.length; i++) {
                        var line = response.lines[i];
                        if ($.inArray(line.monitor_id, flashed) == -1)
                        {
                            var menu_item_div = '#monitor_' + line.monitor_id + '_menu';
                            $(menu_item_div).effect("highlight", {}, 1500);
                            flashed.push(line.monitor_id);
                            console.log(menu_item_div);
                            monitor.last_line_id = line.line_id;
                        }
                    }

                    // Flash Monitors menu header
                    /*
                    if (flashed.length > 0) {
                        $('#monitorsSubmenu').effect("highlight", {}, 1500);

                    }
                    */

                }

                // Wait 1.5 seconds and check again
                monitor.checkForActivity();
            },


            error: function (response) {
                console.log("MonitorMenuActivity.updateLastLine() FAILED");

                // Start next request
                setTimeout(monitor.checkForActivity, 5000);
            }

        });
    }

    return monitor;
}

