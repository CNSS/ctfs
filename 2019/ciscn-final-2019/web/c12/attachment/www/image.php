<?php
include "config.php";

$id=isset($_GET["id"])?$_GET["id"]:"1";
$path=isset($_GET["path"])?$_GET["path"]:"";

$id=addslashes($id);
$path=addslashes($path);

$id=str_replace(array("\\0","%00","\\'","'"),"",$id);
$path=str_replace(array("\\0","%00","\\'","'"),"",$path);

$sql="select * from images where id='{$id}' or path='{$path}'";
if (preg_match("/load/i",$sql))
{
    die("What's your problem?");
}

$result=mysqli_query($con,$sql);
$row=mysqli_fetch_array($result,MYSQLI_ASSOC);

//secure the path
$count=preg_match("/(\.\.)|(config)/i",$row["path"]);
if ($count>0)
{
    die("What's your problem?");
}

$path="./" . $row["path"];
header("Content-Type: image/jpeg");
readfile($path);