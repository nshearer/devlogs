/*
 Inspired by Kenrick Beckett
 https://css-tricks.com/jquery-php-chat/
 */

function LogLineUpdater(monitor_id) {
    var this_monitor = {};

    this_monitor.monitor_id = monitor_id;
    this_monitor.last_line_id = null;
    this_monitor.updateLastLine = function() {
        $.ajax({
            type: "GET",
            url: 'nextline',
            data: {
                'monitor_id': this.monitor_id,
                'last_line_id': (this_monitor.last_line_id == null) ? '-1' : this_monitor.last_line_id},
            dataType: "json",
            success: function (response) {
                console.log("Got: " + response.status + " from " + this_monitor.monitor_id + " (line ID " + response.line_id + ")");
                if (response.status == 'ok') {
                    $('#monitor_' + this_monitor.monitor_id + '_lastline').html(response.text);
                    $('#monitor_' + this_monitor.monitor_id + '_lastline').effect("highlight", {}, 1500);
                    this_monitor.last_line_id = response.line_id;
                }
                this_monitor.updateLastLine();
                /*
                if(data.text) {
                    alert("Got: " + data.text);
                    for (var i = 0; i < data.text.length; i++) {
                        $('#chat-area').append($("

                        "+ data.text[i] +"

                        "));
                    }
                }
                document.getElementById('chat-area').scrollTop = document.getElementById('chat-area').scrollHeight;
                instanse = false;
                state = data.state;
                */
            },
            error: function (response) {
                console.log("Request for monitor " + this_monitor.monitor_id + " FAILED");
                this_monitor.updateLastLine();
            }
        });
    }

    // Start first update
    this_monitor.updateLastLine();

    return this_monitor;
}

