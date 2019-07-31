
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Login</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script type="application/x-javascript"> addEventListener("load", function() { setTimeout(hideURLbar, 0); }, false); function hideURLbar(){ window.scrollTo(0,1); } </script>
<meta name="keywords" content="Flat Dark Web Login Form Responsive Templates, Iphone Widget Template, Smartphone login forms,Login form, Widget Template, Responsive Templates, a Ipad 404 Templates, Flat Responsive Templates" />

<link href="style.css" rel='stylesheet' type='text/css' />

<script type="text/javascript" src="jquery.min.js"></script>

</head>
<body>
<script>$(document).ready(function(c) {
	$('.close').on('click', function(c){
		$('.login-form').fadeOut('slow', function(c){
	  		$('.login-form').remove();
		});
	});	  
});
</script>

<h1>登录</h1>
<div class="login-form">
	<div class="close"> </div>
	<div class="head-info">
		<label class="lbl-1"> </label
		<label class="lbl-2"> </label>
		<label class="lbl-3"> </label>
	</div>
	<div class="clear"> </div>
	<div class="avtar"><img src="image.php?id=<?=rand(1,3)?>" width="200" height="200"/></div>
	<form method="post" action="user.php">
		<input name="username" type="text" class="text" value="username" onFocus="this.value = '';" onBlur="if (this.value == '') {this.value = 'Username';}" >
		<div class="key"><input name="password" type="password" value="password" onFocus="this.value = '';" onBlur="if (this.value == '') {this.value = 'Password';}"></div>
	<div class="signin"><input type="submit" value="Login" ></div>
    </form>
</div>
<div class="copy-rights">
	<p>Copyright &copy; 2019.Company name All rights reserved.
</div>

</body>
</html>