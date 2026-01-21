"""
客户搜索API测试脚本
"""

import requests
import json
from config_api import get_customer_api_config

def test_search_api():
    """测试搜索接口"""
    api_config = get_customer_api_config()
    base_url = api_config["base_url"]
    auth_url = f"{base_url}{api_config['auth_url']}"
    search_url = f"{base_url}{api_config['search_url']}"
    credentials = api_config['credentials']

    print("=" * 60)
    print("步骤1: 获取Token")
    print("=" * 60)

    # 获取Token
    try:
        response = requests.post(auth_url, params=credentials, timeout=10)
        response.raise_for_status()
        auth_result = response.json()
        print(f"认证响应: {json.dumps(auth_result, ensure_ascii=False, indent=2)}")

        token = auth_result.get("access_token")
        if not token:
            print("错误: 无法获取Token")
            return

        print(f"Token: {token[:50]}...")
        print()

    except Exception as e:
        print(f"认证失败: {e}")
        return

    print("=" * 60)
    print("步骤2: 测试搜索接口")
    print("=" * 60)

    keyword = "福州市长乐区福春大药房"

    # 测试不同的认证方式
    auth_methods = [
        {"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        {"Authorization": token, "Content-Type": "application/json"},
        {"token": token, "Content-Type": "application/json"},
        {"access_token": token, "Content-Type": "application/json"},
    ]

    for i, headers in enumerate(auth_methods):
        print(f"\n测试方式 {i+1}: {headers}")
        try:
            params = {
                "name": keyword,
                "page": 1,
                "page_size": 50
            }

            response = requests.get(
                search_url,
                params=params,
                headers=headers,
                timeout=10
            )

            print(f"状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")

            if response.status_code == 200:
                print(f"响应体: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
                print("\n✅ 成功！")
                break
            else:
                print(f"错误响应: {response.text}")

        except Exception as e:
            print(f"请求失败: {e}")

if __name__ == "__main__":
    test_search_api()