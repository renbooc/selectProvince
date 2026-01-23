# 完全免费部署方案（无需信用卡）

本指南提供**真正免费、不需要信用卡**的部署方案。

---

## 🎯 平台对比

| 平台 | 免费套餐 | 需要信用卡 | Python支持 | 网络限制 | 推荐指数 | 限制 |
|------|---------|-----------|-----------|---------|---------|------|
| **Replit** | ✅ | ❌ | ✅ 完整 | ✅ 无限制 | ⭐⭐⭐⭐⭐ | 需保持活跃 |
| **PythonAnywhere** | ✅ | ❌ | ✅ 完整 | ⚠️ 仅白名单 | ⭐⭐⭐ | 每日流量限制 |
| **Koyeb** | ✅ | ❌ | ✅ | ✅ 无限制 | ⭐⭐⭐⭐ | 100GB流量/月 |
| **Glitch** | ✅ | ❌ | ✅ | ✅ 无限制 | ⭐⭐⭐ | 5分钟无活动休眠 |

**⚠️ 重要提示**：
- **PythonAnywhere 免费版只能访问白名单网站**，不适合需要访问自定义API域名的项目
- 本项目需要访问 `sk.hytyao.com`，建议使用 **Replit** 或 **Koyeb**

**强烈推荐**：**Replit** - 无网络限制，完全免费，适合本项目

---

## 方案一：PythonAnywhere 部署（强烈推荐）⭐⭐⭐⭐⭐

### 优势

- ✅ **完全免费**，无需信用卡
- ✅ **专为Python设计**，原生支持Flask
- ✅ **永久在线**，不休眠
- ✅ **简单易用**，Web界面管理
- ✅ **稳定可靠**，老牌Python托管平台
- ✅ **自带MySQL数据库**
- ✅ **提供SSH访问**

### 限制

- 📊 每日流量限制：100,000次请求/天
- 🌐 只能绑定 `username.pythonanywhere.com` 域名
- 🔄 每3个月需要手动续期免费账号
- ⏱️ CPU时间限制：100秒/天（通常足够）

### 详细步骤

#### 1. 注册账号

1. 访问 https://www.pythonanywhere.com
2. 点击 **"Pricing & signup"**
3. 选择 **"Create a Beginner account"**（完全免费）
4. 填写信息：
   - Username: `yourusername`（将成为你的域名）
   - Email: 你的邮箱
   - Password: 设置密码
5. 点击 **"Register"**，验证邮箱

#### 2. 上传代码

**方法A：从GitHub克隆（推荐）**

1. 登录后，点击顶部的 **"Consoles"** 标签
2. 点击 **"Bash"** 启动命令行
3. 在Bash中运行：

```bash
# 克隆项目
git clone https://github.com/renbooc/selectProvince.git
cd selectProvince

# 安装依赖
pip3 install --user -r requirements.txt
```

**方法B：手动上传**

1. 点击 **"Files"** 标签
2. 上传项目文件到 `/home/yourusername/selectProvince/`

#### 3. 创建Web应用

1. 点击顶部的 **"Web"** 标签
2. 点击 **"Add a new web app"**
3. 选择域名：`yourusername.pythonanywhere.com`（点击Next）
4. 选择 Python 框架：**"Flask"**
5. 选择 Python 版本：**"Python 3.10"**
6. 选择路径：`/home/yourusername/selectProvince/app.py`

#### 4. 配置WSGI文件

1. 在 **"Web"** 标签页，找到 **"Code"** 部分
2. 点击 WSGI configuration file 的链接（如：`/var/www/yourusername_pythonanywhere_com_wsgi.py`）
3. 删除所有内容，替换为：

```python
import sys
import os

# 添加项目路径
project_home = '/home/yourusername/selectProvince'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# 导入Flask应用
from app import app as application
```

**注意**：将 `yourusername` 替换为你的实际用户名

4. 点击 **"Save"** 保存

#### 5. 配置静态文件（重要）

