<?php
function encode($str,$key)
{
    $tmp="";
    for ($i=0;$i<strlen($str);$i++)
    {
        $tmp .= chr(ord($str[$i])^ord($key[$i%strlen($key)]));
    }
    return base64_encode($tmp);
}

function decode($str,$key)
{
    $str=base64_decode($str);
    $tmp="";
    for ($i=0;$i<strlen($str);$i++)
    {
        $tmp .= chr(ord($str[$i])^ord($key[$i%strlen($key)]));
    }
    return $tmp;
}

function is_login()
{
    global $username,$secret;
    if (!isset($_COOKIE["username"]))
        return false;
    $username=decode($_COOKIE["username"],$secret);
    return true;
}