# show_me_your_image

上传文件以后拿到cookie，初步确定后端是python

上传文件的文件名提示是base64，但是无法正常解码，推测存在一个转换的表

上传各种文件名来获得映射关系，最后拿到转换表

```
RAW: BCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
NEW: /d3yiNmo7CzalDw2qWZ5JPYL0MTAjS6Iefxk9VXgvsRcuF+8pH4B1rOUbhKGtnQE
```

构造读文件payload，读取`../../../../../../proc/self/cwd/app.py`直接读到源码

根据提示，读取`../../../../../proc/self/cwd/templates/upload.html`读到flag位置

读取flag`../../../../../root/flag.txt`得到flag

