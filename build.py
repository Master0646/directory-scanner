#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动打包脚本
用于将目录扫描器打包为可执行文件
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print("✓ PyInstaller已安装")
        return True
    except ImportError:
        print("✗ PyInstaller未安装")
        return False

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller安装成功")
        return True
    except subprocess.CalledProcessError:
        print("✗ PyInstaller安装失败")
        return False

def build_executable():
    """构建可执行文件"""
    current_dir = Path(__file__).parent
    script_path = current_dir / "directory_scanner.py"
    
    # 查找支持的图标文件格式（优先使用PNG，避免SVG格式）
    icon_path = None
    # 按优先级排序：PNG > ICO > ICNS，完全排除SVG
    supported_icons = ["icon.png", "icon.ico", "icon.icns"]
    
    for icon_name in supported_icons:
        potential_icon = current_dir / icon_name
        if potential_icon.exists():
            icon_path = potential_icon
            print(f"✓ 使用图标文件: {icon_path.name}")
            break
    
    if not script_path.exists():
        print(f"✗ 找不到主程序文件: {script_path}")
        return False
    
    # 获取系统信息
    system = platform.system()
    print(f"当前系统: {system}")
    
    # 检查图标文件
    if icon_path:
        print(f"✓ 找到图标文件: {icon_path.name}")
    else:
        print("⚠️ 未找到支持的图标文件 (ico/png/icns)，将使用默认图标")
        # 检查是否存在SVG文件
        svg_icon = current_dir / "icon.svg"
        if svg_icon.exists():
            print("💡 提示: 发现icon.svg文件，但PyInstaller不支持SVG格式")
            print("   建议将SVG转换为ICO或PNG格式以获得更好的图标支持")
    
    # 基础构建命令
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm"
    ]
    
    # 添加系统特定选项和名称
    if system == "Windows":
        # Windows特定选项
        cmd.extend([
            "--name=DirectoryScanner",
            "--noconsole",  # 隐藏控制台窗口
            "--version-file=version_info.txt" if (current_dir / "version_info.txt").exists() else ""
        ])
        # 如果有支持的图标文件，添加图标
        if icon_path and icon_path.exists():
            cmd.append(f"--icon={icon_path}")
            
    elif system == "Darwin":  # macOS
        # macOS特定选项（简化配置，避免卡顿）
        cmd.extend([
            "--name=目录扫描器",
            "--osx-bundle-identifier=com.chengnanhuakai.directoryscanner"
        ])
        # 如果有支持的图标文件，添加图标
        if icon_path and icon_path.exists():
            cmd.append(f"--icon={icon_path}")
            
    elif system == "Linux":
        # Linux特定选项
        cmd.extend([
            "--name=DirectoryScanner"
        ])
        if icon_path and icon_path.exists():
            cmd.append(f"--icon={icon_path}")
    
    # 过滤空字符串
    cmd = [c for c in cmd if c]
    
    # 添加主脚本路径
    cmd.append(str(script_path))
    
    print("开始打包...")
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, cwd=current_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ 打包成功！")
            
            # 查找生成的可执行文件
            dist_dir = current_dir / "dist"
            if dist_dir.exists():
                exe_files = list(dist_dir.glob("*"))
                if exe_files:
                    for exe_file in exe_files:
                        print(f"可执行文件位置: {exe_file}")
                        if exe_file.is_file():
                            print(f"文件大小: {exe_file.stat().st_size / (1024*1024):.1f} MB")
                        elif exe_file.is_dir() and system == "Darwin":
                            print(f"应用包大小: {get_dir_size(exe_file) / (1024*1024):.1f} MB")
                else:
                    print("未找到生成的可执行文件")
            
            # 显示系统特定的使用说明
            print_usage_instructions(system)
            
            return True
        else:
            print("✗ 打包失败")
            print("错误信息:")
            print(result.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ 打包过程中发生错误: {e}")
        return False
    except FileNotFoundError:
        print("✗ 找不到pyinstaller命令，请确认已正确安装")
        return False

def get_dir_size(path):
    """计算目录大小"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def print_usage_instructions(system):
    """打印系统特定的使用说明"""
    print("\n" + "=" * 50)
    print("使用说明:")
    print("=" * 50)
    
    if system == "Windows":
        print("Windows版本:")
        print("1. 可执行文件: DirectoryScanner.exe")
        print("2. 双击运行即可使用")
        print("3. 无需安装Python环境")
        print("4. 可在任何Windows 10+系统上运行")
        
    elif system == "Darwin":
        print("macOS版本:")
        print("1. 应用包: 目录扫描器.app")
        print("2. 拖拽到应用程序文件夹")
        print("3. 双击运行或从启动台启动")
        print("4. 支持Intel和Apple Silicon Mac")
        print("5. 首次运行可能需要在系统偏好设置中允许")
        
    elif system == "Linux":
        print("Linux版本:")
        print("1. 可执行文件: DirectoryScanner")
        print("2. 添加执行权限: chmod +x DirectoryScanner")
        print("3. 运行: ./DirectoryScanner")
        print("4. 无需安装Python环境")

def create_version_info():
    """为Windows创建版本信息文件"""
    if platform.system() != "Windows":
        return
        
    current_dir = Path(__file__).parent
    version_file = current_dir / "version_info.txt"
    
    version_info = '''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
# filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
# Set not needed items to zero 0.
filevers=(2,0,0,0),
prodvers=(2,0,0,0),
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
StringStruct(u'FileDescription', u'目录文件扫描器 - 智能目录分析工具'),
StringStruct(u'FileVersion', u'2.0.0.0'),
StringStruct(u'InternalName', u'DirectoryScanner'),
StringStruct(u'LegalCopyright', u'© 2024 程楠花开. All rights reserved.'),
StringStruct(u'OriginalFilename', u'DirectoryScanner.exe'),
StringStruct(u'ProductName', u'目录文件扫描器'),
StringStruct(u'ProductVersion', u'2.0.0.0')])
]),
VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
]
)'''
    
    try:
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(version_info)
        print(f"✓ 创建版本信息文件: {version_file}")
    except Exception as e:
        print(f"✗ 创建版本信息文件失败: {e}")

def clean_build_files():
    """清理构建文件"""
    current_dir = Path(__file__).parent
    
    # 要清理的目录和文件
    clean_targets = [
        "build",
        "__pycache__",
        "*.spec"
    ]
    
    print("清理构建文件...")
    
    for target in clean_targets:
        if "*" in target:
            # 处理通配符
            for file in current_dir.glob(target):
                if file.is_file():
                    file.unlink()
                    print(f"删除文件: {file.name}")
        else:
            # 处理目录
            target_path = current_dir / target
            if target_path.exists() and target_path.is_dir():
                import shutil
                shutil.rmtree(target_path)
                print(f"删除目录: {target}")

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 目录扫描器 - 跨平台自动打包脚本 v2.0")
    print("=" * 60)
    
    # 显示当前系统信息
    system = platform.system()
    arch = platform.machine()
    print(f"当前系统: {system} ({arch})")
    print(f"Python版本: {sys.version.split()[0]}")
    
    # 检查依赖
    print("\n📦 检查打包依赖...")
    if not check_pyinstaller():
        print("\n正在安装PyInstaller...")
        if not install_pyinstaller():
            print("❌ 安装失败，请手动安装: pip install pyinstaller")
            return
    
    # 为Windows创建版本信息文件
    if system == "Windows":
        print("\n📝 创建Windows版本信息...")
        create_version_info()
    
    print("\n🔨 开始构建可执行文件...")
    
    # 构建可执行文件
    if build_executable():
        print("\n✅ 构建完成！")
        
        # 询问是否清理构建文件
        try:
            choice = input("\n🧹 是否清理构建临时文件？(y/n): ").lower().strip()
            if choice in ['y', 'yes', '是', 'Y']:
                clean_build_files()
                print("✅ 清理完成")
        except KeyboardInterrupt:
            print("\n⚠️ 用户取消操作")
        
        print("\n" + "=" * 60)
        print("🎉 打包完成！可执行文件位于 dist/ 目录中")
        print("=" * 60)
        
        # 显示分发说明
        print("\n📋 分发说明:")
        if system == "Windows":
            print("• Windows用户: 分发 DirectoryScanner.exe")
        elif system == "Darwin":
            print("• macOS用户: 分发 目录扫描器.app")
            print("• 可以压缩为zip文件便于传输")
        elif system == "Linux":
            print("• Linux用户: 分发 DirectoryScanner")
            print("• 记得告知用户添加执行权限")
        
        print("\n💡 提示:")
        print("• 目标用户无需安装Python环境")
        print("• 首次运行可能需要系统安全确认")
        print("• 建议在目标系统上测试运行")
        
    else:
        print("\n❌ 构建失败，请检查上述错误信息")
        print("\n🔧 常见解决方案:")
        print("1. 确保所有依赖包已正确安装")
        print("2. 检查Python环境是否完整")
        print("3. 尝试更新PyInstaller: pip install --upgrade pyinstaller")
        print("4. 检查防病毒软件是否阻止了打包过程")

if __name__ == "__main__":
    main()