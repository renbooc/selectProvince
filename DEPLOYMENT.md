# 海元堂销售网点查询系统 - 部署指南

## 🚀 方案一：Render（推荐 - 免费）

### 步骤 1：准备代码

1. 确保项目包含以下文件：
   - `app.py` - 主应用文件
   - `Procfile` - 启动配置
   - `runtime.txt` - Python版本
   - `requirements.txt` - 依赖包
   - `templates/` - HTML模板文件夹
   - `customer_data.py` - 客户数据模块
   - `local_data.py` - 本地数据模块
   - `config_api.py` - API配置模块

2. 创建 Git 仓库并提交：
```bash
git init
git add .
git commit -m "Initial commit"
```

### 步骤 2：上传到 GitHub

1. 在 GitHub 创建新仓库
2. 推送代码：
```bash
git remote add origin https://github.com/你的用户名/selectProvince.git
git branch -M main
git push -u origin main
```

### 步骤 3：部署到 Render

1. 访问 [https://render.com](https://render.com)
2. 注册/登录账号
3. 点击 "New +" → "Web Service"
4. 连接 GitHub 仓库
5. 配置：
   - **Name**: `select-province`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Instance Type**: `Free`
6. 点击 "Create Web Service"

### 步骤 4：等待部署

- Render 会自动构建和部署
- 约 2-5 分钟后，会获得一个 HTTPS 地址
- 例如：`https://select-province.onrender.com`

### 步骤 5：配置环境变量（可选）

在 Render 控制台添加环境变量：
- `FLASK_DEBUG`: `False`
- `PORT`: `5000`

---

## 🚀 方案二：Railway（推荐 - 免费）

### 步骤 1：准备代码

同方案一

### 步骤 2：部署到 Railway

1. 访问 [https://railway.app](https://railway.app)
2. 注册/登录账号
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择你的仓库
5. Railway 会自动检测 Python 项目
6. 配置：
   - **Name**: `select-province`
   - **Region**: 选择最近的区域
7. 点击 "Deploy"

### 步骤 3：获取访问地址

- 部署完成后，会获得一个 `.railway.app` 域名
- 例如：`https://select-province.railway.app`

---

## 🚀 方案三：PythonAnywhere（推荐 - 免费）

### 步骤 1：注册账号

1. 访问 [https://www.pythonanywhere.com](https://www.pythonanywhere.com)
2. 注册免费账号（Beginner 账户）

### 步骤 2：创建 Web 应用

1. 登录后，点击 "Web" 标签
2. 点击 "Add a new web app"
3. 选择：
   - **Python version**: `3.13`
   - **Web app name**: `select-province`
   - **Python framework**: `Flask`

### 步骤 3：上传代码

1. 点击 "Files" 标签
2. 进入 `mysite` 文件夹
3. 上传所有项目文件

### 步骤 4：安装依赖

1. 点击 "Consoles" 标签
2. 创建 "Bash" 控制台
3. 运行：
```bash
pip install -r requirements.txt
```

### 步骤 5：配置 Web 应用

1. 在 "Web" 标签中，配置：
   - **Source code**: `/home/你的用户名/mysite/app.py`
   - **Working directory**: `/home/你的用户名/mysite`

2. 在 "WSGI configuration file" 中，添加：
```python
import sys
sys.path.insert(0, '/home/你的用户名/mysite')
from app import app as application
```

### 步骤 6：重载 Web 应用

点击 "Reload" 按钮，等待 1-2 分钟

### 步骤 7：访问应用

访问地址：`https://你的用户名.pythonanywhere.com`

---

## 🚀 方案四：Zeabur（国内访问快 - 免费）

### 步骤 1：注册账号

1. 访问 [https://zeabur.com](https://zeabur.com)
2. 注册账号

### 步骤 2：创建项目

1. 点击 "Create Project"
2. 选择 "Deploy from Git"
3. 连接 GitHub 仓库

### 步骤 3：配置服务

1. 选择 "Prebuilt Image" 或 "Dockerfile"
2. 配置环境变量
3. 部署

### 步骤 4：访问应用

- Zeabur 会提供一个 `.zeabur.app` 域名
- 国内访问速度较快

---

## 🚀 方案五：云服务器（阿里云/腾讯云 - 付费）

### 步骤 1：购买云服务器

- 阿里云：[https://www.aliyun.com](https://www.aliyun.com)
- 腾讯云：[https://cloud.tencent.com](https://cloud.tencent.com)
- 推荐配置：1核2G，40GB SSD（约 ¥50-100/月）

### 步骤 2：安装环境

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 3.13
sudo apt install python3.13 python3-pip python3-venv -y

# 创建虚拟环境
python3.13 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装 Gunicorn（生产服务器）
pip install gunicorn
```

### 步骤 3：上传代码

```bash
# 使用 SCP 上传
scp -r /path/to/project root@your-server-ip:/var/www/

# 或使用 Git
git clone https://github.com/你的用户名/selectProvince.git
```

### 步骤 4：配置 Gunicorn

创建 `gunicorn.service`：
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

添加内容：
```ini
[Unit]
Description=Gunicorn instance for selectProvince
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/selectProvince
Environment="PATH=/var/www/selectProvince/venv/bin"
ExecStart=/var/www/selectProvince/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### 步骤 5：配置 Nginx

```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/selectProvince
```

添加内容：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/selectProvince /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 步骤 6：配置 HTTPS（可选）

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## 📊 方案对比总结

| 方案 | 价格 | 难度 | 国内访问 | HTTPS | 推荐度 |
|------|------|------|----------|-------|--------|
| Render | 免费 | ⭐⭐ | ⭐⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ |
| Railway | 免费 | ⭐⭐ | ⭐⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ |
| PythonAnywhere | 免费 | ⭐⭐⭐ | ⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| Zeabur | 免费 | ⭐⭐ | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| 云服务器 | 付费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐ |

---

## 🎯 最终推荐

### 首选：Render
- ✅ 最简单快速
- ✅ 完全免费
- ✅ 自动部署
- ✅ HTTPS 支持

### 次选：Zeabur
- ✅ 国内访问快
- ✅ 现代化平台
- ✅ 完全免费

### 备选：PythonAnywhere
- ✅ 专业 Python 托管
- ✅ 稳定可靠
- ✅ 免费版可用

---

## 🔧 常见问题

### Q1: 免费版会休眠吗？
- **Render**: 免费版 15 分钟无访问会休眠，首次访问需等待 30 秒
- **Railway**: 免费版有休眠限制
- **PythonAnywhere**: 免费版不会休眠，但功能受限

### Q2: 如何避免休眠？
- 使用定时任务定期访问（如 Uptime Robot）
- 升级到付费版

### Q3: 如何绑定自定义域名？
- 在各平台控制台添加域名
- 配置 DNS 解析
- 自动获取 SSL 证书

### Q4: 如何查看日志？
- **Render**: 在控制台查看 "Logs"
- **Railway**: 在项目页面查看日志
- **PythonAnywhere**: 在 "Web" 标签查看日志

### Q5: 如何更新应用？
- 推送代码到 GitHub
- 平台会自动检测并重新部署

---

## 📞 技术支持

如有问题，请查阅：
- Render 文档：https://render.com/docs
- Railway 文档：https://docs.railway.app
- PythonAnywhere 文档：https://help.pythonanywhere.com