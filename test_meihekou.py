"""
测试梅河口市查询
"""

from local_data import get_province_from_local

# 测试梅河口市
result = get_province_from_local("梅河口市")
print("查询结果:")
print(result)

if result:
    print(f"\n✓ 省份: {result.get('province')}")
    print(f"✓ 城市: {result.get('city')}")
    print(f"✓ 区县: {result.get('district')}")
    print(f"✓ 级别: {result.get('level')}")
    print(f"✓ 介绍: {result.get('intro')}")
else:
    print("\n✗ 未找到匹配")