在 **"Web"** 标签的 **"Static files"** 部分：

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/selectProvince/static/` |

点击 **"Save"** 保存

#### 6. 重启Web应用

1. 滚动到页面顶部
2. 点击绿色的 **"Reload yourusername.pythonanywhere.com"** 按钮
3. 等待几秒钟

#### 7. 访问应用

访问：`https://yourusername.pythonanywhere.com`

---

## 方案二：Replit 部署

### 优势

- ✅ 完全免费，无需信用卡
- ✅ 在线IDE，可以直接编辑代码
- ✅ 自动检测和安装依赖
- ✅ 支持多种编程语言

### 限制

- ⏱️ 1小时无活动后休眠
- 🔄 需要定期访问保持活跃
- 📊 有资源限制

### 步骤

#### 1. 注册Replit

1. 访问 https://replit.com
2. 点击 **"Sign up"**
3. 使用 GitHub 或 Google 账号登录

#### 2. 导入项目

1. 点击 **"+ Create Repl"**
2. 选择 **"Import from GitHub"**
3. 输入仓库URL：`https://github.com/renbooc/selectProvince`
4. 点击 **"Import from GitHub"**

#### 3. 配置运行

Replit会自动检测项目，如果没有：

1. 创建 `.replit` 文件：
```toml
run = "python app.py"
language = "python3"

[nix]
channel = "stable-22_11"
```

2. 创建 `replit.nix` 文件：
```nix
{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.python310Packages.flask
    pkgs.python310Packages.requests
  ];
}
```

#### 4. 运行应用

1. 点击顶部的 **"Run"** 按钮
2. Replit会自动安装依赖并启动应用
3. 右侧会显示应用URL

#### 5. 保持在线（可选）

使用 UptimeRobot 等服务每5分钟ping一次你的应用URL，防止休眠。

---

## 方案三：Koyeb 部署

### 优势

- ✅ 免费，无需信用卡
- ✅ 全球CDN
- ✅ 自动从GitHub部署
- ✅ 免费SSL

### 限制

- 📊 100GB流量/月
- 💾 512MB内存

### 步骤

#### 1. 注册Koyeb

1. 访问 https://www.koyeb.com
2. 点击 **"Start for free"**
3. 使用 GitHub 账号登录（无需信用卡）

#### 2. 创建应用

1. 点击 **"Create App"**
2. 选择 **"GitHub"** 作为部署方式
3. 选择仓库：`renbooc/selectProvince`
4. 配置：
   - **Build command**: `pip install -r requirements.txt`
   - **Run command**: `gunicorn app:app`
   - **Port**: `8000`
5. 点击 **"Deploy"**

#### 3. 等待部署

部署完成后，会显示应用URL

---

## 方案四：Glitch 部署

### 优势

- ✅ 免费，无需信用卡
- ✅ 在线编辑器
- ✅ 即时预览

### 限制

- ⏱️ 5分钟无活动后休眠
- 📊 有资源限制

### 步骤

#### 1. 注册Glitch

1. 访问 https://glitch.com
2. 使用 GitHub 或 Email 注册

#### 2. 导入项目

1. 点击 **"New Project"**
2. 选择 **"Import from GitHub"**
3. 输入：`https://github.com/renbooc/selectProvince`

#### 3. 配置

Glitch会自动检测Python项目

#### 4. 访问

点击 **"Show"** 查看应用

---

## 🔧 通用配置：环境变量

如果需要配置环境变量（API密钥等）：

### PythonAnywhere
在 Web 标签页的 **"Environment variables"** 部分添加

### Replit
在左侧工具栏找到 **"Secrets"**（锁图标），添加环境变量

### Koyeb
在应用设置的 **"Environment variables"** 中添加

---

## 🆓 保持免费服务在线

对于会休眠的服务（Replit、Glitch），使用以下方法保持活跃：

### UptimeRobot（免费监控服务）

1. 访问 https://uptimerobot.com
2. 注册免费账号
3. 添加监控：
   - Monitor Type: HTTP(s)
   - URL: 你的应用URL
   - Monitoring Interval: 5分钟
4. UptimeRobot会每5分钟访问你的应用，防止休眠

### Cron-job.org（免费定时任务）

