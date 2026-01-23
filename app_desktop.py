"""
海元堂查询系统 - 桌面版
使用pywebview嵌入浏览器窗口运行Flask应用
支持Windows 10/11
"""

import sys
import os
import threading
import webview


def run_flask():
    from app import app
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


def main():
    if __name__ == "__main__":
        print("海元堂查询系统启动中...")
        
        threading.Thread(target=run_flask, daemon=True).start()

        webview.create_window(
            title="海元堂查询系统",
            url="http://127.0.0.1:5000/",
            width=1200,
            height=800,
            resizable=True,
            background_color="#FFFFFF",
        )
        print("窗口启动中...")
        webview.start(debug=False)


if __name__ == "__main__":
    main()
