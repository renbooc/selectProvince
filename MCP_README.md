# 中国省份查询系统 - MCP Server版本

这是一个基于**高德地图MCP Server**的中国省份查询Web应用，支持通过城市名称、市级名称或县级名称实时查询对应的中国省份名称。

## 🚀 什么是MCP Server？

**MCP (Model Context Protocol)** 是AI时代的新型协议，类似于AI世界的"USB-C"接口。

### MCP的核心优势：
- 🤖 **AI原生**：专为AI智能体设计，大模型更容易理解
- ⚡ **实时流**：支持SSE实时数据流
- 🔌 **即插即用**：简单配置URL即可使用
- 🛡️ **零运维**：云端服务，无需服务器维护
- 📈 **持续升级**：自动获取最新功能和数据

## 🌟 功能特点

- 🎯 **实时查询**：通过高德MCP Server实时获取行政区划数据
- 🗺️ **完整覆盖**：支持省、市、县三级行政区划查询
- 💻 **简洁界面**：美观的Web界面，支持响应式设计
- 🔄 **智能回退**：MCP不可用时自动使用本地数据
- 📱 **多端适配**：支持PC和移动设备

## 📦 安装与配置

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd selectProvince

# 创建虚拟环境
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置高德MCP Server

#### 方法一：使用Web服务API Key

1. 访问 [高德开放平台](https://lbs.amap.com/dev/key)
2. 注册/登录账号
3. 创建新应用：
   - 应用名称：`ChinaProvinceQuery`
   - 应用类型：`Web服务`
4. 获取API Key
5. 编辑 `app_mcp.py`，设置Key：
   ```python
   AMAP_KEY = "你的高德Web服务Key"
   ```

#### 方法二：使用MCP SSE服务（推荐）

高德提供MCP Server SSE服务，可直接配置URL使用：
- **SSE地址**：`https://mcp.amap.com/sse`
- **认证方式**：API Key或Access Token

详细文档：[高德MCP Server文档](https://lbs.amap.com/api/mcp-server)

### 3. 启动服务

```bash
# 启动MCP版本（使用端口5001）
python app_mcp.py

# 访问地址
http://localhost:5001
```

## 🎮 使用方法

1. 在输入框中输入行政区划名称（如"祁东县"）
2. 点击"查询"按钮或按回车键
3. 系统将通过MCP Server实时查询并显示结果

### 查询示例

| 输入 | 结果 |
|------|------|
| 祁东县 | 湖南省衡阳市 |
| 北京市 | 北京市（直辖市） |
| 广州市 | 广东省 |
| 深圳市 | 广东省 |
| 成都市 | 四川省 |
| 武汉市 | 湖北省 |

## 🏗️ 架构说明

### MCP Server集成

```
用户请求 → Flask后端 → 高德MCP Server → 返回行政区划数据 → 显示结果
```

### 核心功能

1. **行政区划查询** (`search_with_mcp`)
   - 使用高德行政区划API
   - 支持模糊匹配
   - 返回完整层级信息

2. **SSE实时流** (`search_with_mcp_sse`)
   - 使用Server-Sent Events
   - 实时获取数据更新
   - 低延迟响应

3. **智能回退机制**
   - MCP Server不可用时
   - 自动切换到本地数据
   - 确保服务可用性

## 📚 MCP工具列表

高德MCP Server提供12大核心工具：

1. 📍 **地点搜索** - 关键词搜索地点
2. 🏛️ **行政区划查询** - 行政区划信息检索
3. 🧭 **地理编码** - 地址转坐标
4. 📍 **逆地理编码** - 坐标转地址
5. 🚗 **路径规划** - 多方式路线规划
6. 🚦 **实时交通** - 交通态势信息
7. 🌤️ **天气查询** - 天气预报服务
8. 🅿️ **周边搜索** - 附近POI检索
9. 📏 **距离测量** - 两点间距离计算
10. 🏢 **区域搜索** - 指定区域POI搜索
11. 🗺️ **生成专属地图** - 创建个性化地图
12. 📊 **数据可视化** - 地图数据展示

详细文档：[高德MCP Server API文档](https://lbs.amap.com/api/mcp-server)

## 🔧 开发指南

### 运行测试

```bash
# 测试MCP Server连接
http://localhost:5001/api/mcp/test

# 查看MCP状态
http://localhost:5001/api/mcp/status
```

### 添加新功能

```python
# 在app_mcp.py中添加新的MCP工具调用
def search_with_mcp_tool(tool_name, params):
    """调用指定的MCP工具"""
    url = f"https://restapi.amap.com/v3/{tool_name}"
    params['key'] = AMAP_KEY
    
    response = requests.get(url, params=params)
    return response.json()
```

## 🤝 与其他版本对比

| 特性 | MCP版本 | 传统API版本 |
|------|---------|-------------|
| 实时性 | ✅ 实时SSE流 | ✅ 需要轮询 |
| AI友好 | ✅ 语义化输出 | ⚠️ 原始JSON |
| 配置复杂度 | ⚠️ 需要MCP理解 | ✅ 简单直接 |
| 维护成本 | ✅ 零运维 | ⚠️ 需要维护 |
| 扩展性 | ✅ 12+工具 | ⚠️ 受限 |

## 📖 扩展阅读

- [MCP官方文档](https://modelcontextprotocol.info/)
- [高德MCP Server文档](https://lbs.amap.com/api/mcp-server)
- [高德开放平台](https://lbs.amap.com/)

## 📄 许可证

MIT License

---

💡 **提示**：如需更高级的M配置高德MCP ServerCP功能，建议 SSE服务，可获得12大核心API的完整能力。
