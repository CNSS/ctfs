<?php
include "config.php";
include "function.php";

is_login();

if ($username!=="admin")
{
    echo "You have not permission.<script>setTimeout('location.href=\"index.php\"',3000);</script>";
    die;
}

if (!$_FILES["file"]["name"])
{
    echo "Please chose a file to upload.<script>setTimeout('location.href=\"user.php\"',3000);</script>";
    die;
}

$file_name=$_FILES["file"]["name"];

if (preg_match("/php/i",$file_name))
{
    echo "You cant upload php file.<script>setTimeout('location.href=\"user.php\"',3000);</script>";
    die;
}

file_put_contents("logs/upload.log.php","User {$username} uploaded file {$file_name}.\n",FILE_APPEND);
echo "I logged the file name you uploaded. LOL<script>setTimeout('location.href=\"user.php\"',3000);</script>";