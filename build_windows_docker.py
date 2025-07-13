#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker Windows 构建脚本
在 Docker Windows 容器中构建真正的 Windows 可执行文件
作者: 程楠花开
"""

import os
import sys
import subprocess
import shutil
import time
import threading
from pathlib import Path

def safe_print(text, end='\n', flush=False):
    """安全的打印函数，处理编码问题
    
    Args:
        text (str): 要打印的文本
        end (str): 行结束符
        flush (bool): 是否立即刷新输出
    """
    try:
        print(text, end=end, flush=flush)
    except UnicodeEncodeError:
        # Windows 控制台编码处理
        if sys.platform.startswith('win'):
            safe_text = text.encode('gbk', 'ignore').decode('gbk')
            print(safe_text, end=end, flush=flush)
        else:
            safe_text = text.encode('utf-8', 'ignore').decode('utf-8')
            print(safe_text, end=end, flush=flush)
    except Exception as e:
        print(f"[Print Error: {e}]", end=end, flush=flush)

def show_progress():
    """显示构建进度动画"""
    chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    i = 0
    while not progress_stop:
        try:
            print(f"\r🔨 正在构建 Windows 可执行文件 {chars[i % len(chars)]}", end="", flush=True)
            i += 1
            time.sleep(0.1)
        except:
            # 如果出现错误，使用简单的点号显示
            print(".", end="", flush=True)
            time.sleep(0.5)

def check_environment():
    """检查 Docker 构建环境
    
    Returns:
        bool: 环境检查是否通过
    """
    safe_print("🔍 检查 Docker Windows 构建环境...")
    
    # 检查操作系统
    if not sys.platform.startswith('win'):
        safe_print("❌ 错误：此脚本需要在 Windows Docker 容器中运行")
        return False
    
    # 检查 Python 版本
    python_version = sys.version_info
    safe_print(f"🐍 Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        safe_print("⚠️ 警告：建议使用 Python 3.8 或更高版本")
    
    # 检查 PyInstaller
    try:
        import PyInstaller
        safe_print(f"📦 PyInstaller 版本: {PyInstaller.__version__}")
    except ImportError:
        safe_print("❌ 错误：未找到 PyInstaller")
        safe_print("请运行: pip install pyinstaller")
        return False
    
    # 检查必要文件
    required_files = ['directory_scanner.py', 'config.json']
    for file in required_files:
        if not os.path.exists(file):
            safe_print(f"❌ 错误：未找到必要文件 {file}")
            return False
    
    safe_print("✅ 环境检查通过")
    return True

def clean_build_dirs():
    """清理构建目录"""
    safe_print("🧹 清理构建目录...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                safe_print(f"  ✅ 已清理: {dir_name}")
            except Exception as e:
                safe_print(f"  ⚠️ 清理失败 {dir_name}: {e}")

def create_version_info():
    """创建 Windows 版本信息文件
    
    Returns:
        str: 版本信息文件路径
    """
    safe_print("📝 创建版本信息文件...")
    
    version_info = '''
# UTF-8
#
# 版本信息文件
#
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2, 1, 0, 0),
    prodvers=(2, 1, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [StringStruct(u'CompanyName', u'程楠花开'),
          StringStruct(u'FileDescription', u'目录扫描器 - 智能文件管理工具'),
          StringStruct(u'FileVersion', u'2.1.0.0'),
          StringStruct(u'InternalName', u'directory_scanner'),
          StringStruct(u'LegalCopyright', u'Copyright © 2024 程楠花开'),
          StringStruct(u'OriginalFilename', u'目录扫描器.exe'),
          StringStruct(u'ProductName', u'目录扫描器'),
          StringStruct(u'ProductVersion', u'2.1.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    version_file = 'version_info.txt'
    try:
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(version_info)
        safe_print(f"  ✅ 版本信息文件已创建: {version_file}")
        return version_file
    except Exception as e:
        safe_print(f"  ⚠️ 创建版本信息文件失败: {e}")
        return None

def build_windows_executable():
    """构建 Windows 可执行文件
    
    Returns:
        bool: 构建是否成功
    """
    global progress_stop
    progress_stop = False
    
    safe_print("🔨 开始构建 Windows 可执行文件...")
    
    # 启动进度显示线程
    progress_thread = threading.Thread(target=show_progress, daemon=True)
    progress_thread.start()
    
    try:
        # 创建版本信息文件
        version_file = create_version_info()
        
        # 构建 PyInstaller 命令
        cmd = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--name=目录扫描器',
            '--distpath=dist',
            '--workpath=build',
            '--specpath=.',
            '--clean',
            '--noconfirm'
        ]
        
        # 添加图标（如果存在）
        icon_files = ['icon.ico', 'icon.png']
        for icon_file in icon_files:
            if os.path.exists(icon_file):
                cmd.extend(['--icon', icon_file])
                safe_print(f"  📎 使用图标: {icon_file}")
                break
        
        # 添加版本信息
        if version_file and os.path.exists(version_file):
            cmd.extend(['--version-file', version_file])
        
        # 添加数据文件
        data_files = ['config.json', 'config_dev.json']
        for data_file in data_files:
            if os.path.exists(data_file):
                cmd.extend(['--add-data', f'{data_file};.'])
        
        # 隐藏导入
        hidden_imports = [
            'tkinter',
            'tkinter.ttk',
            'tkinter.filedialog',
            'tkinter.messagebox',
            'json',
            'os',
            'sys',
            'pathlib',
            'datetime',
            'threading',
            'queue'
        ]
        
        for module in hidden_imports:
            cmd.extend(['--hidden-import', module])
        
        # 排除不需要的模块
        exclude_modules = [
            'matplotlib',
            'numpy',
            'pandas',
            'scipy',
            'PIL',
            'cv2',
            'tensorflow',
            'torch'
        ]
        
        for module in exclude_modules:
            cmd.extend(['--exclude-module', module])
        
        # 添加主文件
        cmd.append('directory_scanner.py')
        
        # 停止进度显示
        progress_stop = True
        print()  # 换行
        
        safe_print("📋 PyInstaller 命令:")
        safe_print(f"  {' '.join(cmd)}")
        
        # 执行构建
        safe_print("\n🚀 开始执行构建...")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            safe_print("✅ PyInstaller 构建成功")
            
            # 检查生成的文件
            exe_path = Path('dist') / '目录扫描器.exe'
            if exe_path.exists():
                file_size = exe_path.stat().st_size / (1024 * 1024)
                safe_print(f"🎉 Windows 可执行文件构建成功!")
                safe_print(f"📁 文件位置: {exe_path}")
                safe_print(f"📏 文件大小: {file_size:.1f} MB")
                
                # 清理临时文件
                if version_file and os.path.exists(version_file):
                    os.remove(version_file)
                    safe_print(f"🧹 已清理临时文件: {version_file}")
                
                return True
            else:
                safe_print("❌ 错误：未找到生成的可执行文件")
                return False
        else:
            safe_print("❌ PyInstaller 构建失败")
            safe_print(f"错误输出: {result.stderr}")
            return False
            
    except Exception as e:
        progress_stop = True
        safe_print(f"\n❌ 构建过程出错: {e}")
        return False
    finally:
        progress_stop = True

def show_usage_instructions():
    """显示使用说明"""
    safe_print("\n" + "=" * 60)
    safe_print("📖 Windows 可执行文件使用说明")
    safe_print("=" * 60)
    
    safe_print("\n🎯 文件位置:")
    safe_print("• 可执行文件: dist/目录扫描器.exe")
    safe_print("• 这是真正的 Windows 可执行文件，可以在任何 Windows 系统上运行")
    
    safe_print("\n💻 使用方法:")
    safe_print("1. 将 dist/目录扫描器.exe 复制到目标 Windows 电脑")
    safe_print("2. 双击运行，无需安装 Python 环境")
    safe_print("3. 首次运行可能需要 Windows Defender 确认")
    
    safe_print("\n🔒 安全提示:")
    safe_print("• 如果 Windows 提示 '无法验证发布者'，点击 '仍要运行'")
    safe_print("• 这是正常现象，因为我们没有代码签名证书")
    safe_print("• 文件是安全的，由官方 Docker Windows 环境构建")
    
    safe_print("\n📋 技术信息:")
    safe_print("• 构建环境: Docker Windows Server Core")
    safe_print("• Python 版本: 3.11.7")
    safe_print("• 打包工具: PyInstaller")
    safe_print("• 目标架构: Windows x64")

def main():
    """主函数"""
    print("=" * 60)
    safe_print("🐳 Docker Windows 构建工具")
    safe_print("构建真正的 Windows 可执行文件")
    print("=" * 60)
    
    # 检查环境
    if not check_environment():
        safe_print("\n❌ 环境检查失败，构建终止")
        sys.exit(1)
    
    # 清理构建目录
    clean_build_dirs()
    
    # 构建可执行文件
    success = build_windows_executable()
    
    if success:
        show_usage_instructions()
        safe_print("\n🎉 Docker Windows 构建完成！")
        sys.exit(0)
    else:
        safe_print("\n❌ 构建失败，请检查错误信息")
        sys.exit(1)

# 全局变量
progress_stop = False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        progress_stop = True
        safe_print("\n⚠️ 用户取消构建")
        sys.exit(1)
    except Exception as e:
        progress_stop = True
        safe_print(f"\n❌ 程序出错: {e}")
        sys.exit(1)