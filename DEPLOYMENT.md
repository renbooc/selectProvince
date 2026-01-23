# 海元堂查询系统 - 部署指南

本文档提供多种部署方案。

## 🎯 快速选择

| 平台 | 推荐指数 | 免费额度 | 适合场景 | 详细文档 |
|------|---------|---------|----------|---------|
| **Render** | ⭐⭐⭐⭐⭐ | 750小时/月 | 生产环境（推荐） | 本文档 |
| **Vercel** | ⭐⭐⭐ | 100GB流量/月 | 开发测试 | [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) |
| **Railway** | ⭐⭐⭐⭐ | $5/月 | 中小型应用 | 本文档 |
| **Fly.io** | ⭐⭐⭐⭐ | 3个VM | 全球部署 | 本文档 |

**推荐**：生产环境使用 **Render**，开发测试使用 **Vercel**

---

## 方案一：Render 部署（推荐）⭐

**优势**：
- ✅ 免费套餐，无需信用卡
- ✅ 自动从 GitHub 部署
- ✅ 支持 Python/Flask
- ✅ 提供免费 HTTPS
- ✅ 自动重启和健康检查

### 步骤：

#### 1. 准备工作
确保代码已推送到 GitHub：
```bash
git add .
git commit -m "准备部署到Render"
git push origin main
```

#### 2. 注册 Render 账号
访问 https://render.com 并使用 GitHub 账号登录

#### 3. 创建 Web Service

1. 点击 **"New +"** → **"Web Service"**
2. 连接你的 GitHub 仓库：`renbooc/selectProvince`
3. 配置部署参数：

| 配置项 | 值 |
|--------|-----|
| Name | `selectProvince` 或自定义名称 |
| Runtime | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Plan | `Free` |

4. 点击 **"Create Web Service"**

#### 4. 等待部署完成
- 首次部署需要 3-5 分钟
- 部署日志会实时显示在控制台
- 部署成功后会显示访问 URL（如：`https://selectprovince.onrender.com`）

#### 5. 配置环境变量（可选）
如果需要配置环境变量：
- 进入 Service 设置页面
- 点击 **"Environment"**
- 添加环境变量（如 API 密钥）

---

## 方案二：Railway 部署

**优势**：
- ✅ $5 免费额度/月
- ✅ 部署快速
- ✅ 自动 HTTPS

### 步骤：

#### 1. 注册 Railway
访问 https://railway.app 并使用 GitHub 登录

#### 2. 创建新项目
```bash
1. 点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 选择 renbooc/selectProvince
4. Railway 会自动检测 Python 项目并部署
```

#### 3. 配置启动命令
在项目设置中添加：
- **Start Command**: `gunicorn app:app`
- **Port**: `5000`（自动检测）

#### 4. 获取访问 URL
部署完成后，Railway 会提供一个 `.railway.app` 域名

---

## 方案三：Fly.io 部署

**优势**：
- ✅ 全球 CDN
- ✅ 免费额度
- ✅ 支持 Docker

### 步骤：

#### 1. 安装 Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

#### 2. 登录 Fly.io
```bash
fly auth login
```

#### 3. 初始化应用
```bash
fly launch
```

根据提示选择：
- App name: `selectprovince` 或自定义
- Region: 选择最近的区域（如 Hong Kong）
- PostgreSQL: No
- Redis: No

#### 4. 部署
```bash
fly deploy
```

#### 5. 查看应用
```bash
fly open
```

---

## 方案四：自有服务器部署

### 使用 Nginx + Gunicorn

#### 1. 安装依赖
```bash
# 安装 Python 和必要工具
sudo apt update
sudo apt install python3 python3-pip nginx

# 安装项目依赖
pip3 install -r requirements.txt
```

#### 2. 配置 Gunicorn
创建 systemd 服务文件 `/etc/systemd/system/selectprovince.service`：

```ini
[Unit]
Description=海元堂查询系统
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/selectProvince
Environment="PATH=/usr/local/bin"
ExecStart=/usr/local/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

#### 3. 配置 Nginx
创建配置文件 `/etc/nginx/sites-available/selectprovince`：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 4. 启动服务
```bash
# 启用并启动应用
sudo systemctl enable selectprovince
sudo systemctl start selectprovince

# 启用 Nginx 配置
sudo ln -s /etc/nginx/sites-available/selectprovince /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 5. 配置 HTTPS（使用 Let's Encrypt）
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 部署后检查清单

✅ 应用可以正常访问
✅ 省份查询功能正常
✅ 客户分配查询正常
✅ 客户名称查询正常
✅ 证照查询功能正常
✅ API 响应时间合理（< 3秒）
✅ 日志正常记录

---

## 故障排查

### 应用无法启动
```bash
# 检查日志
# Render: 在控制台查看 Logs
# Railway: railway logs
# Fly.io: fly logs

# 常见问题：
# 1. 缺少依赖 → 检查 requirements.txt
# 2. 端口配置错误 → 确保监听 0.0.0.0
# 3. 启动命令错误 → 使用 gunicorn app:app
```

### API 调用失败
```bash
# 检查环境变量配置
# 确保 API 密钥配置正确
# 检查网络出站规则
```

### 性能问题
```bash
# 增加 Gunicorn worker 数量
gunicorn -w 4 app:app  # 4个worker进程

# 使用更高性能的计划（Render/Railway付费版）
```

---

## 监控和维护

### Render 监控
- 在 Dashboard 查看 CPU/内存使用情况
- 设置健康检查端点
- 配置日志保留策略

### 更新部署
```bash
# 推送代码到 GitHub，自动触发部署
git push origin main

# Render/Railway 会自动检测更新并重新部署
```

---

## 推荐配置

**生产环境推荐**：
- **小型应用**（日访问 < 1000）：Render Free
- **中型应用**（日访问 1000-10000）：Render Starter（$7/月）或 Railway
- **大型应用**（日访问 > 10000）：自有服务器或云服务器

---

## 技术支持

- GitHub Issues: https://github.com/renbooc/selectProvince/issues
- 项目文档: README.md

---

## 注意事项

⚠️ **安全提示**：
1. 不要在代码中硬编码敏感信息（API密钥、数据库密码）
2. 使用环境变量管理配置
3. 定期更新依赖包
4. 启用 HTTPS
5. 配置适当的 CORS 策略

📝 **免费套餐限制**：
- Render Free：服务在15分钟无活动后休眠，首次访问需等待唤醒（约30秒）
- Railway：每月 $5 免费额度，超出后需付费
- Fly.io：有一定的免费请求额度

🎯 **性能优化**：
- 使用 CDN 加速静态资源
- 启用 Gzip 压缩
- 配置缓存策略
- 使用数据库连接池
