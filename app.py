"""
中国省份查询系统 - Flask Web应用
功能：通过城市名称、市级名称、县级名称查询对应的中国省份名称
支持客户分配表查询功能
"""

import json
import logging
import os
from datetime import datetime

import requests
from flask import Flask, jsonify, render_template, request

from customer_data import (
    get_customer_by_province,
    get_all_data,
    get_data_by_customer_service,
    get_data_by_manager,
)
from local_data import get_province_from_local
from config_api import get_customer_api_config

# 配置日志
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ============ API配置 ============
# 高德地图API密钥（免费申请：https://lbs.amap.com/dev/key）
AMAP_KEY = "b60b67ba5e4ae864a24ee7cb99a2567d"

# 腾讯地图API密钥（免费申请：https://lbs.qq.com/）
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
        "subdistrict": 3,  # 返回三级行政区划
        "extensions": "base",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") == "1" and data.get("districts"):
            logger.info(
                f"高德API返回数据: {json.dumps(data['districts'][:3], ensure_ascii=False)}"
            )
            return data["districts"]
        return None
    except Exception as e:
        logger.error(f"高德API错误: {e}")
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
    except Exception as e:
        logger.error(f"腾讯API错误: {e}")
        return None


def parse_amap_result(districts, keyword):
    """解析高德API返回结果"""
    if not districts:
        return None

    # 级别映射
    level_map = {"province": "省级", "city": "市级", "district": "县级"}

    keyword = keyword.strip()

    for district in districts:
        name = district.get("name", "")
        level = district.get("level", "")

        # 模糊匹配：支持"汕头"匹配"汕头市"，"祁东"匹配"祁东县"
        if keyword == name or keyword in name or name in keyword:
            # 初始化变量
            province = ""
            city = ""
            district_name = ""

            # 根据级别处理
            if level == "province":
                province = name

            elif level == "city":
                city = name
                # 尝试从本地数据获取省份
                local_result = get_province_from_local(keyword)
                if local_result:
                    province = local_result.get("province", "")

            elif level == "district":
                district_name = name
                city = district.get("city", "")
                province = district.get("province", "")

            # 构建结果
            result = {
                "province": province,
                "city": city,
                "district": district_name,
                "level": level_map.get(level, level),
                "code": district.get("adcode", ""),
                "intro": "",
            }

            # 如果没有省份信息，尝试从本地数据获取
            if not result["province"]:
                local_result = get_province_from_local(keyword)
                if local_result:
                    result["province"] = local_result.get("province", "")
                    result["city"] = local_result.get("city", "") or result["city"]
                    result["district"] = (
                        local_result.get("district", "") or result["district"]
                    )

            # 从本地数据获取简介
            local_result = get_province_from_local(keyword)
            if local_result and local_result.get("intro"):
                result["intro"] = local_result["intro"]

            return result

    return None

    # 级别映射
    level_map = {"province": "省级", "city": "市级", "district": "县级"}

    for district in districts:
        name = district.get("name", "")
        level = district.get("level", "")

        logger.info(f"解析: name={name}, level={level}")

        # 模糊匹配
        if keyword in name or name in keyword:
            # 初始化变量
            province = ""
            city = ""
            district_name = ""

            # 根据级别处理
            if level == "province":
                # 省级
                province = name
                logger.info(f"识别为省级: {province}")

            elif level == "city":
                # 市级
                city = name
                # 高德API返回的市级数据通常不包含province字段
                # 需要从上级数据获取
                logger.info(f"识别为市级: {city}")

            elif level == "district":
                # 区县级
                district_name = name
                city = district.get("city", "")
                province = district.get("province", "")
                print(
                    f"[调试] 识别为县级: {district_name}, city={city}, province={province}"
                )

            # 构建结果
            result = {
                "province": province,
                "city": city,
                "district": district_name,
                "level": level_map.get(level, level),
                "code": district.get("adcode", ""),
                "intro": "",
            }

            # 如果没有省份信息，尝试从本地数据获取
            if not result["province"]:
                local_result = get_province_from_local(keyword)
                if local_result:
                    result["province"] = local_result.get("province", "")
                    result["city"] = local_result.get("city", "") or result["city"]
                    result["district"] = (
                        local_result.get("district", "") or result["district"]
                    )
                    logger.info(f"从本地数据补充: province={result['province']}")

            # 从本地数据获取简介
            local_result = get_province_from_local(keyword)
            if local_result and local_result.get("intro"):
                result["intro"] = local_result["intro"]

            logger.info(f"最终结果: {json.dumps(result, ensure_ascii=False)}")
            return result

    return None


