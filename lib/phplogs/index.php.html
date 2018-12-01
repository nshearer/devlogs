<html>
<head>
	<title>SBC DB Test Logs</title>
	<?php
		$log_paths = json_decode(file_get_contents('paths.json'));
	?>
<style type="text/css">
.log_file div .log_name a:link{
	color: #FF5F00;
}
.log_file div .log_name a:visited{
	color: #FF5F00;
}
.log_file div .log_path {
	color: #999999;
}
.log_file {
	padding-top: 0.6em;
}
.log_file .lastline {
	padding-left: 1em;
	font-family: monospace;
}
</style>


<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="//code.jquery.com/ui/1.12.0/jquery-ui.js"></script>
<script>

var logs_names = ["<?php echo implode(array_keys((array)$log_paths), '", "'); ?>"];

// Script run on document ready
(function($)
{
    $(document).ready(function()
    {
    	<?php foreach($log_paths as $log_name => $log_info): ?>
		setInterval(function(){ update_lastline("<?php echo $log_name ?>"); }, 5000);  // Update lastline every 5 seconds
		<?php endforeach; ?>
    });
})(jQuery);

function update_lastline(log_name)
{
	$("#"+log_name+"_refreshing").show();
	$.getJSON("log_lines.php?file="+log_name+"&limit=1", function( data ) {

		// No lines?
		if (data.lines.length == 0 || data.lines[0] == "")
		{
			$("#"+log_name+"_lastline").html("<em style='color: grey;'>No data</em>");
		}
		else
		{

			var prev_text = $("#"+log_name+"_lastline").text();

			// Update lastline contents
			$("#"+log_name+"_lastline").text(data.lines[0]);

			// Use effect to show update
			if (data.lines[0] != prev_text)
			{
				$("#"+log_name+"_lastline").effect("highlight", {}, 1500);
			}
		}

		$("#"+log_name+"_refreshing").hide();
	});
}


function success(data)
{
  	$("#last_updated").text("Last Updated: " + new Date().toLocaleString());

  	// Iterate over log lines
	var numLines = data.lines.length;
	for (var i = numLines-1; i >= 0; i--)
	{
		// Hash line (I'll only support unique log lines.  Should be ok if line has date stamp)'
		var line_hash = md5(data.lines[i]);

		// Check lines doesn't exist
		if ($('#line_'+line_hash).length == 0)
		{
			// Add line
			$("#log_lines").prepend(`<div class="log_line" id="line_${line_hash}" style="display:none;">${data.lines[i]}</div>`);

			// Fade line in
			$("#line_"+line_hash).fadeIn(1500);
		}	    
	}  
}

</script>


</head>
<body>
<h1>Log Files</h1>
<?php foreach ($log_paths as $name => $log_def): ?>
	<div class="log_file">
		<div class=""log_file_header">
			<span class="log_name"><a href="<?php echo "log_file.php?file=$name&limit=30" ?>"><?php echo $name ?></a></span>
			<span class="log_path"><?php echo $log_def->path ?></span>
			<span id="<?php printf("%s_refreshing", $name); ?>" style="color: #FF5F00;">...</span>
		</div>
		<div class="lastline">
			<span id="<?php printf("%s_lastline", $name); ?>">Loading last line</span>
		</div>
	</div>
<?php endforeach; ?>
</body>
<html>