# 使用二进制方式读取并尝试不同编码
file_path = "7357e693383bb48ace55f9bd96fe6d8f.XLSX"

# 首先检查文件头
with open(file_path, "rb") as f:
    header = f.read(10)
    print(f"文件头: {header}")
    print(f"文件头hex: {header.hex()}")

# 使用xlrd读取
try:
    import xlrd

    wb = xlrd.open_workbook(file_path)
    sheet = wb.sheet_by_index(0)

    print(f"\n工作表: {sheet.name}")
    print(f"行数: {sheet.nrows}")
    print(f"列数: {sheet.ncols}")

    print("\n内容：")
    for row_idx in range(sheet.nrows):
        row = sheet.row(row_idx)
        values = []
        for cell in row:
            if cell.ctype == xlrd.XL_CELL_EMPTY:
                values.append("")
            else:
                values.append(str(cell.value))
        print(f"行{row_idx + 1}: {values}")

except ImportError:
    print("xlrd未安装，尝试其他方法")
except Exception as e:
    print(f"xlrd读取错误: {e}")
