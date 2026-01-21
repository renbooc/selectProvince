# 销售网点查询系统

一个基于Python Flask的Web应用，可以通过城市名称查询对应的中国省份及客户分配信息。

## 🚀 三种运行方式

### 1. Web版本（推荐）

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py

# 访问 http://localhost:5000
```

### 2. 桌面版（.exe）

将项目打包成Windows桌面应用，双击即可运行。

#### 打包步骤：

**方式一：使用打包脚本**
```bash
python build_desktop.py
```

**方式二：使用批处理文件**
```bash
build.bat
```

**方式三：手动打包**
```bash
# 安装PyInstaller
pip install pyinstaller

# 打包
pyinstaller --onefile --windowed --name "销售网点查询系统" --add-data "templates;templates" app.py
```

#### 输出目录：
```
dist/销售网点查询系统.exe
```

双击 `销售网点查询系统.exe` 即可运行，无需Python环境！

### 3. MCP Server版本

基于高德地图MCP协议的版本。

```bash
python app_mcp.py
# 访问 http://localhost:5001
```

## 📋 功能特性

- ✅ 行政区域查询（省/市/县）
- ✅ 城市介绍
- ✅ 客户分配信息（省区经理 + 客服）
- ✅ 模糊搜索
- ✅ 现代化Web界面
- ✅ 响应式设计
- ✅ 离线可用（本地数据）

## 📦 文件结构

```
selectProvince/
├── app.py              # Web版本主程序
├── app_mcp.py          # MCP Server版本
├── build_desktop.py    # 桌面版打包脚本
├── build.bat           # 打包批处理
├── customer_data.py    # 客户分配数据
├── local_data.py       # 行政区划数据
├── requirements.txt    # Python依赖
├── templates/
│   ├── index.html      # Web界面
│   └── customer.html   # 客户查询页面
└── README.md           # 说明文档
```

## 🔧 配置API密钥

### 高德地图API（可选）

1. 访问 [高德开放平台](https://lbs.amap.com/dev/key)
2. 注册账号，创建应用，获取Web服务API Key
3. 在 `app.py` 中设置：
   ```python
   AMAP_KEY = "你的API Key"
   ```

## 📝 使用说明

1. 输入城市/区县名称（如：祁东县、汕头市）
2. 点击查询或按回车
3. 查看结果：
   - 所属省份
   - 城市/区县
   - 城市介绍
   - 省区经理
   - 客服

## 📄 许可证

MIT License
