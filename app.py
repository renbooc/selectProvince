"""
中国省份查询系统 - Flask Web应用
功能：通过城市名称、市级名称、县级名称查询对应的中国省份名称
支持客户分配表查询功能
"""

import json
import logging
import os
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests
from flask import Flask, jsonify, render_template, request, session

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

log_file = os.path.join(os.getcwd(), "app.log")
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')
app.secret_key = "hai-yuan-tang-secret-key-2024"

import os
from flask import send_from_directory

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.getcwd(), "favicon.ico", mimetype="image/vnd.microsoft.icon")

# 记录启动信息
logger.info(f"应用启动，日志文件: {log_file}")
logger.info(f"Python版本: {sys.version}")
logger.info(f"工作目录: {os.getcwd()}")

# ============ API配置 ============
# 高德地图API密钥（免费申请：https://lbs.amap.com/dev/key）
AMAP_KEY = "b60b67ba5e4ae864a24ee7cb99a2567d"

# 腾讯地图API密钥（免费申请：https://lbs.qq.com/）
TENCENT_MAP_KEY = ""

# ============ 登录配置 ============
# 默认登录账户（用户名: 密码）- 备用账户
LOGIN_USERS = {
    "admin": "admin123",
    "hytd": "haiyuan123",
    # 孙灿 - 使用明文密码登录
    "孙灿": "123456",
}


def get_employee_list():
    """从API获取员工列表用于登录验证（遍历所有页面）"""
    try:
        api_config = get_customer_api_config()
        base_url = api_config["base_url"]
        auth_url = f"{base_url}{api_config['auth_url']}"
        employee_url = f"{base_url}/api/employee/list"
        credentials = api_config["credentials"]
        timeout = api_config["timeout"]

        # 先获取Token
        response = requests.post(auth_url, params=credentials, timeout=timeout)
        response.raise_for_status()
        auth_result = response.json()

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
            logger.error("[员工列表] 无法获取Token")
            return []

        # 使用Token获取所有页的员工列表
        headers = {"Authorization": f"Bearer {token}"}
        all_employees = []
        page = 1
        
        while True:
            params = {"page": page, "page_size": 100}
            response = requests.get(employee_url, headers=headers, params=params, timeout=timeout)
            response.raise_for_status()
            result = response.json()

            # 解析员工列表
            employees = []
            if isinstance(result, dict) and "items" in result:
                employees = result.get("items", [])
            elif isinstance(result, dict) and "data" in result:
                data = result["data"]
                if isinstance(data, list):
                    employees = data
                elif isinstance(data, dict) and "list" in data:
                    employees = data["list"]
            elif isinstance(result, list):
                employees = result

            if not employees:
                break
                
            all_employees.extend(employees)
            page += 1
            
            # 防止无限循环
            if page > 50:
                break

        logger.info(f"[员工列表] 获取到 {len(all_employees)} 条员工记录")
        return all_employees

    except Exception as e:
        logger.error(f"[员工列表] 获取失败: {e}")
        return []


def validate_employee_login(username, password):
    """验证员工登录
    用户名: dzyname字段值
    密码: dzycode字段值
    """
    employees = get_employee_list()

    for emp in employees:
        dzyname = emp.get("dzyname", "").strip()
        dzycode = emp.get("dzycode", "").strip()

        # 用户名和密码都匹配则验证成功
        if dzyname == username and dzycode == password:
            logger.info(f"[登录验证] 用户 {username} 验证成功")
            return True, emp

    logger.warning(f"[登录验证] 用户 {username} 验证失败")
    return False, None


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


def get_province_by_adcode(adcode):
    """
    通过行政区划代码推断省份
    行政代码规则：前2位是省份代码
    例如：430181 -> 43 -> 湖南省
    """
    if not adcode or len(adcode) < 2:
        return None

    # 省级行政代码映射（前2位）
    province_code_map = {
        "11": "北京市",
        "12": "天津市",
        "13": "河北省",
        "14": "山西省",
        "15": "内蒙古自治区",
        "21": "辽宁省",
        "22": "吉林省",
        "23": "黑龙江省",
        "31": "上海市",
        "32": "江苏省",
        "33": "浙江省",
        "34": "安徽省",
        "35": "福建省",
        "36": "江西省",
        "37": "山东省",
        "41": "河南省",
        "42": "湖北省",
        "43": "湖南省",
        "44": "广东省",
        "45": "广西壮族自治区",
        "46": "海南省",
        "50": "重庆市",
        "51": "四川省",
        "52": "贵州省",
        "53": "云南省",
        "54": "西藏自治区",
        "61": "陕西省",
        "62": "甘肃省",
        "63": "青海省",
        "64": "宁夏回族自治区",
        "65": "新疆维吾尔自治区",
    }

    province_code = adcode[:2]
    return province_code_map.get(province_code)


