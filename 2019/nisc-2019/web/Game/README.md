# Game

打开题目链接 看到一个老虎机一样的东西 
点击shuffle 和 stop burp代理并未产生流量 说明是前端代码校验
f12审查元素看到得到flag的函数 是向score.php post score=15

于是

```python
import requests

res = requests.post("url of the docker"+"score.php",data={"score":15})
print(res.text)
```
