#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨平台打包脚本 - 支持Windows、macOS、Linux
作者: 程楠花开
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import time
import threading
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

def show_progress():
    """显示打包进度动画"""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    i = 0
    while not progress_done:
        safe_print(f"\r🔨 正在打包中 {chars[i % len(chars)]} 请耐心等待...", end="", flush=True)
        time.sleep(0.1)
        i += 1
    safe_print("\r✅ 打包完成！" + " " * 30)

def create_github_workflow():
    """创建GitHub Actions工作流文件用于自动化打包"""
    workflow_content = '''
name: Build Executables

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        include:
          - os: windows-latest
            platform: windows
            ext: .exe
          - os: macos-latest
            platform: macos
            ext: .app
          - os: ubuntu-latest
            platform: linux
            ext: ""
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pyinstaller
        pip install -r requirements.txt
    
    - name: Build executable (Windows)
      if: matrix.platform == 'windows'
      run: |
        pyinstaller --onefile --windowed --clean --noconfirm --name="目录扫描器" --icon=icon.png --distpath=dist/windows directory_scanner.py
    
    - name: Build executable (macOS)
      if: matrix.platform == 'macos'
      run: |
        pyinstaller --onefile --windowed --clean --noconfirm --name="目录扫描器" --icon=icon.png --distpath=dist/macos directory_scanner.py
    
    - name: Build executable (Linux)
      if: matrix.platform == 'linux'
      run: |
        pyinstaller --onefile --clean --noconfirm --name="目录扫描器" --icon=icon.png --distpath=dist/linux directory_scanner.py
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: 目录扫描器-${{ matrix.platform }}
        path: dist/${{ matrix.platform }}/
'''
    
    # 创建.github/workflows目录
    workflow_dir = Path(__file__).parent / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_file = workflow_dir / "build.yml"
    with open(workflow_file, 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    
    return workflow_file

def create_docker_build():
    """创建Docker构建文件"""
    dockerfile_content = '''
# 多阶段构建 - Windows
FROM python:3.12-windowsservercore as windows-builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyinstaller
COPY . .
RUN pyinstaller --onefile --windowed --clean --noconfirm --name="目录扫描器" directory_scanner.py

# 多阶段构建 - Linux
FROM python:3.12-slim as linux-builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyinstaller
COPY . .
RUN pyinstaller --onefile --clean --noconfirm --name="目录扫描器" directory_scanner.py

# 最终镜像
FROM alpine:latest
WORKDIR /output
COPY --from=windows-builder /app/dist/ ./windows/
COPY --from=linux-builder /app/dist/ ./linux/
CMD ["sh"]
'''
    
    dockerfile = Path(__file__).parent / "Dockerfile"
    with open(dockerfile, 'w', encoding='utf-8') as f:
        f.write(dockerfile_content)
    
    # 创建docker-compose文件
    compose_content = '''
version: '3.8'
services:
  build-windows:
    build:
      context: .
      target: windows-builder
    volumes:
      - ./dist/windows:/app/dist
  
  build-linux:
    build:
      context: .
      target: linux-builder
    volumes:
      - ./dist/linux:/app/dist
'''
    
    compose_file = Path(__file__).parent / "docker-compose.yml"
    with open(compose_file, 'w', encoding='utf-8') as f:
        f.write(compose_content)
    
    return dockerfile, compose_file

def create_build_instructions():
    """创建详细的构建说明文档"""
    instructions = '''
# 跨平台打包说明

## 问题说明

在macOS上使用PyInstaller无法直接生成真正的Windows exe文件。PyInstaller只能为当前运行的操作系统生成可执行文件。

## 解决方案

### 方案1: GitHub Actions自动化打包 (推荐)

1. 将代码推送到GitHub仓库
2. GitHub Actions会自动在Windows、macOS、Linux环境中分别打包
3. 下载生成的artifacts

**使用步骤:**
```bash
# 1. 初始化git仓库(如果还没有)
git init
git add .
git commit -m "Initial commit"

# 2. 推送到GitHub
git remote add origin https://github.com/你的用户名/目录扫描器.git
git push -u origin main

# 3. 在GitHub仓库的Actions页面查看构建进度
# 4. 构建完成后下载artifacts
```

### 方案2: 使用Windows虚拟机

1. 安装Windows虚拟机(VMware/VirtualBox/Parallels)
2. 在虚拟机中安装Python和依赖
3. 运行打包脚本

### 方案3: 使用Docker (高级用户)

```bash
# 构建Docker镜像
docker-compose up build-windows
docker-compose up build-linux

# 或者使用单独的Docker命令
docker build --target windows-builder -t scanner-windows .
docker run -v $(pwd)/dist/windows:/app/dist scanner-windows
```

### 方案4: 云端构建服务

- **GitHub Codespaces**: 在线开发环境
- **GitPod**: 基于浏览器的IDE
- **Replit**: 在线Python环境

## 当前可用的打包

在macOS上，你可以生成:
- ✅ macOS应用包 (.app)
- ✅ macOS可执行文件
- ❌ Windows exe文件 (需要Windows环境)
- ❌ Linux可执行文件 (需要Linux环境)

## 文件说明

- `cross_platform_build.py`: 本脚本，提供跨平台打包指导
- `.github/workflows/build.yml`: GitHub Actions工作流
- `Dockerfile`: Docker构建文件
- `docker-compose.yml`: Docker编排文件

## 推荐流程

1. **开发阶段**: 在macOS上开发和测试
2. **打包阶段**: 使用GitHub Actions自动化打包
3. **分发阶段**: 从GitHub Releases下载对应平台的可执行文件

这样可以确保为每个平台生成真正原生的可执行文件。
'''
    
    readme_file = Path(__file__).parent / "BUILD_INSTRUCTIONS.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    return readme_file

def local_build():
    """本地打包 - 只能生成当前平台的可执行文件"""
    global progress_done
    progress_done = False
    
    current_dir = Path(__file__).parent
    script_path = current_dir / "directory_scanner.py"
    
    if not script_path.exists():
        safe_print(f"❌ 找不到主程序文件: {script_path}")
        return False
    
    system = platform.system()
    safe_print(f"🖥️  当前系统: {system}")
    
    # 检查图标文件
    icon_path = None
    for icon_name in ["icon.ico", "icon.png", "icon.icns"]:
        test_path = current_dir / icon_name
        if test_path.exists():
            icon_path = test_path
            safe_print(f"✅ 找到图标文件: {icon_path.name}")
            break
    
    if not icon_path:
        safe_print("⚠️ 未找到图标文件，将使用默认图标")
    
    # 根据系统选择打包参数
    if system == "Windows":
        dist_path = "dist/windows"
        build_path = "build/windows"
        windowed = "--windowed"
    elif system == "Darwin":
        dist_path = "dist/macos"
        build_path = "build/macos"
        windowed = "--windowed"
    else:  # Linux
        dist_path = "dist/linux"
        build_path = "build/linux"
        windowed = ""
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--clean",
        "--noconfirm",
        "--name=目录扫描器",
        f"--distpath={dist_path}",
        f"--workpath={build_path}"
    ]
    
    if windowed:
        cmd.append(windowed)
    
    if icon_path:
        cmd.extend(["--icon", str(icon_path)])
    
    # 添加隐藏导入
    hidden_imports = [
        "tkinter", "tkinter.filedialog", "tkinter.messagebox",
        "json", "pathlib", "os", "sys"
    ]
    
    for module in hidden_imports:
        cmd.extend(["--hidden-import", module])
    
    cmd.append(str(script_path))
    
    safe_print(f"\n🚀 开始{system}平台打包...")
    safe_print(f"📝 目标目录: {dist_path}")
    
    # 启动进度显示线程
    progress_thread = threading.Thread(target=show_progress)
    progress_thread.daemon = True
    progress_thread.start()
    
    try:
        result = subprocess.run(cmd, cwd=current_dir, capture_output=True, text=True)
        progress_done = True
        
        if result.returncode == 0:
            safe_print(f"\n🎉 {system}平台打包成功！")
            
            # 查找生成的文件
            dist_dir = current_dir / dist_path.split('/')[0] / dist_path.split('/')[1]
            if dist_dir.exists():
                files = list(dist_dir.glob("*"))
                if files:
                    for file in files:
                        safe_print(f"📦 生成文件: {file}")
                        if file.is_file() and not file.name.startswith('.'):
                            size_mb = file.stat().st_size / (1024*1024)
                            safe_print(f"📏 文件大小: {size_mb:.1f} MB")
            
            return True
        else:
            progress_done = True
            safe_print(f"\n❌ {system}平台打包失败")
            safe_print(f"错误信息: {result.stderr}")
            return False
            
    except Exception as e:
        progress_done = True
        safe_print(f"\n❌ 打包过程出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 70)
    safe_print("🌍 目录扫描器 - 跨平台打包脚本")
    print("=" * 70)
    
    system = platform.system()
    safe_print(f"🖥️  当前系统: {system}")
    safe_print(f"🐍 Python版本: {sys.version.split()[0]}")
    
    safe_print("\n📋 可用选项:")
    safe_print("1. 本地打包 (只能生成当前平台的可执行文件)")
    safe_print("2. 创建GitHub Actions工作流 (推荐)")
    safe_print("3. 创建Docker构建文件")
    safe_print("4. 查看详细说明")
    safe_print("5. 退出")
    
    try:
        choice = input("\n请选择操作 (1-5): ").strip()
        
        if choice == "1":
            print("\n" + "="*50)
            if local_build():
                safe_print(f"\n🎊 恭喜！{system}平台打包完成")
            else:
                safe_print("\n😞 打包失败")
                
        elif choice == "2":
            safe_print("\n📝 创建GitHub Actions工作流...")
            workflow_file = create_github_workflow()
            safe_print(f"✅ 已创建: {workflow_file}")
            safe_print("\n📋 下一步:")
            safe_print("1. 将代码推送到GitHub仓库")
            safe_print("2. 在仓库的Actions页面查看构建进度")
            safe_print("3. 构建完成后下载artifacts")
            
        elif choice == "3":
            safe_print("\n🐳 创建Docker构建文件...")
            dockerfile, compose_file = create_docker_build()
            safe_print(f"✅ 已创建: {dockerfile}")
            safe_print(f"✅ 已创建: {compose_file}")
            safe_print("\n📋 使用方法:")
            print("docker-compose up build-windows")
            print("docker-compose up build-linux")
            
        elif choice == "4":
            safe_print("\n📖 创建详细说明文档...")
            readme_file = create_build_instructions()
            safe_print(f"✅ 已创建: {readme_file}")
            safe_print("\n请查看该文件了解详细的跨平台打包方法")
            
        elif choice == "5":
            safe_print("\n👋 再见！")
            
        else:
            safe_print("\n❌ 无效选择")
            
    except KeyboardInterrupt:
        safe_print("\n\n👋 再见！")
    except Exception as e:
        safe_print(f"\n❌ 发生错误: {e}")

if __name__ == "__main__":
    # 全局变量
    progress_done = False
    main()