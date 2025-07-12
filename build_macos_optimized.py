#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS优化构建脚本
解决PyInstaller打包后启动缓慢的问题
作者：张牛牛
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_optimized_macos():
    """
    构建优化的macOS应用程序
    使用--onedir模式替代--onefile以提升启动速度
    """
    print("🚀 开始构建优化的macOS应用程序...")
    
    # 清理之前的构建文件
    build_dirs = ['build', 'dist']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            print(f"🧹 清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 构建命令参数
    cmd = [
        'pyinstaller',
        '--onedir',              # 使用目录模式而非单文件模式
        '--windowed',            # 无控制台窗口
        '--clean',               # 清理缓存
        '--noconfirm',           # 不询问确认
        '--name=目录扫描器',      # 应用名称
        '--icon=icon.png',       # 应用图标
        '--optimize=2',          # Python字节码优化级别
        '--strip',               # 去除调试符号
        '--exclude-module=matplotlib',  # 排除不需要的大型模块
        '--exclude-module=numpy',
        '--exclude-module=scipy',
        '--exclude-module=PIL.ImageQt',
        '--exclude-module=PyQt5',
        '--exclude-module=PyQt6',
        '--exclude-module=PySide2',
        '--exclude-module=PySide6',
        '--add-data=icon.png:.',  # 添加图标文件
        'directory_scanner.py'    # 主程序文件
    ]
    
    print("📦 执行PyInstaller构建...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        # 执行构建
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 构建成功！")
        
        # 检查构建结果
        app_path = Path('dist/目录扫描器.app')
        if app_path.exists():
            print(f"📱 应用程序已生成: {app_path.absolute()}")
            
            # 计算应用大小
            size = get_directory_size(app_path)
            print(f"📏 应用大小: {format_size(size)}")
            
            # 提供使用说明
            print("\n🎉 构建完成！")
            print("\n📋 使用说明:")
            print(f"1. 应用位置: {app_path.absolute()}")
            print("2. 双击即可运行")
            print("3. 首次运行可能需要允许未知开发者应用")
            print("4. 启动速度已优化，比单文件模式快很多")
            
            # 性能优化说明
            print("\n⚡ 性能优化:")
            print("• 使用--onedir模式避免解压延迟")
            print("• 启用字节码优化(--optimize=2)")
            print("• 去除调试符号(--strip)")
            print("• 排除不必要的大型模块")
            
        else:
            print("❌ 未找到生成的应用程序")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ 构建过程中发生错误: {e}")
        return False
    
    return True

def get_directory_size(path):
    """
    计算目录大小
    
    Args:
        path (Path): 目录路径
        
    Returns:
        int: 目录大小（字节）
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def format_size(size_bytes):
    """
    格式化文件大小显示
    
    Args:
        size_bytes (int): 字节大小
        
    Returns:
        str: 格式化的大小字符串
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def check_dependencies():
    """
    检查构建依赖
    
    Returns:
        bool: 依赖是否满足
    """
    print("🔍 检查构建依赖...")
    
    # 检查PyInstaller
    try:
        result = subprocess.run(['pyinstaller', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ PyInstaller版本: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller未安装，请运行: pip install pyinstaller")
        return False
    
    # 检查主程序文件
    if not os.path.exists('directory_scanner.py'):
        print("❌ 未找到主程序文件: directory_scanner.py")
        return False
    
    # 检查图标文件
    if not os.path.exists('icon.png'):
        print("⚠️  未找到图标文件: icon.png")
        print("   构建将继续，但应用将使用默认图标")
    
    print("✅ 依赖检查完成")
    return True

def main():
    """
    主函数
    """
    print("🔧 macOS应用程序优化构建工具")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 执行构建
    if build_optimized_macos():
        print("\n🎊 构建成功完成！")
        print("\n💡 提示: 如果启动仍然较慢，可以尝试:")
        print("1. 将应用移动到/Applications目录")
        print("2. 首次运行后，macOS会缓存应用，后续启动会更快")
        print("3. 确保系统有足够的可用内存")
    else:
        print("\n💥 构建失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()