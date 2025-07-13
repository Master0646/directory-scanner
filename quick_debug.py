#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超快速调试脚本
一键运行，无需构建，适合日常开发调试
作者：张牛牛
"""

import os
import sys
import subprocess

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

def quick_run():
    """快速运行主程序
    
    直接运行Python脚本，跳过所有构建步骤
    适合：功能测试、界面调试、逻辑验证
    """
    safe_print("🚀 快速启动目录扫描器...")
    
    # 检查主程序文件
    if not os.path.exists('directory_scanner.py'):
        safe_print("❌ 错误：未找到 directory_scanner.py")
        safe_print("请确保在项目根目录运行此脚本")
        return False
    
    try:
        # 直接运行，实时显示输出
        safe_print("📱 启动应用程序...")
        safe_print("💡 提示：如果出现错误，请查看下方的错误信息")
        print("-" * 50)
        
        # 运行主程序
        result = subprocess.run([sys.executable, 'directory_scanner.py'])
        
        print("-" * 50)
        if result.returncode == 0:
            safe_print("✅ 程序正常退出")
        else:
            safe_print(f"⚠️  程序退出码: {result.returncode}")
            
        return result.returncode == 0
        
    except KeyboardInterrupt:
        safe_print("\n⏹️  用户中断程序")
        return True
    except Exception as e:
        safe_print(f"❌ 启动失败: {e}")
        return False

def check_quick():
    """快速检查环境
    
    检查基本的运行环境和依赖
    """
    safe_print("🔍 快速环境检查...")
    
    # Python版本
    version = sys.version_info
    print(f"Python: {version.major}.{version.minor}.{version.micro}")
    
    # 关键依赖
    deps = ['tkinter', 'pandas', 'openpyxl']
    missing = []
    
    for dep in deps:
        try:
            __import__(dep)
            safe_print(f"✅ {dep}")
        except ImportError:
            safe_print(f"❌ {dep} (缺失)")
            missing.append(dep)
    
    if missing:
        safe_print(f"\n⚠️  缺少依赖: {', '.join(missing)}")
        safe_print("运行: pip install -r requirements.txt")
        return False
    
    safe_print("✅ 环境检查通过")
    return True

def main():
    """主函数 - 超简化流程"""
    safe_print("⚡ 超快速调试工具")
    print("=" * 30)
    
    # 快速检查
    if not check_quick():
        safe_print("\n❌ 环境检查失败，请先安装依赖")
        return
    
    safe_print("\n🎯 选择操作:")
    safe_print("1. 🚀 直接运行 (推荐)")
    safe_print("2. 🔍 仅检查环境")
    safe_print("3. 📋 查看帮助")
    
    choice = input("\n选择 (1-3): ").strip()
    
    if choice == '1' or choice == '':
        quick_run()
    elif choice == '2':
        safe_print("\n✅ 环境检查已完成")
    elif choice == '3':
        show_help()
    else:
        safe_print("❌ 无效选择")

def show_help():
    """显示帮助信息"""
    help_text = """
📚 快速调试指南

🚀 直接运行模式:
   • 最快的调试方式
   • 无需构建，直接运行Python脚本
   • 适合功能测试和界面调试
   • 错误信息会直接显示在终端

🔧 常见问题解决:
   • 如果提示缺少依赖：pip install -r requirements.txt
   • 如果界面异常：检查tkinter是否正常安装
   • 如果导入错误：确保在项目根目录运行

💡 调试技巧:
   • 修改代码后直接重新运行，无需重新构建
   • 使用safe_print()语句添加调试信息
   • 在IDE中设置断点进行调试

🆚 对比其他方式:
   • GitHub Actions构建：慢，但测试完整打包
   • PyInstaller本地构建：中速，测试打包效果
   • 直接运行：最快，适合开发调试
"""
    print(help_text)

if __name__ == "__main__":
    main()