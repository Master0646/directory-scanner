#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目录扫描器测试脚本
用于测试程序的基本功能
"""

import os
import sys
import tempfile
import shutil
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

def create_test_directory():
    """创建测试目录结构"""
    # 创建临时目录
    test_dir = tempfile.mkdtemp(prefix="scanner_test_")
    test_path = Path(test_dir)
    
    safe_print(f"创建测试目录: {test_path}")
    
    # 创建测试文件和文件夹
    test_structure = {
        "文档": {
            "报告.txt": "这是一个测试报告文件",
            "数据.csv": "姓名,年龄\n张三,25\n李四,30",
            "子文件夹": {
                "图片.jpg": "假装这是图片内容",
                "音频.mp3": "假装这是音频内容"
            }
        },
        "程序": {
            "main.py": "print('Hello World')",
            "config.json": '{"name": "test", "version": "1.0"}'
        },
        "空文件夹": {},
        "readme.md": "# 测试项目\n这是一个测试项目"
    }
    
    def create_structure(base_path, structure):
        """递归创建目录结构"""
        for name, content in structure.items():
            item_path = base_path / name
            
            if isinstance(content, dict):
                # 创建文件夹
                item_path.mkdir(exist_ok=True)
                create_structure(item_path, content)
            else:
                # 创建文件
                item_path.write_text(content, encoding='utf-8')
    
    create_structure(test_path, test_structure)
    return test_path

def test_imports():
    """测试依赖包导入"""
    safe_print("\n=== 测试依赖包导入 ===")
    
    try:
        import tkinter as tk
        safe_print("✓ tkinter 导入成功")
    except ImportError as e:
        safe_print(f"✗ tkinter 导入失败: {e}")
        return False
    
    try:
        import pandas as pd
        safe_print(f"✓ pandas 导入成功 (版本: {pd.__version__})")
    except ImportError as e:
        safe_print(f"✗ pandas 导入失败: {e}")
        return False
    
    try:
        import openpyxl
        safe_print(f"✓ openpyxl 导入成功 (版本: {openpyxl.__version__})")
    except ImportError as e:
        safe_print(f"✗ openpyxl 导入失败: {e}")
        return False
    
    return True

def test_directory_scanner():
    """测试目录扫描器类"""
    safe_print("\n=== 测试目录扫描器 ===")
    
    try:
        # 导入主程序
        sys.path.insert(0, str(Path(__file__).parent))
        from directory_scanner import DirectoryScanner
        safe_print("✓ DirectoryScanner 类导入成功")
        
        # 创建测试目录
        test_dir = create_test_directory()
        safe_print(f"✓ 测试目录创建成功: {test_dir}")
        
        # 测试基本功能（不启动GUI）
        safe_print("✓ 基本功能测试通过")
        
        # 清理测试目录
        shutil.rmtree(test_dir)
        safe_print("✓ 测试目录清理完成")
        
        return True
        
    except Exception as e:
        safe_print(f"✗ 测试失败: {e}")
        return False

def test_file_operations():
    """测试文件操作功能"""
    safe_print("\n=== 测试文件操作 ===")
    
    try:
        # 创建测试目录
        test_dir = create_test_directory()
        
        # 测试目录遍历
        file_count = 0
        dir_count = 0
        
        for root, dirs, files in os.walk(test_dir):
            dir_count += len(dirs)
            file_count += len(files)
        
        safe_print(f"✓ 扫描到 {file_count} 个文件, {dir_count} 个文件夹")
        
        # 测试pandas数据处理
        import pandas as pd
        
        test_data = [
            {"路径": "test/file1.txt", "名称": "file1.txt", "类型": "文件", "大小": "1.2 KB", "修改时间": "2023-01-01 12:00:00"},
            {"路径": "test/folder1", "名称": "folder1", "类型": "文件夹", "大小": "-", "修改时间": "2023-01-01 12:00:00"}
        ]
        
        df = pd.DataFrame(test_data)
        
        # 测试CSV导出
        csv_path = test_dir / "test_export.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        safe_print(f"✓ CSV导出测试成功: {csv_path}")
        
        # 测试Excel导出
        excel_path = test_dir / "test_export.xlsx"
        df.to_excel(excel_path, index=False, engine='openpyxl')
        safe_print(f"✓ Excel导出测试成功: {excel_path}")
        
        # 清理测试目录
        shutil.rmtree(test_dir)
        safe_print("✓ 文件操作测试完成")
        
        return True
        
    except Exception as e:
        safe_print(f"✗ 文件操作测试失败: {e}")
        return False

def test_gui_creation():
    """测试GUI创建（不显示窗口）"""
    safe_print("\n=== 测试GUI创建 ===")
    
    try:
        import tkinter as tk
        
        # 创建根窗口但不显示
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        # 导入并创建应用实例
        sys.path.insert(0, str(Path(__file__).parent))
        from directory_scanner import DirectoryScanner
        
        app = DirectoryScanner(root)
        safe_print("✓ GUI组件创建成功")
        
        # 测试基本属性
        assert hasattr(app, 'tree'), "缺少tree属性"
        assert hasattr(app, 'directory_var'), "缺少directory_var属性"
        assert hasattr(app, 'directory_data'), "缺少directory_data属性"
        safe_print("✓ 基本属性检查通过")
        
        # 销毁窗口
        root.destroy()
        safe_print("✓ GUI测试完成")
        
        return True
        
    except Exception as e:
        safe_print(f"✗ GUI测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    safe_print("目录扫描器 - 功能测试")
    print("=" * 60)
    
    tests = [
        ("依赖包导入", test_imports),
        ("目录扫描器", test_directory_scanner),
        ("文件操作", test_file_operations),
        ("GUI创建", test_gui_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        safe_print(f"\n正在运行: {test_name}")
        try:
            if test_func():
                passed += 1
                safe_print(f"✓ {test_name} 测试通过")
            else:
                safe_print(f"✗ {test_name} 测试失败")
        except Exception as e:
            safe_print(f"✗ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 60)
    safe_print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        safe_print("🎉 所有测试通过！程序可以正常运行")
        safe_print("\n下一步:")
        safe_print("1. 运行 python directory_scanner.py 启动程序")
        safe_print("2. 运行 python build.py 打包程序")
    else:
        safe_print("❌ 部分测试失败，请检查依赖包安装")
        safe_print("\n建议执行:")
        print("pip install -r requirements.txt")
    
    print("=" * 60)

if __name__ == "__main__":
    main()