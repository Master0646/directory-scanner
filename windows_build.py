#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows平台打包脚本 - 生成exe可执行文件
作者: 程楠花开
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import time
import threading

def show_progress():
    """显示打包进度动画"""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    i = 0
    while not progress_done:
        print(f"\r🔨 正在打包中 {chars[i % len(chars)]} 请耐心等待...", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print("\r✅ 打包完成！" + " " * 30)

def create_version_info():
    """创建Windows版本信息文件"""
    version_info = '''
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
# filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
# Set not needed items to zero 0.
filevers=(1,0,0,0),
prodvers=(1,0,0,0),
# Contains a bitmask that specifies the valid bits 'flags'r
mask=0x3f,
# Contains a bitmask that specifies the Boolean attributes of the file.
flags=0x0,
# The operating system for which this file was designed.
# 0x4 - NT and there is no need to change it.
OS=0x4,
# The general type of file.
# 0x1 - the file is an application.
fileType=0x1,
# The function of the file.
# 0x0 - the function is not defined for this fileType
subtype=0x0,
# Creation date and time stamp.
date=(0, 0)
),
  kids=[
StringFileInfo(
  [
  StringTable(
    u'040904B0',
    [StringStruct(u'CompanyName', u'程楠花开'),
    StringStruct(u'FileDescription', u'目录文件扫描器'),
    StringStruct(u'FileVersion', u'1.0.0.0'),
    StringStruct(u'InternalName', u'目录扫描器'),
    StringStruct(u'LegalCopyright', u'Copyright © 2024 程楠花开'),
    StringStruct(u'OriginalFilename', u'目录扫描器.exe'),
    StringStruct(u'ProductName', u'目录文件扫描器'),
    StringStruct(u'ProductVersion', u'1.0.0.0')])
  ]), 
VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    version_file = Path(__file__).parent / "version_info.txt"
    with open(version_file, 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    return version_file

def windows_build():
    """Windows平台打包函数"""
    global progress_done
    progress_done = False
    
    current_dir = Path(__file__).parent
    script_path = current_dir / "directory_scanner.py"
    
    if not script_path.exists():
        print(f"❌ 找不到主程序文件: {script_path}")
        return False
    
    # 检查图标文件
    icon_path = None
    for icon_name in ["icon.ico", "icon.png"]:
        test_path = current_dir / icon_name
        if test_path.exists():
            icon_path = test_path
            print(f"✅ 找到图标文件: {icon_path.name}")
            break
    
    if not icon_path:
        print("⚠️ 未找到图标文件，将使用默认图标")
    
    # 创建版本信息文件
    print("📝 创建Windows版本信息文件...")
    version_file = create_version_info()
    
    # Windows优化的打包命令
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        "--name=目录扫描器",
        "--distpath=dist/windows",
        "--workpath=build/windows",
        "--specpath=."
    ]
    
    # 添加版本信息
    cmd.extend(["--version-file", str(version_file)])
    
    # 添加图标
    if icon_path:
        cmd.extend(["--icon", str(icon_path)])
    
    # Windows特定优化 - 根据当前系统调整分隔符
    system = platform.system()
    data_separator = ":" if system != "Windows" else ";"
    
    # 检查配置文件是否存在
    config_file = current_dir / "config.json"
    if config_file.exists():
        cmd.extend(["--add-data", f"config.json{data_separator}."])
    
    cmd.extend([
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.filedialog",
        "--hidden-import", "tkinter.messagebox",
        "--hidden-import", "json",
        "--hidden-import", "pathlib",
        "--hidden-import", "os",
        "--hidden-import", "sys"
    ])
    
    # 排除不必要的模块以减小文件大小
    excluded_modules = [
        'numpy', 'scipy', 'pandas', 'matplotlib', 'sklearn',
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
        'jupyter', 'notebook', 'IPython',
        'sphinx', 'docutils', 'babel'
    ]
    
    for module in excluded_modules:
        cmd.extend(["--exclude-module", module])
    
    # 添加主脚本
    cmd.append(str(script_path))
    
    print("\n🚀 开始Windows平台打包...")
    print(f"📝 执行命令: {' '.join(cmd[:8])}... (已简化显示)")
    print("\n💡 提示: Windows exe打包需要较长时间（3-8分钟）")
    print("   - 正在分析依赖关系")
    print("   - 正在收集模块文件")
    print("   - 正在生成exe文件")
    print("   - 正在添加版本信息")
    print()
    
    # 启动进度显示线程
    progress_thread = threading.Thread(target=show_progress)
    progress_thread.daemon = True
    progress_thread.start()
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, cwd=current_dir, capture_output=True, text=True)
        progress_done = True
        
        if result.returncode == 0:
            print("\n🎉 Windows exe打包成功！")
            
            # 查找生成的文件
            dist_dir = current_dir / "dist" / "windows"
            if dist_dir.exists():
                files = list(dist_dir.glob("*.exe"))
                if files:
                    for file in files:
                        print(f"📦 生成文件: {file}")
                        size_mb = file.stat().st_size / (1024*1024)
                        print(f"📏 文件大小: {size_mb:.1f} MB")
                
                print("\n✨ Windows使用说明:")
                print("1. exe文件位于 dist/windows/ 目录")
                print("2. 双击即可运行，无需Python环境")
                print("3. 可以复制到其他Windows电脑使用")
                print("4. 支持Windows 7/8/10/11")
                
                # 清理版本信息文件
                if version_file.exists():
                    version_file.unlink()
                    print("🧹 已清理临时版本信息文件")
                
                return True
            else:
                print("❌ 未找到生成的exe文件")
                return False
        else:
            progress_done = True
            print("\n❌ Windows打包失败")
            print(f"错误信息: {result.stderr}")
            print("\n🔧 可能的解决方案:")
            print("1. 确保在Windows系统上运行此脚本")
            print("2. 检查PyInstaller版本: pip install --upgrade pyinstaller")
            print("3. 安装Windows SDK工具")
            print("4. 检查防病毒软件是否阻止了打包")
            return False
            
    except KeyboardInterrupt:
        progress_done = True
        print("\n⚠️ 用户取消打包")
        return False
    except Exception as e:
        progress_done = True
        print(f"\n❌ 打包过程出错: {e}")
        return False
    finally:
        # 确保清理临时文件
        if 'version_file' in locals() and version_file.exists():
            version_file.unlink()

def main():
    """主函数"""
    print("=" * 60)
    print("🪟 目录扫描器 - Windows平台打包脚本")
    print("=" * 60)
    
    system = platform.system()
    print(f"🖥️  当前系统: {system}")
    print(f"🐍 Python版本: {sys.version.split()[0]}")
    
    if system == "Windows":
        print("✅ 检测到Windows系统，开始打包")
    else:
        print("⚠️ 当前不是Windows系统，但仍可尝试交叉编译")
        choice = input("是否继续？(y/n): ").lower().strip()
        if choice not in ['y', 'yes', '是']:
            print("👋 已取消打包")
            return
    
    # 检查PyInstaller
    try:
        result = subprocess.run(["pyinstaller", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PyInstaller已安装: {result.stdout.strip()}")
        else:
            print("❌ PyInstaller未安装，正在安装...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    except FileNotFoundError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    print("\n" + "="*60)
    
    # 开始打包
    if windows_build():
        print("\n🎊 恭喜！Windows exe打包完成")
        
        # 询问是否清理临时文件
        try:
            choice = input("\n🧹 是否清理临时文件？(y/n): ").lower().strip()
            if choice in ['y', 'yes', '是']:
                import shutil
                build_dir = Path(__file__).parent / "build" / "windows"
                if build_dir.exists():
                    shutil.rmtree(build_dir)
                    print("✅ 临时文件已清理")
        except KeyboardInterrupt:
            print("\n👋 再见！")
    else:
        print("\n😞 打包失败，请检查错误信息")
        print("\n💡 提示: 如果在macOS上打包Windows版本，建议:")
        print("1. 使用Windows虚拟机")
        print("2. 使用GitHub Actions自动化打包")
        print("3. 使用Docker容器")

if __name__ == "__main__":
    # 全局变量
    progress_done = False
    main()