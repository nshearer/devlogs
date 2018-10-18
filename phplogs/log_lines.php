<?php

$file = $_GET['file'];
$limit = $_GET['limit'];
$log_paths = json_decode(file_get_contents('paths.json'));
$lines = file($log_paths->$file->path);

# Limit lines
$lines = array_slice($lines, -1 * intval($limit));

# Reverse sort to put most recent on top
$lines = array_reverse($lines);

# Output JSON
$output = array(
	'comment' => sprintf("Fetching %d from %s", $limit, $file),
	'lines' => $lines,
	);
header('Content-Type: application/json');
echo json_encode($output);