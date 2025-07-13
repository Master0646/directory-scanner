# 🚀 部署指南

本指南将帮助你快速部署目录文件生成器到GitHub，并设置自动化构建流程。

## 📋 前置要求

- [x] Git 已安装
- [x] GitHub 账户
- [x] Python 3.8+ 环境
- [x] 项目代码已准备就绪

## 🎯 快速部署

### 1. 初始化Git仓库（如果还没有）

```bash
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 首次提交
git commit -m "🎉 初始提交 - 目录文件生成器"
```

### 2. 创建GitHub仓库

1. 访问 [GitHub](https://github.com)
2. 点击 "New repository"
3. 仓库名称：`目录文件生成器` 或 `directory-file-generator`
4. 设置为公开或私有
5. **不要**初始化README、.gitignore或LICENSE（我们已经有了）
6. 点击 "Create repository"

### 3. 连接远程仓库

```bash
# 添加远程仓库（替换为你的GitHub用户名）
git remote add origin https://github.com/你的用户名/目录文件生成器.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 4. 使用自动化部署脚本

我们提供了便捷的部署脚本：

```bash
# 基本提交和推送
python commit_and_deploy.py

# 带自定义提交信息
python commit_and_deploy.py "添加新功能：支持更多文件格式"

# 创建发布版本（会触发自动构建和发布）
python commit_and_deploy.py "发布v1.0.0" v1.0.0

# 或者直接指定版本
python commit_and_deploy.py v1.0.0
```

## 🔧 GitHub Actions 设置

### 自动启用

当你推送代码到GitHub后，GitHub Actions会自动启用：

1. 访问你的仓库页面
2. 点击 "Actions" 标签
3. 你会看到两个工作流：
   - 🚀 **跨平台自动构建** - 每次推送时运行
   - 📦 **自动发布** - 创建标签时运行

### 手动触发构建

1. 进入 "Actions" 页面
2. 选择 "🚀 跨平台自动构建"
3. 点击 "Run workflow"
4. 选择分支并点击 "Run workflow"

## 📦 发布新版本

### 方法1：使用部署脚本（推荐）

```bash
# 创建并推送v1.0.0版本
python commit_and_deploy.py v1.0.0
```

### 方法2：手动创建标签

```bash
# 创建标签
git tag -a v1.0.0 -m "Release v1.0.0"

# 推送标签
git push origin v1.0.0
```

### 方法3：GitHub网页界面

1. 访问仓库页面
2. 点击 "Releases"
3. 点击 "Create a new release"
4. 输入标签版本（如 `v1.0.0`）
5. 填写发布说明
6. 点击 "Publish release"

## 🎯 版本号规范

我们建议使用[语义化版本](https://semver.org/lang/zh-CN/)：

- `v1.0.0` - 主要版本（重大更改）
- `v1.1.0` - 次要版本（新功能）
- `v1.0.1` - 补丁版本（错误修复）

### 示例

```bash
# 修复bug
python commit_and_deploy.py "修复文件扫描bug" v1.0.1

# 添加新功能
python commit_and_deploy.py "添加PDF导出功能" v1.1.0

# 重大更新
python commit_and_deploy.py "重构UI界面" v2.0.0
```

## 📊 监控构建状态

### GitHub Actions页面

1. 访问仓库的 "Actions" 页面
2. 查看最新的工作流运行状态
3. 点击具体的运行查看详细日志

### 构建状态徽章

在README中已经添加了状态徽章：

```markdown
[![构建状态](https://github.com/用户名/目录文件生成器/workflows/🚀%20跨平台自动构建/badge.svg)](https://github.com/用户名/目录文件生成器/actions)
```

记得将 `用户名` 替换为你的GitHub用户名。

## 📥 下载构建产物

### 开发构建

1. 访问 "Actions" 页面
2. 点击最新的成功构建
3. 在 "Artifacts" 部分下载对应平台的文件

### 正式发布

1. 访问 "Releases" 页面
2. 选择最新版本
3. 在 "Assets" 部分下载对应平台的文件

## 🔧 自定义构建

### 修改构建配置

编辑 `.github/workflows/build.yml` 或 `.github/workflows/release.yml`：

```yaml
# 添加新的构建平台
strategy:
  matrix:
    include:
      - os: ubuntu-latest
        platform: Linux
        script: cross_platform_build.py
      - os: windows-latest
        platform: Windows
        script: build_windows_fixed.py
      - os: macos-latest
        platform: macOS
        script: build_macos_fixed.py
      # 添加新平台...
```

### 添加构建步骤

```yaml
# 在构建前添加额外步骤
- name: 运行额外测试
  run: python additional_tests.py

- name: 生成文档
  run: python generate_docs.py
```

## 🚨 故障排除

### 常见问题

#### 1. 推送失败

```bash
# 检查远程仓库配置
git remote -v

# 重新设置远程仓库
git remote set-url origin https://github.com/你的用户名/目录文件生成器.git
```

#### 2. 构建失败

1. 检查 "Actions" 页面的错误日志
2. 运行本地测试：`python test_build_scripts.py`
3. 检查依赖是否正确安装

#### 3. 权限问题

确保你有仓库的写入权限，或者使用个人访问令牌。

### 获取帮助

1. 查看GitHub Actions文档
2. 检查项目的Issues页面
3. 运行本地诊断：`python fix_packaging_issues.py`

## 📈 最佳实践

### 开发流程

1. **本地开发** → 修改代码
2. **本地测试** → `python test_build_scripts.py`
3. **提交代码** → `python commit_and_deploy.py "描述更改"`
4. **检查构建** → 查看GitHub Actions状态
5. **发布版本** → `python commit_and_deploy.py v1.x.x`

### 提交信息规范

使用清晰的提交信息：

```bash
# 好的示例
python commit_and_deploy.py "🐛 修复Windows下文件路径问题"
python commit_and_deploy.py "✨ 添加JSON导出功能"
python commit_and_deploy.py "📚 更新用户文档"
python commit_and_deploy.py "🚀 优化构建性能"

# 避免的示例
python commit_and_deploy.py "修改"
python commit_and_deploy.py "更新代码"
```

### 版本发布策略

- **每周发布** - 小的改进和bug修复
- **每月发布** - 新功能和重要更新
- **按需发布** - 紧急修复

## 🎉 完成部署

恭喜！你已经成功设置了自动化部署流程。现在你可以：

- ✅ 自动构建跨平台可执行文件
- ✅ 自动创建GitHub Releases
- ✅ 监控构建状态
- ✅ 轻松发布新版本

开始享受自动化带来的便利吧！🚀