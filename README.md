# 🗂️ 目录文件生成器

[![构建状态](https://github.com/用户名/目录文件生成器/workflows/🚀%20跨平台自动构建/badge.svg)](https://github.com/用户名/目录文件生成器/actions)
[![最新发布](https://img.shields.io/github/v/release/用户名/目录文件生成器)](https://github.com/用户名/目录文件生成器/releases/latest)
[![下载量](https://img.shields.io/github/downloads/用户名/目录文件生成器/total)](https://github.com/用户名/目录文件生成器/releases)
[![许可证](https://img.shields.io/github/license/用户名/目录文件生成器)](LICENSE)

一个功能强大、简单易用的目录文件扫描工具，支持扫描指定目录下的所有文件和文件夹，并可以导出为Excel或CSV格式。

## 📥 快速下载

**无需安装Python环境，直接下载可执行文件：**

| 平台 | 下载链接 | 说明 |
|------|----------|------|
| 🪟 Windows | [下载 .exe](https://github.com/用户名/目录文件生成器/releases/latest/download/目录文件生成器-Windows-x64.exe) | 双击即可运行 |
| 🍎 macOS | [下载 .app.zip](https://github.com/用户名/目录文件生成器/releases/latest/download/目录文件生成器-macOS-Universal.app.zip) | 解压后拖入应用程序文件夹 |
| 🐧 Linux | [下载 .tar.gz](https://github.com/用户名/目录文件生成器/releases/latest/download/目录文件生成器-Linux-x64.tar.gz) | 解压后运行可执行文件 |

> 💡 **提示**: 点击上方链接直接下载最新版本，或访问 [Releases 页面](https://github.com/用户名/目录文件生成器/releases) 查看所有版本。

## 功能特性

- 🔍 **目录扫描**：递归扫描指定目录下的所有文件和文件夹
- 📊 **可视化显示**：以树形结构显示目录结构
- 📁 **详细信息**：显示文件类型、大小、修改时间等信息
- 📤 **多格式导出**：支持导出为Excel (.xlsx) 和CSV (.csv) 格式
- 🖥️ **跨平台支持**：支持Windows和Mac系统
- 🎯 **用户友好**：简洁直观的图形界面，无需技术背景

## 系统要求

- Python 3.7 或更高版本
- 支持的操作系统：Windows 7+, macOS 10.12+

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行程序

```bash
python directory_scanner.py
```

## 使用方法

1. **选择目录**：点击"浏览"按钮选择要扫描的目录
2. **开始扫描**：点击"开始扫描"按钮开始扫描选定的目录
3. **查看结果**：扫描完成后，在结果区域查看目录树结构
4. **导出数据**：点击"导出为Excel"或"导出为CSV"按钮保存扫描结果

## 🔨 开发者构建

如果你想从源码构建应用程序，我们提供了完整的构建工具链：

### 快速构建

```bash
# 1. 克隆仓库
git clone https://github.com/用户名/目录文件生成器.git
cd 目录文件生成器

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行测试
python test_build_scripts.py

# 4. 选择平台构建
# macOS:
python build_macos_fixed.py

# Windows:
python build_windows_fixed.py

# 跨平台:
python cross_platform_build.py
```

### 构建工具说明

| 脚本 | 用途 | 推荐指数 |
|------|------|----------|
| `build_macos_fixed.py` | macOS优化构建 | ⭐⭐⭐⭐⭐ |
| `build_windows_fixed.py` | Windows优化构建 | ⭐⭐⭐⭐⭐ |
| `cross_platform_build.py` | 跨平台自动化构建 | ⭐⭐⭐⭐ |
| `test_build_scripts.py` | 构建环境测试 | ⭐⭐⭐⭐ |
| `fix_packaging_issues.py` | 问题诊断修复 | ⭐⭐⭐⭐ |

### 详细文档

- 📖 [构建指南](BUILD_GUIDE.md) - 完整的构建说明
- 🧪 [测试指南](TESTING_GUIDE.md) - 测试流程说明
- 🚀 [发布指南](RELEASE_GUIDE.md) - 自动化发布流程

## 输出格式说明

### Excel/CSV文件包含以下列：

- **路径**：文件或文件夹的相对路径
- **名称**：文件或文件夹名称
- **类型**：文件或文件夹
- **大小**：文件大小（文件夹显示为"-"）
- **修改时间**：最后修改时间

## 注意事项

1. 扫描大型目录可能需要较长时间，请耐心等待
2. 某些系统文件夹可能因权限限制无法访问
3. 导出的CSV文件使用UTF-8编码，确保中文字符正确显示
4. 建议在扫描前关闭其他占用大量系统资源的程序

## 故障排除

### 常见问题

1. **程序无法启动**
   - 检查Python版本是否为3.7+
   - 确认已安装所有依赖包

2. **扫描失败**
   - 检查目录路径是否正确
   - 确认对目标目录有读取权限

3. **导出失败**
   - 检查目标保存路径是否有写入权限
   - 确认文件名不包含特殊字符

## 技术支持

如遇到问题，请检查以下内容：
- Python版本兼容性
- 依赖包是否正确安装
- 系统权限设置

## 🔄 自动化构建

本项目使用GitHub Actions实现自动化构建和发布：

- ✅ **持续集成**: 每次代码提交自动运行测试
- 🔨 **跨平台构建**: 自动构建Windows、macOS、Linux版本
- 📦 **自动发布**: 标签推送时自动创建Release
- 🧪 **质量保证**: 构建前自动运行完整测试套件

## 📊 项目统计

- 🛠️ **构建脚本**: 6个专用构建脚本
- 🧪 **测试工具**: 3个测试和诊断工具
- 📚 **文档**: 4个详细指南文档
- 🌍 **平台支持**: Windows、macOS、Linux
- 🔧 **开发工具**: 5个开发调试脚本

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢所有贡献者的支持
- 感谢开源社区提供的优秀工具和库

## 📞 联系我们

- 🐛 [报告问题](https://github.com/Master0646/目录文件生成器/issues)
- 💡 [功能建议](https://github.com/Master0646/目录文件生成器/issues/new?template=feature_request.md)
- 📧 [联系邮箱](mailto:15047831679@126.com)

---

⭐ 如果这个项目对你有帮助，请给我们一个星标！