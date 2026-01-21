# 客户分配数据表
# 省区经理 -> 区域 -> 客服 对应关系
# 严格按照用户提供的客户关系表配置

CUSTOMER_ALLOCATION_DATA = {
    "南方区": {
        "朱丹负责": [
            {"省区经理": "文海涛", "区域": "陕西", "客服": "朱丹"},
            {"省区经理": "郭蝶", "区域": "湖南", "客服": "朱丹"},
            {"省区经理": "肖坤怡", "区域": "江西", "客服": "朱丹"},
            {"省区经理": "廖小伦/周", "区域": "广东", "客服": "朱丹"},
            {"省区经理": "余朋", "区域": "黑龙江", "客服": "朱丹"},
        ],
        "黄蕾负责": [
            {"省区经理": "邹易/张宇", "区域": "山东", "客服": "黄蕾"},
            {"省区经理": "刘庆玲", "区域": "四川", "客服": "黄蕾"},
            {"省区经理": "陈钱", "区域": "重庆", "客服": "黄蕾"},
            {"省区经理": "谷静", "区域": "广西", "客服": "黄蕾"},
            {"省区经理": "贵树龙", "区域": "贵州", "客服": "黄蕾"},
            {"省区经理": "董鹏程/梁", "区域": "云南", "客服": "黄蕾"},
        ],
        "曾明菊负责": [
            {"省区经理": "杨光义", "区域": "湖北", "客服": "曾明菊"},
            {"省区经理": "周义光", "区域": "西北五省", "客服": "曾明菊"},
            {"省区经理": "李玲", "区域": "江苏", "客服": "曾明菊"},
            {"省区经理": "卢井滔代", "区域": "浙江", "客服": "曾明菊"},
            {"省区经理": "樊鑫", "区域": "安徽", "客服": "曾明菊"},
        ],
    },
    "北方区": {
        "孙灿负责": [
            {"省区经理": "韦文炎/郭", "区域": "河南", "客服": "孙灿"},
            {"省区经理": "苏准", "区域": "河北", "客服": "孙灿"},
            {"省区经理": "高毅/苏准", "区域": "京津", "客服": "孙灿"},
            {"省区经理": "苏文明", "区域": "辽宁", "客服": "孙灿"},
            {"省区经理": "魏一旻", "区域": "福建", "客服": "孙灿"},
            {"省区经理": "林海英", "区域": "吉林", "客服": "孙灿"},
            {"省区经理": "陈维", "区域": "山西/内蒙", "客服": "孙灿"},
        ],
    },
}

# 省份名称到客户区域名称的映射
# 按照客户分配表中的实际负责区域配置
PROVINCE_TO_CUSTOMER_MAP = {
    # 南方区 - 朱丹负责
    "陕西省": "陕西",
    "湖南省": "湖南",
    "江西省": "江西",
    "广东省": "广东",
    "黑龙江省": "黑龙江",
    # 南方区 - 黄蕾负责
    "山东省": "山东",
    "四川省": "四川",
    "重庆市": "重庆",
    "广西壮族自治区": "广西",
    "贵州省": "贵州",
    "云南省": "云南",
    # 南方区 - 曾明菊负责
    "湖北省": "湖北",
    "甘肃省": "西北五省",
    "宁夏回族自治区": "西北五省",
    "青海省": "西北五省",
    "新疆维吾尔自治区": "西北五省",
    "江苏省": "江苏",
    "浙江省": "浙江",
    "安徽省": "安徽",
    # 北方区 - 孙灿负责
    "河南省": "河南",
    "河北省": "河北",
    "北京市": "京津",
    "天津市": "京津",
    "辽宁省": "辽宁",
    "福建省": "福建",
    "吉林省": "吉林",
    "山西省": "山西/内蒙",
    "内蒙古自治区": "山西/内蒙",
}


def get_customer_by_province(province_name):
    """
    根据省份名称查询对应的客户分配信息

    Args:
        province_name: 省份名称（如：陕西、湖南、广东等）

    Returns:
        dict: 包含省区经理和客服信息的字典，未找到返回None
    """
    province_name = province_name.strip()

    # 首先尝试直接匹配
    for zone, customer_groups in CUSTOMER_ALLOCATION_DATA.items():
        for group_name, customers in customer_groups.items():
            for customer in customers:
                if (
                    province_name in customer.get("区域", "")
                    or customer.get("区域", "") in province_name
                ):
                    return {
                        "zone": zone,
                        "group": group_name,
                        "province": province_name,
                        "manager": customer.get("省区经理"),
                        "customer_service": customer.get("客服"),
                        "region": customer.get("区域"),
                    }

    # 如果直接匹配失败，尝试使用映射表
    customer_region = PROVINCE_TO_CUSTOMER_MAP.get(province_name)
    if customer_region:
        for zone, customer_groups in CUSTOMER_ALLOCATION_DATA.items():
            for group_name, customers in customer_groups.items():
                for customer in customers:
                    # 检查客户区域是否匹配
                    customer_area = (
                        customer.get("区域", "").replace("/", "").replace("内蒙", "")
                    )
                    if (
                        customer_region in customer_area
                        or customer_area in customer_region
                    ):
                        return {
                            "zone": zone,
                            "group": group_name,
                            "province": province_name,
                            "manager": customer.get("省区经理"),
                            "customer_service": customer.get("客服"),
                            "region": customer.get("区域"),
                        }

    return None


def get_all_data():
    """获取所有客户分配数据"""
    return CUSTOMER_ALLOCATION_DATA


def get_data_by_customer_service(customer_service_name):
    """
    根据客服名称查询所有负责的省区经理

    Args:
        customer_service_name: 客服名称（如：朱丹、孙灿等）

    Returns:
        list: 匹配的省区经理列表
    """
    customer_service_name = customer_service_name.strip()
    results = []

    for zone, customer_groups in CUSTOMER_ALLOCATION_DATA.items():
        for group_name, customers in customer_groups.items():
            if customer_service_name in group_name:
                for customer in customers:
                    results.append(
                        {
                            "zone": zone,
                            "manager": customer.get("省区经理"),
                            "region": customer.get("区域"),
                            "customer_service": customer.get("客服"),
                        }
                    )

    return results


def get_data_by_manager(manager_name):
    """
    根据省区经理名称查询信息

    Args:
        manager_name: 省区经理名称

    Returns:
        dict: 匹配的信息，未找到返回None
    """
    manager_name = manager_name.strip()

    for zone, customer_groups in CUSTOMER_ALLOCATION_DATA.items():
        for group_name, customers in customer_groups.items():
            for customer in customers:
                if (
                    manager_name in customer.get("省区经理", "")
                    or customer.get("省区经理", "").replace("/", "").replace("代", "")
                    in manager_name
                ):
                    return {
                        "zone": zone,
                        "group": group_name,
                        "manager": customer.get("省区经理"),
                        "region": customer.get("区域"),
                        "customer_service": customer.get("客服"),
                    }

    return None
