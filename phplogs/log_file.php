<html>
<head>
<?php
$file = $_GET['file'];
$limit = $_GET['limit'];
if (empty($file))
	die("file= required");

$log_paths = json_decode(file_get_contents('paths.json'));
$long_info = $log_paths->$file;
$lines = file($long_info->path);

$data_url = "log_lines.php?file=${file}&limit=${limit}";
?>
<title>Apache Error Log</title>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="md5.js"></script>
<link rel="stylesheet" type="text/css" href="phplogs.css">
<script>

// Script run on document ready
(function($)
{
    $(document).ready(function()
    {
    	// Start first load
		//$.getJSON('<?php echo $data_url ?>', success);

		// Refresh every 3 seconds
		setInterval(function(){ $.getJSON('<?php echo $data_url ?>', success); }, 3000);
    });
})(jQuery);

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
<h1><?php echo $file ?></h1>
<div><?php echo $long_info->path ?></div>
<div id='last_updated'>Please Wait...</div>
<div id='log_lines'>
</div>
</body>
</html>