def query_province_by_adcode(adcode):
    """
    通过行政区划代码查询完整的省市县信息
    使用高德API根据adcode查询
    """
    if not adcode or not AMAP_KEY:
        return None

    url = "https://restapi.amap.com/v3/config/district"
    params = {
        "key": AMAP_KEY,
        "keywords": adcode,
        "subdistrict": 0,
        "extensions": "base",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") == "1" and data.get("districts"):
            district_info = data["districts"][0]
            logger.info(
                f"通过adcode {adcode} 查询到: {district_info.get('name')}, 级别: {district_info.get('level')}"
            )
            return district_info
        return None
    except Exception as e:
        logger.error(f"通过adcode查询失败: {e}")
        return None


def parse_amap_result(districts, keyword):
    """解析高德API返回结果，支持省-市-县-镇-村多级地名"""
    if not districts:
        return None

    # 级别映射
    level_map = {
        "province": "省级",
        "city": "市级",
        "district": "县级",
        "street": "镇级/街道",
    }

    keyword = keyword.strip()

    for district in districts:
        name = district.get("name", "")
        level = district.get("level", "")
        adcode = district.get("adcode", "")

        # 模糊匹配：支持"汕头"匹配"汕头市"，"龙伏"匹配"龙伏镇"
        if keyword == name or keyword in name or name in keyword:
            # 初始化变量
            province = ""
            city = ""
            district_name = ""
            street_name = ""

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

            elif level == "street":
                # 镇级或街道级
                street_name = name
                logger.info(f"识别为镇级/街道: {street_name}, adcode={adcode}")

                # 通过adcode推断省份
                province = get_province_by_adcode(adcode)
                logger.info(f"通过adcode推断省份: {province}")

                # 如果adcode是6位，尝试查询上级信息
                if adcode and len(adcode) == 6:
                    # 县级代码（前4位+00）
                    county_code = adcode[:4] + "00"
                    county_info = query_province_by_adcode(county_code)
                    if county_info:
                        district_name = county_info.get("name", "")
                        logger.info(f"查询到县级: {district_name}")

                    # 市级代码（前2位+0000）
                    city_code = adcode[:2] + "0000"
                    # 对于直辖市和部分省会，市级代码可能是前4位
                    if adcode[:2] in ["11", "12", "31", "50"]:  # 北京、天津、上海、重庆
                        city = province
                    else:
                        # 尝试从citycode获取市名
                        citycode = district.get("citycode", "")
                        if citycode:
                            # 使用原始关键字查询本地数据，尝试获取城市名
                            city_guess = adcode[:4]
                            city_info = query_province_by_adcode(city_guess + "00")
                            if city_info and city_info.get("level") == "city":
                                city = city_info.get("name", "")
                                logger.info(f"查询到市级: {city}")

            # 构建结果
            result = {
                "province": province,
                "city": city,
                "district": district_name,
                "street": street_name,
                "level": level_map.get(level, level),
                "code": adcode,
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

            # 如果还是没有省份，但有adcode，再次尝试通过adcode推断
            if not result["province"] and adcode:
                result["province"] = get_province_by_adcode(adcode)

            # 从本地数据获取简介
            local_result = get_province_from_local(keyword)
            if local_result and local_result.get("intro"):
                result["intro"] = local_result["intro"]

            logger.info(f"最终解析结果: {json.dumps(result, ensure_ascii=False)}")
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
    """登录页面"""
    if session.get("logged_in"):
        return render_template("customer_search_new.html")
    return render_template("login.html")


@app.route("/api/login", methods=["POST"])
def api_login():
    """登录API"""
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"success": False, "message": "请输入用户名和密码"})

    success, employee = validate_employee_login(username, password)

    if success:
        session["logged_in"] = True
        session["username"] = username
        session["employee_info"] = employee
        logger.info(f"用户 {username} 登录成功")
        return jsonify({"success": True, "message": "登录成功"})

    logger.warning(f"用户 {username} 登录失败")
    return jsonify({"success": False, "message": "用户名或密码错误"})


