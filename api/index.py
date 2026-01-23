"""
Vercel Serverless Function 入口文件
将 Flask 应用适配为 Vercel 的 Serverless Functions
"""
import sys
import os

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app

# Vercel 会自动检测并使用这个 WSGI 应用
# 无需额外的 handler 函数，直接导出 app 即可
