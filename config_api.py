"""
API配置文件
存储外部API的认证信息和配置
"""

# 客户查询API配置
CUSTOMER_API_CONFIG = {
    # API基础URL
    "base_url": "https://sk.hytyao.com",
    # 认证接口
    "auth_url": "/auth/token",
    # 客户查询接口
    "search_url": "/api/customer/search",
    # 认证凭据（请根据实际情况配置）
    "credentials": {
        "access_id": "hytyao-sk-erp",  # 请在此处填写实际的access_id
        "secret_key": "Hyt2025SkErpApi@Xk9mN3pQ7wR5tY1z",  # 请在此处填写实际的secret_key
    },
    # 请求超时时间（秒）
    "timeout": 10,
    # 分页配置
    "default_page_size": 50,
}


def get_customer_api_config():
    """获取客户API配置"""
    return CUSTOMER_API_CONFIG
