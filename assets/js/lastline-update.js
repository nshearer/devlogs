/*
 Inspired by Kenrick Beckett
 https://css-tricks.com/jquery-php-chat/
 */

function LogLineUpdater(monitor_id) {
    var obj = {};

    obj.monitor_id = monitor_id;
    obj.updateLastLine = function() {
        $.ajax({
            type: "GET",
            url: "nextline",
            data: {'monitor_id': this.monitor_id},
            dataType: "json",
            success: function (data) {
                console.log("Got: " + data.status + " from " + obj.monitor_id);
                if (data.status == 'ok') {
                    console.log(data.text);
                    $('#monitor_' + obj.monitor_id + '_lastline').html(data.text);
                }
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
            }
        });
    }

    // Start first update
    obj.updateLastLine();

    return obj;
}

