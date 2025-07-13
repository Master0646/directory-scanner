#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版Windows构建脚本
解决常见的Windows打包问题
基于macOS修复版的经验优化
作者: 程楠花开
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import time
import threading
import shutil

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
    """创建Windows版本信息文件
    
    Returns:
        Path: 版本信息文件路径
    """
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

def build_fixed_windows():
    """构建修复版Windows应用程序
    
    包含所有必要的修复参数，解决常见的打包问题
    
    Returns:
        bool: 构建是否成功
    """
    global progress_done
    progress_done = False
    
    print("🚀 开始构建修复版Windows应用程序...")
    
    current_dir = Path(__file__).parent
    script_path = current_dir / "directory_scanner.py"
    
    if not script_path.exists():
        print(f"❌ 找不到主程序文件: {script_path}")
        return False
    
    # 清理之前的构建文件
    build_dirs = ['build/windows', 'dist/windows']
    for dir_name in build_dirs:
        dir_path = current_dir / dir_name
        if dir_path.exists():
            print(f"🧹 清理目录: {dir_name}")
            shutil.rmtree(dir_path)
    
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
    
    # 增强的Windows构建命令参数
    cmd = [
        'pyinstaller',
        '--onefile',             # 单文件模式
        '--windowed',            # 无控制台窗口
        '--clean',               # 清理缓存
        '--noconfirm',           # 不询问确认
        '--name=目录扫描器',      # 应用名称
        '--distpath=dist/windows',  # 输出目录
        '--workpath=build/windows', # 工作目录
        '--specpath=.',          # spec文件位置
        '--optimize=2',          # Python字节码优化
    ]
    
    # 添加版本信息
    cmd.extend(['--version-file', str(version_file)])
    
    # 添加图标
    if icon_path:
        cmd.extend(['--icon', str(icon_path)])
    
    # Windows特定的数据分隔符
    system = platform.system()
    data_separator = ":" if system != "Windows" else ";"
    
    # 检查并添加数据文件
    data_files = ['config.json', 'icon.png', 'icon.ico']
    for data_file in data_files:
        file_path = current_dir / data_file
        if file_path.exists():
            cmd.extend(['--add-data', f'{data_file}{data_separator}.'])
            print(f"📄 添加数据文件: {data_file}")
    
    # 核心隐藏导入（基于macOS修复版经验）
    hidden_imports = [
        # 基础模块
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        'json',
        'pathlib',
        'os',
        'sys',
        'datetime',
        'collections',
        'threading',
        'subprocess',
        'fnmatch',
        
        # 如果项目使用了pandas/numpy/openpyxl，添加相关导入
        # 注意：这里先注释掉，避免不必要的依赖
        # 'pandas',
        # 'numpy', 
        # 'openpyxl',
        # 'pandas._libs.tslibs.timedeltas',
        # 'pandas._libs.tslibs.np_datetime',
        # 'pandas._libs.tslibs.nattype',
        # 'pandas._libs.skiplist',
        # 'pandas.io.formats.style',
        # 'numpy.core._methods',
        # 'numpy.lib.recfunctions',
        # 'openpyxl.cell',
        # 'openpyxl.styles',
    ]
    
    for hidden_import in hidden_imports:
        cmd.extend(['--hidden-import', hidden_import])
    
    # 排除不必要的大型模块以减小文件大小
    excluded_modules = [
        'matplotlib', 'scipy', 'pandas', 'numpy', 'sklearn',
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
        'jupyter', 'notebook', 'IPython',
        'sphinx', 'docutils', 'babel',
        'PIL.ImageQt', 'cv2', 'tensorflow', 'torch'
    ]
    
    for module in excluded_modules:
        cmd.extend(['--exclude-module', module])
    
    # 禁用UPX压缩（避免兼容性问题）
    cmd.append('--noupx')
    
    # 添加主脚本
    cmd.append(str(script_path))
    
    print("📦 执行增强版PyInstaller构建...")
    print(f"命令参数数量: {len(cmd)}")
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
        # 执行构建
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
                
                print("\n🎉 修复版Windows构建完成！")
                print("\n🔧 应用的修复:")
                print("• 增加了完整的隐藏导入配置")
                print("• 包含了所有必要的数据文件")
                print("• 优化了模块排除策略")
                print("• 禁用了UPX压缩避免兼容性问题")
                print("• 添加了Windows版本信息")
                
                print("\n✨ Windows使用说明:")
                print("1. exe文件位于 dist/windows/ 目录")
                print("2. 双击即可运行，无需Python环境")
                print("3. 可以复制到其他Windows电脑使用")
                print("4. 支持Windows 7/8/10/11")
                
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
            print("5. 尝试以管理员权限运行")
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
        if version_file.exists():
            version_file.unlink()
            print("🧹 已清理临时版本信息文件")

def check_windows_environment():
    """检查Windows构建环境
    
    Returns:
        bool: 环境是否满足要求
    """
    print("🔍 检查Windows构建环境...")
    
    system = platform.system()
    print(f"🖥️  当前系统: {system}")
    print(f"🐍 Python版本: {sys.version.split()[0]}")
    
    if system == "Windows":
        print("✅ 检测到Windows系统，环境最佳")
    else:
        print("⚠️ 当前不是Windows系统，可能需要交叉编译")
        print("💡 建议使用以下方案:")
        print("   1. Windows虚拟机")
        print("   2. GitHub Actions自动化打包")
        print("   3. Docker容器")
    
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
    
    # 检查主程序文件
    if not os.path.exists('directory_scanner.py'):
        print("❌ 未找到主程序文件: directory_scanner.py")
        return False
    
    print("✅ 环境检查完成")
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("🪟 目录扫描器 - 修复版Windows打包脚本")
    print("=" * 60)
    
    # 检查环境
    if not check_windows_environment():
        print("❌ 环境检查失败，无法继续")
        sys.exit(1)
    
    system = platform.system()
    if system != "Windows":
        choice = input("\n是否继续尝试交叉编译？(y/n): ").lower().strip()
        if choice not in ['y', 'yes', '是']:
            print("👋 已取消打包")
            return
    
    print("\n" + "="*60)
    
    # 开始打包
    if build_fixed_windows():
        print("\n🎊 恭喜！Windows exe打包完成")
        
        # 询问是否清理临时文件
        try:
            choice = input("\n🧹 是否清理临时文件？(y/n): ").lower().strip()
            if choice in ['y', 'yes', '是']:
                build_dir = Path(__file__).parent / "build" / "windows"
                if build_dir.exists():
                    shutil.rmtree(build_dir)
                    print("✅ 临时文件已清理")
        except KeyboardInterrupt:
            print("\n👋 再见！")
    else:
        print("\n😞 打包失败，请检查错误信息")
        print("\n💡 如果问题持续存在，建议:")
        print("1. 使用 python fix_packaging_issues.py 诊断问题")
        print("2. 查看 BUILD_GUIDE.md 获取更多帮助")
        print("3. 考虑使用GitHub Actions自动化打包")

if __name__ == "__main__":
    # 全局变量
    progress_done = False
    main()