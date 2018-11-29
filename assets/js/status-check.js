(function status_check_worker() {
  $.ajax({
    url: '/status',
    success: function(data) {
        // $('#status_result').html(data['status']);
        if (data['status'] == 'ok') {
            $("#status-online-card").show();
            $("#status-offline-card").hide();
        } else {
            $("#status-online-card").hide();
            $("#status-offline-card").show();
        }
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(status_check_worker, 5000);
    },
    error: function() {
        $("#status-online-card").hide();
        $("#status-offline-card").show();
    }
  });
})();