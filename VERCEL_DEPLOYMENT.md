# Vercel 部署指南

本指南帮助你将海元堂查询系统部署到 Vercel。

---

## ⚠️ Vercel 部署注意事项

### Vercel 的限制

Vercel 主要为 **Node.js/前端应用**设计，对 Python Flask 有以下限制：

| 项目 | 免费版限制 | Pro版限制 |
|------|-----------|----------|
| **执行时间** | 10秒 | 60秒 |
| **内存** | 1024 MB | 3008 MB |
| **并发请求** | 无限 | 无限 |
| **冷启动** | 有 | 有 |
| **文件系统** | 只读 | 只读 |

### 适用场景

✅ **适合**：
- API 接口调用
- 轻量级查询服务
- 响应时间 < 10秒的请求

❌ **不适合**：
- 长时间运行的任务
- 需要写入文件系统
- 大量数据处理
- WebSocket 长连接

### 本项目的兼容性

我们的应用：
- ✅ 主要是API调用和查询，适合Vercel
- ⚠️ 证照查询可能需要30秒（可能超时），建议优化或使用Render
- ✅ 无需文件写入
- ✅ 响应时间通常 < 5秒

---

## 🚀 部署步骤

### 方案一：通过 Vercel 网站部署（推荐）

#### 1. 准备工作

确保代码已推送到 GitHub：
```bash
git add .
git commit -m "配置Vercel部署"
git push origin main
```

#### 2. 注册并登录 Vercel

1. 访问 https://vercel.com
2. 点击 **"Sign Up"** 或 **"Login"**
3. 使用 **GitHub 账号**登录

#### 3. 导入项目

1. 在 Vercel Dashboard，点击 **"Add New..."** → **"Project"**
2. 在 "Import Git Repository" 中找到 `renbooc/selectProvince`
3. 点击 **"Import"**

#### 4. 配置项目

在配置页面：

| 配置项 | 值 |
|--------|-----|
| **Project Name** | `selectprovince` 或自定义 |
| **Framework Preset** | `Other` |
| **Root Directory** | `.` （默认） |
| **Build Command** | 留空 |
| **Output Directory** | 留空 |
| **Install Command** | `pip install -r requirements.txt` |

#### 5. 环境变量（可选）

如果需要配置环境变量：
- 点击 **"Environment Variables"**
- 添加变量（当前项目API密钥已在代码中配置）

#### 6. 部署

1. 点击 **"Deploy"** 按钮
2. 等待部署完成（约 1-2 分钟）
3. 部署成功后会显示访问 URL：`https://selectprovince.vercel.app`

---

### 方案二：通过 Vercel CLI 部署

#### 1. 安装 Vercel CLI

```bash
# 使用 npm（需要先安装 Node.js）
npm install -g vercel

# 或使用 pnpm
pnpm add -g vercel
```

#### 2. 登录

```bash
vercel login
```

选择使用 GitHub 登录

#### 3. 初始化项目

在项目目录中运行：
```bash
vercel
```

根据提示选择：
- Set up and deploy? **Y**
- Which scope? 选择你的账号
- Link to existing project? **N**
- What's your project's name? `selectprovince`
- In which directory is your code located? `./`

#### 4. 部署

```bash
# 部署到生产环境
vercel --prod
```

#### 5. 查看应用

部署成功后，CLI 会显示访问 URL

---

## 🔄 自动部署

配置完成后，每次推送代码到 GitHub，Vercel 会自动部署：

```bash
git add .
git commit -m "更新功能"
git push origin main

# Vercel 自动检测并部署
```

---

## ⚙️ 优化建议

### 1. 减少冷启动时间

在 `vercel.json` 中配置缓存：
```json
{
  "github": {
    "silent": true
  }
}
```

### 2. 处理超时问题

对于可能超时的请求（如证照查询）：

```python
# 在 app.py 中添加超时处理
@app.route("/api/certificates")
def api_certificates():
    try:
        # ... 原有代码 ...
        # 设置更短的超时时间
        timeout = 8  # Vercel免费版10秒限制，留2秒缓冲
    except requests.exceptions.Timeout:
        return jsonify({
            "success": False,
            "error": "请求超时，请稍后重试"
        })
```

### 3. 使用环境变量

