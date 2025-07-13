#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows编码兼容性修复工具
专门解决Windows环境下的Unicode编码问题
"""

import os
import sys
import re
import subprocess
from pathlib import Path

def safe_print(text):
    """安全的打印函数，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        # 在Windows环境下，如果无法显示Unicode字符，使用ASCII替代
        if sys.platform.startswith('win'):
            # 移除emoji和特殊字符，保留基本信息
            safe_text = text.encode('ascii', 'ignore').decode('ascii')
            if not safe_text.strip():
                safe_text = "[Unicode content - see logs for details]"
            print(safe_text)
        else:
            print(text.encode('utf-8', 'ignore').decode('utf-8'))
    except Exception:
        print("[Output encoding error - see logs for details]")

def detect_encoding_issues():
    """检测项目中的编码问题"""
    safe_print("Checking for encoding issues in Python files...")
    
    issues = []
    python_files = list(Path('.').glob('*.py'))
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查是否包含可能导致Windows编码问题的字符
            emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]'
            chinese_pattern = r'[\u4e00-\u9fff]'
            
            emoji_matches = re.findall(emoji_pattern, content)
            chinese_matches = re.findall(chinese_pattern, content)
            
            if emoji_matches or chinese_matches:
                issues.append({
                    'file': str(file_path),
                    'emoji_count': len(emoji_matches),
                    'chinese_count': len(chinese_matches),
                    'has_print_statements': 'print(' in content
                })
                
        except Exception as e:
            safe_print(f"Error reading {file_path}: {e}")
    
    return issues

def fix_print_statements(file_path):
    """修复文件中的print语句，使其兼容Windows"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果文件中没有safe_print函数，添加它
        if 'def safe_print(' not in content:
            safe_print_function = '''def safe_print(text):
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

'''
            # 在第一个函数定义之前插入safe_print函数
            if 'def ' in content:
                first_def_pos = content.find('def ')
                content = content[:first_def_pos] + safe_print_function + content[first_def_pos:]
            else:
                # 如果没有函数定义，在文件末尾添加
                content += '\n' + safe_print_function
        
        # 替换包含Unicode字符的print语句
        lines = content.split('\n')
        modified = False
        
        for i, line in enumerate(lines):
            if 'safe_print(' in line and ('\\u' in line or any(ord(c) > 127 for c in line)):
                # 将print替换为safe_print
                lines[i] = line.replace('print(', 'safe_print(')
                modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            return True
        
    except Exception as e:
        safe_print(f"Error fixing {file_path}: {e}")
    
    return False

def create_windows_build_script():
    """创建Windows专用构建脚本"""
    script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows专用构建脚本
解决Windows环境下的编码和构建问题
"""

import os
import sys
import subprocess
from pathlib import Path

def safe_print(text):
    """安全的打印函数"""
    try:
        print(text)
    except UnicodeEncodeError:
        if sys.platform.startswith('win'):
            safe_text = text.encode('ascii', 'ignore').decode('ascii')
            print(safe_text if safe_text.strip() else "[Unicode content]")
        else:
            print(text.encode('utf-8', 'ignore').decode('utf-8'))
    except Exception:
        print("[Encoding error]")

def main():
    """主函数"""
    safe_print("Windows Build Script")
    safe_print("=" * 30)
    
    # 设置环境变量
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    # 构建命令
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=DirectoryScanner',
        '--add-data=config.json;.',
        '--add-data=icon.png;.',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=openpyxl',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageTk',
        '--exclude-module=matplotlib',
        '--exclude-module=scipy',
        '--exclude-module=IPython',
        '--exclude-module=jupyter',
        '--noupx',
        'directory_scanner.py'
    ]
    
    try:
        safe_print("Starting build process...")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            safe_print("Build completed successfully!")
            safe_print(f"Executable created in dist/ directory")
        else:
            safe_print(f"Build failed with return code: {result.returncode}")
            safe_print(f"Error: {result.stderr}")
            
    except Exception as e:
        safe_print(f"Build error: {e}")

if __name__ == "__main__":
    main()
'''
    
    with open('build_windows_safe.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    safe_print("Created build_windows_safe.py")

def update_github_actions():
    """更新GitHub Actions配置以处理Windows编码问题"""
    workflows_dir = Path('.github/workflows')
    if not workflows_dir.exists():
        safe_print("No GitHub Actions workflows found")
        return
    
    for workflow_file in workflows_dir.glob('*.yml'):
        try:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经设置了编码环境变量
            if 'PYTHONIOENCODING' not in content:
                # 在Windows步骤中添加编码设置
                if 'windows-latest' in content:
                    # 在Python设置之后添加编码环境变量
                    python_setup_pattern = r'(- name: Set up Python.*?\n(?:.*\n)*?.*python-version.*\n)'
                    encoding_setup = '''      - name: Set encoding for Windows
        if: runner.os == 'Windows'
        run: |
          echo "PYTHONIOENCODING=utf-8" >> $GITHUB_ENV
          echo "PYTHONUTF8=1" >> $GITHUB_ENV
        shell: bash

'''
                    
                    content = re.sub(python_setup_pattern, r'\1' + encoding_setup, content)
                    
                    with open(workflow_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    safe_print(f"Updated {workflow_file} with Windows encoding fixes")
        
        except Exception as e:
            safe_print(f"Error updating {workflow_file}: {e}")

def main():
    """主函数"""
    safe_print("Windows Encoding Compatibility Fixer")
    safe_print("=" * 40)
    
    # 1. 检测编码问题
    safe_print("\n1. Detecting encoding issues...")
    issues = detect_encoding_issues()
    
    if issues:
        safe_print(f"Found {len(issues)} files with potential encoding issues:")
        for issue in issues:
            safe_print(f"  - {issue['file']}: {issue['emoji_count']} emojis, {issue['chinese_count']} Chinese chars")
        
        # 2. 修复print语句
        safe_print("\n2. Fixing print statements...")
        fixed_count = 0
        for issue in issues:
            if issue['has_print_statements']:
                if fix_print_statements(issue['file']):
                    fixed_count += 1
                    safe_print(f"  Fixed: {issue['file']}")
        
        safe_print(f"Fixed {fixed_count} files")
    else:
        safe_print("No encoding issues detected")
    
    # 3. 创建Windows安全构建脚本
    safe_print("\n3. Creating Windows-safe build script...")
    create_windows_build_script()
    
    # 4. 更新GitHub Actions
    safe_print("\n4. Updating GitHub Actions for Windows compatibility...")
    update_github_actions()
    
    safe_print("\nWindows encoding fixes completed!")
    safe_print("\nRecommendations:")
    safe_print("1. Use build_windows_safe.py for Windows builds")
    safe_print("2. Test the fixed scripts locally")
    safe_print("3. Commit and push changes to trigger GitHub Actions")
    safe_print("4. Monitor build logs for encoding issues")

if __name__ == "__main__":
    main()