@app.route("/api/logout", methods=["POST"])
def api_logout():
    """登出API"""
    username = session.get("username")
    session.clear()
    if username:
        logger.info(f"用户 {username} 已登出")
    return jsonify({"success": True, "message": "已登出"})


@app.route("/api/check-login")
def api_check_login():
    """检查登录状态API"""
    return jsonify({
        "logged_in": session.get("logged_in", False),
        "username": session.get("username", "")
    })


@app.route("/customer")
def customer():
    """客户分配查询页面"""
    if not session.get("logged_in"):
        return render_template("login.html")
    return render_template("customer.html")


@app.route("/customer/search")
def customer_search():
    """客户名称查询页面 - 集成销售网点查询"""
    if not session.get("logged_in"):
        return render_template("login.html")
    return render_template("customer_search_new.html")


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
    支持按省份名称、城市名称、省区经理名称、客服名称查询
    """
    query = request.args.get("query", "").strip()
    query_type = request.args.get("type", "province")  # province, manager, service

    if not query:
        return jsonify({"error": "请输入查询内容"})

    result = None

    if query_type == "province":
        # 先尝试直接按省份名查询
        result = get_customer_by_province(query)

        # 如果直接查询失败，尝试将输入作为城市名查询，获取其所属省份
        if not result:
            logger.info(f"[客户分配] 省份名直接查询失败，尝试作为地区名查询: {query}")

            # 策略1: 使用本地数据查询省份信息
            local_result = get_province_from_local(query)
            if local_result and local_result.get("province"):
                province_name = local_result.get("province")
                logger.info(f"[客户分配] 本地数据识别出省份: {province_name}")
                # 用识别出的省份名再次查询
                result = get_customer_by_province(province_name)
                if result:
                    # 更新结果中的字段
                    result["query_keyword"] = query
                    result["matched_by"] = "local_data"
                    result["area_info"] = {
                        "city": local_result.get("city", ""),
                        "district": local_result.get("district", ""),
                        "level": local_result.get("level", ""),
                    }

            # 策略2: 如果本地数据查询失败，使用高德API
            if not result and AMAP_KEY:
                logger.info(f"[客户分配] 本地数据未找到，尝试使用高德API查询: {query}")
                amap_result = search_with_amap(query)
                if amap_result:
                    parsed = parse_amap_result(amap_result, query)
                    if parsed and parsed.get("province"):
                        province_name = parsed.get("province")
                        logger.info(f"[客户分配] 高德API识别出省份: {province_name}")
                        # 用识别出的省份名再次查询
                        result = get_customer_by_province(province_name)
                        if result:
                            # 更新结果中的字段
                            result["query_keyword"] = query
                            result["matched_by"] = "amap_api"
                            result["area_info"] = {
                                "province": parsed.get("province", ""),
                                "city": parsed.get("city", ""),
                                "district": parsed.get("district", ""),
                                "street": parsed.get("street", ""),
                                "level": parsed.get("level", ""),
                                "adcode": parsed.get("code", ""),
                            }
                    else:
                        logger.warning(f"[客户分配] 高德API未能识别出省份: {query}")
                else:
                    logger.warning(f"[客户分配] 高德API未返回结果: {query}")
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
        return jsonify(
            {"success": False, "error": "API认证凭据未配置，请联系管理员配置"}
        )

    try:
        # 步骤1: 获取Token
        logger.info(f"[认证] 正在获取Token...")
        # 使用查询参数传递认证信息
        try:
            response = requests.post(auth_url, params=credentials, timeout=timeout)
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
                return jsonify(
                    {"success": False, "error": "认证失败：无法获取访问令牌"}
                )

            logger.info(f"[认证] Token获取成功")

        except Exception as e:
            logger.error(f"[认证] 失败: {e}")
            return jsonify({"success": False, "error": f"认证失败: {str(e)}"})

        # 步骤2: 使用Token查询客户信息
        logger.info(f"[客户查询] 关键词: {keyword}")
        # 构建查询参数（根据实际API文档调整）
        params = {
            "name": keyword,
            "page": 1,
            "page_size": api_config["default_page_size"],
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
                logger.info(f"[客户查询] 尝试认证方式 {i + 1}")
                search_response = requests.get(
                    search_url, params=params, headers=headers, timeout=timeout
                )
                search_response.raise_for_status()
                search_data = search_response.json()
                logger.info(f"[客户查询] 查询成功（认证方式 {i + 1}）")
                break
            except Exception as e:
                logger.warning(f"[客户查询] 认证方式 {i + 1} 失败: {e}")
                continue

        if search_data is None:
            raise Exception("所有认证方式均失败")

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

        # 标准化客户数据格式并添加销售网点信息
        standardized_customers = []
        for customer in customers:
            # API返回的字段映射
            address = (
                customer.get("dzhdh")
                or customer.get("address")
                or customer.get("contact_address")
                or customer.get("联系地址")
                or customer.get("contactAddress")
                or ""
            )

            standardized = {
                "customer_id": customer.get("dwbh")
                or customer.get("customer_id")
                or customer.get("id")
                or customer.get("客户ID")
                or customer.get("customerId"),
                "customer_code": customer.get("dwbh")
                or customer.get("customer_code")
                or customer.get("code")
                or customer.get("客户编号")
                or customer.get("customerCode"),
                "customer_name": customer.get("dwmch")
                or customer.get("customer_name")
                or customer.get("name")
                or customer.get("客户名称")
                or customer.get("customerName"),
                "address": address,
                "status": customer.get("beactive")
                or customer.get("status")
                or customer.get("state")
                or customer.get("状态")
                or customer.get("customerStatus"),
                "jingyfw": customer.get("jingyfw")
                or customer.get("business_scope")
                or customer.get("经营范围")
                or customer.get("businessScope"),
                "last_updated": customer.get("lastmodifytime")
                or customer.get("last_updated")
                or customer.get("update_time")
                or customer.get("最后更新日期")
                or customer.get("updatedAt")
                or customer.get("updateTime"),
            }

            # 集成销售网点查询功能
            # 从地址中提取省份信息，查询对应的省区经理和客服
            province_info = None
            sales_network_info = {
                "province": "",
                "region": "",
                "zone": "",
                "manager": "",
                "customer_service": "",
                "matched_by": "none",
            }

            if address:
                logger.info(
                    f"[销售网点查询] 为客户 {standardized.get('customer_name')} 查询地址: {address}"
                )

                # 策略1: 尝试从本地数据提取省份
                local_result = get_province_from_local(address)
                if local_result and local_result.get("province"):
                    province_name = local_result.get("province")
                    logger.info(f"[销售网点查询] 本地数据识别出省份: {province_name}")
                    province_info = get_customer_by_province(province_name)
                    if province_info:
                        sales_network_info = {
                            "province": province_name,
                            "region": province_info.get("region", ""),
                            "zone": province_info.get("zone", ""),
                            "manager": province_info.get("manager", ""),
                            "customer_service": province_info.get(
                                "customer_service", ""
                            ),
                            "matched_by": "local_data",
                        }

                # 策略2: 如果本地数据失败，使用高德API
                if not province_info and AMAP_KEY:
                    logger.info(f"[销售网点查询] 本地数据未找到，尝试使用高德API")
                    amap_result = search_with_amap(address)
                    if amap_result:
                        parsed = parse_amap_result(amap_result, address)
                        if parsed and parsed.get("province"):
                            province_name = parsed.get("province")
                            logger.info(
                                f"[销售网点查询] 高德API识别出省份: {province_name}"
                            )
                            province_info = get_customer_by_province(province_name)
                            if province_info:
                                sales_network_info = {
                                    "province": province_name,
                                    "region": province_info.get("region", ""),
                                    "zone": province_info.get("zone", ""),
                                    "manager": province_info.get("manager", ""),
                                    "customer_service": province_info.get(
                                        "customer_service", ""
                                    ),
                                    "matched_by": "amap_api",
                                }

            # 将销售网点信息添加到客户数据中
            standardized.update(sales_network_info)
            standardized_customers.append(standardized)

        logger.info(
            f"[客户查询] 关键词: {keyword}, 找到 {len(standardized_customers)} 条记录"
        )

        return jsonify(
            {
                "success": True,
                "data": standardized_customers,
                "total": len(standardized_customers),
            }
        )

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
        return jsonify({"success": False, "error": error_msg})
    except requests.exceptions.RequestException as e:
        logger.error(f"[客户查询] 网络错误: {e}")
        return jsonify({"success": False, "error": f"网络连接失败: {str(e)}"})
    except Exception as e:
        logger.error(f"[客户查询] 处理失败: {e}")
        return jsonify({"success": False, "error": f"数据处理失败: {str(e)}"})


@app.route("/api/certificates")
def api_certificates():
    """
    客户证照查询接口
    根据客户编号查询证照资料
    """
    try:
        customer_code = request.args.get("customer_code", "").strip()
        logger.info(f"[证照查询] 开始查询，客户编号: {customer_code}")

        if not customer_code:
            return jsonify({"success": False, "error": "请提供客户编号"})

        # 获取API配置
        api_config = get_customer_api_config()
        base_url = api_config["base_url"]
        auth_url = f"{base_url}{api_config['auth_url']}"
        cert_url = f"{base_url}/api/certificate/list"
        timeout = 30  # 增加超时时间到30秒
        credentials = api_config["credentials"]

        logger.info(f"[证照查询] API配置: base_url={base_url}, timeout={timeout}")

        # 检查认证凭据
        if not credentials.get("access_id") or not credentials.get("secret_key"):
            logger.error("[证照查询] 认证凭据未配置")
            return jsonify(
                {"success": False, "error": "API认证凭据未配置，请联系管理员配置"}
            )
        # 步骤1: 获取Token
        logger.info(f"[证照查询] 正在获取Token...")
        token_response = requests.post(auth_url, params=credentials, timeout=timeout)
        token_response.raise_for_status()

        token_data = token_response.json()
        logger.info(f"[证照查询] Token响应: {token_data}")

        # 解析Token - 支持多种字段名
        access_token = None
        if "token" in token_data:
            access_token = token_data["token"]
        elif "access_token" in token_data:
            access_token = token_data["access_token"]
        elif "data" in token_data:
            data = token_data["data"]
            if isinstance(data, dict):
                access_token = data.get("token") or data.get("access_token")
            elif isinstance(data, str):
                access_token = data

        if not access_token:
            logger.error(f"[证照查询] 无法从响应中获取Token: {token_data}")
            return jsonify({"success": False, "error": "认证失败，未获取到访问令牌"})

        logger.info("[证照查询] Token获取成功")

        # 步骤2: 查询证照
        logger.info(f"[证照查询] 查询客户 {customer_code} 的证照...")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        params = {"dwbh": customer_code, "page": 1, "page_size": 50}

        cert_response = requests.get(
            cert_url, headers=headers, params=params, timeout=timeout
        )

        if cert_response.status_code != 200:
            logger.error(f"[证照查询] 证照查询失败: {cert_response.status_code}")
            return jsonify(
                {
                    "success": False,
                    "error": f"证照查询失败，状态码: {cert_response.status_code}",
                }
            )

        cert_data = cert_response.json()
        logger.info(
            f"[证照查询] 原始API响应数据结构: {type(cert_data)}, keys: {cert_data.keys() if isinstance(cert_data, dict) else 'N/A'}"
        )

        # 提取证照列表 - 处理多种可能的数据结构
        certificates = []
        if isinstance(cert_data, dict):
            # 尝试从各种可能的嵌套结构中提取证照列表
            if "data" in cert_data:
                data = cert_data["data"]
                if isinstance(data, list):
                    certificates = data
                elif isinstance(data, dict):
                    # 可能是 {"data": {"list": [...]} } 或 {"data": {"items": [...]} }
                    certificates = (
                        data.get("list")
                        or data.get("items")
                        or data.get("records")
                        or data.get("data")
                        or []
                    )
            elif "list" in cert_data:
                certificates = cert_data["list"]
            elif "items" in cert_data:
                certificates = cert_data["items"]
            elif "records" in cert_data:
                certificates = cert_data["records"]
        elif isinstance(cert_data, list):
            certificates = cert_data

        logger.info(f"[证照查询] 提取到的证照列表长度: {len(certificates)}")

        # 获取当前北京时间
        try:
            beijing_tz = ZoneInfo("Asia/Shanghai")
            current_date = datetime.now(beijing_tz).date()
        except:
            # 如果zoneinfo不可用，使用UTC+8
            current_date = (datetime.utcnow() + timedelta(hours=8)).date()

        logger.info(f"[证照查询] 当前北京时间: {current_date}")

        # 计算证照状态的辅助函数
        def calculate_cert_status(expire_date_str):
            """
            根据有效期计算证照状态
            返回: (status, status_text, status_class)
            """
            if not expire_date_str:
                return "unknown", "未知", "status-unknown"

            try:
                # 确保是字符串类型
                if not isinstance(expire_date_str, str):
                    expire_date_str = str(expire_date_str)

                expire_date_str = expire_date_str.strip()
                if not expire_date_str:
                    return "unknown", "未知", "status-unknown"

                # 尝试解析日期，支持多种格式
                expire_date = None
                for date_format in ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]:
                    try:
                        expire_date = datetime.strptime(
                            expire_date_str, date_format
                        ).date()
                        break
                    except (ValueError, TypeError):
                        continue

                if not expire_date:
                    # 所有格式都失败
                    return "unknown", "日期格式错误", "status-unknown"

                # 计算距离过期的天数
                days_until_expire = (expire_date - current_date).days

                if days_until_expire < 0:
                    # 已过期
                    return "expired", "已过期", "status-expired"
                elif days_until_expire <= 30:
                    # 一个月内到期
                    return "one_month", "一个月近效期", "status-one-month"
                elif days_until_expire <= 90:
                    # 三个月内到期
                    return "three_months", "三个月近效期", "status-three-months"
                else:
                    # 正常
                    return "valid", "正常", "status-valid"

            except Exception as e:
                logger.warning(f"[证照查询] 解析日期失败: {expire_date_str}, 错误: {e}")
                return "unknown", "未知", "status-unknown"

        # 标准化证照数据格式
        standardized_certificates = []
        logger.info(f"[证照查询] 开始处理 {len(certificates)} 条证照数据")
        for i, cert in enumerate(certificates):
            try:
                # 提取有效期
                valid_date = (
                    cert.get("expire_date")
                    or cert.get("yxqz")
                    or cert.get("expiry_date")
                    or cert.get("valid_date")
                    or cert.get("有效期至")
                    or ""
                )

                # 计算证照状态
                status_code, status_text, status_class = calculate_cert_status(valid_date)

                standardized = {
                    "name": (
                        cert.get("cert_name")
                        or cert.get("zlmch")
                        or cert.get("certificate_name")
                        or cert.get("name")
                        or cert.get("证照名称")
                        or ""
                    ),
                    "number": (
                        cert.get("cert_no")
                        or cert.get("zlbh")
                        or cert.get("certificate_number")
                        or cert.get("number")
                        or cert.get("证照编号")
                        or ""
                    ),
                    "valid_date": valid_date,
                    "issue_date": (
                        cert.get("issue_date")
                        or cert.get("fzrq")
                        or cert.get("发证日期")
                        or ""
                    ),
                    "issuer": (
                        cert.get("issue_org")
                        or cert.get("fzjg")
                        or cert.get("issuer")
                        or cert.get("发证机关")
                        or ""
                    ),
                    "status": status_code,
                    "status_text": status_text,
                    "status_class": status_class,
                }
                standardized_certificates.append(standardized)
                logger.info(f"[证照查询] 处理完成第 {i+1}/{len(certificates)} 条证照")
            except Exception as cert_error:
                logger.error(f"[证照查询] 处理第 {i+1} 条证照失败: {cert_error}", exc_info=True)
                # 继续处理下一条
                continue

        logger.info(
            f"[证照查询] 客户编号 {customer_code}，找到 {len(standardized_certificates)} 条证照记录"
        )

        # 构建返回数据
        response_data = {
            "success": True,
            "data": standardized_certificates,
            "total": len(standardized_certificates),
        }
        logger.info(f"[证照查询] 准备返回 {len(standardized_certificates)} 条记录")

        try:
            json_response = jsonify(response_data)
            logger.info(f"[证照查询] JSON序列化成功")
            return json_response
        except Exception as json_error:
            logger.error(f"[证照查询] JSON序列化失败: {json_error}", exc_info=True)
            return jsonify({"success": False, "error": f"数据序列化失败: {str(json_error)}"})

    except requests.exceptions.Timeout as e:
        logger.error(f"[证照查询] 请求超时: {e}")
        return jsonify({"success": False, "error": "API请求超时，请稍后重试"})
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
        return jsonify({"success": False, "error": error_msg})
    except requests.exceptions.RequestException as e:
        logger.error(f"[证照查询] 网络错误: {e}")
        return jsonify({"success": False, "error": f"网络连接失败: {str(e)}"})
    except Exception as e:
        logger.error(f"[证照查询] 处理失败: {e}", exc_info=True)
        return jsonify({"success": False, "error": f"数据处理失败: {str(e)}"})
    except:
        logger.error("[证照查询] 发生未知错误", exc_info=True)
        return jsonify({"success": False, "error": "服务器内部错误"})


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
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.environ.get("PORT", 5000))

    app.run(debug=debug_mode, host="0.0.0.0", port=port)
