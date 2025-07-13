#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows打包问题诊断工具
专门针对Windows平台的PyInstaller打包问题进行诊断和修复
作者: 程楠花开
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import importlib.util
import json

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

def check_windows_environment():
    """检查Windows环境和工具
    
    Returns:
        dict: 环境检查结果
    """
    safe_print("🔍 检查Windows环境...")
    results = {
        'system': platform.system(),
        'python_version': sys.version.split()[0],
        'architecture': platform.architecture()[0],
        'pyinstaller_installed': False,
        'pyinstaller_version': None,
        'windows_sdk': False,
        'antivirus_warning': False
    }
    
    safe_print(f"🖥️  系统: {results['system']}")
    safe_print(f"🐍 Python版本: {results['python_version']}")
    safe_print(f"🏗️  架构: {results['architecture']}")
    
    # 检查PyInstaller
    try:
        result = subprocess.run(['pyinstaller', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            results['pyinstaller_installed'] = True
            results['pyinstaller_version'] = result.stdout.strip()
            safe_print(f"✅ PyInstaller: {results['pyinstaller_version']}")
        else:
            safe_print("❌ PyInstaller未正确安装")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        safe_print("❌ PyInstaller未安装或无法访问")
    
    # 检查Windows SDK（通过查找常见路径）
    sdk_paths = [
        r"C:\Program Files (x86)\Windows Kits",
        r"C:\Program Files\Windows Kits",
        r"C:\Program Files (x86)\Microsoft SDKs",
        r"C:\Program Files\Microsoft SDKs"
    ]
    
    for sdk_path in sdk_paths:
        if os.path.exists(sdk_path):
            results['windows_sdk'] = True
            safe_print(f"✅ 找到Windows SDK: {sdk_path}")
            break
    
    if not results['windows_sdk']:
        safe_print("⚠️ 未检测到Windows SDK")
    
    # 检查常见的防病毒软件进程
    antivirus_processes = [
        'MsMpEng.exe',  # Windows Defender
        'avp.exe',      # Kaspersky
        'avgnt.exe',    # Avira
        'mcshield.exe', # McAfee
        'NortonSecurity.exe'  # Norton
    ]
    
    try:
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        if result.returncode == 0:
            running_processes = result.stdout.lower()
            for av_process in antivirus_processes:
                if av_process.lower() in running_processes:
                    results['antivirus_warning'] = True
                    safe_print(f"⚠️ 检测到防病毒软件: {av_process}")
                    break
    except:
        pass
    
    return results

def check_windows_dependencies():
    """检查Windows特定的依赖问题
    
    Returns:
        dict: 依赖检查结果
    """
    safe_print("\n🔍 检查Windows依赖...")
    results = {
        'missing_modules': [],
        'version_conflicts': [],
        'dll_issues': []
    }
    
    # 检查关键模块
    critical_modules = {
        'tkinter': 'GUI框架',
        'pathlib': '路径处理',
        'json': 'JSON处理',
        'subprocess': '进程管理',
        'threading': '多线程'
    }
    
    for module, description in critical_modules.items():
        try:
            spec = importlib.util.find_spec(module)
            if spec is None:
                results['missing_modules'].append((module, description))
                safe_print(f"❌ 缺少模块: {module} ({description})")
            else:
                safe_print(f"✅ 模块正常: {module}")
        except ImportError:
            results['missing_modules'].append((module, description))
            safe_print(f"❌ 导入失败: {module} ({description})")
    
    # 检查可能的版本冲突
    try:
        import pkg_resources
        installed_packages = [d for d in pkg_resources.working_set]
        
        # 检查PyInstaller版本兼容性
        for package in installed_packages:
            if package.project_name.lower() == 'pyinstaller':
                version = package.version
                major_version = int(version.split('.')[0])
                if major_version < 4:
                    results['version_conflicts'].append(
                        f"PyInstaller版本过低: {version} (建议4.0+)"
                    )
                    safe_print(f"⚠️ PyInstaller版本过低: {version}")
    except ImportError:
        safe_print("⚠️ 无法检查包版本")
    
    return results

def check_windows_file_permissions():
    """检查Windows文件权限问题
    
    Returns:
        dict: 权限检查结果
    """
    safe_print("\n🔍 检查Windows文件权限...")
    results = {
        'write_permission': True,
        'execution_permission': True,
        'temp_access': True
    }
    
    current_dir = Path(__file__).parent
    
    # 检查写入权限
    try:
        test_file = current_dir / "test_write_permission.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        test_file.unlink()
        safe_print("✅ 写入权限正常")
    except PermissionError:
        results['write_permission'] = False
        safe_print("❌ 写入权限不足")
    except Exception as e:
        safe_print(f"⚠️ 写入权限检查失败: {e}")
    
    # 检查临时目录访问
    import tempfile
    try:
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(b"test")
        safe_print("✅ 临时目录访问正常")
    except Exception as e:
        results['temp_access'] = False
        safe_print(f"❌ 临时目录访问失败: {e}")
    
    return results

def generate_windows_fixes(env_results, dep_results, perm_results):
    """生成Windows特定的修复建议
    
    Args:
        env_results (dict): 环境检查结果
        dep_results (dict): 依赖检查结果
        perm_results (dict): 权限检查结果
        
    Returns:
        list: 修复建议列表
    """
    fixes = []
    
    # PyInstaller相关修复
    if not env_results['pyinstaller_installed']:
        fixes.append({
            'issue': 'PyInstaller未安装',
            'solution': 'pip install pyinstaller',
            'priority': 'high'
        })
    
    # Windows SDK相关修复
    if not env_results['windows_sdk']:
        fixes.append({
            'issue': '缺少Windows SDK',
            'solution': '安装Visual Studio Build Tools或Windows SDK',
            'priority': 'medium',
            'details': [
                '下载Visual Studio Installer',
                '选择"C++ build tools"工作负载',
                '或下载独立的Windows 10/11 SDK'
            ]
        })
    
    # 防病毒软件相关修复
    if env_results['antivirus_warning']:
        fixes.append({
            'issue': '防病毒软件可能干扰打包',
            'solution': '临时禁用实时保护或添加排除项',
            'priority': 'medium',
            'details': [
                '将项目目录添加到防病毒软件排除列表',
                '临时禁用实时保护进行打包',
                '打包完成后重新启用保护'
            ]
        })
    
    # 权限相关修复
    if not perm_results['write_permission']:
        fixes.append({
            'issue': '写入权限不足',
            'solution': '以管理员身份运行或更改目录权限',
            'priority': 'high'
        })
    
    # 依赖相关修复
    if dep_results['missing_modules']:
        for module, desc in dep_results['missing_modules']:
            fixes.append({
                'issue': f'缺少模块: {module}',
                'solution': f'pip install {module}',
                'priority': 'high'
            })
    
    return fixes

def create_windows_build_script(fixes):
    """创建针对Windows问题的修复版构建脚本
    
    Args:
        fixes (list): 修复建议列表
        
    Returns:
        str: 生成的脚本路径
    """
    script_content = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成的Windows修复版构建脚本
基于诊断结果优化
"""

import subprocess
import sys
from pathlib import Path

def main():
    safe_print("🚀 开始Windows修复版构建...")
    
    # 基于诊断结果的构建命令
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        '--name=目录扫描器',
        '--distpath=dist/windows',
        
        # Windows特定优化
        '--noupx',  # 禁用UPX避免防病毒软件误报
        '--strip',  # 去除调试信息
        
        # 隐藏导入
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=json',
        '--hidden-import=pathlib',
        
        # 主脚本
        'directory_scanner.py'
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        safe_print("✅ 构建成功！")
        return True
    except subprocess.CalledProcessError as e:
        safe_print(f"❌ 构建失败: {e}")
        return False

if __name__ == "__main__":
    main()
'''
    
    script_path = Path(__file__).parent / "build_windows_auto_fixed.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    return str(script_path)

def main():
    """主函数"""
    print("=" * 60)
    safe_print("🪟 Windows打包问题诊断工具")
    print("=" * 60)
    
    # 执行各项检查
    env_results = check_windows_environment()
    dep_results = check_windows_dependencies()
    perm_results = check_windows_file_permissions()
    
    # 生成修复建议
    fixes = generate_windows_fixes(env_results, dep_results, perm_results)
    
    print("\n" + "=" * 60)
    safe_print("📋 诊断结果")
    print("=" * 60)
    
    if not fixes:
        safe_print("🎉 恭喜！未发现Windows打包问题")
        safe_print("✅ 您的环境已准备就绪，可以直接使用 build_windows_fixed.py 进行打包")
    else:
        safe_print(f"⚠️ 发现 {len(fixes)} 个潜在问题:")
        
        high_priority = [f for f in fixes if f['priority'] == 'high']
        medium_priority = [f for f in fixes if f['priority'] == 'medium']
        
        if high_priority:
            safe_print("\n🔴 高优先级问题（必须解决）:")
            for i, fix in enumerate(high_priority, 1):
                print(f"{i}. {fix['issue']}")
                safe_print(f"   解决方案: {fix['solution']}")
                if 'details' in fix:
                    for detail in fix['details']:
                        print(f"   - {detail}")
                print()
        
        if medium_priority:
            safe_print("🟡 中优先级问题（建议解决）:")
            for i, fix in enumerate(medium_priority, 1):
                print(f"{i}. {fix['issue']}")
                safe_print(f"   解决方案: {fix['solution']}")
                if 'details' in fix:
                    for detail in fix['details']:
                        print(f"   - {detail}")
                print()
    
    safe_print("\n💡 建议的解决步骤:")
    safe_print("1. 解决上述高优先级问题")
    safe_print("2. 使用 python build_windows_fixed.py 进行打包")
    safe_print("3. 如果仍有问题，考虑使用GitHub Actions自动化打包")
    
    # 保存诊断报告
    report = {
        'environment': env_results,
        'dependencies': dep_results,
        'permissions': perm_results,
        'fixes': fixes
    }
    
    report_file = Path(__file__).parent / "windows_diagnosis_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    safe_print(f"\n📄 详细报告已保存到: {report_file}")

if __name__ == "__main__":
    main()