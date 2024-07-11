## YourSpace, a lightweight community/forum project

## 快速开始(以debian系为例)
### 1.安装相关软件包
```bash
sudo apt install -y python3 mariadb-server pkg-config libmariadb-dev git
```
### 配置MariaDB
#### 初始化数据库
>如果您有已建立好的MySQL/MariaDB数据库，请跳至[配置数据库连接信息](#3-配置数据库连接信息)

执行MariaDB的安全脚本
```bash
sudo mysql_secure_installation
```
这个脚本会引导你完成以下步骤：

1.设置 root 密码

2.移除匿名用户

3.禁止 root 远程登录

4.删除测试数据库

5.重新加载权限表
#### 建立数据库
进入mysql
```bash
mysql -u root -p
```
接下来输入密码或使用unix socket登录

创建数据库YourSpace
```SQL
CREATE DATABASE YourSpace;
```
创建YourSpace用户并赋予YS库权限（可选）
```SQL
CREATE USER 'yourspace'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON yourspace.* TO 'yourspace'@'localhost';
FLUSH PRIVILEGES;
```
### 2.下载源代码及Python依赖
#### 下载源代码
1.可直接Download

2.也可使用git clone
```bash
git clone https://github.com/Godtokoo666/yourspace
```
#### 配置Python虚拟环境
```bash
cd yourspace
python3 -m venv venv
source venv/bin/activate
```
#### 下载Python依赖
```bash
pip install -r requirements.txt
```

### 3.配置数据库连接信息
编辑config.yaml

在SQLALCHEMY_DATABASE_URI:后填入正确的信息

格式：
```YAML
SQLALCHEMY_DATABASE_URI: "mysql://username:password@localhost/yourspace"
```

### 4.启动程序
可直接启动run.py运行程序，但不建议，Flask内置的服务器仅推荐调试时使用

可使用WSGI Server gunicorn，requirement.txt已写入gunicorn，若无，请：
```bash
pip install gunicorn
```
接下来创建gunicorn配置文件gunicorn_config.py
```Python
# 是否开启debug模式
debug = False
# 访问地址
bind = "127.0.0.1:5000"
# 工作进程数
workers = 2
# 设置协程模式，后续支持
# worker_class="gevent"  
# 最大客户端并发数量，默认情况下这个值为1000。此设置将影响gevent和eventlet工作模式
worker_connections=500
# 超时时间
timeout = 600
# 输出日志级别
loglevel = 'info'
# 存放日志路径
pidfile = "log/gunicorn.pid"
# 存放日志路径
accesslog = "log/access.log"
# 存放日志路径
errorlog = "log/error.log"
# gunicorn + apscheduler场景下，解决多worker运行定时任务重复执行的问题
preload_app = True
```
启动gunicorn
```bash
gunicorn -c gunicorn_config.py run:app
```
### 5.写入进程管理工具（以systemd为例）
在/etc/systemd/system下新建yourspace.service文件，并编辑

填入内容（/path/to/your/app需替换为正确的路径）：
```CONFIG
[Unit]
Description=Yourspace Main App
After=network.target

[Service]
WorkingDirectory=/path/to/your/app
ExecStart=/path/to/your/app/venv/bin/gunicorn -c gunicorn_config.py run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动和管理服务
```bash
sudo systemctl daemon-reload
sudo systemctl start yourspace
sudo systemctl enable yourspace #启用开机自启和守护进程
```
### 6.部署至WEB服务器（以Nginx为例）
location块的内容为

## DEMO

[https://yourspace.funfs.com/](https://yourspace.funfs.com/)

## TO DO LIST
- [ ] 加入SMTP邮箱验证
- [ ] 异步ReWrite
- [ ] 编写移动端前端UI

