<?php
include "config.php";
include "function.php";

$username="";

if (!is_login() && !isset($_POST["username"]) && !isset($_POST["password"]))
{
    header('Location: index.php');
    die;
}

if ($username==="")
{
    $stmt=$con->prepare("select * from users where username=?");
    $stmt->bind_param("s",$_POST["username"]);
    $stmt->execute();
    $result=$stmt->get_result();
    $row=$result->fetch_assoc();
    if ($row["password"]===$_POST["password"])
    {
        $username=$_POST["username"];
        setcookie("username",encode($username,$secret));
    }
    else
    {
        header('Location: index.php');
        die;
    }
}

$admin_html=<<<EOF
Hello, admin!
<form action="upload.php" method="post"enctype="multipart/form-data">
<label for="file">Filename:</label>
<input type="file" name="file" id="file" /> 
<br />
<input type="submit" name="submit" value="Submit" />
</form>
EOF;

if ($username!=="admin")
{
    echo "Hello, {$username}, if you are admin, I will give you a surprise.";
}
else
{
    echo $admin_html;
}