/*
 Inspired by Kenrick Beckett
 https://css-tricks.com/jquery-php-chat/
 */

// ref: https://stackoverflow.com/questions/487073/check-if-element-is-visible-after-scrolling
function isScrolledIntoView(elem)
{
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop = $(elem).offset().top;
    var elemBottom = elemTop + $(elem).height();

    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}

function LogTailMonitor(monitor_id) {
    /*
     Object to watch for updates from a specific log file and add the entries to
     a list of log lines.

     Function creates and returns an object.
     */
    var monitor = {};

    monitor.monitor_id = monitor_id;
    monitor.last_line_id = null;
    monitor.checkForNewLines = function() {
        $.ajax({
            type: "GET",
            url: 'nextlines',
            data: {
                'monitor_id': monitor.monitor_id,
                'last_line_id': (monitor.last_line_id == null) ? '-1' : monitor.last_line_id,
                'how_many': 'all',
            },
            dataType: "json",


            success: function (response) {

                console.log("Got " + response.status + " /nextlines ");

                // Check to see if we should scroll if last element is currently visible
                var scroll = (monitor.last_line_id == null || isScrolledIntoView($('#line_'+monitor.last_line_id)));

                if (response.status == 'ok') {

                    // Collect just the last lines
                    for (var i = 0; i < response.lines.length; i++) {

                        var line = response.lines[i];

                        // Update displayed text
                        $('#log_lines').append(`<div id='line_${line.line_id}'>${line.text}</div>`);

                        // Record line id
                        if (monitor.last_line_id === null || line.line_id > monitor.last_line_id)
                            monitor.last_line_id = line.line_id;

                    }
                }

                // Scroll to show new line
                if (scroll)
                {
                    var elmnt = document.getElementById('line_'+monitor.last_line_id);
                    elmnt.scrollIntoView();
                }

                // Start a new request to get the next data (long poll)
                monitor.checkForNewLines();
            },


            error: function (response) {
                console.log("Request for monitor " + monitor.monitor_id + " FAILED");

                // Start next request
                monitor.checkForNewLines();
            }
        });
    }

    return monitor;
}

