# 🚀 发布指南

本指南介绍如何使用GitHub Actions自动构建和发布跨平台可执行文件。

## 📋 工作流概览

### 1. 自动构建工作流 (`build.yml`)
- **触发条件**: 推送到主分支、创建PR、手动触发
- **功能**: 自动构建Windows、macOS、Linux版本
- **输出**: 构建产物和日志

### 2. 自动发布工作流 (`release.yml`)
- **触发条件**: 推送标签、手动触发
- **功能**: 构建所有平台并创建GitHub Release
- **输出**: 正式发布版本

## 🔄 开发工作流

### 日常开发

```bash
# 1. 开发和测试
git add .
git commit -m "feat: 添加新功能"
git push origin main

# 2. 自动触发构建
# GitHub Actions 会自动运行构建测试
```

### 发布新版本

```bash
# 1. 确保代码已提交到主分支
git checkout main
git pull origin main

# 2. 创建并推送标签
git tag v1.0.0
git push origin v1.0.0

# 3. 自动创建发布
# GitHub Actions 会自动构建并创建Release
```

## 📦 构建流程详解

### 阶段1: 预检查
- ✅ 代码检出
- ✅ Python环境设置
- ✅ 依赖安装
- ✅ 构建脚本测试
- ✅ 版本号生成

### 阶段2: 跨平台构建
- 🪟 **Windows**: 使用 `build_windows_fixed.py`
- 🍎 **macOS**: 使用 `build_macos_fixed.py`
- 🐧 **Linux**: 使用 `cross_platform_build.py`

### 阶段3: 验证和上传
- ✅ 构建结果验证
- 📦 产物上传
- 📋 日志保存

## 🎯 手动触发构建

### 通过GitHub界面

1. 访问你的GitHub仓库
2. 点击 "Actions" 标签
3. 选择 "🚀 跨平台自动构建" 工作流
4. 点击 "Run workflow"
5. 可选择指定版本号

### 通过GitHub CLI

```bash
# 安装GitHub CLI
brew install gh  # macOS
# 或 sudo apt install gh  # Linux

# 登录
gh auth login

# 触发构建
gh workflow run "🚀 跨平台自动构建"

# 触发发布 (需要指定标签)
gh workflow run "📦 自动发布" -f tag=v1.0.0
```

## 📋 版本管理策略

### 语义化版本控制

- **主版本号** (v1.0.0 → v2.0.0): 不兼容的API修改
- **次版本号** (v1.0.0 → v1.1.0): 向后兼容的功能性新增
- **修订号** (v1.0.0 → v1.0.1): 向后兼容的问题修正

### 标签命名规范

```bash
# 正式版本
git tag v1.0.0
git tag v1.1.0
git tag v2.0.0

# 预发布版本
git tag v1.0.0-alpha.1
git tag v1.0.0-beta.1
git tag v1.0.0-rc.1
```

## 🔧 构建配置

### 环境变量

| 变量 | 值 | 说明 |
|------|----|----- |
| `PYTHON_VERSION` | 3.12 | Python版本 |
| `APP_NAME` | 目录文件生成器 | 应用名称 |

### 构建矩阵

| 平台 | 运行环境 | 构建脚本 | 输出格式 |
|------|----------|----------|----------|
| Windows | windows-latest | build_windows_fixed.py | .exe |
| macOS | macos-latest | build_macos_fixed.py | .app |
| Linux | ubuntu-latest | cross_platform_build.py | 可执行文件 |

## 📁 产物说明

### 构建产物

- **命名格式**: `目录文件生成器-{平台}-{版本号}`
- **保留时间**: 30天
- **包含内容**: 可执行文件和必要资源

### 发布文件

| 平台 | 文件名 | 格式 | 说明 |
|------|--------|------|------|
| Windows | `目录文件生成器-Windows-x64.exe` | 单文件 | 直接运行 |
| macOS | `目录文件生成器-macOS-Universal.app.zip` | 压缩包 | 解压后拖入应用程序 |
| Linux | `目录文件生成器-Linux-x64.tar.gz` | 压缩包 | 解压后运行 |

## 🐛 故障排除

### 常见构建失败原因

#### 1. 依赖问题
```
❌ ModuleNotFoundError: No module named 'xxx'
```
**解决方案**: 检查 `requirements.txt` 是否包含所有依赖

#### 2. 测试失败
```
❌ 构建脚本测试失败
```
**解决方案**: 本地运行 `python test_build_scripts.py` 检查问题

#### 3. 平台特定问题
```
❌ Linux构建失败: tkinter相关错误
```
**解决方案**: 已在工作流中添加 `python3-tk` 安装

#### 4. 权限问题
```
❌ Permission denied
```
**解决方案**: 检查文件权限和GitHub token权限

### 调试步骤

1. **查看构建日志**
   - 在GitHub Actions页面查看详细日志
   - 下载构建日志产物进行分析

2. **本地复现**
   ```bash
   # 运行相同的构建脚本
   python test_build_scripts.py
   python build_macos_fixed.py  # 或对应平台脚本
   ```

3. **检查环境**
   ```bash
   # 验证Python版本
   python --version
   
   # 检查依赖
   pip list
   
   # 运行诊断
   python fix_packaging_issues.py
   ```

## 📊 监控和通知

### 构建状态徽章

在README.md中添加构建状态徽章:

```markdown
[![构建状态](https://github.com/用户名/仓库名/workflows/🚀%20跨平台自动构建/badge.svg)](https://github.com/用户名/仓库名/actions)
```

### 发布通知

- GitHub会自动发送发布通知给关注者
- 可以在Release页面查看下载统计
- 支持RSS订阅发布更新

## 🔄 持续改进

### 定期维护

- **每月**: 更新依赖版本
- **每季度**: 检查GitHub Actions版本
- **每半年**: 评估构建策略和优化空间

### 性能优化

- 使用缓存加速依赖安装
- 并行构建减少总时间
- 增量构建避免重复工作

## 📞 获取帮助

如果遇到问题:

1. 查看GitHub Actions日志
2. 参考本指南的故障排除部分
3. 在仓库Issues中提问
4. 查看GitHub Actions官方文档

---

💡 **提示**: 建议在每次重要更新前先在分支中测试构建流程，确保一切正常后再合并到主分支。