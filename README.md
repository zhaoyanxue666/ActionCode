### flask制作的web，用于管理软件授权码，

### 在config.py文件下更改账号密码登陆

### 1.txt是依赖环境

### 功能就是对授权码增删改查

### 接口是/search，post请求，参数1是code，参数2是电脑mac地址，返回信息见models.py的set_mac_check_time
![1612519550379](https://github.com/cc-ling/actionCode/blob/master/img/show.png)

### 在app.py下初始化管理员账号密码，也可以在数据库内自行添加
![1612519550379](https://github.com/cc-ling/actionCode/blob/master/img/create.png)