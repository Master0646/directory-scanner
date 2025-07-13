#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows专用构建脚本
解决Windows环境下的编码和构建问题
"""

import os
import sys
import subprocess
from pathlib import Path

def safe_print(text):
    """安全的打印函数"""
    try:
        print(text)
    except UnicodeEncodeError:
        if sys.platform.startswith('win'):
            safe_text = text.encode('ascii', 'ignore').decode('ascii')
            print(safe_text if safe_text.strip() else "[Unicode content]")
        else:
            print(text.encode('utf-8', 'ignore').decode('utf-8'))
    except Exception:
        print("[Encoding error]")

def main():
    """主函数"""
    safe_print("Windows Build Script")
    safe_print("=" * 30)
    
    # 设置环境变量
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    # 构建命令
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=DirectoryScanner',
        '--add-data=config.json;.',
        '--add-data=icon.png;.',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=openpyxl',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageTk',
        '--exclude-module=matplotlib',
        '--exclude-module=scipy',
        '--exclude-module=IPython',
        '--exclude-module=jupyter',
        '--noupx',
        'directory_scanner.py'
    ]
    
    try:
        safe_print("Starting build process...")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            safe_print("Build completed successfully!")
            safe_print(f"Executable created in dist/ directory")
        else:
            safe_print(f"Build failed with return code: {result.returncode}")
            safe_print(f"Error: {result.stderr}")
            
    except Exception as e:
        safe_print(f"Build error: {e}")

if __name__ == "__main__":
    main()
