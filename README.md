# 前端部署
## 打包

1.首先找到config/index.js文件，将assetPublicPath的路径改为“./”
2.在build目录下utils.js修改，找到如下配置添加publicPath: '../../'

```
 
if (options.extract) {
  return ExtractTextPlugin.extract({
    use: loaders,
    fallback: 'vue-style-loader',
    publicPath: '../../',    //添加上的
  })
} else {
  return ['vue-style-loader'].concat(loaders)
}
```

3.npm run build产生dist文件夹

## 安装nginx

```
sudo yum -y install nginx

sudo systemctl start nginx

如果想在系统启动时启用Nginx。请输入以下命令
sudo systemctl enable nginx
```

## 上传部署

```
将dist文件夹上传到服务器

vi /etc/nginx/nginx.conf

在include /etc/nginx/default.d/*.conf;下方
location / {
	root /var/myapp/dist/;
	index index.html index.htm;
	try_files $uri $uri/ /index.html;
}

sudo systemctl restart nginx
```

# 后端部署

## python3安装

```
安装必要工具 yum-utils ，它的功能是管理repository及扩展包的工具 
sudo yum install yum-utils

使用yum-builddep为Python3构建环境,安装缺失的软件依赖,使用下面的命令会自动处理
sudo yum-builddep python

完成后下载Python3的源码包
curl -O https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz

最后一步，编译安装Python3，默认的安装目录是 /usr/local
tar xf Python-3.7.6.tgz
cd Python-3.7.6
./configure
make
sudo make install

#如果你要使用Python3作为python的默认版本，你需要修改一下 #bashrc 文件，增加一行alias参数
#alias python='/usr/local/bin/python3.7'

由于CentOS 7建议不要动/etc/bashrc文件，而是把用户自定义的配置放入/etc/profile.d/目录中，具体方法为
vi /etc/profile.d/python.sh
写入
alias python='/usr/local/bin/python3.7'

chmod 755 /etc/profile.d/python.sh

重启会话使配置生效
source /etc/profile.d/python.sh
```

## 安装需要的库

## 后台运行

```
nohup /usr/local/bin/python3.7 -u app.py > test.log 2>&1 &

定时运行

用如下命令查看当前系统中的定时任务列表
crontab -l

对crontab进行编辑
crontab -e

这里设置的是每天6,、12、20点整运行脚本
0 6,12,20 * * * /usr/local/bin/python3.7 /home/ec2-user/cov19/app.py > /home/ec2-user/cov19/auto.log

完成后，可以重启一下crontab的服务即可
service crond restart
```

# 安装数据库

## 下载安装

```
配置MySQL 8.0的安装源
sudo rpm -Uvh https://dev.mysql.com/get/mysql80-community-release-el7-1.noarch.rpm

安装MySQL 8.0
sudo yum --enablerepo=mysql80-community install mysql-community-server

开启命令systemctl start mysqld

查看状态systemctl status mysqld

在日志文件中找出密码
grep "password" /var/log/mysqld.log

mysql -uroot -p

其中‘new password’替换成你要设置的密码，注意:密码设置必须要大小写字母数字和特殊符号（,/';:等）,不然不能配置成功
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new password';

修改root账号远程访问权限
mysql> use mysql;
mysql> select host, user, authentication_string, plugin from user; #查看现有用户
mysql>  CREATE USER 'root'@'%' IDENTIFIED BY 'Password';# 创建新用户
mysql> GRANT ALL ON *.* TO 'root'@'%'; # 为新用户授权
mysql>ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '040315';#把加密方式改成mysql_native_password
mysql> flush privileges;
```

**参考**
*该系统大屏展示页面参考[https://www.bilibili.com/video/BV177411j7qJ](https://www.bilibili.com/video/BV177411j7qJ)实现*

---
> GitHub [@ndmiao](https://github.com/ndmiao) &nbsp;&middot;&nbsp;
> BiliBili [@南岛鹋](https://space.bilibili.com/260584233) &nbsp;&middot;&nbsp;
> 知乎 [@南岛鹋](https://www.zhihu.com/people/ndmiao) &nbsp;&middot;&nbsp;
> CSDN [@南岛鹋](https://blog.csdn.net/qq_40851534?spm=1010.2135.3001.5343) &nbsp;&middot;&nbsp;
> 博客园 [@南岛鹋](https://www.cnblogs.com/ndmiao) &nbsp;&middot;&nbsp;
> 个人站点 [@南岛鹋](https://www.ndmiao.cn) &nbsp;&middot;&nbsp;

![](https://www.ndmiao.cn/follow.png)

## 打赏
| 支付宝                             | 微信                                  |
| ---------------------------------- | ------------------------------------- |
| ![](https://www.ndmiao.cn/pay.png) | ![](https://www.ndmiao.cn/wechat.png) |
