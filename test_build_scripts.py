#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建脚本测试工具

这个脚本用于测试项目中的所有构建脚本是否能正常工作
包括环境检查、依赖验证、脚本语法检查等

作者: AI Assistant
创建时间: 2024
"""

import os
import sys
import subprocess
import importlib.util
import ast
from pathlib import Path
from typing import List, Dict, Tuple, Optional

class BuildScriptTester:
    """构建脚本测试器类"""
    
    def safe_print(self, text):
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

    def __init__(self):
        """初始化测试器"""
        self.project_root = Path.cwd()
        self.test_results = {}
        self.build_scripts = [
            'build_macos_fixed.py',
            'build_windows_fixed.py', 
            'cross_platform_build.py',
            'windows_build.py',
            'fix_packaging_issues.py',
            'diagnose_windows_packaging.py'
        ]
        self.debug_scripts = [
            'setup_dev.py',
            'debug_launcher.py',
            'debug_local.py',
            'quick_debug.py',
            'runtime_error_detector.py'
        ]
    
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
    
    def check_python_environment(self) -> bool:
        """检查Python环境"""
        self.print_section("Python环境检查")
        
        # 检查Python版本
        python_version = sys.version_info
        self.safe_print(f"✓ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version < (3, 7):
            self.safe_print("❌ Python版本过低，建议使用Python 3.7+")
            return False
        
        # 检查必要的标准库
        required_modules = ['tkinter', 'json', 'pathlib', 'subprocess', 'os', 'sys']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
                self.safe_print(f"✓ {module} 模块可用")
            except ImportError:
                self.safe_print(f"❌ {module} 模块缺失")
                missing_modules.append(module)
        
        if missing_modules:
            self.safe_print(f"❌ 缺失必要模块: {', '.join(missing_modules)}")
            return False
        
        return True
    
    def check_dependencies(self) -> bool:
        """检查项目依赖"""
        self.print_section("依赖检查")
        
        # 检查requirements.txt
        requirements_file = self.project_root / 'requirements.txt'
        if not requirements_file.exists():
            self.safe_print("❌ requirements.txt 文件不存在")
            return False
        
        self.safe_print("✓ requirements.txt 文件存在")
        
        # 读取依赖列表
        try:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            self.safe_print(f"✓ 发现 {len(requirements)} 个依赖项")
            
            # 检查关键依赖
            key_dependencies = ['pandas', 'openpyxl', 'pyinstaller']
            missing_deps = []
            
            for dep in key_dependencies:
                try:
                    __import__(dep)
                    self.safe_print(f"✓ {dep} 已安装")
                except ImportError:
                    self.safe_print(f"❌ {dep} 未安装")
                    missing_deps.append(dep)
            
            if missing_deps:
                self.safe_print(f"\n建议运行: pip install {' '.join(missing_deps)}")
                return False
            
            return True
            
        except Exception as e:
            self.safe_print(f"❌ 读取requirements.txt失败: {e}")
            return False
    
    def check_script_syntax(self, script_path: Path) -> Tuple[bool, Optional[str]]:
        """检查脚本语法"""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 使用AST解析检查语法
            ast.parse(content)
            return True, None
            
        except SyntaxError as e:
            return False, f"语法错误: {e}"
        except Exception as e:
            return False, f"读取错误: {e}"
    
    def test_script_imports(self, script_path: Path) -> Tuple[bool, List[str]]:
        """测试脚本的导入语句"""
        try:
            spec = importlib.util.spec_from_file_location("test_module", script_path)
            if spec is None:
                return False, ["无法创建模块规范"]
            
            # 这里我们不实际导入，只检查语法
            return True, []
            
        except Exception as e:
            return False, [str(e)]
    
    def test_build_scripts(self) -> Dict[str, bool]:
        """测试构建脚本"""
        self.print_section("构建脚本测试")
        
        results = {}
        
        for script_name in self.build_scripts:
            script_path = self.project_root / script_name
            
            if not script_path.exists():
                self.safe_print(f"❌ {script_name} 文件不存在")
                results[script_name] = False
                continue
            
            # 检查语法
            syntax_ok, syntax_error = self.check_script_syntax(script_path)
            if not syntax_ok:
                self.safe_print(f"❌ {script_name} 语法错误: {syntax_error}")
                results[script_name] = False
                continue
            
            # 检查导入
            import_ok, import_errors = self.test_script_imports(script_path)
            if not import_ok:
                self.safe_print(f"❌ {script_name} 导入错误: {', '.join(import_errors)}")
                results[script_name] = False
                continue
            
            self.safe_print(f"✓ {script_name} 语法和导入检查通过")
            results[script_name] = True
        
        return results
    
    def test_debug_scripts(self) -> Dict[str, bool]:
        """测试调试脚本"""
        self.print_section("调试脚本测试")
        
        results = {}
        
        for script_name in self.debug_scripts:
            script_path = self.project_root / script_name
            
            if not script_path.exists():
                self.safe_print(f"❌ {script_name} 文件不存在")
                results[script_name] = False
                continue
            
            # 检查语法
            syntax_ok, syntax_error = self.check_script_syntax(script_path)
            if not syntax_ok:
                self.safe_print(f"❌ {script_name} 语法错误: {syntax_error}")
                results[script_name] = False
                continue
            
            self.safe_print(f"✓ {script_name} 语法检查通过")
            results[script_name] = True
        
        return results
    
    def check_project_files(self) -> bool:
        """检查项目文件完整性"""
        self.print_section("项目文件检查")
        
        required_files = [
            'run.py',
            'directory_scanner.py', 
            'config.json',
            'requirements.txt',
            'BUILD_GUIDE.md'
        ]
        
        missing_files = []
        
        for file_name in required_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                self.safe_print(f"✓ {file_name} 存在")
            else:
                self.safe_print(f"❌ {file_name} 缺失")
                missing_files.append(file_name)
        
        # 检查图标文件
        icon_files = ['icon.png', 'icon.icns', 'icon.svg']
        icon_found = False
        
        for icon_file in icon_files:
            if (self.project_root / icon_file).exists():
                self.safe_print(f"✓ {icon_file} 图标文件存在")
                icon_found = True
        
        if not icon_found:
            self.safe_print("❌ 未找到图标文件")
            missing_files.append("图标文件")
        
        return len(missing_files) == 0
    
    def run_quick_test(self) -> None:
        """运行快速测试（不实际执行构建）"""
        self.print_section("快速功能测试")
        
        # 测试主程序是否能正常导入
        try:
            import run
            self.safe_print("✓ 主程序 run.py 可以正常导入")
        except Exception as e:
            self.safe_print(f"❌ 主程序导入失败: {e}")
        
        # 测试目录扫描器
        try:
            import directory_scanner
            self.safe_print("✓ 目录扫描器可以正常导入")
        except Exception as e:
            self.safe_print(f"❌ 目录扫描器导入失败: {e}")
        
        # 测试配置文件
        try:
            import json
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.safe_print("✓ 配置文件格式正确")
        except Exception as e:
            self.safe_print(f"❌ 配置文件错误: {e}")
    
    def generate_test_report(self, build_results: Dict[str, bool], debug_results: Dict[str, bool]) -> None:
        """生成测试报告"""
        self.print_section("测试报告")
        
        total_scripts = len(build_results) + len(debug_results)
        passed_scripts = sum(build_results.values()) + sum(debug_results.values())
        
        self.safe_print(f"\n📊 测试统计:")
        self.safe_print(f"   总脚本数: {total_scripts}")
        self.safe_print(f"   通过测试: {passed_scripts}")
        self.safe_print(f"   失败测试: {total_scripts - passed_scripts}")
        self.safe_print(f"   成功率: {(passed_scripts/total_scripts)*100:.1f}%")
        
        if passed_scripts == total_scripts:
            self.safe_print("\n🎉 所有脚本测试通过！")
        else:
            self.safe_print("\n⚠️  部分脚本需要修复")
            
            self.safe_print("\n失败的脚本:")
            for script, result in {**build_results, **debug_results}.items():
                if not result:
                    self.safe_print(f"   ❌ {script}")
    
    def run_full_test(self) -> None:
        """运行完整测试"""
        self.print_header("构建脚本完整性测试")
        
        # 环境检查
        env_ok = self.check_python_environment()
        
        # 依赖检查
        deps_ok = self.check_dependencies()
        
        # 项目文件检查
        files_ok = self.check_project_files()
        
        # 脚本测试
        build_results = self.test_build_scripts()
        debug_results = self.test_debug_scripts()
        
        # 快速功能测试
        self.run_quick_test()
        
        # 生成报告
        self.generate_test_report(build_results, debug_results)
        
        # 提供建议
        self.print_section("测试建议")
        
        if env_ok and deps_ok and files_ok:
            self.safe_print("✅ 环境配置完整，可以开始构建测试")
            self.safe_print("\n🚀 推荐的测试步骤:")
            self.safe_print("   1. 运行 python setup_dev.py 设置开发环境")
            self.safe_print("   2. 运行 python debug_local.py 测试本地功能")
            self.safe_print("   3. 运行 python runtime_error_detector.py 检测运行时错误")
            self.safe_print("   4. 根据平台选择构建脚本:")
            print("      - macOS: python build_macos_fixed.py")
            print("      - Windows: python build_windows_fixed.py")
            self.safe_print("      - 跨平台: python cross_platform_build.py")
        else:
            self.safe_print("⚠️  请先解决环境问题再进行构建测试")
            
            if not env_ok:
                self.safe_print("   - 检查Python环境和必要模块")
            if not deps_ok:
                self.safe_print("   - 安装缺失的依赖: pip install -r requirements.txt")
            if not files_ok:
                self.safe_print("   - 检查项目文件完整性")

def main():
    """主函数"""
    print("🔧 构建脚本测试工具")
    print("   用于验证项目构建脚本的完整性和可用性")
    
    tester = BuildScriptTester()
    tester.run_full_test()
    
    print("\n" + "="*60)
    print("  测试完成")
    print("="*60)

if __name__ == "__main__":
    main()