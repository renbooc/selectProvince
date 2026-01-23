# Replit 快速部署指南（推荐）

**为什么推荐 Replit？**
- ✅ 完全免费，无需信用卡
- ✅ **无网络限制**，可以访问任何API
- ✅ 在线IDE，可直接编辑代码
- ✅ 5分钟完成部署
- ✅ 自动安装依赖

**适合本项目**：因为需要访问自定义API域名 `sk.hytyao.com`

---

## 🚀 快速部署步骤

### 1. 注册并登录

1. 访问 https://replit.com
2. 点击 **"Sign up"**
3. 使用 **GitHub** 账号登录（推荐）

### 2. 导入项目

1. 点击左侧的 **"+ Create Repl"** 按钮
2. 选择 **"Import from GitHub"** 标签
3. 在输入框中粘贴：
   ```
   https://github.com/renbooc/selectProvince
   ```
4. 点击 **"Import from GitHub"** 按钮

### 3. 自动配置

Replit 会自动：
- ✅ 检测 Python 项目
- ✅ 安装 `requirements.txt` 中的依赖
- ✅ 配置运行环境

### 4. 配置启动命令（如果需要）

如果 Replit 没有自动检测，手动配置：

#### 创建 `.replit` 文件

点击左侧的 **"+ Add file"**，创建 `.replit` 文件，内容：

```toml
run = "python app.py"
language = "python3"

[nix]
channel = "stable-22_11"

[deployment]
run = ["sh", "-c", "python app.py"]
```

#### 修改 `app.py` 最后部分

确保 `app.py` 末尾的运行配置适合 Replit：

```python
if __name__ == "__main__":
    # Replit 环境配置
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
```

### 5. 运行应用

1. 点击顶部的绿色 **"Run"** 按钮
2. Replit 会自动安装依赖并启动应用
3. 右侧会显示一个预览窗口和访问URL
4. 点击右上角的 **"Open in a new tab"** 图标获取完整URL

### 6. 获取公开URL

运行后，你会得到类似这样的URL：
```
https://selectprovince.renbooc.repl.co
```

---

## 🔄 保持应用在线（防止休眠）

Replit 免费版在 **1小时无活动后会休眠**。

### 使用 UptimeRobot（免费服务）

#### 1. 注册 UptimeRobot

访问 https://uptimerobot.com 并注册（免费，无需信用卡）

#### 2. 添加监控

1. 登录后点击 **"+ Add New Monitor"**
2. 配置监控：
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: `SelectProvince on Replit`
   - **URL**: 你的 Replit 应用URL
   - **Monitoring Interval**: 5 minutes
3. 点击 **"Create Monitor"**

#### 3. 完成

UptimeRobot 会每 5 分钟访问一次你的应用，防止休眠。

---

## ⚙️ 环境变量配置（可选）

如果需要配置环境变量：

### 在 Replit 中配置

1. 点击左侧工具栏的 **"Secrets"**（🔒 锁图标）
2. 点击 **"+ New Secret"**
3. 添加键值对，例如：
   - Key: `AMAP_KEY`
   - Value: `your_api_key_here`

### 在代码中使用

```python
import os

# 从环境变量读取
AMAP_KEY = os.environ.get("AMAP_KEY", "default_value")
```

---

## 🎨 自定义域名（可选）

### Replit 免费域名

默认域名格式：`https://projectname.username.repl.co`

### 自定义域名（需要付费）

Replit 的 Hacker 计划（$7/月）支持自定义域名。

---

## 🐛 常见问题

### 1. 应用启动失败

**检查步骤**：
1. 查看 **Console** 窗口的错误信息
2. 确认 `requirements.txt` 中的依赖是否正确
3. 点击 **"Shell"** 标签，手动安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 2. 应用可以本地运行但部署失败

**常见原因**：
- 端口配置问题
- 绑定地址问题

**解决方案**：
确保 `app.py` 中使用：
```python
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
```

### 3. 依赖安装失败

**解决方案**：
在 **Shell** 中手动安装：
```bash
pip install flask requests werkzeug gunicorn
```

### 4. 静态文件无法访问

Replit 会自动处理静态文件，无需额外配置。

### 5. 应用频繁休眠

使用 UptimeRobot 保持活跃（见上文）。

---

## 📊 性能优化

### 1. 使用 Gunicorn（可选）

修改 `.replit` 文件：
```toml
run = "gunicorn -w 2 -b 0.0.0.0:5000 app:app"
```

### 2. 启用缓存

在代码中添加响应缓存：
```python
from flask import Flask, make_response
from functools import wraps

def cache_response(timeout=300):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            response.headers['Cache-Control'] = f'public, max-age={timeout}'
            return response
        return decorated_function
    return decorator
```

---

## 🔄 更新部署

### 方法1：通过 GitHub（推荐）

1. 本地修改代码并推送到 GitHub
2. 在 Replit 中点击左侧 **"Version control"**
3. 点击 **"Pull"** 拉取最新代码
4. 点击 **"Run"** 重启应用

### 方法2：直接在 Replit 编辑

在 Replit 的在线编辑器中直接修改代码，保存后自动重启。

---

## 💰 费用对比

| 功能 | Free | Hacker ($7/月) | Pro ($20/月) |
|------|------|---------------|--------------|
| **运行时间** | 有休眠 | 永久在线 | 永久在线 |
| **CPU** | 0.5 vCPU | 2 vCPU | 4 vCPU |
| **内存** | 512 MB | 2 GB | 4 GB |
| **自定义域名** | ❌ | ✅ | ✅ |
| **私有项目** | 5个 | 无限 | 无限 |

**建议**：个人项目使用 Free + UptimeRobot 即可。

---

## 🆚 Replit vs PythonAnywhere

| 特性 | Replit | PythonAnywhere |
|------|--------|----------------|
| **网络访问** | ✅ 无限制 | ❌ 仅白名单 |
| **在线编辑** | ✅ 完整IDE | ⚠️ 基础编辑器 |
| **休眠** | 1小时后休眠 | 永不休眠 |
| **适合本项目** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

**结论**：因为本项目需要访问自定义API，**Replit 更适合**。

---

## 🎯 最佳实践

### 1. 代码结构

确保项目根目录有：
```
selectProvince/
├── app.py              # 主应用
├── requirements.txt    # 依赖
├── .replit            # Replit配置（可选）
├── templates/         # HTML模板
├── static/            # 静态文件（如果有）
└── other files...
```

### 2. 日志记录

在 Replit Console 中查看日志：
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("应用启动成功")
```

### 3. 错误处理

添加全局错误处理：
```python
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "服务器内部错误"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "页面未找到"}), 404
```

---

## 📱 移动端优化

应用已经适配移动端，无需额外配置。

---

## 🔐 安全建议

### 1. 使用环境变量

不要在代码中硬编码敏感信息，使用 Secrets：
```python
import os

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("请配置 API_KEY 环境变量")
```

### 2. 启用 HTTPS

Replit 自动提供 HTTPS，无需配置。

### 3. 限制请求频率

使用 Flask-Limiter：
```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

---

## 🆘 获取帮助

- **Replit 文档**: https://docs.replit.com
- **Replit 社区**: https://ask.replit.com
- **GitHub Issues**: https://github.com/renbooc/selectProvince/issues

---

## 🎉 总结

**Replit 优势**：
- ✅ 无网络限制（可访问任何API）
- ✅ 完全免费
- ✅ 部署简单
- ✅ 在线编辑

**适合本项目**：⭐⭐⭐⭐⭐

**立即部署**：https://replit.com/new/github/renbooc/selectProvince
