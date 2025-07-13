#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试启动器 - 开发专用
自动加载开发配置，启用调试模式
"""

import os
import sys

# 设置开发环境变量
os.environ['APP_ENV'] = 'development'
os.environ['DEBUG'] = '1'
os.environ['PYTHONUNBUFFERED'] = '1'

# 添加当前目录到Python路径
sys.path.insert(0, os.getcwd())

if __name__ == "__main__":
    try:
        safe_print("🐛 调试模式启动...")
        safe_print(f"📁 工作目录: {os.getcwd()}")
        safe_print(f"🐍 Python版本: {sys.version}")
        print("-" * 50)
        
        # 导入并运行主程序
        import directory_scanner
        directory_scanner.main()
        
    except ImportError as e:
        safe_print(f"❌ 导入错误: {e}")
        safe_print("请确保所有依赖已安装: pip install -r requirements.txt")
    except Exception as e:
        safe_print(f"❌ 运行错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        safe_print("\n🔚 调试会话结束")

def safe_print(text):
    """安全的打印函数，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        import sys
        if sys.platform.startswith('win'):
            safe_text = text.encode('ascii', 'ignore').decode('ascii')
            if not safe_text.strip():
                safe_text = "[Unicode content - check logs for details]"
            print(safe_text)
        else:
            print(text.encode('utf-8', 'ignore').decode('utf-8'))
    except Exception:
        print("[Output encoding error - check logs for details]")

