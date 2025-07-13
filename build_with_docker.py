#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker 构建管理脚本
使用 Docker 构建真正的 Windows 可执行文件
作者: 程楠花开
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

def safe_print(text):
    """安全的打印函数，处理编码问题
    
    Args:
        text (str): 要打印的文本
    """
    try:
        print(text)
    except UnicodeEncodeError:
        if sys.platform.startswith('win'):
            safe_text = text.encode('ascii', 'ignore').decode('ascii')
            print(safe_text)
        else:
            print(text.encode('utf-8', 'ignore').decode('utf-8'))
    except Exception:
        print("[Output encoding error - check logs for details]")

def check_docker():
    """检查 Docker 是否可用
    
    Returns:
        bool: Docker 是否可用
    """
    safe_print("🐳 检查 Docker 环境...")
    
    try:
        # 检查 Docker 是否安装
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            safe_print("❌ Docker 未安装或无法访问")
            return False
        
        safe_print(f"✅ {result.stdout.strip()}")
        
        # 检查 Docker 是否运行
        result = subprocess.run(['docker', 'info'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            safe_print("❌ Docker 服务未运行")
            safe_print("请启动 Docker Desktop 或 Docker 服务")
            return False
        
        safe_print("✅ Docker 服务正常运行")
        return True
        
    except subprocess.TimeoutExpired:
        safe_print("❌ Docker 命令超时")
        return False
    except FileNotFoundError:
        safe_print("❌ 未找到 Docker 命令")
        safe_print("请安装 Docker Desktop: https://www.docker.com/products/docker-desktop")
        return False
    except Exception as e:
        safe_print(f"❌ 检查 Docker 时出错: {e}")
        return False

def check_windows_support():
    """检查 Windows 容器支持
    
    Returns:
        bool: 是否支持 Windows 容器
    """
    safe_print("🪟 检查 Windows 容器支持...")
    
    try:
        # 在 macOS/Linux 上，需要使用远程 Windows Docker 或 GitHub Actions
        if not sys.platform.startswith('win'):
            safe_print("⚠️ 当前系统不是 Windows")
            safe_print("💡 建议使用以下方案之一:")
            safe_print("   1. GitHub Actions (推荐) - 自动化构建")
            safe_print("   2. Windows 虚拟机 + Docker")
            safe_print("   3. 远程 Windows Docker 主机")
            return False
        
        # 检查 Windows 容器模式
        result = subprocess.run(['docker', 'system', 'info', '--format', '{{.OSType}}'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            os_type = result.stdout.strip()
            if os_type.lower() == 'windows':
                safe_print("✅ Docker 已配置为 Windows 容器模式")
                return True
            else:
                safe_print(f"❌ Docker 当前为 {os_type} 容器模式")
                safe_print("请切换到 Windows 容器模式:")
                safe_print("   右键 Docker Desktop 图标 -> Switch to Windows containers")
                return False
        else:
            safe_print("❌ 无法检查容器模式")
            return False
            
    except Exception as e:
        safe_print(f"❌ 检查 Windows 容器支持时出错: {e}")
        return False

def build_docker_image():
    """构建 Docker 镜像
    
    Returns:
        bool: 构建是否成功
    """
    safe_print("🔨 构建 Docker 镜像...")
    
    try:
        cmd = [
            'docker', 'build',
            '-f', 'Dockerfile.windows',
            '-t', 'directory-scanner-windows:latest',
            '.'
        ]
        
        safe_print(f"📋 执行命令: {' '.join(cmd)}")
        safe_print("⏳ 这可能需要几分钟时间，请耐心等待...")
        
        # 执行构建
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT, text=True)
        
        # 实时显示输出
        for line in process.stdout:
            print(line.rstrip())
        
        process.wait()
        
        if process.returncode == 0:
            safe_print("✅ Docker 镜像构建成功")
            return True
        else:
            safe_print("❌ Docker 镜像构建失败")
            return False
            
    except Exception as e:
        safe_print(f"❌ 构建 Docker 镜像时出错: {e}")
        return False

def run_build_container():
    """运行构建容器
    
    Returns:
        bool: 构建是否成功
    """
    safe_print("🚀 运行构建容器...")
    
    try:
        # 确保 dist 目录存在
        dist_dir = Path('dist')
        dist_dir.mkdir(exist_ok=True)
        
        # 获取绝对路径
        current_dir = Path.cwd().resolve()
        dist_path = current_dir / 'dist'
        
        cmd = [
            'docker', 'run',
            '--rm',  # 运行完成后自动删除容器
            '-v', f'{dist_path}:C:\\app\\dist',  # 映射输出目录
            'directory-scanner-windows:latest'
        ]
        
        safe_print(f"📋 执行命令: {' '.join(cmd)}")
        safe_print("⏳ 正在构建 Windows 可执行文件...")
        
        # 执行构建
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT, text=True)
        
        # 实时显示输出
        for line in process.stdout:
            print(line.rstrip())
        
        process.wait()
        
        if process.returncode == 0:
            safe_print("✅ 容器构建完成")
            
            # 检查生成的文件
            exe_files = list(dist_dir.glob('*.exe'))
            if exe_files:
                for exe_file in exe_files:
                    file_size = exe_file.stat().st_size / (1024 * 1024)
                    safe_print(f"🎯 生成的可执行文件: {exe_file}")
                    safe_print(f"📏 文件大小: {file_size:.1f} MB")
                return True
            else:
                safe_print("❌ 未找到生成的可执行文件")
                return False
        else:
            safe_print("❌ 容器构建失败")
            return False
            
    except Exception as e:
        safe_print(f"❌ 运行构建容器时出错: {e}")
        return False

def show_alternative_solutions():
    """显示替代解决方案"""
    safe_print("\n" + "=" * 60)
    safe_print("🔄 替代解决方案")
    safe_print("=" * 60)
    
    safe_print("\n🚀 方案 1: GitHub Actions (推荐)")
    safe_print("• 优点: 完全自动化，无需本地 Windows 环境")
    safe_print("• 使用: git push 后自动构建")
    safe_print("• 获取: 从 GitHub Releases 或 Actions 下载")
    
    safe_print("\n💻 方案 2: Windows 虚拟机")
    safe_print("• 使用 VMware、VirtualBox 或 Parallels")
    safe_print("• 在虚拟机中安装 Python 和依赖")
    safe_print("• 直接运行 build_windows_fixed.py")
    
    safe_print("\n☁️ 方案 3: 云服务")
    safe_print("• 使用 AWS EC2 Windows 实例")
    safe_print("• 使用 Azure Windows 虚拟机")
    safe_print("• 使用 Google Cloud Windows 实例")
    
    safe_print("\n🛠️ 方案 4: 自动化工具")
    safe_print("• 运行: python get_windows_build.py")
    safe_print("• 自动检查并下载可用的 Windows 版本")

def show_usage_guide():
    """显示使用指南"""
    safe_print("\n" + "=" * 60)
    safe_print("📖 Docker 构建使用指南")
    safe_print("=" * 60)
    
    safe_print("\n🐳 前置要求:")
    safe_print("1. 安装 Docker Desktop")
    safe_print("2. 切换到 Windows 容器模式")
    safe_print("3. 确保 Docker 服务正在运行")
    
    safe_print("\n🔧 使用步骤:")
    safe_print("1. python build_with_docker.py")
    safe_print("2. 等待镜像构建完成")
    safe_print("3. 等待容器构建完成")
    safe_print("4. 在 dist/ 目录获取 .exe 文件")
    
    safe_print("\n📁 输出位置:")
    safe_print("• 可执行文件: dist/目录扫描器.exe")
    safe_print("• 这是真正的 Windows 可执行文件")
    
    safe_print("\n🔍 故障排除:")
    safe_print("• 如果构建失败，检查 Docker 日志")
    safe_print("• 确保有足够的磁盘空间 (>5GB)")
    safe_print("• 确保网络连接正常 (下载 Python)")

def main():
    """主函数"""
    print("=" * 60)
    safe_print("🐳 Docker Windows 构建管理工具")
    safe_print("使用 Docker 构建真正的 Windows 可执行文件")
    print("=" * 60)
    
    # 检查 Docker
    if not check_docker():
        show_alternative_solutions()
        return False
    
    # 检查 Windows 容器支持
    if not check_windows_support():
        show_alternative_solutions()
        return False
    
    safe_print("\n🎯 开始 Docker 构建流程...")
    
    # 构建 Docker 镜像
    if not build_docker_image():
        safe_print("\n❌ 镜像构建失败")
        return False
    
    # 运行构建容器
    if not run_build_container():
        safe_print("\n❌ 容器构建失败")
        return False
    
    safe_print("\n🎉 Docker 构建完成！")
    safe_print("📁 请检查 dist/ 目录中的 Windows 可执行文件")
    safe_print("💻 现在可以将 .exe 文件复制到任何 Windows 电脑使用")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            show_usage_guide()
            sys.exit(1)
    except KeyboardInterrupt:
        safe_print("\n⚠️ 用户取消操作")
        sys.exit(1)
    except Exception as e:
        safe_print(f"\n❌ 程序出错: {e}")
        show_usage_guide()
        sys.exit(1)