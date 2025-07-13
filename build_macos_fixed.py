#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版macOS构建脚本
解决常见的打包问题
自动生成于打包问题诊断工具
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

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

def build_fixed_macos():
    """构建修复版macOS应用程序
    
    包含所有必要的修复参数
    """
    safe_print("🚀 开始构建修复版macOS应用程序...")
    
    # 清理之前的构建文件
    build_dirs = ['build', 'dist']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            safe_print(f"🧹 清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 增强的构建命令参数
    cmd = [
        'pyinstaller',
        '--onedir',              # 使用目录模式
        '--windowed',            # 无控制台窗口
        '--clean',               # 清理缓存
        '--noconfirm',           # 不询问确认
        '--name=目录扫描器',      # 应用名称
        '--icon=icon.png',       # 应用图标
        '--optimize=2',          # Python字节码优化
        '--strip',               # 去除调试符号
        
        # 排除不需要的模块
        '--exclude-module=matplotlib',
        '--exclude-module=scipy',
        '--exclude-module=PIL.ImageQt',
        '--exclude-module=PyQt5',
        '--exclude-module=PyQt6',
        '--exclude-module=PySide2',
        '--exclude-module=PySide6',
        '--exclude-module=IPython',
        '--exclude-module=jupyter',
        
        # 核心隐藏导入
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=openpyxl',
        
        # tkinter相关隐藏导入
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.simpledialog',
        
        # pandas相关隐藏导入
        '--hidden-import=pandas._libs.tslibs.timedeltas',
        '--hidden-import=pandas._libs.tslibs.np_datetime',
        '--hidden-import=pandas._libs.tslibs.nattype',
        '--hidden-import=pandas._libs.skiplist',
        '--hidden-import=pandas.io.formats.style',
        
        # numpy相关隐藏导入
        '--hidden-import=numpy.core._methods',
        '--hidden-import=numpy.lib.recfunctions',
        '--hidden-import=numpy.random.common',
        '--hidden-import=numpy.random.bounded_integers',
        '--hidden-import=numpy.random.entropy',
        
        # openpyxl相关隐藏导入
        '--hidden-import=openpyxl.cell',
        '--hidden-import=openpyxl.styles',
        '--hidden-import=openpyxl.chart',
        '--hidden-import=openpyxl.drawing',
        
        # 其他必要的隐藏导入
        '--hidden-import=datetime',
        '--hidden-import=pathlib',
        '--hidden-import=collections',
        '--hidden-import=json',
        '--hidden-import=threading',
        '--hidden-import=subprocess',
        '--hidden-import=fnmatch',
        
        # 收集所有子模块
        '--collect-all=numpy',
        '--collect-all=pandas',
        '--collect-all=openpyxl',
        
        # 禁用UPX压缩
        '--noupx',
        
        # 添加数据文件
        '--add-data=icon.png:.',
        
        # 主程序文件
        'directory_scanner.py'
    ]
    
    # 检查并添加额外的数据文件
    extra_data_files = ['icon.icns', 'config.json']
    for data_file in extra_data_files:
        if os.path.exists(data_file):
            cmd.insert(-1, f'--add-data={data_file}:.')
            safe_print(f"📄 添加数据文件: {data_file}")
    
    safe_print("📦 执行增强版PyInstaller构建...")
    safe_print(f"命令参数数量: {len(cmd)}")
    
    try:
        # 执行构建
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        safe_print("✅ 构建成功！")
        
        # 检查构建结果
        app_path = Path('dist/目录扫描器.app')
        if app_path.exists():
            safe_print(f"📱 应用程序已生成: {app_path.absolute()}")
            safe_print("\n🎉 修复版构建完成！")
            safe_print("\n🔧 应用的修复:")
            safe_print("• 增加了完整的隐藏导入配置")
            safe_print("• 包含了所有必要的数据文件")
            safe_print("• 优化了模块收集策略")
            safe_print("• 排除了不必要的大型模块")
            
        else:
            safe_print("❌ 未找到生成的应用程序")
            
    except subprocess.CalledProcessError as e:
        safe_print(f"❌ 构建失败: {e}")
        if e.stderr:
            safe_print(f"错误输出: {e.stderr}")
        return False
    except Exception as e:
        safe_print(f"❌ 构建过程中发生错误: {e}")
        return False
    
    return True

if __name__ == "__main__":
    safe_print("🔧 修复版macOS应用程序构建工具")
    print("=" * 50)
    build_fixed_macos()
