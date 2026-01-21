# encoding: utf-8
import sys

sys.stdout.reconfigure(encoding="utf-8")

from customer_data import get_customer_by_province
from local_data import get_province_from_local

# 测试通过城市名查询省份，然后获取客户信息
test_cases = [
    "祁东县",  # 湖南
    "景德镇",  # 江西
    "汕头市",  # 广东
    "梅河口市",  # 吉林
    "武汉市",  # 湖北
]

print("完整查询流程测试")
print("=" * 60)

for city in test_cases:
    print(f"\n查询城市: {city}")

    # 1. 先查询省份
    province_info = get_province_from_local(city)
    if province_info:
        province = province_info.get("province", "")
        print(f"  省份: {province}")

        # 2. 根据省份查询客户信息
        customer_info = get_customer_by_province(province)
        if customer_info:
            print(
                f"  ✓ 客户分配: {customer_info['manager']} -> 客服 {customer_info['customer_service']}"
            )
        else:
            print(f"  ✗ 未找到客户分配信息")
    else:
        print(f"  ✗ 未找到省份信息")
