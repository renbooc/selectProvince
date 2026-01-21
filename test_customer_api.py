"""
客户API测试脚本
用于调试API认证和查询接口
"""

import requests
import json
from config_api import get_customer_api_config

def test_auth_api():
    """测试认证接口"""
    api_config = get_customer_api_config()
    auth_url = f"{api_config['base_url']}{api_config['auth_url']}"
    credentials = api_config['credentials']

    print("=" * 60)
    print("测试认证接口")
    print("=" * 60)
    print(f"认证URL: {auth_url}")
    print(f"用户名: {credentials['username']}")
    print()

    # 测试1: JSON格式
    print("测试1: JSON格式请求")
    try:
        response = requests.post(
            auth_url,
            json=credentials,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应体: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"错误: {e}")
    print()

    # 测试2: 表单格式
    print("测试2: 表单格式请求")
    try:
        response = requests.post(
            auth_url,
            data=credentials,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应体: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"错误: {e}")
    print()

    # 测试3: GET请求
    print("测试3: GET请求")
    try:
        response = requests.get(
            auth_url,
            params=credentials,
            timeout=10
        )
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应体: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"错误: {e}")
    print()

if __name__ == "__main__":
    test_auth_api()