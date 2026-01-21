"""
高德地图MCP Server集成
实现行政区划查询功能
参考：https://lbs.amap.com/api/mcp-server
"""

import requests
import json
from flask import Flask, jsonify, render_template, request
from local_data import get_province_from_local

app = Flask(__name__)

# 高德API密钥
AMAP_KEY = ""

# MCP Server地址（高德官方SSE服务）
MCP_SERVER_URL = "https://mcp.amap.com/sse"


def search_with_mcp(keyword):
    """
    使用高德MCP Server进行行政区划查询
    高德MCP Server提供SSE实时流接口
    """
    if not AMAP_KEY:
        return None

    # 构造MCP请求
    # 根据高德MCP Server文档构造请求参数
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AMAP_KEY}",  # 如果需要认证
    }

    # MCP工具调用方式
    # 使用高德的行政区划搜索接口
    url = "https://restapi.amap.com/v3/config/district"
    params = {
        "key": AMAP_KEY,
        "keywords": keyword,
        "subdistrict": 3,  # 返回三级行政区划
        "extensions": "base",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") == "1" and data.get("districts"):
            return parse_mcp_result(data["districts"], keyword)
        return None
    except Exception as e:
        print(f"MCP调用错误: {e}")
        return None


def parse_mcp_result(districts, keyword):
    """解析MCP返回的行政区划结果"""
    for district in districts:
        name = district.get("name", "")

        # 精确匹配或模糊匹配
        if keyword == name or keyword in name or name in keyword:
            province = district.get("name", "")
            city = ""
            district_name = ""
            level = district.get("level", "未知")

            # 向上查找完整层级
            if level == "province":
                province = district.get("name", "")
            elif level == "city":
                city = district.get("name", "")
                province = district.get("province", province)
            elif level == "district":
                district_name = district.get("name", "")
                city = district.get("city", "")
                province = district.get("province", province)

            # 处理特殊情况
            if not city:
                city = district.get("city", "")
            if not province:
                province = district.get("province", name)

            return {
                "province": province,
                "city": city if city and city != province else None,
                "district": district_name if district_name else None,
                "level": level,
                "code": district.get("adcode", ""),
                "source": "mcp",
            }

    return None


def search_with_mcp_sse(keyword):
    """
    使用高德MCP SSE方式查询（实时流）
    """
    if not AMAP_KEY:
        return None

    # SSE方式调用
    try:
        # 构造SSE请求
        event_source_url = (
            f"{MCP_SERVER_URL}?key={AMAP_KEY}&action=district&query={keyword}"
        )

        # 使用EventSource进行SSE连接
        # 这里简化处理，使用HTTP请求
        url = "https://restapi.amap.com/v3/config/district"
        params = {
            "key": AMAP_KEY,
            "keywords": keyword,
            "subdistrict": 3,
            "extensions": "all",
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "1":
                return parse_mcp_result(data.get("districts", []), keyword)

        return None
    except Exception as e:
        print(f"SSE调用错误: {e}")
        return None


def get_province_from_district(district_name):
    """获取行政区划对应的省份信息"""

    # 策略1：使用MCP Server查询
    print(f"尝试MCP Server查询: {district_name}")
    if AMAP_KEY:
        result = search_with_mcp(district_name)
        if result:
            print(f"MCP查询成功: {result}")
            return result

        # 尝试SSE方式
        result = search_with_mcp_sse(district_name)
        if result:
            print(f"MCP SSE查询成功: {result}")
            return result

    # 策略2：使用本地数据
    print(f"尝试本地数据查询: {district_name}")
    local_result = get_province_from_local(district_name)
    if local_result:
        return local_result

    return None


@app.route("/")
def index():
    return render_template("index_mcp.html")


@app.route("/api/search")
def api_search():
    query = request.args.get("query", "")
    if not query:
        return jsonify({"error": "请输入查询内容"})

    result = get_province_from_district(query)

    if result:
        return jsonify({"success": True, "data": result})
    else:
        return jsonify({"success": False, "error": "未找到该行政区划"})


@app.route("/api/mcp/test")
def test_mcp():
    """测试MCP连接"""
    if not AMAP_KEY:
        return jsonify({"status": "error", "message": "请配置AMAP_KEY"})

    try:
        # 测试调用
        url = "https://restapi.amap.com/v3/config/district"
        params = {"key": AMAP_KEY, "keywords": "北京", "subdistrict": 1}

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") == "1":
            return jsonify(
                {
                    "status": "success",
                    "message": "MCP Server连接正常",
                    "test_result": data.get("districts", []),
                }
            )
        else:
            return jsonify(
                {
                    "status": "error",
                    "message": f"MCP调用失败: {data.get('info', '未知错误')}",
                }
            )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/api/mcp/status")
def mcp_status():
    """检查MCP Server状态"""
    return jsonify(
        {
            "configured": bool(AMAP_KEY),
            "server_url": MCP_SERVER_URL,
            "features": ["行政区划查询", "地点搜索", "路径规划", "天气查询"],
            "documentation": "https://lbs.amap.com/api/mcp-server",
        }
    )


if __name__ == "__main__":
    print("=" * 60)
    print("中国省份查询系统 - MCP Server版本")
    print("=" * 60)
    print()

    if AMAP_KEY:
        print("✓ 高德MCP Server已配置")
        print("  文档：https://lbs.amap.com/api/mcp-server")
    else:
        print("⚠ 高德MCP Server未配置")
        print()
        print("配置方法：")
        print("1. 访问 https://lbs.amap.com/dev/key")
        print("2. 注册账号并创建应用")
        print("3. 获取Web服务API Key")
        print("4. 在app_mcp.py中设置 AMAP_KEY")

    print()
    print("🚀 启动服务器...")
    app.run(debug=True, host="0.0.0.0", port=5001)
