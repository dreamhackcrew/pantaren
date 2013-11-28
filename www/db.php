<?php
include "dbconfig.php";

class db {

	static function connect() { 

		mysql_connect(config::host, config::username, config::password) or die('Could not connect: ' . mysql_error());
		mysql_select_db(config::database) or die('Could not select database');
		mysql_query("SET NAMES 'ISO-8859-1'");

	}

	static function query( $query ) {
		if( $result = mysql_query($query))
			return $result;
		
		else die('Query failed: ' . mysql_error());

	}

	static function fetch( $sql_query ) {
		if( !$result = db::query($sql_query))
			return false;

		$array = array();

		while ( $row = mysql_fetch_array($result, MYSQL_ASSOC) )
			$array[] = $row;

		return $array;
	}

	static function insert( $fields, $table ) {
		
		$table = mysql_real_escape_string($table);

		$sql = 'INSERT INTO `'.$table.'` SET ';

			foreach($fields as $key => $val) {
				$key = mysql_real_escape_string($key);
				$val = mysql_real_escape_string($val);

					if (!isset($notFirst)) {
						$notFirst = 'Y';
					} else $sql .= ', ';

					$sql .= '`'.$key.'` = "'.$val.'"';
				}
				//echo $sql;
		if (db::query($sql)) return mysql_insert_id();
		else return false;

	}
}
?>
