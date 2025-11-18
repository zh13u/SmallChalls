<?php
$DB_HOST = getenv('MYSQL_HOST') ?: 'db';
$DB_USER = getenv('MYSQL_USER') ?: 'ctf';
$DB_PASS = getenv('MYSQL_PASSWORD') ?: 'ctfpass';
$DB_NAME = getenv('MYSQL_DATABASE') ?: 'ctfdb';

$db = @mysqli_connect($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);
if (!$db) {
    die("DB connect error");
}
?>
