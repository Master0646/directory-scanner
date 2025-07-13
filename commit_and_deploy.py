#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码提交和部署脚本
自动化提交代码到GitHub并触发构建流程
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def run_command(cmd, cwd=None):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True, 
            encoding='utf-8'
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_git_status():
    """检查Git状态"""
    print("🔍 检查Git状态...")
    
    # 检查是否在Git仓库中
    success, _, _ = run_command("git rev-parse --git-dir")
    if not success:
        print("❌ 当前目录不是Git仓库，请先初始化Git仓库")
        print("   运行: git init")
        return False
    
    # 检查是否有远程仓库
    success, output, _ = run_command("git remote -v")
    if not success or not output:
        print("⚠️  未配置远程仓库，请先添加远程仓库")
        print("   运行: git remote add origin <your-repo-url>")
        return False
    
    print(f"✅ Git仓库状态正常")
    print(f"   远程仓库: {output.split()[1] if output else '未知'}")
    return True

def check_uncommitted_changes():
    """检查未提交的更改"""
    print("\n📝 检查未提交的更改...")
    
    success, output, _ = run_command("git status --porcelain")
    if not success:
        print("❌ 无法检查Git状态")
        return False
    
    if not output:
        print("✅ 没有未提交的更改")
        return True
    
    print("📋 发现以下未提交的更改:")
    for line in output.split('\n'):
        if line.strip():
            status = line[:2]
            file_path = line[3:]
            status_desc = {
                'M ': '修改',
                ' M': '修改',
                'A ': '新增',
                'D ': '删除',
                'R ': '重命名',
                'C ': '复制',
                '??': '未跟踪'
            }.get(status, '未知')
            print(f"   {status_desc}: {file_path}")
    
    return True

def run_tests():
    """运行测试"""
    print("\n🧪 运行构建测试...")
    
    if os.path.exists("test_build_scripts.py"):
        success, output, error = run_command("python test_build_scripts.py")
        if success:
            print("✅ 构建测试通过")
            return True
        else:
            print("❌ 构建测试失败")
            print(f"错误信息: {error}")
            return False
    else:
        print("⚠️  未找到测试脚本，跳过测试")
        return True

def commit_changes(message=None):
    """提交更改"""
    print("\n📦 提交更改...")
    
    # 添加所有更改
    success, _, error = run_command("git add .")
    if not success:
        print(f"❌ 添加文件失败: {error}")
        return False
    
    # 生成提交信息
    if not message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"🚀 自动提交 - {timestamp}"
    
    # 提交更改
    success, output, error = run_command(f'git commit -m "{message}"')
    if not success:
        if "nothing to commit" in error:
            print("✅ 没有需要提交的更改")
            return True
        else:
            print(f"❌ 提交失败: {error}")
            return False
    
    print(f"✅ 提交成功: {message}")
    return True

def push_changes():
    """推送更改"""
    print("\n🚀 推送到远程仓库...")
    
    # 获取当前分支
    success, branch, _ = run_command("git branch --show-current")
    if not success:
        branch = "main"
    
    # 推送更改
    success, output, error = run_command(f"git push origin {branch}")
    if not success:
        print(f"❌ 推送失败: {error}")
        print("\n💡 可能的解决方案:")
        print("   1. 检查网络连接")
        print("   2. 检查Git凭据")
        print("   3. 检查远程仓库权限")
        return False
    
    print(f"✅ 推送成功到分支: {branch}")
    return True

def create_release_tag(version=None):
    """创建发布标签"""
    if not version:
        return True
    
    print(f"\n🏷️  创建发布标签: {version}")
    
    # 创建标签
    success, _, error = run_command(f'git tag -a {version} -m "Release {version}"')
    if not success:
        print(f"❌ 创建标签失败: {error}")
        return False
    
    # 推送标签
    success, _, error = run_command(f"git push origin {version}")
    if not success:
        print(f"❌ 推送标签失败: {error}")
        return False
    
    print(f"✅ 发布标签创建成功: {version}")
    print(f"🎉 这将触发自动构建和发布流程!")
    return True

def main():
    """主函数"""
    print("🚀 目录文件生成器 - 自动提交和部署")
    print("=" * 50)
    
    # 检查参数
    commit_message = None
    release_version = None
    
    if len(sys.argv) > 1:
        if sys.argv[1].startswith("v"):
            release_version = sys.argv[1]
        else:
            commit_message = " ".join(sys.argv[1:])
    
    if len(sys.argv) > 2:
        release_version = sys.argv[2] if sys.argv[2].startswith("v") else None
    
    # 执行检查和提交流程
    steps = [
        ("检查Git状态", check_git_status),
        ("检查未提交更改", check_uncommitted_changes),
        ("运行测试", run_tests),
        ("提交更改", lambda: commit_changes(commit_message)),
        ("推送更改", push_changes),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ {step_name}失败，停止执行")
            sys.exit(1)
    
    # 如果指定了版本，创建发布标签
    if release_version:
        if not create_release_tag(release_version):
            print("\n❌ 创建发布标签失败")
            sys.exit(1)
    
    print("\n🎉 所有步骤完成!")
    print("\n📋 后续步骤:")
    print("   1. 查看GitHub Actions构建状态")
    print("   2. 等待自动构建完成")
    if release_version:
        print("   3. 检查自动创建的Release")
        print("   4. 下载构建的可执行文件")
    else:
        print("   3. 如需发布新版本，运行: python commit_and_deploy.py v1.0.0")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)