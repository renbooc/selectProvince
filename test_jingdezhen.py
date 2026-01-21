"""
测试景德镇查询
"""

# 简单测试
keyword = "景德镇"

print(f"查询关键词: {keyword}")
print("-" * 50)

# 检查本地数据中的江西省
from local_data import LOCAL_AREA_DATA

if "江西省" in LOCAL_AREA_DATA:
    cities = LOCAL_AREA_DATA["江西省"].get("cities", {})
    print("江西省城市列表:")
    for city in cities.keys():
        print(f"  - {city}")

    print()
    # 检查景德镇
    if "景德镇" in cities:
        print(f"✓ 找到景德镇市: {cities['景德镇']}")
    else:
        print("✗ 未找到景德镇市")
        # 检查模糊匹配
        for city in cities.keys():
            if keyword in city or city in keyword:
                print(f"✓ 模糊匹配: {city}")
else:
    print("本地数据中没有江西省")
