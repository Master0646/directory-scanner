#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发环境快速设置脚本
自动配置本地开发环境，提供最佳的调试体验
作者：张牛牛
"""

import os
import sys
import subprocess
import json
from pathlib import Path

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

def create_dev_config():
    """创建开发配置文件
    
    生成针对开发环境优化的配置
    """
    safe_print("📝 创建开发配置...")
    
    dev_config = {
        "development": {
            "debug_mode": True,
            "log_level": "DEBUG",
            "auto_reload": True,
            "show_console": True,
            "max_depth_default": 2,  # 开发时用较小深度
            "update_interval": 50,   # 更频繁的界面更新
            "enable_profiling": False
        },
        "debugging": {
            "verbose_logging": True,
            "trace_imports": False,
            "memory_monitoring": False,
            "performance_timing": True
        },
        "ui": {
            "theme": "default",
            "window_size": "1000x800",
            "remember_position": True,
            "auto_save_settings": True
        }
    }
    
    config_file = Path("config_dev.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(dev_config, f, indent=2, ensure_ascii=False)
    
    safe_print(f"✅ 开发配置已创建: {config_file}")
    return config_file

def create_debug_launcher():
    """创建调试启动器脚本
    
    生成一个简化的启动脚本，包含调试选项
    """
    safe_print("🚀 创建调试启动器...")
    
    launcher_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试启动器 - 开发专用
自动加载开发配置，启用调试模式
"""

import os
import sys

# 设置开发环境变量
os.environ['APP_ENV'] = 'development'
os.environ['DEBUG'] = '1'
os.environ['PYTHONUNBUFFERED'] = '1'

# 添加当前目录到Python路径
sys.path.insert(0, os.getcwd())

