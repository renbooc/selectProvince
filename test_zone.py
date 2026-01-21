# encoding: utf-8
import sys

sys.stdout.reconfigure(encoding="utf-8")

from customer_data import get_customer_by_province

# 测试各个省份的区域划分
test_provinces = [
    # 南方区
    "湖南省",
    "广东省",
    "江西省",
    "江苏省",
    "浙江省",
    "安徽省",
    "湖北省",
    "四川省",
    "重庆市",
    "广西壮族自治区",
    "贵州省",
    "云南省",
    "陕西省",
    "山东省",
    # 北方区
    "黑龙江省",
    "吉林省",
    "辽宁省",
    "河北省",
    "北京市",
    "天津市",
    "河南省",
    "山西省",
    "内蒙古自治区",
    "福建省",
]

print("区域划分测试")
print("=" * 70)

南方区_count = 0
北方区_count = 0

for province in test_provinces:
    result = get_customer_by_province(province)
    if result:
        zone = result.get("zone", "N/A")
        print(
            f"{province:12} -> {zone:6} | {result.get('manager', 'N/A'):8} -> {result.get('customer_service', 'N/A')}"
        )
        if zone == "南方区":
            南方区_count += 1
        elif zone == "北方区":
            北方区_count += 1
    else:
        print(f"{province:12} -> 未找到")

print("=" * 70)
print(f"南方区: {南方区_count} 个省份")
print(f"北方区: {北方区_count} 个省份")
