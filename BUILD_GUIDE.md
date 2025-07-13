# 构建脚本使用指南

## 📋 脚本概览

经过整理，项目现在包含以下构建相关脚本，每个都有其独特的用途：

### 🔧 开发调试脚本
- `setup_dev.py` - 开发环境配置脚本
- `debug_launcher.py` - 调试启动器
- `debug_local.py` - 本地调试脚本
- `quick_debug.py` - 快速调试脚本
- `runtime_error_detector.py` - 运行时错误检测器

### 📦 打包构建脚本
- `build_macos_fixed.py` - **主要的macOS打包脚本**（推荐使用）
- `build_windows_fixed.py` - **修复版Windows打包脚本**（推荐使用）
- `cross_platform_build.py` - 跨平台自动化打包
- `windows_build.py` - Windows基础打包脚本
- `fix_packaging_issues.py` - 打包问题诊断工具

## 🎯 使用场景

### 日常开发调试
```bash
# 快速启动（推荐）
make run

# 或使用调试启动器
python debug_launcher.py

# 快速调试
python quick_debug.py
```

### macOS打包
```bash
# 使用修复版构建脚本（推荐）
python build_macos_fixed.py
```

### 跨平台打包
```bash
# 设置GitHub Actions自动化打包
python cross_platform_build.py
```

### Windows打包
```bash
# 使用修复版构建脚本（推荐）
python build_windows_fixed.py

# 或使用基础版本
python windows_build.py
```

### 问题排查
```bash
# 诊断打包问题
python fix_packaging_issues.py

# 检测运行时错误
python runtime_error_detector.py
```

## 🔍 脚本详细说明

### build_macos_fixed.py
- **用途：** 主要的macOS打包脚本
- **特点：** 包含完整的隐藏导入配置，解决"本地运行正常，打包后出现问题"
- **输出：** `dist/目录扫描器.app`
- **推荐指数：** ⭐⭐⭐⭐⭐

### cross_platform_build.py
- **用途：** 创建GitHub Actions工作流，支持云端自动化打包
- **特点：** 解决macOS无法直接生成Windows exe的问题
- **输出：** GitHub Actions配置文件
- **适用场景：** 需要生成多平台可执行文件

### build_windows_fixed.py
- **用途：** 修复版Windows打包脚本
- **特点：** 包含完整的隐藏导入配置，解决常见Windows打包问题
- **输出：** `dist/windows/目录扫描器.exe`
- **推荐指数：** ⭐⭐⭐⭐⭐

### windows_build.py
- **用途：** Windows平台基础打包
- **特点：** 包含Windows版本信息文件创建
- **输出：** `dist/windows/目录扫描器.exe`
- **适用场景：** 基础Windows打包需求

### fix_packaging_issues.py
- **用途：** 自动诊断打包问题
- **特点：** 检测依赖、路径、隐藏导入等问题
- **输出：** 问题报告和修复建议
- **适用场景：** 打包出现问题时使用

## 💡 最佳实践

1. **开发阶段：** 使用 `make run` 进行快速调试
2. **本地打包：** macOS使用 `build_macos_fixed.py`，Windows使用 `build_windows_fixed.py`
3. **多平台发布：** 使用 `cross_platform_build.py` 设置自动化
4. **问题排查：** 使用 `fix_packaging_issues.py` 诊断

## 🚀 快速开始

```bash
# 1. 设置开发环境
python setup_dev.py

# 2. 开发调试
make run

# 3. 打包发布（根据系统选择）
# macOS:
python build_macos_fixed.py
# Windows:
python build_windows_fixed.py
```

## ⚠️ 注意事项

- 所有脚本都已经过测试和验证
- 建议按照推荐的使用场景选择合适的脚本
- 如遇到问题，优先使用诊断工具排查
- 保持依赖更新：`pip install -r requirements.txt`