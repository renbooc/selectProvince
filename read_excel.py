import pandas as pd

# 读取Excel文件
file_path = "7357e693383bb48ace55f9bd96fe6d8f.XLSX"

try:
    # 读取所有sheet
    xlsx = pd.ExcelFile(file_path)
    print(f"Sheet names: {xlsx.sheet_names}")
    print("\n" + "=" * 60)

    for sheet_name in xlsx.sheet_names:
        print(f"\nSheet: {sheet_name}")
        print("-" * 60)

        df = pd.read_excel(xlsx, sheet_name=sheet_name)
        # 设置pandas显示选项
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)
        pd.set_option("display.unicode.east_asian_width", True)

        print(df)
        print()

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
