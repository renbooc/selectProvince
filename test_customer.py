# encoding: utf-8
import sys

sys.stdout.reconfigure(encoding="utf-8")

# 测试客户分配查询
from customer_data import get_customer_by_province

# 测试
print("客户分配查询测试")
print("=" * 60)

results = [
    ("陕西", None),
    ("广东", None),
    ("江苏", None),
    ("湖北", None),
]

for province, _ in results:
    result = get_customer_by_province(province)
    print(f"\n{province}:")
    if result:
        print(f"  区域: {result.get('zone', 'N/A')}")
        print(f"  省区经理: {result.get('manager', 'N/A')}")
        print(f"  客服: {result.get('customer_service', 'N/A')}")
        print(f"  负责区域: {result.get('region', 'N/A')}")
    else:
        print(f"  未找到")
