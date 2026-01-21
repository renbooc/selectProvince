#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
销售网点查询系统 - 桌面版打包脚本

使用方法:
    python build_desktop.py

输出:
    dist/销售网点查询系统.exe
"""

import os
import sys
import subprocess
import shutil


def check_dependencies():
    """检查并安装依赖"""
    print("📦 检查依赖...")

    # 检查PyInstaller
    try:
        import PyInstaller

        print("✅ PyInstaller 已安装")
    except ImportError:
        print("🔧 正在安装 PyInstaller...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyinstaller"], check=True
        )
        print("✅ PyInstaller 安装完成")

    # 检查requests
    try:
        import requests

        print("✅ requests 已安装")
    except ImportError:
        print("🔧 正在安装 requests...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        print("✅ requests 安装完成")


def build_executable():
    """打包可执行文件"""
    print("\n🚀 开始打包...")
    print("   这可能需要几分钟时间，请耐心等待...\n")

    # PyInstaller命令参数
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",  # 打包成单个exe
        "--windowed",  # 无控制台窗口（GUI应用）
        "--name",
        "销售网点查询系统",
        "--clean",  # 清理临时文件
        "--add-data",
        "templates;templates",
        "--hidden-import",
        "requests",
        "--hidden-import",
        "flask",
        "--hidden-import",
        "jinja2",
        "--hidden-import",
        "markupsafe",
        "--hidden-import",
        "werkzeug",
        "--hidden-import",
        "click",
        "--hidden-import",
        "itsdangerest",
        "--hidden-import",
        "certifi",
        "--hidden-import",
        "charset_normalizer",
        "--hidden-import",
        "idna",
        "--hidden-import",
        "urllib3",
        "app.py",
    ]

    # 执行打包
    result = subprocess.run(cmd, capture_output=False)

    return result.returncode == 0


def main():
    """主函数"""
    print("=" * 60)
    print("   销售网点查询系统 - 桌面版打包工具")
    print("=" * 60)
    print()

    # 检查依赖
    check_dependencies()

    # 打包
    success = build_executable()

    print()
    print("=" * 60)
    if success:
        exe_path = os.path.join("dist", "销售网点查询系统.exe")
        if os.path.exists(exe_path):
            print("✅ 打包成功！")
            print()
            print(f"📂 输出目录: {os.path.abspath(exe_path)}")
            print()
            print("🚀 双击 '销售网点查询系统.exe' 即可运行")

            # 询问是否删除build目录
            print()
            ans = input("是否删除临时文件目录? (y/n): ").strip().lower()
            if ans == "y" or ans == "yes":
                if os.path.exists("build"):
                    shutil.rmtree("build")
                    print("✅ 已删除 build 目录")
        else:
            print("❌ 打包失败：未找到输出文件")
    else:
        print("❌ 打包失败，请检查上方错误信息")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已取消打包")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback

        traceback.print_exc()