if __name__ == "__main__":
    try:
        safe_print("🐛 调试模式启动...")
        safe_print(f"📁 工作目录: {os.getcwd()}")
        safe_print(f"🐍 Python版本: {sys.version}")
        print("-" * 50)
        
        # 导入并运行主程序
        import directory_scanner
        directory_scanner.main()
        
    except ImportError as e:
        safe_print(f"❌ 导入错误: {e}")
        safe_print("请确保所有依赖已安装: pip install -r requirements.txt")
    except Exception as e:
        safe_print(f"❌ 运行错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        safe_print("\n🔚 调试会话结束")
'''
    
    launcher_file = Path("debug_launcher.py")
    with open(launcher_file, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    # 设置可执行权限 (Unix系统)
    if os.name != 'nt':
        os.chmod(launcher_file, 0o755)
    
    safe_print(f"✅ 调试启动器已创建: {launcher_file}")
    return launcher_file

def create_vscode_config():
    """创建VS Code调试配置
    
    生成VS Code的launch.json配置文件
    """
    safe_print("🔧 创建VS Code调试配置...")
    
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)
    
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "调试目录扫描器",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/directory_scanner.py",
                "console": "integratedTerminal",
                "cwd": "${workspaceFolder}",
                "env": {
                    "PYTHONPATH": "${workspaceFolder}",
                    "DEBUG": "1",
                    "APP_ENV": "development"
                },
                "args": [],
                "justMyCode": True,
                "stopOnEntry": False
            },
            {
                "name": "快速调试启动",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/debug_launcher.py",
                "console": "integratedTerminal",
                "cwd": "${workspaceFolder}"
            }
        ]
    }
    
    launch_file = vscode_dir / "launch.json"
    with open(launch_file, 'w', encoding='utf-8') as f:
        json.dump(launch_config, f, indent=2)
    
    # 创建settings.json
    settings_config = {
        "python.defaultInterpreterPath": sys.executable,
        "python.terminal.activateEnvironment": True,
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": False,
        "python.linting.flake8Enabled": True,
        "python.formatting.provider": "black",
        "files.associations": {
            "*.py": "python"
        }
    }
    
    settings_file = vscode_dir / "settings.json"
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(settings_config, f, indent=2)
    
    safe_print(f"✅ VS Code配置已创建: {vscode_dir}")
    return vscode_dir

def install_dev_dependencies():
    """安装开发依赖
    
    安装额外的开发工具和调试工具
    """
    safe_print("📦 检查开发依赖...")
    
    # 基础依赖
    basic_deps = ['tkinter', 'pandas', 'openpyxl', 'numpy']
    
    # 开发依赖（可选）
    dev_deps = {
        'black': '代码格式化',
        'flake8': '代码检查',
        'pytest': '单元测试',
        'memory_profiler': '内存分析',
        'line_profiler': '性能分析'
    }
    
    # 检查基础依赖
    missing_basic = []
    for dep in basic_deps:
        try:
            __import__(dep)
            safe_print(f"✅ {dep}")
        except ImportError:
            missing_basic.append(dep)
            safe_print(f"❌ {dep} (必需)")
    
    if missing_basic:
        safe_print(f"\n⚠️  缺少必需依赖: {', '.join(missing_basic)}")
        safe_print("请运行: pip install -r requirements.txt")
        return False
    
    # 检查开发依赖
    safe_print("\n🔍 检查开发工具...")
    available_dev_tools = []
    
    for tool, description in dev_deps.items():
        try:
            __import__(tool)
            safe_print(f"✅ {tool} - {description}")
            available_dev_tools.append(tool)
        except ImportError:
            safe_print(f"⚪ {tool} - {description} (可选)")
    
    if available_dev_tools:
        safe_print(f"\n🎉 可用开发工具: {', '.join(available_dev_tools)}")
    else:
        safe_print("\n💡 提示: 可安装开发工具提升开发体验")
        print("   pip install black flake8 pytest")
    
    return True

def create_makefile():
    """创建Makefile简化常用命令
    
    提供make命令快捷方式
    """
    safe_print("📜 创建Makefile...")
    
    makefile_content = '''# 目录扫描器开发工具
# 使用 make <命令> 执行常用操作

.PHONY: run debug test clean install build help

# 默认目标
help:
	@echo "🛠️  目录扫描器开发工具"
	@echo "可用命令:"
	@echo "  make run     - 🚀 直接运行程序"
	@echo "  make debug   - 🐛 调试模式运行"
	@echo "  make test    - 🧪 运行测试"
	@echo "  make install - 📦 安装依赖"
	@echo "  make build   - 🔨 快速构建"
	@echo "  make clean   - 🧹 清理文件"
	@echo "  make format  - 🎨 格式化代码"

# 直接运行
run:
	@echo "🚀 启动目录扫描器..."
	python directory_scanner.py

# 调试模式
debug:
	@echo "🐛 调试模式启动..."
	python debug_launcher.py

# 快速测试
test:
	@echo "🧪 运行快速测试..."
	python quick_debug.py

# 安装依赖
install:
	@echo "📦 安装依赖..."
	pip install -r requirements.txt

# 快速构建
build:
	@echo "🔨 快速构建..."
	python build_macos_optimized.py

# 清理文件
clean:
	@echo "🧹 清理构建文件..."
	rm -rf build/ dist/ *.spec __pycache__/ *.pyc
	@echo "✅ 清理完成"

# 格式化代码（如果安装了black）
format:
	@echo "🎨 格式化代码..."
	@if command -v black >/dev/null 2>&1; then \
		black *.py; \
	else \
		echo "⚠️  black未安装，跳过格式化"; \
	fi

# 完整开发环境检查
check:
	@echo "🔍 检查开发环境..."
	python setup_dev.py
'''
    
    makefile_path = Path("Makefile")
    with open(makefile_path, 'w', encoding='utf-8') as f:
        f.write(makefile_content)
    
    safe_print(f"✅ Makefile已创建: {makefile_path}")
    safe_print("💡 现在可以使用 'make run' 快速启动程序")
    return makefile_path

def show_quick_start_guide():
    """显示快速开始指南
    
    提供开发环境使用说明
    """
    guide = """
🎉 开发环境设置完成！

🚀 快速开始:
  • make run          - 直接运行程序
  • make debug        - 调试模式运行
  • python quick_debug.py - 超快速调试

🔧 开发工具:
  • VS Code: 打开项目，按F5开始调试
  • 命令行: 使用make命令简化操作
  • 配置文件: config_dev.json (开发专用配置)

🐛 调试技巧:
  1. 修改代码后直接重新运行，无需构建
  2. 使用safe_print()添加调试信息
  3. 在VS Code中设置断点进行调试
  4. 查看终端输出的详细错误信息

📁 新增文件:
  • debug_local.py    - 完整调试工具
  • quick_debug.py    - 超快速调试
  • debug_launcher.py - 调试启动器
  • config_dev.json   - 开发配置
  • .vscode/          - VS Code配置
  • Makefile          - 命令快捷方式

💡 推荐工作流:
  1. 开发时: make run 或 python quick_debug.py
  2. 调试时: 在VS Code中按F5
  3. 测试打包: python build_macos_optimized.py
  4. 最终发布: GitHub Actions自动构建
"""
    print(guide)

def main():
    """主函数 - 设置完整的开发环境"""
    safe_print("🛠️  开发环境快速设置")
    print("=" * 40)
    
    try:
        # 检查基础环境
        if not install_dev_dependencies():
            safe_print("\n❌ 基础依赖检查失败，请先安装必需依赖")
            return
        
        safe_print("\n📝 创建开发配置文件...")
        
        # 创建各种配置文件
        create_dev_config()
        create_debug_launcher()
        create_vscode_config()
        create_makefile()
        
        safe_print("\n✅ 开发环境设置完成！")
        
        # 显示使用指南
        show_quick_start_guide()
        
    except Exception as e:
        safe_print(f"❌ 设置过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()