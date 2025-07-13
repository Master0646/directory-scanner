#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目录文件扫描器 - 打包脚本
简洁高效的PyInstaller打包方案
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import time

class AppBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.app_name = "目录文件扫描器"
        self.main_script = "directory_scanner.py"
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        
    def check_environment(self):
        """检查打包环境"""
        print("🔍 检查打包环境...")
        
        # 检查Python版本
        if sys.version_info < (3, 7):
            print("❌ Python版本过低，需要3.7或更高版本")
            return False
        print(f"✅ Python版本: {sys.version.split()[0]}")
        
        # 检查主程序文件
        if not (self.project_root / self.main_script).exists():
            print(f"❌ 未找到主程序文件: {self.main_script}")
            return False
        print(f"✅ 主程序文件: {self.main_script}")
        
        # 检查依赖
        try:
            import pandas
            import openpyxl
            import tkinter
            print("✅ 核心依赖检查通过")
        except ImportError as e:
            print(f"❌ 依赖检查失败: {e}")
            return False
        
        return True
    
    def install_pyinstaller(self):
        """安装PyInstaller"""
        print("📦 检查PyInstaller...")
        try:
            import PyInstaller
            print(f"✅ PyInstaller已安装: {PyInstaller.__version__}")
            return True
        except ImportError:
            print("📥 安装PyInstaller...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
                print("✅ PyInstaller安装成功")
                return True
            except subprocess.CalledProcessError:
                print("❌ PyInstaller安装失败")
                return False
    
    def clean_build_dirs(self):
        """清理构建目录"""
        print("🧹 清理构建目录...")
        for dir_path in [self.dist_dir, self.build_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"✅ 已清理: {dir_path.name}")
    
    def find_icon(self):
        """查找图标文件"""
        icon_files = ["icon.icns","icon.ico", "icon.png" ]
        for icon_name in icon_files:
            icon_path = self.project_root / icon_name
            if icon_path.exists():
                print(f"✅ 找到图标: {icon_name}")
                return str(icon_path)
        print("⚠️ 未找到图标文件，使用默认图标")
        return None
    
    def build_command(self):
        """构建PyInstaller命令"""
        system = platform.system()
        print(f"🖥️ 目标平台: {system}")
        
        # 基础命令
        cmd = [
            "pyinstaller",
            "--clean",             # 清理临时文件
            "--noconfirm",         # 不确认覆盖
            f"--name={self.app_name}",
            "--log-level=WARN"     # 减少日志输出
        ]
        
        # 平台特定配置
        if system == "Darwin":  # macOS
            cmd.extend([
                "--windowed"      # 无控制台窗口
                # 不加--onefile，不加--target-architecture=universal2
            ])
        elif system == "Windows":
            cmd.extend([
                "--onefile",
                "--windowed",      # 无控制台窗口
                "--uac-admin"      # 请求管理员权限
            ])
        else:  # Linux
            cmd.extend([
                "--onefile",
                "--console"        # 保留控制台窗口
            ])
        
        # 添加图标
        icon_path = self.find_icon()
        if icon_path:
            cmd.extend(["--icon", icon_path])
        
        # 添加数据文件
        config_file = self.project_root / "config.json"
        if config_file.exists():
            cmd.extend(["--add-data", f"{config_file}:."])
        
        # 添加主程序
        cmd.append(self.main_script)
        
        return cmd
    
    def run_build(self, cmd):
        """执行打包命令"""
        print("🚀 开始打包...")
        print(f"📝 命令: {' '.join(cmd)}")
        
        start_time = time.time()
        
        try:
            # 执行打包命令
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            build_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ 打包成功！耗时: {build_time:.1f}秒")
                return True
            else:
                print(f"❌ 打包失败")
                print(f"错误信息: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 打包过程出错: {e}")
            return False
    
    def verify_output(self):
        """验证输出文件"""
        print("🔍 验证输出文件...")
        
        system = platform.system()
        if system == "Darwin":
            exe_name = f"{self.app_name}.app"
        elif system == "Windows":
            exe_name = f"{self.app_name}.exe"
        else:
            exe_name = self.app_name
        
        exe_path = self.dist_dir / exe_name
        
        if not exe_path.exists():
            print(f"❌ 未找到输出文件: {exe_path}")
            return False
        
        # 获取文件大小
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ 输出文件: {exe_path}")
        print(f"📏 文件大小: {size_mb:.1f} MB")
        
        return True
    
    def create_launcher(self):
        """创建启动脚本"""
        system = platform.system()
        
        if system == "Darwin":
            # macOS启动脚本
            launcher_content = f'''#!/bin/bash
# 目录文件扫描器启动脚本
cd "$(dirname "$0")"
./"{self.app_name}.app/Contents/MacOS/{self.app_name}" "$@"
'''
            launcher_path = self.dist_dir / "启动扫描器.command"
        elif system == "Windows":
            # Windows批处理文件
            launcher_content = f'''@echo off
cd /d "%~dp0"
start "" "{self.app_name}.exe" %*
'''
            launcher_path = self.dist_dir / "启动扫描器.bat"
        else:
            # Linux启动脚本
            launcher_content = f'''#!/bin/bash
# 目录文件扫描器启动脚本
cd "$(dirname "$0")"
./{self.app_name} "$@"
'''
            launcher_path = self.dist_dir / "启动扫描器.sh"
        
        # 写入启动脚本
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        # 设置执行权限
        if system != "Windows":
            os.chmod(launcher_path, 0o755)
        
        print(f"✅ 创建启动脚本: {launcher_path.name}")
    
    def build(self):
        """执行完整打包流程"""
        print("=" * 60)
        print(f"🔨 {self.app_name} - 打包工具")
        print("=" * 60)
        
        # 1. 检查环境
        if not self.check_environment():
            return False
        
        # 2. 安装PyInstaller
        if not self.install_pyinstaller():
            return False
        
        # 3. 清理构建目录
        self.clean_build_dirs()
        
        # 4. 构建命令
        cmd = self.build_command()
        
        # 5. 执行打包
        if not self.run_build(cmd):
            return False
        
        # 6. 验证输出
        if not self.verify_output():
            return False
        
        # 7. 创建启动脚本
        self.create_launcher()
        
        print("\n🎉 打包完成！")
        print(f"📁 输出目录: {self.dist_dir}")
        print("\n📋 使用说明:")
        print("1. 进入dist目录")
        print("2. 运行生成的可执行文件")
        print("3. 或使用启动脚本")
        
        return True

def main():
    """主函数"""
    builder = AppBuilder()
    
    try:
        success = builder.build()
        if success:
            print("\n✅ 打包成功完成！")
            sys.exit(0)
        else:
            print("\n❌ 打包失败！")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断打包")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 打包过程出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 