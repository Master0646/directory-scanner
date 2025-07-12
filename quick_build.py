#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速打包脚本 - 简化版本，专为解决打包卡顿问题
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

def quick_build():
    """快速打包函数 - 使用最简配置"""
    global progress_done
    progress_done = False
    
    current_dir = Path(__file__).parent
    script_path = current_dir / "directory_scanner.py"
    
    if not script_path.exists():
        print(f"❌ 找不到主程序文件: {script_path}")
        return False
    
    # 检查图标文件
    icon_path = current_dir / "icon.png"
    if not icon_path.exists():
        icon_path = None
        print("⚠️ 未找到icon.png，将使用默认图标")
    else:
        print(f"✅ 找到图标文件: {icon_path.name}")
    
    # 最简化的打包命令
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        "--name=目录扫描器"
    ]
    
    # 只在有图标时添加图标参数
    if icon_path:
        cmd.append(f"--icon={icon_path}")
    
    # 添加主脚本
    cmd.append(str(script_path))
    
    print("\n🚀 开始快速打包...")
    print(f"📝 执行命令: {' '.join(cmd)}")
    print("\n💡 提示: PyInstaller首次运行需要较长时间（3-10分钟），这是正常现象")
    print("   - 正在分析依赖关系")
    print("   - 正在收集模块文件")
    print("   - 正在生成可执行文件")
    print()
    
    # 启动进度显示线程
    progress_thread = threading.Thread(target=show_progress)
    progress_thread.daemon = True
    progress_thread.start()
    
    try:
        # 执行打包命令，不捕获输出以便实时显示
        result = subprocess.run(cmd, cwd=current_dir)
        progress_done = True
        
        if result.returncode == 0:
            print("\n🎉 打包成功！")
            
            # 查找生成的文件
            dist_dir = current_dir / "dist"
            if dist_dir.exists():
                files = list(dist_dir.glob("*"))
                if files:
                    for file in files:
                        print(f"📦 生成文件: {file}")
                        if file.is_file():
                            size_mb = file.stat().st_size / (1024*1024)
                            print(f"📏 文件大小: {size_mb:.1f} MB")
                        elif file.is_dir():
                            print(f"📁 应用包: {file.name}")
                
                print("\n✨ 使用说明:")
                print("1. 可执行文件位于 dist/ 目录")
                print("2. 双击即可运行，无需Python环境")
                print("3. 可以复制到其他Mac电脑使用")
                return True
            else:
                print("❌ 未找到生成的文件")
                return False
        else:
            progress_done = True
            print("\n❌ 打包失败")
            print("\n🔧 可能的解决方案:")
            print("1. 检查是否安装了所有依赖: pip install -r requirements.txt")
            print("2. 更新PyInstaller: pip install --upgrade pyinstaller")
            print("3. 清理缓存后重试: rm -rf build/ dist/ *.spec")
            return False
            
    except KeyboardInterrupt:
        progress_done = True
        print("\n⚠️ 用户取消打包")
        return False
    except Exception as e:
        progress_done = True
        print(f"\n❌ 打包过程出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("⚡ 目录扫描器 - 快速打包脚本")
    print("=" * 60)
    
    system = platform.system()
    print(f"🖥️  当前系统: {system}")
    print(f"🐍 Python版本: {sys.version.split()[0]}")
    
    if system != "Darwin":
        print("⚠️ 此脚本专为macOS优化，其他系统请使用 build.py")
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
    if quick_build():
        print("\n🎊 恭喜！打包完成")
        
        # 询问是否清理临时文件
        try:
            choice = input("\n🧹 是否清理临时文件？(y/n): ").lower().strip()
            if choice in ['y', 'yes', '是']:
                import shutil
                build_dir = Path(__file__).parent / "build"
                if build_dir.exists():
                    shutil.rmtree(build_dir)
                    print("✅ 临时文件已清理")
        except KeyboardInterrupt:
            print("\n👋 再见！")
    else:
        print("\n😞 打包失败，请检查错误信息")

if __name__ == "__main__":
    # 全局变量
    progress_done = False
    main()