1. 访问 https://cron-job.org
2. 注册账号
3. 创建定时任务ping你的应用

---

## 📊 平台详细对比

### 性能对比

| 平台 | 启动速度 | 稳定性 | 适合场景 |
|------|---------|--------|---------|
| **PythonAnywhere** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 生产环境（推荐） |
| **Replit** | ⭐⭐⭐⭐ | ⭐⭐⭐ | 开发测试 |
| **Koyeb** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 小型应用 |
| **Glitch** | ⭐⭐⭐ | ⭐⭐⭐ | 快速原型 |

### 流量限制对比

| 平台 | 每月流量 | 每日请求 | 带宽 |
|------|---------|---------|------|
| **PythonAnywhere** | 无限 | 100,000次 | 足够个人/小型项目 |
| **Replit** | 无限 | 无限 | 有CPU限制 |
| **Koyeb** | 100GB | 无限 | 良好 |
| **Glitch** | 无限 | 4000次/小时 | 足够测试 |

---

## 💡 推荐方案

### 个人项目/学习：
**首选：PythonAnywhere**
```
✅ 永久在线
✅ 稳定可靠
✅ 足够的免费额度
```

### 开发测试：
**首选：Replit**
```
✅ 在线编辑器
✅ 快速迭代
✅ 即时预览
```

### 快速展示：
**首选：Glitch**
```
✅ 最简单
✅ 即时部署
```

---

## 🎯 PythonAnywhere 详细配置技巧

### 1. 自定义域名（免费版不支持）

免费版只能使用 `username.pythonanywhere.com`，如需自定义域名需升级

### 2. 查看日志

在 **"Web"** 标签页：
- **Error log** - 查看错误日志
- **Server log** - 查看访问日志

### 3. 定时任务（免费版不支持）

免费版不支持定时任务，需要升级到付费版

### 4. 续期免费账号

免费账号每3个月需要续期：
1. 登录后会看到提示
2. 点击 **"Extend"** 按钮即可
3. 操作简单，不会丢失数据

### 5. 更新代码

```bash
# 在 Bash 控制台
cd ~/selectProvince
git pull origin main
pip install --user -r requirements.txt

# 在 Web 标签页点击 Reload
```

### 6. 数据库（可选）

免费版提供 MySQL 数据库：
1. 点击 **"Databases"** 标签
2. 创建数据库
3. 在代码中使用提供的连接信息

---

## 🔧 故障排查

### PythonAnywhere

**问题：应用无法访问**
```bash
# 检查步骤：
1. Web标签页确认应用状态为 "Enabled"
2. 检查 Error log 中的错误信息
3. 确认 WSGI 配置文件正确
4. 点击 Reload 重启应用
```

**问题：导入模块失败**
```bash
# 解决方案：
1. 在 Bash 控制台重新安装依赖
cd ~/selectProvince
pip3 install --user -r requirements.txt

2. 检查 WSGI 文件中的路径是否正确
```

**问题：静态文件404**
```bash
# 解决方案：
在 Web 标签的 Static files 中配置正确的路径
```

### Replit

**问题：应用休眠**
```
使用 UptimeRobot 每5分钟ping一次
```

**问题：依赖安装失败**
```
在 Secrets 中添加：
PYTHONUSERBASE=/home/runner/.local
```

---

## 📱 移动端访问

所有平台部署后的应用都支持移动端访问，自适应屏幕大小。

---

## 🆘 技术支持

- **PythonAnywhere论坛**：https://www.pythonanywhere.com/forums/
- **Replit社区**：https://ask.replit.com/
- **GitHub Issues**：https://github.com/renbooc/selectProvince/issues

---

## 总结

| 需求 | 推荐平台 | 理由 |
|------|---------|------|
| 稳定的生产环境 | **PythonAnywhere** | 永久在线，无需信用卡 |
| 快速测试 | **Replit** | 即时部署，在线编辑 |
| 临时展示 | **Glitch** | 最简单快速 |
| 全球访问 | **Koyeb** | CDN加速 |

**最推荐**：**PythonAnywhere** - 专业、稳定、完全免费！🎉
