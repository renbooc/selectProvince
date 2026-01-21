# -*- coding: utf-8 -*-
"""
销售网点查询系统 - 桌面应用版本
使用 pywebview 在桌面窗口中显示Web应用
"""

import sys
import threading
import webview
from flask import Flask, render_template, request, jsonify
from customer_data import (
    get_customer_by_province,
    get_all_data,
    get_data_by_customer_service,
    get_data_by_manager,
)
from local_data import get_province_from_local
import requests

# Flask应用
app = Flask(__name__)

# 高德地图API密钥
AMAP_KEY = ""
TENCENT_MAP_KEY = ""


# ============ API调用函数 ============


def search_with_amap(keyword):
    """使用高德地图API查询行政区划"""
    if not AMAP_KEY:
        return None

    url = "https://restapi.amap.com/v3/config/district"
    params = {
        "key": AMAP_KEY,
        "keywords": keyword,
        "subdistrict": 3,
        "extensions": "base",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") == "1" and data.get("districts"):
            return data["districts"]
        return None
    except Exception:
        return None


def search_with_tencent(keyword):
    """使用腾讯地图API查询行政区划"""
    if not TENCENT_MAP_KEY:
        return None

    url = "https://apis.map.qq.com/ws/district/v1/search"
    params = {"keyword": keyword, "key": TENCENT_MAP_KEY, "output": "json"}

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") == 0:
            return data.get("result", [])
        return None
    except Exception:
        return None


# ============ 解析函数 ============


def parse_amap_result(districts, keyword):
    """解析高德API返回结果"""
    if not districts:
        return None

    level_map = {"province": "省级", "city": "市级", "district": "县级"}
    keyword = keyword.strip()

    for district in districts:
        name = district.get("name", "")
        level = district.get("level", "")

        if keyword == name or keyword in name or name in keyword:
            province = ""
            city = ""
            district_name = ""

            if level == "province":
                province = name
            elif level == "city":
                city = name
            elif level == "district":
                district_name = name
                city = district.get("city", "")
                province = district.get("province", "")

            result = {
                "province": province,
                "city": city,
                "district": district_name,
                "level": level_map.get(level, level),
                "code": district.get("adcode", ""),
                "intro": "",
            }

            if not result["province"]:
                local_result = get_province_from_local(keyword)
                if local_result:
                    result["province"] = local_result.get("province", "")
                    result["city"] = local_result.get("city", "") or result["city"]
                    result["district"] = (
                        local_result.get("district", "") or result["district"]
                    )

            local_result = get_province_from_local(keyword)
            if local_result and local_result.get("intro"):
                result["intro"] = local_result["intro"]

            return result

    return None


def parse_tencent_result(results, keyword):
    """解析腾讯API返回结果"""
    if not results or len(results) == 0:
        return None

    level_map = {"province": "省级", "city": "市级", "district": "县级"}

    if not results[0] or len(results[0]) == 0:
        return None

    province_district = results[0][0]
    province = province_district.get("fullname", province_district.get("name", ""))

    result = {
        "province": province,
        "level": "省级",
        "code": province_district.get("id", ""),
        "intro": "",
    }

    if len(results) > 1 and results[1] and len(results[1]) > 0:
        city_district = results[1][0]
        result["city"] = city_district.get("fullname", city_district.get("name", ""))
        result["level"] = "市级"
        result["code"] = city_district.get("id", "")

    if len(results) > 2 and results[2] and len(results[2]) > 0:
        district_district = results[2][0]
        result["district"] = district_district.get(
            "fullname", district_district.get("name", "")
        )
        result["level"] = "县级"
        result["code"] = district_district.get("id", "")

    local_result = get_province_from_local(keyword)
    if local_result and local_result.get("intro"):
        result["intro"] = local_result["intro"]

    return result


# ============ 主查询函数 ============


def get_province_from_district(district_name):
    """获取行政区划对应的省份信息"""
    if AMAP_KEY:
        result = search_with_amap(district_name)
        if result:
            parsed = parse_amap_result(result, district_name)
            if parsed and parsed.get("province"):
                customer_info = get_customer_by_province(parsed.get("province", ""))
                if customer_info:
                    parsed["manager"] = customer_info.get("manager")
                    parsed["customer_service"] = customer_info.get("customer_service")
                return parsed

    if TENCENT_MAP_KEY:
        result = search_with_tencent(district_name)
        if result:
            parsed = parse_tencent_result(result, district_name)
            if parsed and parsed.get("province"):
                customer_info = get_customer_by_province(parsed.get("province", ""))
                if customer_info:
                    parsed["manager"] = customer_info.get("manager")
                    parsed["customer_service"] = customer_info.get("customer_service")
                return parsed

    local_result = get_province_from_local(district_name)
    if local_result and local_result.get("province"):
        customer_info = get_customer_by_province(local_result.get("province", ""))
        if customer_info:
            local_result["manager"] = customer_info.get("manager")
            local_result["customer_service"] = customer_info.get("customer_service")
        return local_result

    return None


# ============ Flask路由 ============


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search")
def api_search():
    query = request.args.get("query", "")
    if not query:
        return jsonify({"error": "请输入查询内容"})

    result = get_province_from_district(query)

    if result and result.get("province"):
        return jsonify(
            {
                "success": True,
                "data": result,
                "source": "api" if result.get("code") else "local",
            }
        )
    else:
        return jsonify({"success": False, "error": "未找到该行政区划"})


# ============ Flask启动函数 ============


def run_flask():
    """在独立线程中运行Flask"""
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


# ============ 桌面应用入口 ============


def main():
    """主函数"""
    # 在后台线程中启动Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    print("=" * 50)
    print("  销售网点查询系统 - 桌面版")
    print("=" * 50)
    print()
    print("  正在启动应用窗口...")
    print()

    # 创建桌面窗口
    webview.create_window(
        title="销售网点查询系统",
        url="http://127.0.0.1:5000",
        width=520,
        height=680,
        resizable=False,
        min_size=(520, 680),
    )

    print("  感谢使用！")


if __name__ == "__main__":
    main()
