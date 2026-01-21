# Render 部署操作指南

## ✅ 已完成
- [x] 代码已推送到 GitHub
- [x] 部署文件已创建（Procfile, runtime.txt, .gitignore）

---

## 📋 Render 部署步骤

### 步骤 1：访问 Render

1. 打开浏览器，访问：https://render.com
2. 点击右上角 "Sign Up" 或 "Login"
3. 使用 GitHub 账号登录（推荐）

### 步骤 2：创建 Web Service

1. 登录后，点击右上角 "+" 按钮
2. 选择 "New Web Service"

### 步骤 3：连接 GitHub 仓库

1. 在 "Connect a repository" 页面
2. 搜索或找到 `renbooc/selectProvince` 仓库
3. 点击 "Connect" 按钮
4. 如果提示授权，点击 "Authorize render"

### 步骤 4：配置部署参数

填写以下配置：

| 配置项 | 值 | 说明 |
|--------|-----|------|
| **Name** | `select-province` | 应用名称 |
| **Region** | `Oregon (US West)` | 或选择 `Singapore`（国内访问更快） |
| **Branch** | `main` | Git 分支 |
| **Runtime** | `Python 3` | 运行环境 |
| **Build Command** | `pip install -r requirements.txt` | 构建命令 |
| **Start Command** | `python app.py` | 启动命令 |
| **Instance Type** | `Free` | 免费实例 |

### 步骤 5：配置环境变量（可选但推荐）

点击 "Advanced" 按钮，在 "Environment Variables" 部分添加：

| 变量名 | 值 |
|--------|-----|
| `FLASK_DEBUG` | `False` |
| `PORT` | `5000` |

### 步骤 6：创建并部署

1. 检查所有配置是否正确
2. 点击 "Create Web Service" 按钮
3. 等待 2-5 分钟

### 步骤 7：查看部署状态

1. 部署开始后，会自动跳转到 "Events" 页面
2. 查看部署进度：
   - 🟡 **In Progress** - 正在部署
   - 🟢 **Live** - 部署成功
   - 🔴 **Failed** - 部署失败

### 步骤 8：获取访问地址

部署成功后，会显示：
- **URL**: `https://select-province.onrender.com`
- 点击该链接即可访问应用

---

## 🔍 部署验证

### 检查清单

- [ ] 应用可以正常访问
- [ ] 首页显示2个功能卡片
- [ ] 点击"销售网点查询"可以跳转
- [ ] 点击"客户查询"可以跳转
- [ ] 没有显示"快捷查询"区域

---

## 📊 监控和管理

### 查看日志

1. 在 Render 控制台
2. 点击 "Logs" 标签
3. 实时查看应用日志

### 查看指标

1. 点击 "Metrics" 标签
2. 查看 CPU、内存、网络使用情况

### 查看事件

1. 点击 "Events" 标签
2. 查看部署历史和事件记录

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
3. Render 会自动检测并重新部署

---

## 🐛 常见问题排查

### 问题 1：部署失败

**可能原因**：
- `Procfile` 文件缺失或格式错误
- `requirements.txt` 文件缺失
- Python 版本不兼容

**解决方案**：
1. 查看 "Logs" 获取详细错误信息
2. 确保所有必需文件存在
3. 检查 `runtime.txt` 中的 Python 版本

### 问题 2：应用无法访问

**可能原因**：
- 应用还在部署中
- 应用已休眠
- 端口配置错误

**解决方案**：
1. 等待部署完成
2. 访问应用唤醒（首次访问可能需要30秒）
3. 检查 `app.py` 中的 `host="0.0.0.0"`

### 问题 3：页面显示错误

**可能原因**：
- 模板文件路径错误
- 静态文件缺失

**解决方案**：
1. 查看 "Logs" 获取错误信息
2. 确认 `templates/` 文件夹存在
3. 确认所有 HTML 文件正确

---

## 💡 优化建议

### 1. 避免休眠

使用 Uptime Robot 等工具定期访问应用：
- 注册：https://uptimerobot.com
- 添加监控：`https://select-province.onrender.com`
- 设置每 5 分钟检查一次

### 2. 绑定自定义域名

1. 在 Render 控制台
2. 点击 "Domains" 标签
3. 添加自定义域名
4. 配置 DNS 解析

### 3. 升级实例

如果免费版不够用：
- 点击 "Settings" 标签
- 选择 "Change Instance Type"
- 升级到付费实例

---

## 📞 技术支持

- Render 文档：https://render.com/docs
- Render 社区：https://community.render.com
- GitHub Issues：https://github.com/render/render/issues

---

## 🎉 部署成功后

恭喜！您的应用已成功部署到线上！

**访问地址**：`https://select-province.onrender.com`

**功能**：
- ✅ 销售网点查询
- ✅ 客户查询
- ✅ HTTPS 加密
- ✅ 自动部署
- ✅ 完全免费

享受您的线上应用吧！🚀