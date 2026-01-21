import requests

# 测试腾讯地图API
TENCENT_MAP_KEY = "FJRBZ-CKJC4-XAYUB-FYIE6-STLPZ-UHFGT"


def test_api():
    url = f"https://apis.map.qq.com/ws/district/v1/search"
    params = {"keyword": "祁东县", "key": TENCENT_MAP_KEY, "output": "json"}

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    print("API返回状态:", data.get("status"))
    print("返回消息:", data.get("message"))
    print("\n结果结构:")

    results = data.get("result", [])
    for i, level_results in enumerate(results):
        print(f"\n层级 {i}:")
        if level_results:
            for district in level_results:
                print(
                    f"  - {district.get('fullname', district.get('name', 'N/A'))} (ID: {district.get('id', 'N/A')})"
                )
        else:
            print("  (无数据)")


if __name__ == "__main__":
    test_api()