def parse_tencent_result(results, keyword):
    """解析腾讯API返回结果"""
    if not results or len(results) == 0:
        return None

    # 级别映射
    level_map = {"province": "省级", "city": "市级", "district": "县级"}

    # results[0] 是省份列表
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

    # results[1] 是城市列表
    if len(results) > 1 and results[1] and len(results[1]) > 0:
        city_district = results[1][0]
        result["city"] = city_district.get("fullname", city_district.get("name", ""))
        result["level"] = "市级"
        result["code"] = city_district.get("id", "")

    # results[2] 是区县列表
    if len(results) > 2 and results[2] and len(results[2]) > 0:
        district_district = results[2][0]
        result["district"] = district_district.get(
            "fullname", district_district.get("name", "")
        )
        result["level"] = "县级"
        result["code"] = district_district.get("id", "")

    # 从本地数据获取简介
    local_result = get_province_from_local(keyword)
    if local_result and local_result.get("intro"):
        result["intro"] = local_result["intro"]

    return result


def get_province_from_district(district_name):
    """获取行政区划对应的省份信息"""

    # 策略1：尝试使用高德API
    logger.info(f"[查询] 关键词: {district_name}")
    logger.info("[策略1] 尝试高德API查询...")
    if AMAP_KEY:
        result = search_with_amap(district_name)
        if result:
            parsed = parse_amap_result(result, district_name)
            if parsed and parsed.get("province"):
                # 添加客户分配信息
                customer_info = get_customer_by_province(parsed.get("province", ""))
                if customer_info:
                    parsed["manager"] = customer_info.get("manager")
                    parsed["customer_service"] = customer_info.get("customer_service")
                    parsed["zone"] = customer_info.get("zone")
                    logger.info(f"[成功] 高德API查询到: {parsed}")
                    return parsed

    # 策略2：尝试使用腾讯API
    logger.info("[策略2] 尝试腾讯API查询...")
    if TENCENT_MAP_KEY:
        result = search_with_tencent(district_name)
        if result:
            parsed = parse_tencent_result(result, district_name)
            if parsed and parsed.get("province"):
                # 添加客户分配信息
                customer_info = get_customer_by_province(parsed.get("province", ""))
                if customer_info:
                    parsed["manager"] = customer_info.get("manager")
                    parsed["customer_service"] = customer_info.get("customer_service")
                    parsed["zone"] = customer_info.get("zone")
                logger.info(f"[成功] 腾讯API查询到: {parsed}")
                return parsed

    # 策略3：尝试使用本地数据
    logger.info("[策略3] 尝试本地数据查询...")
    local_result = get_province_from_local(district_name)
    if local_result and local_result.get("province"):
        # 添加客户分配信息
        customer_info = get_customer_by_province(local_result.get("province", ""))
        if customer_info:
            local_result["manager"] = customer_info.get("manager")
            local_result["customer_service"] = customer_info.get("customer_service")
            local_result["zone"] = customer_info.get("zone")
        logger.info(f"[成功] 本地数据查询到: {local_result}")
        return local_result

    logger.warning(f"[失败] 未能找到: {district_name}")
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/customer")
def customer():
    """客户分配查询页面"""
    return render_template("customer.html")


@app.route("/customer/search")
def customer_search():
    """客户名称查询页面"""
    return render_template("customer_search.html")


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
        return jsonify(
            {"success": False, "error": "未找到该行政区划，请检查输入是否正确"}
        )


