# flask-web-project
A simple flaskweb project

## Python版本 
   python == 3.7.7

## 依赖第三方包

```bash
pip install -r requirements.txt
```
## 数据库表操作
数据库的操作
初始化数据库  flask db init
自动创建迁移脚本   flask db migrate -m 'initial migration'
更新数据库 flask db upgrade

## 运行flask

```bash
export FLASK_APP=XXX
export FLASK_DEBUG=1
flask run -h 0.0.0.0 -p 9000
```

## 支持shell命令

```bash
flask shell
```


## 功能
1、文件托管服务
上传后文件被永久存放
上传后有一个预览页，预览页显示文件大小，文件类型，上传时间，下载地址和短连接等信息
可以通过传参数对图片进行缩放和剪切
页面提示效果
节省空间，相同文件不重复上传，如果文件已经上传过，则直接返回之前上传的文件。