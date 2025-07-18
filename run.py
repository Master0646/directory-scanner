#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目录扫描器启动脚本
用于快速启动程序并处理可能的错误
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """检查依赖包是否已安装"""
    missing_packages = []
    
    try:
        import tkinter
    except ImportError:
        missing_packages.append("tkinter (通常随Python一起安装)")
    
    try:
        import pandas
    except ImportError:
        missing_packages.append("pandas")
    
    try:
        import openpyxl
    except ImportError:
        missing_packages.append("openpyxl")
    
    return missing_packages

def install_dependencies():
    """安装缺失的依赖包"""
    print("正在安装依赖包...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError:
        print("✗ 依赖包安装失败")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("目录文件扫描器 v1.0")
    print("=" * 50)
    
    # 检查依赖
    missing = check_dependencies()
    if missing:
        print("缺少以下依赖包:")
        for pkg in missing:
            print(f"  - {pkg}")
        
        choice = input("\n是否自动安装依赖包？(y/n): ").lower().strip()
        if choice in ['y', 'yes', '是']:
            if not install_dependencies():
                print("\n请手动安装依赖包:")
                print("pip install -r requirements.txt")
                return
        else:
            print("\n请手动安装依赖包后再运行程序")
            return
    
    # 启动主程序
    try:
        print("\n正在启动目录扫描器...")
        from directory_scanner import main as scanner_main
        scanner_main()
    except ImportError as e:
        print(f"\n导入错误: {e}")
        print("请确保所有文件都在同一目录下")
    except Exception as e:
        print(f"\n程序运行错误: {e}")
        print("请检查系统环境和依赖包")

if __name__ == "__main__":
    main()