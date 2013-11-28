<html>
	<head>
		<meta http-equiv="refresh" content=1 URL="https://192.168.1.16/index.php"/>
		<style>
			body {
				position: relative;
			}
			#bar {
				background-color: #999;
				text-align: center;
				font-size: 80px;
				position: absolute;
				bottom: 10%;
				width: 100%;
				opacity: 0.5;
			}
		</style>
	</head>

<body background="Recycling_1920x1080_se.jpg">


<?php

include('db.php');

db::connect();

$count = db::fetch('SELECT sum(total) FROM `counters`');
?>
<div id="bar">
	<?php
	echo $count[0]['sum(total)']." cans recycled";
	?>
</div>

</body>
</html>
