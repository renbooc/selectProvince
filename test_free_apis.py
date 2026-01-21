import requests


def test_free_apis():
    # 测试 dwo.cc 行政区划API
    print("=== 测试 dwo.cc 行政区划API ===")
    try:
        url = "https://api.dwo.cc/api/convert"
        params = {"text": "祁东县"}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        print(f"状态: {response.status_code}")
        print(f"返回: {data}")
    except Exception as e:
        print(f"错误: {e}")

    # 测试 aa1.cn 的API
    print("\n=== 测试 aa1.cn 行政区划API ===")
    try:
        # 这个API需要用行政区划代码查询
        url = "https://zj.v.api.aa1.cn/api/xz/"
        params = {"code": "430426"}  # 祁东县代码
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        print(f"状态: {response.status_code}")
        print(f"返回: {data}")
    except Exception as e:
        print(f"错误: {e}")

    # 测试另一个免费API
    print("\n=== 测试 23bt.cn 行政区划API ===")
    try:
        url = "https://api.23bt.cn/doc/123"  # 这个可能需要查看具体文档
        print("需要查看具体文档")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    test_free_apis()
