#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包问题诊断和修复工具
专门解决"本地运行正常，打包后出现问题"的常见情况
作者：张牛牛
"""

import os
import sys
import subprocess
import shutil
import json
import importlib
from pathlib import Path
from typing import List, Dict, Tuple

class PackagingDiagnostic:
    """打包问题诊断类
    
    用于检测和修复PyInstaller打包过程中的常见问题
    """
    
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

def __init__(self):
        """初始化诊断工具"""
        self.issues_found = []
        self.fixes_applied = []
        self.main_script = "directory_scanner.py"
        
    def run_full_diagnostic(self) -> bool:
        """运行完整的诊断流程
        
        Returns:
            bool: 是否发现并修复了问题
        """
        safe_print("🔍 开始打包问题诊断...")
        print("=" * 50)
        
        # 1. 检查基础环境
        self.check_basic_environment()
        
        # 2. 检查依赖导入
        self.check_import_issues()
        
        # 3. 检查文件路径问题
        self.check_file_path_issues()
        
        # 4. 检查隐藏导入
        self.check_hidden_imports()
        
        # 5. 检查数据文件
        self.check_data_files()
        
        # 6. 生成修复后的构建脚本
        self.generate_fixed_build_script()
        
        # 7. 提供解决方案
        self.provide_solutions()
        
        return len(self.issues_found) > 0
    
    def check_basic_environment(self):
        """检查基础环境配置
        
        检查Python版本、PyInstaller版本等基础信息
        """
        safe_print("📋 检查基础环境...")
        
        # Python版本检查
        python_version = sys.version_info
        safe_print(f"🐍 Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version < (3, 8):
            self.issues_found.append({
                "type": "environment",
                "issue": "Python版本过低",
                "description": f"当前版本 {python_version.major}.{python_version.minor}，建议使用3.8+",
                "fix": "升级Python版本到3.8或更高"
            })
        
        # PyInstaller版本检查
        try:
            result = subprocess.run(['pyinstaller', '--version'], 
                                  capture_output=True, text=True, check=True)
            pyinstaller_version = result.stdout.strip()
            safe_print(f"📦 PyInstaller版本: {pyinstaller_version}")
            
            # 检查是否是已知有问题的版本
            if "5.0" in pyinstaller_version:
                self.issues_found.append({
                    "type": "environment",
                    "issue": "PyInstaller版本问题",
                    "description": "PyInstaller 5.0版本存在已知问题",
                    "fix": "升级到PyInstaller 5.1+或降级到4.10"
                })
        except Exception as e:
            self.issues_found.append({
                "type": "environment",
                "issue": "PyInstaller未安装或无法运行",
                "description": str(e),
                "fix": "重新安装PyInstaller: pip install --upgrade pyinstaller"
            })
    
    def check_import_issues(self):
        """检查导入问题
        
        分析主程序的导入语句，识别可能的隐藏导入问题
        """
        safe_print("📥 检查导入问题...")
        
        if not os.path.exists(self.main_script):
            self.issues_found.append({
                "type": "file",
                "issue": "主程序文件不存在",
                "description": f"找不到 {self.main_script}",
                "fix": "确保主程序文件存在"
            })
            return
        
        # 分析导入语句
        imports = self.analyze_imports()
        problematic_imports = self.identify_problematic_imports(imports)
        
        for imp in problematic_imports:
            self.issues_found.append({
                "type": "import",
                "issue": f"可能的隐藏导入问题: {imp}",
                "description": f"模块 {imp} 可能需要显式声明为隐藏导入",
                "fix": f"添加 --hidden-import={imp} 到构建命令"
            })
    
    def analyze_imports(self) -> List[str]:
        """分析Python文件中的导入语句
        
        Returns:
            List[str]: 导入的模块列表
        """
        imports = []
        
        try:
            with open(self.main_script, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 简单的导入语句解析
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    # 提取模块名
                    if line.startswith('import '):
                        module = line.replace('import ', '').split(' as ')[0].split(',')[0].strip()
                        imports.append(module)
                    elif line.startswith('from '):
                        module = line.split(' import ')[0].replace('from ', '').strip()
                        imports.append(module)
                        
        except Exception as e:
            safe_print(f"⚠️  分析导入语句时出错: {e}")
            
        return imports
    
    def identify_problematic_imports(self, imports: List[str]) -> List[str]:
        """识别可能有问题的导入
        
        Args:
            imports: 导入的模块列表
            
        Returns:
            List[str]: 可能有问题的导入列表
        """
        # 已知容易出问题的模块
        problematic_modules = {
            'pandas': ['pandas._libs', 'pandas.io.formats.style'],
            'numpy': ['numpy.core._methods', 'numpy.lib.recfunctions'],
            'openpyxl': ['openpyxl.cell', 'openpyxl.styles'],
            'tkinter': ['tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog'],
            'datetime': ['datetime'],
            'pathlib': ['pathlib'],
            'collections': ['collections.defaultdict'],
            'json': ['json'],
            'threading': ['threading'],
            'subprocess': ['subprocess']
        }
        
        problematic = []
        for imp in imports:
            base_module = imp.split('.')[0]
            if base_module in problematic_modules:
                problematic.extend(problematic_modules[base_module])
                
        return list(set(problematic))
    
    def check_file_path_issues(self):
        """检查文件路径问题
        
        检查相对路径、资源文件等可能的路径问题
        """
        safe_print("📁 检查文件路径问题...")
        
        # 检查是否使用了相对路径
        try:
            with open(self.main_script, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 查找可能的相对路径使用
            if 'open(' in content and ('./' in content or '../' in content):
                self.issues_found.append({
                    "type": "path",
                    "issue": "使用了相对路径",
                    "description": "代码中可能使用了相对路径，打包后可能找不到文件",
                    "fix": "使用绝对路径或sys._MEIPASS处理资源文件路径"
                })
                
            # 检查资源文件
            resource_files = ['icon.png', 'icon.icns', 'config.json']
            missing_resources = []
            
            for resource in resource_files:
                if resource in content and not os.path.exists(resource):
                    missing_resources.append(resource)
                    
            if missing_resources:
                self.issues_found.append({
                    "type": "resource",
                    "issue": "缺少资源文件",
                    "description": f"代码中引用但文件不存在: {', '.join(missing_resources)}",
                    "fix": "确保资源文件存在，并在构建时使用--add-data参数包含"
                })
                
        except Exception as e:
            safe_print(f"⚠️  检查文件路径时出错: {e}")
    
    def check_hidden_imports(self):
        """检查隐藏导入配置
        
        验证当前构建脚本中的隐藏导入是否完整
        """
        safe_print("🔍 检查隐藏导入配置...")
        
        # 读取当前构建脚本
        build_script = "build_macos_optimized.py"
        if not os.path.exists(build_script):
            self.issues_found.append({
                "type": "config",
                "issue": "构建脚本不存在",
                "description": f"找不到 {build_script}",
                "fix": "创建或恢复构建脚本"
            })
            return
            
        try:
            with open(build_script, 'r', encoding='utf-8') as f:
                build_content = f.read()
                
            # 检查必要的隐藏导入
            required_hidden_imports = [
                'pandas', 'numpy', 'openpyxl', 'tkinter.ttk', 
                'tkinter.messagebox', 'tkinter.filedialog'
            ]
            
            missing_imports = []
            for imp in required_hidden_imports:
                if f'--hidden-import={imp}' not in build_content:
                    missing_imports.append(imp)
                    
            if missing_imports:
                self.issues_found.append({
                    "type": "config",
                    "issue": "缺少隐藏导入",
                    "description": f"构建脚本中缺少隐藏导入: {', '.join(missing_imports)}",
                    "fix": "在构建命令中添加缺少的--hidden-import参数"
                })
                
        except Exception as e:
            safe_print(f"⚠️  检查隐藏导入时出错: {e}")
    
    def check_data_files(self):
        """检查数据文件配置
        
        检查是否正确配置了数据文件的打包
        """
        safe_print("📄 检查数据文件配置...")
        
        # 检查可能需要打包的数据文件
        data_files = {
            'icon.png': '图标文件',
            'icon.icns': 'macOS图标文件',
            'config.json': '配置文件',
            'requirements.txt': '依赖文件'
        }
        
        missing_data_files = []
        for file_path, description in data_files.items():
            if os.path.exists(file_path):
                # 检查是否在构建脚本中配置了
                build_script = "build_macos_optimized.py"
                if os.path.exists(build_script):
                    with open(build_script, 'r', encoding='utf-8') as f:
                        build_content = f.read()
                        
                    if file_path not in build_content and '--add-data' not in build_content:
                        missing_data_files.append((file_path, description))
                        
        if missing_data_files:
            files_desc = ', '.join([f"{f}({d})" for f, d in missing_data_files])
            self.issues_found.append({
                "type": "data",
                "issue": "数据文件未配置打包",
                "description": f"存在但未配置打包的文件: {files_desc}",
                "fix": "在构建命令中添加--add-data参数包含这些文件"
            })
    
    def generate_fixed_build_script(self):
        """生成修复后的构建脚本
        
        基于发现的问题生成一个改进的构建脚本
        """
        safe_print("🔧 生成修复后的构建脚本...")
        
        fixed_script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版macOS构建脚本
解决常见的打包问题
自动生成于打包问题诊断工具
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_fixed_macos():
    """构建修复版macOS应用程序
    
    包含所有必要的修复参数
    """
    safe_print("🚀 开始构建修复版macOS应用程序...")
    
    # 清理之前的构建文件
    build_dirs = ['build', 'dist']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            safe_print(f"🧹 清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 增强的构建命令参数
    cmd = [
        'pyinstaller',
        '--onedir',              # 使用目录模式
        '--windowed',            # 无控制台窗口
        '--clean',               # 清理缓存
        '--noconfirm',           # 不询问确认
        '--name=目录扫描器',      # 应用名称
        '--icon=icon.png',       # 应用图标
        '--optimize=2',          # Python字节码优化
        '--strip',               # 去除调试符号
        
        # 排除不需要的模块
        '--exclude-module=matplotlib',
        '--exclude-module=scipy',
        '--exclude-module=PIL.ImageQt',
        '--exclude-module=PyQt5',
        '--exclude-module=PyQt6',
        '--exclude-module=PySide2',
        '--exclude-module=PySide6',
        '--exclude-module=IPython',
        '--exclude-module=jupyter',
        
        # 核心隐藏导入
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=openpyxl',
        
        # tkinter相关隐藏导入
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.simpledialog',
        
        # pandas相关隐藏导入
        '--hidden-import=pandas._libs.tslibs.timedeltas',
        '--hidden-import=pandas._libs.tslibs.np_datetime',
        '--hidden-import=pandas._libs.tslibs.nattype',
        '--hidden-import=pandas._libs.skiplist',
        '--hidden-import=pandas.io.formats.style',
        
        # numpy相关隐藏导入
        '--hidden-import=numpy.core._methods',
        '--hidden-import=numpy.lib.recfunctions',
        '--hidden-import=numpy.random.common',
        '--hidden-import=numpy.random.bounded_integers',
        '--hidden-import=numpy.random.entropy',
        
        # openpyxl相关隐藏导入
        '--hidden-import=openpyxl.cell',
        '--hidden-import=openpyxl.styles',
        '--hidden-import=openpyxl.chart',
        '--hidden-import=openpyxl.drawing',
        
        # 其他必要的隐藏导入
        '--hidden-import=datetime',
        '--hidden-import=pathlib',
        '--hidden-import=collections',
        '--hidden-import=json',
        '--hidden-import=threading',
        '--hidden-import=subprocess',
        '--hidden-import=fnmatch',
        
        # 收集所有子模块
        '--collect-all=numpy',
        '--collect-all=pandas',
        '--collect-all=openpyxl',
        
        # 禁用UPX压缩
        '--noupx',
        
        # 添加数据文件
        '--add-data=icon.png:.',
        
        # 主程序文件
        'directory_scanner.py'
    ]
    
    # 检查并添加额外的数据文件
    extra_data_files = ['icon.icns', 'config.json']
    for data_file in extra_data_files:
        if os.path.exists(data_file):
            cmd.insert(-1, f'--add-data={data_file}:.')
            safe_print(f"📄 添加数据文件: {data_file}")
    
    safe_print("📦 执行增强版PyInstaller构建...")
    safe_print(f"命令参数数量: {len(cmd)}")
    
    try:
        # 执行构建
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        safe_print("✅ 构建成功！")
        
        # 检查构建结果
        app_path = Path('dist/目录扫描器.app')
        if app_path.exists():
            safe_print(f"📱 应用程序已生成: {app_path.absolute()}")
            safe_print("\n🎉 修复版构建完成！")
            safe_print("\n🔧 应用的修复:")
            safe_print("• 增加了完整的隐藏导入配置")
            safe_print("• 包含了所有必要的数据文件")
            safe_print("• 优化了模块收集策略")
            safe_print("• 排除了不必要的大型模块")
            
        else:
            safe_print("❌ 未找到生成的应用程序")
            
    except subprocess.CalledProcessError as e:
        safe_print(f"❌ 构建失败: {e}")
        if e.stderr:
            safe_print(f"错误输出: {e.stderr}")
        return False
    except Exception as e:
        safe_print(f"❌ 构建过程中发生错误: {e}")
        return False
    
    return True

if __name__ == "__main__":
    safe_print("🔧 修复版macOS应用程序构建工具")
    print("=" * 50)
    build_fixed_macos()
'''
        
        fixed_script_path = "build_macos_fixed.py"
        with open(fixed_script_path, 'w', encoding='utf-8') as f:
            f.write(fixed_script_content)
            
        self.fixes_applied.append(f"生成修复版构建脚本: {fixed_script_path}")
        safe_print(f"✅ 修复版构建脚本已生成: {fixed_script_path}")
    
    def provide_solutions(self):
        """提供解决方案总结
        
        根据发现的问题提供具体的解决方案
        """
        print("\n" + "=" * 50)
        safe_print("📋 诊断结果总结")
        print("=" * 50)
        
        if not self.issues_found:
            safe_print("✅ 未发现明显的打包问题！")
            safe_print("\n💡 如果仍有问题，建议:")
            safe_print("1. 使用修复版构建脚本: python build_macos_fixed.py")
            safe_print("2. 检查运行时错误日志")
            safe_print("3. 在不同环境中测试")
            return
            
        safe_print(f"⚠️  发现 {len(self.issues_found)} 个潜在问题:")
        print()
        
        # 按类型分组显示问题
        issues_by_type = {}
        for issue in self.issues_found:
            issue_type = issue['type']
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)
            
        type_icons = {
            'environment': '🌍',
            'import': '📥',
            'path': '📁',
            'resource': '📄',
            'config': '⚙️',
            'data': '💾'
        }
        
        for issue_type, issues in issues_by_type.items():
            icon = type_icons.get(issue_type, '❓')
            safe_print(f"{icon} {issue_type.upper()} 问题:")
            
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue['issue']}")
                safe_print(f"     描述: {issue['description']}")
                safe_print(f"     解决: {issue['fix']}")
                print()
        
        safe_print("🚀 推荐解决方案:")
        safe_print("1. 使用生成的修复版构建脚本:")
        print("   python build_macos_fixed.py")
        print()
        safe_print("2. 如果问题仍然存在，尝试调试构建:")
        print("   python fix_packaging_issues.py --debug-build")
        print()
        safe_print("3. 检查运行时错误:")
        safe_print("   - 在终端中运行打包后的应用")
        safe_print("   - 查看详细的错误信息")
        safe_print("   - 检查缺少的依赖或文件")

def debug_build():
    """调试模式构建
    
    使用详细输出进行构建，便于问题定位
    """
    safe_print("🐛 调试模式构建...")
    
    cmd = [
        'pyinstaller',
        '--onedir',
        '--windowed',
        '--clean',
        '--noconfirm',
        '--debug=all',           # 启用所有调试信息
        '--log-level=DEBUG',     # 详细日志
        '--name=目录扫描器_调试版',
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=openpyxl',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.filedialog',
        '--collect-all=numpy',
        '--collect-all=pandas',
        '--noupx',
        'directory_scanner.py'
    ]
    
    safe_print("执行调试构建...")
    try:
        result = subprocess.run(cmd, check=False, text=True)
        safe_print(f"构建完成，退出码: {result.returncode}")
    except Exception as e:
        safe_print(f"调试构建失败: {e}")

def main():
    """主函数"""
    safe_print("🔧 打包问题诊断和修复工具")
    safe_print("专门解决'本地运行正常，打包后出现问题'的情况")
    print("=" * 60)
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == '--debug-build':
        debug_build()
        return
    
    # 运行诊断
    diagnostic = PackagingDiagnostic()
    diagnostic.run_full_diagnostic()
    
    safe_print("\n🎯 下一步建议:")
    safe_print("1. 运行修复版构建: python build_macos_fixed.py")
    safe_print("2. 测试打包后的应用")
    safe_print("3. 如有问题，运行调试构建: python fix_packaging_issues.py --debug-build")

if __name__ == "__main__":
    main()