@app.route("/api/customer")
def api_customer():
    """
    客户分配表查询接口
    支持按省份名称、省区经理名称、客服名称查询
    """
    query = request.args.get("query", "").strip()
    query_type = request.args.get("type", "province")  # province, manager, service

    if not query:
        return jsonify({"error": "请输入查询内容"})

    result = None

    if query_type == "province":
        result = get_customer_by_province(query)
    elif query_type == "manager":
        result = get_data_by_manager(query)
    elif query_type == "service":
        managers = get_data_by_customer_service(query)
        if managers:
            result = {"customer_service": query, "managers": managers}

    if result:
        return jsonify({"success": True, "data": result})
    else:
        return jsonify({"success": False, "error": "未找到匹配的记录"})


@app.route("/api/customer/all")
def api_customer_all():
    """获取所有客户分配数据"""
    return jsonify({"success": True, "data": get_all_data()})


@app.route("/api/customer/zones")
def api_customer_zones():
    """获取所有区域和客服列表"""
    data = get_all_data()
    zones = []
    for zone, customer_groups in data.items():
        for group_name, customers in customer_groups.items():
            for customer in customers:
                zones.append(
                    {
                        "zone": zone,
                        "region": customer.get("区域"),
                        "manager": customer.get("省区经理"),
                        "customer_service": customer.get("客服"),
                    }
                )

    return jsonify({"success": True, "data": zones})


@app.route("/api/status")
def api_status():
    """检查API配置状态"""
    return jsonify(
        {
            "amap_configured": bool(AMAP_KEY),
            "tencent_configured": bool(TENCENT_MAP_KEY),
            "local_data_available": True,
            "message": "请配置高德或腾讯地图API密钥以获得更好的查询体验",
        }
    )


