# 软件部署和操作说明

## 云服务器基本使用

- 从cmd登录云服务器：  
  `ssh root@113.44.59.183`
- psw：暂不公布，有需要请私信我
- 手动进行SQL操作：  
  `sqlite3 /var/www/html/backend/instance/flaskr.sqlite`

## 上传代码

**以下操作均基于当前根目录相对路径进行上传，请务必确保cmd进入forum-0.0-main文件夹！**

### 前端

- 打包前端文件：  
  `npm run build`
- 将打包好的前端文件上传到云服务器（不需要事先登录）：  
  `scp -r dist/* root@113.44.59.183:/var/www/html/`

### 后端

- 直接将后端文件上传到对应的后端目录下：  
  `scp -r backend/* root@113.44.59.183:/var/www/html/backend`

### 环境

由于我在本地使用了一个巨大的conda环境，因此暂时无法将自动生成的environment.yml用于服务器端自动搭建环境，此处需要在服务器端切换至清华源并手动安装至少以下库：  

- Flask=3.1.0
- Flask-Cors=5.0.0
- Flask-Mail=0.10.0
- Flask-Session=0.8.0
- Jinja2=3.1.4
- MarkupSafe=3.0.2
- Werkzeug=3.1.3
- blinker=1.9.0
- cachelib=0.13.0
- click=8.1.7
- colorama=0.4.6
- itsdangerous=2.2.0
- msgspec=0.18.6
- pip=24.0

## 网络配置

- 进入Nginx配置项：  
  `sudo nano /etc/nginx/nginx.conf`
- 修改server配置：  

      server {
        listen 80;
        server_name 113.44.59.183;  

        location / {
            root /var/www/html;
            try_files $uri $uri/ /index.html;
        }

        location /api/ {
            proxy_pass http://127.0.0.1:5000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        error_page 404 /404.html;
        location = /404.html {
            root /usr/share/nginx/html;
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root /usr/share/nginx/html;
        }
      }
  按 `Ctrl + O` 保存，`Ctrl + X` 退出
- 测试已完成的Nginx配置：  
  `sudo nginx -t`

## 运行网站

1. 进入后端入口函数app.py所在位置：  
   `cd /var/www/html/backend`
2. 使用gunicorn作为WSGI服务器，并保持运行状态：  
   `nohup gunicorn -w 4 -b 0.0.0.0:5000 app:app > flask_app.log 2>&1 &`
3. 查看当前Flask项目的进程号：  
   `ps aux | grep gunicorn`
4. 终止相应进程：  
   `kill <PID>`
5. 查看Flask后端的运行日志输出：  
   `tail -f flask_app.log`
6. 客户端使用：  
   点击链接 [TJ Life Forum](http://113.44.59.183) 或直接访问 [http://113.44.59.183](http://113.44.59.183)
7. 本地版代码参见 [https://github.com/xhc926/TJ-Life-Forum/tree/local](https://github.com/xhc926/TJ-Life-Forum/tree/local)
