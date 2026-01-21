@echo off
echo 🚀 中国省份查询系统 - MCP Server版本
echo.
echo 📋 使用说明：
echo    1. 先配置API密钥（推荐）：python config_api.py
echo    2. 安装依赖：pip install -r requirements.txt
echo    3. 启动MCP版本服务：python app_mcp.py
echo.
echo 🌟 MCP Server优势：
echo    • AI原生设计，大模型易理解
echo    • SSE实时数据流，低延迟
echo    • 12大核心API工具
echo    • 零运维成本
echo.
echo 📖 文档：
echo    • MCP文档：https://lbs.amap.com/api/mcp-server
echo    • 高德Key：https://lbs.amap.com/dev/key
echo.
echo 🌐 正在启动MCP Server版本...
echo    请访问：http://localhost:5001
echo.
python app_mcp.py
pause