@app.route("/api/customer/search")
def api_customer_search():
    """
    客户名称查询接口
    根据客户名称关键字查询客户详细信息
    """
    keyword = request.args.get("name", "").strip()

    if not keyword:
        return jsonify({"success": False, "error": "请输入客户名称关键字"})

    # 获取API配置
    api_config = get_customer_api_config()
    base_url = api_config["base_url"]
    auth_url = f"{base_url}{api_config['auth_url']}"
    search_url = f"{base_url}{api_config['search_url']}"
    credentials = api_config["credentials"]
    timeout = api_config["timeout"]

    # 检查认证凭据是否已配置
    if not credentials.get("access_id") or not credentials.get("secret_key"):
        logger.error("[客户查询] 认证凭据未配置")
        return jsonify({
            "success": False,
            "error": "API认证凭据未配置，请联系管理员配置"
        })

    try:
        # 步骤1: 获取Token
        logger.info(f"[认证] 正在获取Token...")
        # 使用查询参数传递认证信息
        try:
            response = requests.post(
                auth_url,
                params=credentials,
                timeout=timeout
            )
            response.raise_for_status()
            auth_result = response.json()

            logger.info(f"[认证] 响应: {auth_result}")

            # 解析Token
            token = None
            if "token" in auth_result:
                token = auth_result["token"]
            elif "access_token" in auth_result:
                token = auth_result["access_token"]
            elif "data" in auth_result:
                data = auth_result["data"]
                if isinstance(data, dict):
                    token = data.get("token") or data.get("access_token")
                elif isinstance(data, str):
                    token = data

            if not token:
                logger.error(f"[认证] 无法从响应中获取Token: {auth_result}")
                return jsonify({
                    "success": False,
                    "error": "认证失败：无法获取访问令牌"
                })

            logger.info(f"[认证] Token获取成功")

        except Exception as e:
            logger.error(f"[认证] 失败: {e}")
            return jsonify({
                "success": False,
                "error": f"认证失败: {str(e)}"
            })
        

        # 步骤2: 使用Token查询客户信息
        logger.info(f"[客户查询] 关键词: {keyword}")
        # 构建查询参数（根据实际API文档调整）
        params = {
            "name": keyword,
            "page": 1,
            "page_size": api_config["default_page_size"]
        }

        # 尝试多种Token传递方式
        auth_methods = [
            {"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            {"Authorization": token, "Content-Type": "application/json"},
            {"token": token, "Content-Type": "application/json"},
            {"access_token": token, "Content-Type": "application/json"},
        ]

        search_data = None
        for i, headers in enumerate(auth_methods):
            try:
                logger.info(f"[客户查询] 尝试认证方式 {i+1}")
                search_response = requests.get(
                    search_url,
                    params=params,
                    headers=headers,
                    timeout=timeout
                )
                search_response.raise_for_status()
                search_data = search_response.json()
                logger.info(f"[客户查询] 查询成功（认证方式 {i+1}）")
                break
            except Exception as e:
                logger.warning(f"[客户查询] 认证方式 {i+1} 失败: {e}")
                continue

        if search_data is None:
            raise Exception("所有认证方式均失败")
        search_response.raise_for_status()
        search_data = search_response.json()

        # 解析API返回的数据
        customers = []

        if isinstance(search_data, dict):
            # 如果API返回的是字典，提取数据列表
            if "data" in search_data:
                data = search_data["data"]
                if isinstance(data, list):
                    customers = data
                elif isinstance(data, dict) and "list" in data:
                    customers = data["list"]
                elif isinstance(data, dict) and "items" in data:
                    customers = data["items"]
                elif isinstance(data, dict) and "records" in data:
                    customers = data["records"]
            elif "results" in search_data:
                customers = search_data["results"]
            elif "customers" in search_data:
                customers = search_data["customers"]
            elif "list" in search_data:
                customers = search_data["list"]
            elif "items" in search_data:
                customers = search_data["items"]
            elif "records" in search_data:
                customers = search_data["records"]
            else:
                customers = [search_data]
        elif isinstance(search_data, list):
            # 如果API返回的是列表
            customers = search_data

        # 标准化客户数据格式
        standardized_customers = []
        for customer in customers:
            # API返回的字段映射
            standardized = {
                "customer_id": customer.get("dwbh") or customer.get("customer_id") or customer.get("id") or customer.get("客户ID") or customer.get("customerId"),
                "customer_code": customer.get("dwbh") or customer.get("customer_code") or customer.get("code") or customer.get("客户编号") or customer.get("customerCode"),
                "customer_name": customer.get("dwmch") or customer.get("customer_name") or customer.get("name") or customer.get("客户名称") or customer.get("customerName"),
                "address": customer.get("dzhdh") or customer.get("address") or customer.get("contact_address") or customer.get("联系地址") or customer.get("contactAddress"),
                "status": customer.get("beactive") or customer.get("status") or customer.get("state") or customer.get("状态") or customer.get("customerStatus"),
                "jingyfw": customer.get("jingyfw") or customer.get("business_scope") or customer.get("经营范围") or customer.get("businessScope"),
                "last_updated": customer.get("lastmodifytime") or customer.get("last_updated") or customer.get("update_time") or customer.get("最后更新日期") or customer.get("updatedAt") or customer.get("updateTime"),
            }
            standardized_customers.append(standardized)

        logger.info(f"[客户查询] 关键词: {keyword}, 找到 {len(standardized_customers)} 条记录")

        return jsonify({
            "success": True,
            "data": standardized_customers,
            "total": len(standardized_customers)
        })

    except requests.exceptions.HTTPError as e:
        logger.error(f"[客户查询] HTTP错误: {e}")
        error_msg = f"API调用失败: {str(e)}"
        if e.response is not None:
            try:
                error_data = e.response.json()
                if "message" in error_data:
                    error_msg = error_data["message"]
                elif "error" in error_data:
                    error_msg = error_data["error"]
            except:
                pass
        return jsonify({
            "success": False,
            "error": error_msg
        })
    except requests.exceptions.RequestException as e:
        logger.error(f"[客户查询] 网络错误: {e}")
        return jsonify({
            "success": False,
            "error": f"网络连接失败: {str(e)}"
        })
    except Exception as e:
        logger.error(f"[客户查询] 处理失败: {e}")
        return jsonify({
            "success": False,
            "error": f"数据处理失败: {str(e)}"
        })


@app.route("/api/certificates")
def api_certificates():
    """
    客户证照查询接口
    根据客户编号查询证照资料
    """
    customer_code = request.args.get("customer_code", "").strip()

    if not customer_code:
        return jsonify({"success": False, "error": "请提供客户编号"})

    # 获取API配置
    api_config = get_customer_api_config()
    base_url = api_config["base_url"]
    auth_url = f"{base_url}{api_config['auth_url']}"
    cert_url = f"{base_url}/api/certificate/list"
    timeout = api_config["timeout"]
    credentials = api_config["credentials"]

    # 检查认证凭据
    if not credentials.get("access_id") or not credentials.get("secret_key"):
        logger.error("[证照查询] 认证凭据未配置")
        return jsonify({
            "success": False,
            "error": "API认证凭据未配置，请联系管理员配置"
        })

    try:
        # 步骤1: 获取Token
        logger.info(f"[证照查询] 正在获取Token...")
        token_response = requests.post(
            auth_url,
            params=credentials,
            timeout=timeout
        )

        if token_response.status_code != 200:
            logger.error(f"[证照查询] Token获取失败: {token_response.status_code}")
            return jsonify({
                "success": False,
                "error": f"认证失败，状态码: {token_response.status_code}"
            })

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            logger.error("[证照查询] Token响应中无access_token")
            return jsonify({
                "success": False,
                "error": "认证失败，未获取到访问令牌"
            })

        logger.info("[证照查询] Token获取成功")

        # 步骤2: 查询证照
        logger.info(f"[证照查询] 查询客户 {customer_code} 的证照...")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        params = {
            "dwbh": customer_code,
            "page": 1,
            "page_size": 50
        }

        cert_response = requests.get(
            cert_url,
            headers=headers,
            params=params,
            timeout=timeout
        )

        if cert_response.status_code != 200:
            logger.error(f"[证照查询] 证照查询失败: {cert_response.status_code}")
            return jsonify({
                "success": False,
                "error": f"证照查询失败，状态码: {cert_response.status_code}"
            })

        cert_data = cert_response.json()

        logger.info(f"[证照查询] 查询成功，找到 {cert_data.get('total', 0)} 条证照记录")

        return jsonify({
            "success": True,
            "data": cert_data,
            "total": cert_data.get("total", 0)
        })

    except requests.exceptions.HTTPError as e:
        logger.error(f"[证照查询] HTTP错误: {e}")
        error_msg = f"API调用失败: {str(e)}"
        if e.response is not None:
            try:
                error_data = e.response.json()
                if "message" in error_data:
                    error_msg = error_data["message"]
            except:
                pass
        return jsonify({
            "success": False,
            "error": error_msg
        })
    except requests.exceptions.RequestException as e:
        logger.error(f"[证照查询] 网络错误: {e}")
        return jsonify({
            "success": False,
            "error": f"网络连接失败: {str(e)}"
        })
    except Exception as e:
        logger.error(f"[证照查询] 处理失败: {e}")
        return jsonify({
            "success": False,
            "error": f"数据处理失败: {str(e)}"
        })


if __name__ == "__main__":
    print("=" * 60)
    print("中国省份查询系统")
    print("=" * 60)
    print("\nAPI配置状态:")
    print(f"  高德地图: {'已配置' if AMAP_KEY else '未配置'}")
    print(f"  腾讯地图: {'已配置' if TENCENT_MAP_KEY else '未配置'}")
    print(f"  本地数据: 可用")
    print("\n如需使用在线API，请:")
    print("  1. 高德地图: https://lbs.amap.com/dev/key (免费申请)")
    print("  2. 腾讯地图: https://lbs.qq.com/ (免费申请)")
    print("\n启动服务器...")

    # 生产环境配置
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))

    app.run(debug=debug_mode, host="0.0.0.0", port=port)