创建 `.env.local`（不要提交到Git）：
```bash
AMAP_KEY=your_key_here
TENCENT_MAP_KEY=your_key_here
```

在 Vercel 中配置相同的环境变量。

---

## 🐛 故障排查

### 部署失败

**问题**：Build 失败
```bash
# 查看 Vercel 部署日志
# 通常是依赖安装问题
```

**解决方案**：
1. 检查 `requirements.txt` 是否正确
2. 确保 Python 版本兼容（3.9+）
3. 在 Vercel Dashboard 查看详细日志

### 应用超时

**问题**：Function execution timeout
```
Error: Function execution timed out after 10s
```

**解决方案**：
1. 优化 API 调用，减少等待时间
2. 使用 Vercel Pro（60秒限制）
3. 考虑改用 Render（无超时限制）

### 路由不工作

**问题**：404 Not Found

**解决方案**：
1. 检查 `vercel.json` 配置是否正确
2. 确保 `api/index.py` 正确导入 app
3. 清除 Vercel 缓存重新部署

### 静态文件无法访问

**问题**：模板或静态文件 404

**解决方案**：
```json
// 在 vercel.json 中添加静态文件路由
{
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

---

## 📊 监控和日志

### 查看日志

1. 进入 Vercel Dashboard
2. 选择你的项目
3. 点击 **"Logs"** 标签
4. 可以看到实时请求日志和错误信息

### 性能监控

Vercel 免费提供：
- **Analytics**：访问统计
- **Speed Insights**：性能指标
- **Web Vitals**：用户体验指标

在 Project Settings → Analytics 中启用。

---

## 💰 费用对比

| 套餐 | 价格 | 执行时间 | 带宽 | 推荐场景 |
|------|------|---------|------|---------|
| **Hobby（免费）** | $0 | 10秒 | 100 GB/月 | 个人项目、测试 |
| **Pro** | $20/月 | 60秒 | 1 TB/月 | 小型商业应用 |
| **Enterprise** | 定制 | 定制 | 定制 | 大型企业应用 |

---

## 🔄 从 Vercel 迁移到其他平台

如果 Vercel 不满足需求，可以轻松迁移到：

### 迁移到 Render（推荐）
```bash
# 无需修改代码
# 按照 DEPLOYMENT.md 中的 Render 部署步骤操作
```

### 迁移到 Railway
```bash
# 无需修改代码
# 按照 DEPLOYMENT.md 中的 Railway 部署步骤操作
```

---

## ⚡ Vercel vs Render 对比

| 特性 | Vercel | Render |
|------|--------|--------|
| **Python 支持** | 基础（Serverless） | 原生（Web Service） |
| **执行时间限制** | 10秒（免费） | 无限制 |
| **冷启动** | 快（全球CDN） | 中等（特定区域） |
| **价格** | $0 - $20/月 | $0 - $7/月 |
| **适合场景** | 前端为主的应用 | 后端服务 |
| **推荐度** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**建议**：
- 如果应用主要是轻量级API调用 → 使用 **Vercel**
- 如果有长时间运行的任务 → 使用 **Render**（推荐）

---

## 📝 最佳实践

### 1. 版本管理

在 `vercel.json` 中指定 Python 版本：
```json
{
  "env": {
    "PYTHON_VERSION": "3.9"
  }
}
```

### 2. 缓存优化

启用依赖缓存：
```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb"
      }
    }
  ]
}
```

### 3. 安全配置

配置 CORS 和安全头：
```python
# 在 app.py 中添加
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('X-Content-Type-Options', 'nosniff')
    return response
```

---

## 🆘 获取帮助

- **Vercel 文档**：https://vercel.com/docs
- **Python on Vercel**：https://vercel.com/docs/functions/runtimes/python
- **GitHub Issues**：https://github.com/renbooc/selectProvince/issues

---

## 总结

✅ **Vercel 适合**：
- 轻量级 API 服务
- 快速部署和迭代
- 全球 CDN 加速

⚠️ **Vercel 限制**：
- 10秒执行时间限制（免费版）
- 不适合长时间任务
- Serverless 架构

💡 **推荐**：
- 开发/测试阶段：使用 Vercel（快速部署）
- 生产环境：使用 Render（更稳定，无超时限制）
