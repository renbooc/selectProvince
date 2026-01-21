# Vercel 部署操作指南

## ✅ 已完成
- [x] 代码已推送到 GitHub
- [x] vercel.json 配置文件已创建

---

## 📋 Vercel 部署步骤

### 步骤 1：访问 Vercel

1. 打开浏览器，访问：https://vercel.com
2. 点击右上角 "Sign Up" 或 "Login"
3. 使用 GitHub 账号登录（推荐）

### 步骤 2：创建新项目

1. 登录后，点击右上角 "Add New..."
2. 选择 "Project"

### 步骤 3：导入 GitHub 仓库

1. 在 "Import Git Repository" 页面
2. 找到 `renbooc/selectProvince` 仓库
3. 点击 "Import" 按钮

### 步骤 4：配置项目

填写以下配置：

| 配置项 | 值 |
|--------|-----|
| **Project Name** | `select-province` |
| **Framework Preset** | `Other` |
| **Root Directory** | `./` |
| **Build Command** | `pip install -r requirements.txt` |
| **Output Directory** | `.` |

### 步骤 5：配置环境变量

在 "Environment Variables" 部分添加：

| 变量名 | 值 | 环境 |
|--------|-----|------|
| `FLASK_DEBUG` | `False` | Production, Preview, Development |
| `PORT` | `5000` | Production, Preview, Development |

### 步骤 6：部署

1. 检查所有配置
2. 点击 "Deploy" 按钮
3. 等待 2-3 分钟

### 步骤 7：获取访问地址

部署成功后，您将获得：
```
https://select-province.vercel.app
```

---

## 🔍 部署验证

部署成功后，请检查：

- [ ] 应用可以正常访问
- [ ] 首页显示2个功能卡片
- [ ] 点击"销售网点查询"可以跳转
- [ ] 点击"客户查询"可以跳转
- [ ] 没有显示"快捷查询"区域

---

## 📊 监控和管理

### 查看日志

1. 在 Vercel 控制台
2. 点击项目名称
3. 点击 "Logs" 标签
4. 实时查看应用日志

### 查看部署历史

1. 点击 "Deployments" 标签
2. 查看所有部署记录
3. 可以回滚到之前的版本

### 查看域名

1. 点击 "Settings" 标签
2. 点击 "Domains"
3. 查看和配置域名

---

## 🔄 更新应用

当您需要更新代码时：

1. 修改代码
2. 提交到 Git：
   ```bash
   git add .
   git commit -m "更新描述"
   git push
   ```
3. Vercel 会自动检测并重新部署

---

## 🐛 常见问题排查

### 问题 1：部署失败 - Python 版本不兼容

**解决方案**：
1. 检查 `runtime.txt` 中的 Python 版本
2. Vercel 支持的 Python 版本：3.8, 3.9, 3.10, 3.11, 3.12
3. 如果使用 Python 3.13，需要修改 `runtime.txt`：
   ```
   python-3.12.0
   ```

### 问题 2：应用无法访问

**可能原因**：
- 应用还在部署中
- 端口配置错误

**解决方案**：
1. 等待部署完成
2. 检查 `app.py` 中的 `host="0.0.0.0"`
3. 确认环境变量 `PORT` 设置正确

### 问题 3：页面显示 404

**可能原因**：
- 路由配置错误
- `vercel.json` 配置错误

**解决方案**：
1. 检查 `vercel.json` 配置
2. 确认路由配置正确：
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```

---

## 💡 优化建议

### 1. 绑定自定义域名

1. 在 Vercel 控制台
2. 点击 "Settings" → "Domains"
3. 添加自定义域名
4. 配置 DNS 解析

### 2. 启用预览部署

Vercel 默认为每个 Git 分支创建预览部署：
- 推送到 `main` 分支 → 生产部署
- 推送到其他分支 → 预览部署

### 3. 配置环境变量

为不同环境配置不同的环境变量：
- Production: 生产环境
- Preview: 预览环境
- Development: 开发环境

---

## 📞 技术支持

- Vercel 文档：https://vercel.com/docs
- Vercel 社区：https://vercel.com/community
- GitHub Issues：https://github.com/vercel/vercel/issues

---

## 🎉 部署成功后

恭喜！您的应用已成功部署到 Vercel！

**访问地址**：`https://select-province.vercel.app`

**优势**：
- ✅ 全球 CDN 加速
- ✅ 自动 HTTPS
- ✅ 自动部署
- ✅ 免费额度充足
- ✅ 国内访问速度较快

享受您的线上应用吧！🚀