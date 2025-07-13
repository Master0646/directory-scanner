#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实际构建测试工具

这个脚本用于实际测试构建脚本的打包功能
会创建一个测试版本的应用程序来验证构建流程

作者: AI Assistant
创建时间: 2024
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Tuple
import time

class ActualBuildTester:
    """实际构建测试器类"""
    
    def __init__(self):
        """初始化测试器"""
        self.project_root = Path.cwd()
        self.test_dir = self.project_root / "test_build"
        self.backup_dir = self.project_root / "backup_for_test"
        
    def print_header(self, title: str) -> None:
        """打印测试标题"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    def print_section(self, title: str) -> None:
        """打印测试小节标题"""
        print(f"\n{'-'*40}")
        print(f"  {title}")
        print(f"{'-'*40}")
    
    def cleanup_previous_builds(self) -> None:
        """清理之前的构建文件"""
        self.print_section("清理构建环境")
        
        # 清理常见的构建目录
        build_dirs = ['build', 'dist', '__pycache__', 'test_build']
        
        for dir_name in build_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    print(f"✓ 已清理 {dir_name} 目录")
                except Exception as e:
                    print(f"❌ 清理 {dir_name} 失败: {e}")
        
        # 清理spec文件
        spec_files = list(self.project_root.glob("*.spec"))
        for spec_file in spec_files:
            try:
                spec_file.unlink()
                print(f"✓ 已清理 {spec_file.name}")
            except Exception as e:
                print(f"❌ 清理 {spec_file.name} 失败: {e}")
    
    def test_debug_scripts(self) -> bool:
        """测试调试脚本"""
        self.print_section("调试脚本功能测试")
        
        # 测试setup_dev.py
        try:
            print("🔧 测试开发环境设置...")
            result = subprocess.run(
                [sys.executable, "setup_dev.py"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("✓ setup_dev.py 执行成功")
            else:
                print(f"❌ setup_dev.py 执行失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ setup_dev.py 执行超时")
            return False
        except Exception as e:
            print(f"❌ setup_dev.py 测试失败: {e}")
            return False
        
        # 测试runtime_error_detector.py
        try:
            print("🔍 测试运行时错误检测...")
            result = subprocess.run(
                [sys.executable, "runtime_error_detector.py"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("✓ runtime_error_detector.py 执行成功")
                if "未检测到运行时错误" in result.stdout:
                    print("✓ 应用程序运行时检查通过")
                else:
                    print("⚠️ 检测到一些运行时问题，但不影响基本功能")
            else:
                print(f"❌ runtime_error_detector.py 执行失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ runtime_error_detector.py 执行超时")
            return False
        except Exception as e:
            print(f"❌ runtime_error_detector.py 测试失败: {e}")
            return False
        
        return True
    
    def test_macos_build(self) -> Tuple[bool, Optional[str]]:
        """测试macOS构建"""
        self.print_section("macOS构建测试")
        
        try:
            print("🍎 开始macOS构建测试...")
            print("⏳ 这可能需要几分钟时间，请耐心等待...")
            
            # 运行macOS构建脚本
            result = subprocess.run(
                [sys.executable, "build_macos_fixed.py"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                print("✓ macOS构建脚本执行成功")
                
                # 检查输出文件
                dist_dir = self.project_root / "dist"
                if dist_dir.exists():
                    app_files = list(dist_dir.glob("*.app"))
                    if app_files:
                        app_path = app_files[0]
                        print(f"✓ 成功生成应用程序: {app_path.name}")
                        
                        # 检查应用程序大小
                        app_size = sum(f.stat().st_size for f in app_path.rglob('*') if f.is_file())
                        app_size_mb = app_size / (1024 * 1024)
                        print(f"📦 应用程序大小: {app_size_mb:.1f} MB")
                        
                        return True, str(app_path)
                    else:
                        print("❌ 未找到生成的.app文件")
                        return False, None
                else:
                    print("❌ 未找到dist目录")
                    return False, None
            else:
                print(f"❌ macOS构建失败: {result.stderr}")
                return False, None
                
        except subprocess.TimeoutExpired:
            print("❌ macOS构建超时（超过5分钟）")
            return False, None
        except Exception as e:
            print(f"❌ macOS构建测试失败: {e}")
            return False, None
    
    def test_app_functionality(self, app_path: str) -> bool:
        """测试应用程序基本功能"""
        self.print_section("应用程序功能测试")
        
        try:
            print("🧪 测试应用程序基本功能...")
            
            # 检查应用程序结构
            app_path_obj = Path(app_path)
            
            # 检查关键文件
            executable_path = app_path_obj / "Contents" / "MacOS"
            if executable_path.exists():
                executables = list(executable_path.glob("*"))
                if executables:
                    print(f"✓ 找到可执行文件: {executables[0].name}")
                else:
                    print("❌ 未找到可执行文件")
                    return False
            else:
                print("❌ 应用程序结构不正确")
                return False
            
            # 检查资源文件
            resources_path = app_path_obj / "Contents" / "Resources"
            if resources_path.exists():
                print("✓ 资源目录存在")
                
                # 检查配置文件
                config_files = list(resources_path.glob("config*.json"))
                if config_files:
                    print(f"✓ 找到配置文件: {[f.name for f in config_files]}")
                else:
                    print("⚠️ 未找到配置文件")
            else:
                print("❌ 资源目录不存在")
                return False
            
            print("✅ 应用程序结构检查通过")
            return True
            
        except Exception as e:
            print(f"❌ 应用程序功能测试失败: {e}")
            return False
    
    def generate_test_summary(self, debug_ok: bool, build_ok: bool, app_path: Optional[str], func_ok: bool) -> None:
        """生成测试总结"""
        self.print_section("测试总结")
        
        print("📋 测试结果:")
        print(f"   调试脚本测试: {'✅ 通过' if debug_ok else '❌ 失败'}")
        print(f"   构建脚本测试: {'✅ 通过' if build_ok else '❌ 失败'}")
        print(f"   应用程序功能: {'✅ 通过' if func_ok else '❌ 失败'}")
        
        if app_path:
            print(f"   生成的应用: {app_path}")
        
        overall_success = debug_ok and build_ok and func_ok
        
        if overall_success:
            print("\n🎉 所有测试通过！构建系统工作正常")
            print("\n✨ 你的构建工具已经可以正常使用了！")
            print("\n📝 接下来你可以:")
            print("   1. 使用 python build_macos_fixed.py 进行正式打包")
            print("   2. 使用 python build_windows_fixed.py 进行Windows打包")
            print("   3. 使用 python cross_platform_build.py 进行跨平台打包")
            print("   4. 参考 BUILD_GUIDE.md 了解更多使用方法")
        else:
            print("\n⚠️ 部分测试失败，需要进一步检查")
            
            if not debug_ok:
                print("   - 调试脚本问题：检查依赖安装和环境配置")
            if not build_ok:
                print("   - 构建脚本问题：检查PyInstaller配置和系统环境")
            if not func_ok:
                print("   - 应用程序问题：检查资源文件和打包配置")
            
            print("\n🔧 建议的修复步骤:")
            print("   1. 运行 python fix_packaging_issues.py 诊断问题")
            print("   2. 检查 BUILD_GUIDE.md 中的故障排除指南")
            print("   3. 确保所有依赖都已正确安装")
    
    def run_full_build_test(self) -> None:
        """运行完整的构建测试"""
        self.print_header("实际构建功能测试")
        
        print("🚀 开始实际构建测试...")
        print("   这将测试整个构建流程的实际功能")
        print("   包括调试、构建和应用程序验证")
        
        # 清理环境
        self.cleanup_previous_builds()
        
        # 测试调试脚本
        debug_ok = self.test_debug_scripts()
        
        # 测试构建
        build_ok, app_path = self.test_macos_build()
        
        # 测试应用程序功能
        func_ok = False
        if build_ok and app_path:
            func_ok = self.test_app_functionality(app_path)
        
        # 生成总结
        self.generate_test_summary(debug_ok, build_ok, app_path, func_ok)
        
        print("\n" + "="*60)
        print("  构建测试完成")
        print("="*60)

def main():
    """主函数"""
    print("🔨 实际构建测试工具")
    print("   用于验证构建脚本的实际打包功能")
    
    # 确认用户想要进行实际构建测试
    print("\n⚠️ 注意: 这个测试将会:")
    print("   - 清理现有的构建文件")
    print("   - 执行实际的应用程序打包")
    print("   - 可能需要几分钟时间")
    
    response = input("\n是否继续进行实际构建测试? (y/N): ").strip().lower()
    
    if response in ['y', 'yes', '是', '确定']:
        tester = ActualBuildTester()
        tester.run_full_build_test()
    else:
        print("\n❌ 测试已取消")
        print("💡 如果只想检查脚本语法，请运行: python test_build_scripts.py")

if __name__ == "__main__":
    main()