<?php

include('db.php');

db::connect();

$count = db::fetch('SELECT COUNT(id) from dhs13');

echo $count[0]['COUNT(id)'];
?>
