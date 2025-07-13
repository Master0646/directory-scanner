#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地快速调试脚本
提供多种调试方案，避免依赖GitHub Actions的慢速构建
作者：张牛牛
"""

import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path
import time

def check_dependencies():
    """检查调试所需的依赖
    
    Returns:
        bool: 依赖是否满足
    """
    print("🔍 检查调试环境...")
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"✅ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查必要的包
    required_packages = ['tkinter', 'pandas', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}: 已安装")
        except ImportError:
            print(f"❌ {package}: 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖检查通过")
    return True

def run_direct():
    """方案1：直接运行Python脚本（最快）
    
    适用于：快速功能测试、界面调试
    """
    print("\n🚀 方案1：直接运行Python脚本")
    print("=" * 40)
    
    if not os.path.exists('directory_scanner.py'):
        print("❌ 未找到主程序文件: directory_scanner.py")
        return False
    
    try:
        print("📱 启动应用程序...")
        # 直接运行Python脚本
        subprocess.run([sys.executable, 'directory_scanner.py'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 运行失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️  用户中断运行")
        return True

def build_quick_test():
    """方案2：快速构建测试（中等速度）
    
    适用于：测试打包效果、依赖问题调试
    """
    print("\n📦 方案2：快速构建测试")
    print("=" * 40)
    
    # 检查PyInstaller
    try:
        result = subprocess.run(['pyinstaller', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ PyInstaller版本: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller未安装，请运行: pip install pyinstaller")
        return False
    
    # 创建临时构建目录
    temp_dir = tempfile.mkdtemp(prefix='debug_build_')
    print(f"📁 临时构建目录: {temp_dir}")
    
    try:
        # 快速构建命令（最小化参数）
        cmd = [
            'pyinstaller',
            '--onedir',              # 目录模式（比onefile快）
            '--windowed',            # 无控制台
            '--clean',               # 清理缓存
            '--noconfirm',           # 不询问
            '--distpath', temp_dir,  # 输出到临时目录
            '--workpath', os.path.join(temp_dir, 'work'),  # 工作目录
            '--specpath', temp_dir,  # spec文件目录
            '--name=DebugTest',      # 简单名称
            '--hidden-import=pandas',
            '--hidden-import=numpy',
            '--hidden-import=openpyxl',
            'directory_scanner.py'
        ]
        
        print("⚡ 开始快速构建...")
        start_time = time.time()
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        build_time = time.time() - start_time
        print(f"⏱️  构建耗时: {build_time:.1f}秒")
        
        if result.returncode == 0:
            app_path = os.path.join(temp_dir, 'DebugTest')
            if os.path.exists(app_path):
                print(f"✅ 构建成功: {app_path}")
                
                # 询问是否运行
                response = input("\n🤔 是否运行构建的应用？(y/n): ")
                if response.lower() in ['y', 'yes', '是']:
                    try:
                        if sys.platform == 'darwin':  # macOS
                            subprocess.run(['open', f"{app_path}.app"])
                        else:
                            subprocess.run([app_path])
                        print("🎉 应用已启动")
                    except Exception as e:
                        print(f"❌ 启动失败: {e}")
                
                return True
            else:
                print("❌ 构建文件未找到")
                return False
        else:
            print(f"❌ 构建失败:\n{result.stderr}")
            return False
            
    finally:
        # 清理临时文件
        try:
            shutil.rmtree(temp_dir)
            print(f"🧹 已清理临时目录: {temp_dir}")
        except Exception as e:
            print(f"⚠️  清理临时目录失败: {e}")

def test_imports():
    """方案3：测试导入依赖（最快的问题诊断）
    
    适用于：快速诊断导入问题、依赖冲突
    """
    print("\n🔬 方案3：测试导入依赖")
    print("=" * 40)
    
    # 测试主要导入
    imports_to_test = [
        ('tkinter', 'GUI框架'),
        ('pandas', '数据处理'),
        ('numpy', '数值计算'),
        ('openpyxl', 'Excel处理'),
        ('datetime', '日期时间'),
        ('threading', '多线程'),
        ('pathlib', '路径处理'),
        ('fnmatch', '文件匹配'),
        ('collections', '集合工具'),
        ('subprocess', '进程管理'),
        ('json', 'JSON处理')
    ]
    
    success_count = 0
    total_count = len(imports_to_test)
    
    for module_name, description in imports_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name:12} - {description}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module_name:12} - {description} (错误: {e})")
        except Exception as e:
            print(f"⚠️  {module_name:12} - {description} (异常: {e})")
    
    print(f"\n📊 导入测试结果: {success_count}/{total_count} 成功")
    
    if success_count == total_count:
        print("🎉 所有依赖导入正常！")
        
        # 测试主程序导入
        print("\n🧪 测试主程序导入...")
        try:
            # 尝试导入主程序的关键部分
            import directory_scanner
            print("✅ 主程序导入成功")
            
            # 测试创建主类（不启动GUI）
            print("🧪 测试主类创建...")
            # 这里不实际创建GUI，只是验证类定义
            if hasattr(directory_scanner, 'DirectoryScanner'):
                print("✅ DirectoryScanner类定义正常")
            else:
                print("❌ DirectoryScanner类未找到")
                
        except Exception as e:
            print(f"❌ 主程序导入失败: {e}")
            return False
    else:
        print("❌ 存在依赖问题，请先解决导入错误")
        return False
    
    return True

def run_with_debug():
    """方案4：调试模式运行（详细日志）
    
    适用于：问题诊断、错误追踪
    """
    print("\n🐛 方案4：调试模式运行")
    print("=" * 40)
    
    if not os.path.exists('directory_scanner.py'):
        print("❌ 未找到主程序文件: directory_scanner.py")
        return False
    
    try:
        print("🔍 启动调试模式...")
        print("📝 详细日志将显示在控制台")
        print("⏹️  按Ctrl+C停止运行\n")
        
        # 设置调试环境变量
        env = os.environ.copy()
        env['PYTHONPATH'] = os.getcwd()
        env['PYTHONUNBUFFERED'] = '1'  # 实时输出
        
        # 运行时显示详细信息
        subprocess.run([
            sys.executable, '-v',  # 详细模式
            'directory_scanner.py'
        ], env=env, check=True)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 调试运行失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️  调试会话结束")
        return True

def show_menu():
    """显示调试选项菜单
    
    Returns:
        str: 用户选择的选项
    """
    print("\n" + "=" * 50)
    print("🛠️  本地快速调试工具")
    print("=" * 50)
    print("\n选择调试方案:")
    print("\n1️⃣  直接运行 (最快，适合功能测试)")
    print("2️⃣  快速构建测试 (中速，测试打包效果)")
    print("3️⃣  导入依赖测试 (最快，诊断导入问题)")
    print("4️⃣  调试模式运行 (详细日志，问题追踪)")
    print("5️⃣  运行所有测试 (全面检查)")
    print("0️⃣  退出")
    
    return input("\n请选择 (1-5, 0退出): ").strip()

def run_all_tests():
    """运行所有测试方案
    
    Returns:
        bool: 是否所有测试都通过
    """
    print("\n🧪 运行所有测试方案")
    print("=" * 40)
    
    tests = [
        ("依赖检查", check_dependencies),
        ("导入测试", test_imports),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔄 执行: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name}: 通过")
            else:
                print(f"❌ {test_name}: 失败")
        except Exception as e:
            print(f"💥 {test_name}: 异常 - {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 40)
    print("📊 测试总结:")
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！可以尝试直接运行或快速构建")
        return True
    else:
        print("⚠️  存在问题，建议先解决失败的测试项")
        return False

def main():
    """主函数"""
    while True:
        choice = show_menu()
        
        if choice == '0':
            print("\n👋 再见！")
            break
        elif choice == '1':
            if check_dependencies():
                run_direct()
        elif choice == '2':
            if check_dependencies():
                build_quick_test()
        elif choice == '3':
            test_imports()
        elif choice == '4':
            if check_dependencies():
                run_with_debug()
        elif choice == '5':
            run_all_tests()
        else:
            print("❌ 无效选择，请重新输入")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()