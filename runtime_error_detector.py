#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行时错误检测器
专门用于检测打包后应用的运行时问题
作者：张牛牛
"""

import os
import sys
import traceback
import logging
from pathlib import Path
from datetime import datetime

class RuntimeErrorDetector:
    """运行时错误检测类
    
    用于捕获和分析打包后应用的运行时错误
    """
    
    def __init__(self):
        """初始化错误检测器"""
        self.setup_logging()
        self.errors_detected = []
        
    def setup_logging(self):
        """设置日志记录
        
        配置详细的日志记录，便于问题追踪
        """
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"runtime_debug_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"运行时错误检测器启动，日志文件: {log_file}")
        
    def detect_environment_issues(self):
        """检测环境问题
        
        检查打包后的运行环境是否正常
        """
        self.logger.info("🔍 检测运行环境...")
        
        # 检查Python路径
        self.logger.info(f"Python可执行文件: {sys.executable}")
        self.logger.info(f"Python版本: {sys.version}")
        self.logger.info(f"Python路径: {sys.path}")
        
        # 检查是否在打包环境中运行
        if hasattr(sys, '_MEIPASS'):
            self.logger.info(f"✅ 检测到PyInstaller环境: {sys._MEIPASS}")
            self.logger.info(f"临时目录: {sys._MEIPASS}")
            
            # 检查临时目录中的文件
            try:
                temp_files = list(Path(sys._MEIPASS).rglob('*'))
                self.logger.info(f"临时目录文件数量: {len(temp_files)}")
                
                # 列出重要文件
                important_files = [f for f in temp_files if f.name in [
                    'icon.png', 'config.json', 'pandas', 'numpy', 'openpyxl'
                ]]
                
                if important_files:
                    self.logger.info("重要文件:")
                    for f in important_files[:10]:  # 只显示前10个
                        self.logger.info(f"  - {f}")
                        
            except Exception as e:
                self.logger.error(f"检查临时目录失败: {e}")
                self.errors_detected.append({
                    "type": "environment",
                    "error": "无法访问PyInstaller临时目录",
                    "details": str(e)
                })
        else:
            self.logger.info("⚠️  未检测到PyInstaller环境（可能是开发模式）")
            
        # 检查工作目录
        self.logger.info(f"当前工作目录: {os.getcwd()}")
        
    def test_critical_imports(self):
        """测试关键模块导入
        
        逐个测试关键模块的导入情况
        """
        self.logger.info("📦 测试关键模块导入...")
        
        critical_modules = {
            'tkinter': 'GUI框架',
            'tkinter.ttk': 'TTK组件',
            'tkinter.messagebox': '消息框',
            'tkinter.filedialog': '文件对话框',
            'pandas': '数据处理',
            'numpy': '数值计算',
            'openpyxl': 'Excel处理',
            'datetime': '日期时间',
            'pathlib': '路径处理',
            'json': 'JSON处理',
            'threading': '多线程',
            'subprocess': '子进程',
            'collections': '集合类型'
        }
        
        failed_imports = []
        
        for module_name, description in critical_modules.items():
            try:
                __import__(module_name)
                self.logger.info(f"✅ {module_name} ({description})")
            except ImportError as e:
                self.logger.error(f"❌ {module_name} ({description}): {e}")
                failed_imports.append({
                    "module": module_name,
                    "description": description,
                    "error": str(e)
                })
                self.errors_detected.append({
                    "type": "import",
                    "error": f"无法导入 {module_name}",
                    "details": str(e)
                })
            except Exception as e:
                self.logger.error(f"⚠️  {module_name} ({description}): 其他错误 {e}")
                
        if failed_imports:
            self.logger.error(f"导入失败的模块数量: {len(failed_imports)}")
        else:
            self.logger.info("✅ 所有关键模块导入成功")
            
    def test_file_access(self):
        """测试文件访问
        
        测试应用是否能正确访问所需的文件
        """
        self.logger.info("📁 测试文件访问...")
        
        # 测试资源文件访问
        resource_files = ['icon.png', 'config.json']
        
        for resource_file in resource_files:
            try:
                # 尝试不同的路径解析方式
                paths_to_try = [
                    resource_file,  # 相对路径
                    os.path.abspath(resource_file),  # 绝对路径
                ]
                
                # 如果在PyInstaller环境中，尝试临时目录
                if hasattr(sys, '_MEIPASS'):
                    paths_to_try.append(os.path.join(sys._MEIPASS, resource_file))
                    
                found = False
                for path in paths_to_try:
                    if os.path.exists(path):
                        self.logger.info(f"✅ 找到 {resource_file}: {path}")
                        found = True
                        break
                        
                if not found:
                    self.logger.warning(f"⚠️  未找到 {resource_file}")
                    self.errors_detected.append({
                        "type": "file",
                        "error": f"找不到资源文件 {resource_file}",
                        "details": f"尝试的路径: {paths_to_try}"
                    })
                    
            except Exception as e:
                self.logger.error(f"❌ 访问 {resource_file} 时出错: {e}")
                
    def test_gui_creation(self):
        """测试GUI创建
        
        尝试创建基本的GUI组件，检查是否有显示问题
        """
        self.logger.info("🖥️  测试GUI创建...")
        
        try:
            import tkinter as tk
            from tkinter import ttk, messagebox, filedialog
            
            # 创建测试窗口
            self.logger.info("创建测试窗口...")
            test_root = tk.Tk()
            test_root.withdraw()  # 隐藏窗口
            
            # 测试基本组件
            test_frame = ttk.Frame(test_root)
            test_label = ttk.Label(test_frame, text="测试标签")
            test_button = ttk.Button(test_frame, text="测试按钮")
            
            self.logger.info("✅ 基本GUI组件创建成功")
            
            # 清理
            test_root.destroy()
            
        except Exception as e:
            self.logger.error(f"❌ GUI创建失败: {e}")
            self.logger.error(traceback.format_exc())
            self.errors_detected.append({
                "type": "gui",
                "error": "GUI创建失败",
                "details": str(e)
            })
            
    def test_data_processing(self):
        """测试数据处理功能
        
        测试pandas、numpy等数据处理模块的基本功能
        """
        self.logger.info("📊 测试数据处理功能...")
        
        try:
            import pandas as pd
            import numpy as np
            
            # 测试pandas基本功能
            test_data = {'name': ['测试1', '测试2'], 'value': [1, 2]}
            df = pd.DataFrame(test_data)
            self.logger.info(f"✅ pandas DataFrame创建成功: {df.shape}")
            
            # 测试numpy基本功能
            arr = np.array([1, 2, 3, 4, 5])
            self.logger.info(f"✅ numpy数组创建成功: {arr.shape}")
            
            # 测试openpyxl
            try:
                import openpyxl
                wb = openpyxl.Workbook()
                ws = wb.active
                ws['A1'] = '测试'
                self.logger.info("✅ openpyxl工作簿创建成功")
            except Exception as e:
                self.logger.error(f"❌ openpyxl测试失败: {e}")
                
        except Exception as e:
            self.logger.error(f"❌ 数据处理测试失败: {e}")
            self.logger.error(traceback.format_exc())
            self.errors_detected.append({
                "type": "data",
                "error": "数据处理功能测试失败",
                "details": str(e)
            })
            
    def run_comprehensive_test(self):
        """运行综合测试
        
        执行所有测试项目
        """
        self.logger.info("🚀 开始运行时错误检测...")
        self.logger.info("=" * 50)
        
        try:
            # 1. 环境检测
            self.detect_environment_issues()
            
            # 2. 导入测试
            self.test_critical_imports()
            
            # 3. 文件访问测试
            self.test_file_access()
            
            # 4. GUI测试
            self.test_gui_creation()
            
            # 5. 数据处理测试
            self.test_data_processing()
            
        except Exception as e:
            self.logger.error(f"测试过程中发生严重错误: {e}")
            self.logger.error(traceback.format_exc())
            
        # 生成报告
        self.generate_report()
        
    def generate_report(self):
        """生成检测报告
        
        汇总所有检测结果并提供解决建议
        """
        self.logger.info("\n" + "=" * 50)
        self.logger.info("📋 运行时错误检测报告")
        self.logger.info("=" * 50)
        
        if not self.errors_detected:
            self.logger.info("🎉 恭喜！未检测到运行时错误")
            self.logger.info("应用应该可以正常运行")
            return
            
        self.logger.error(f"⚠️  检测到 {len(self.errors_detected)} 个问题:")
        
        # 按类型分组错误
        errors_by_type = {}
        for error in self.errors_detected:
            error_type = error['type']
            if error_type not in errors_by_type:
                errors_by_type[error_type] = []
            errors_by_type[error_type].append(error)
            
        # 显示错误详情
        for error_type, errors in errors_by_type.items():
            self.logger.error(f"\n{error_type.upper()} 错误:")
            for i, error in enumerate(errors, 1):
                self.logger.error(f"  {i}. {error['error']}")
                self.logger.error(f"     详情: {error['details']}")
                
        # 提供解决建议
        self.logger.info("\n🔧 解决建议:")
        
        if 'import' in errors_by_type:
            self.logger.info("📦 导入问题解决方案:")
            self.logger.info("  1. 使用修复版构建脚本重新打包")
            self.logger.info("  2. 检查requirements.txt中的依赖版本")
            self.logger.info("  3. 添加缺失的--hidden-import参数")
            
        if 'file' in errors_by_type:
            self.logger.info("📁 文件访问问题解决方案:")
            self.logger.info("  1. 确保资源文件存在于项目目录")
            self.logger.info("  2. 在构建时使用--add-data参数包含文件")
            self.logger.info("  3. 修改代码使用正确的资源文件路径")
            
        if 'gui' in errors_by_type:
            self.logger.info("🖥️  GUI问题解决方案:")
            self.logger.info("  1. 检查tkinter相关的隐藏导入")
            self.logger.info("  2. 确保系统支持GUI显示")
            self.logger.info("  3. 检查macOS的安全设置")
            
        self.logger.info("\n📞 如需进一步帮助:")
        self.logger.info("  1. 查看详细日志文件")
        self.logger.info("  2. 运行调试构建: python fix_packaging_issues.py --debug-build")
        self.logger.info("  3. 在终端中直接运行打包后的可执行文件")

def safe_main():
    """安全的主函数
    
    包装主函数，确保即使出错也能生成报告
    """
    detector = None
    try:
        detector = RuntimeErrorDetector()
        detector.run_comprehensive_test()
    except Exception as e:
        print(f"❌ 运行时错误检测器本身出现问题: {e}")
        print(traceback.format_exc())
        
        if detector:
            detector.logger.error(f"检测器错误: {e}")
            detector.logger.error(traceback.format_exc())

def main():
    """主函数"""
    print("🔍 运行时错误检测器")
    print("专门检测打包后应用的运行时问题")
    print("=" * 50)
    
    safe_main()
    
    print("\n✅ 检测完成！")
    print("📄 详细日志已保存到 logs/ 目录")
    print("💡 建议查看日志文件获取完整信息")

if __name__ == "__main__":
    main()