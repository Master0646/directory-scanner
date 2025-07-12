# 目录文件扫描器

一个简单易用的目录文件扫描工具，支持扫描指定目录下的所有文件和文件夹，并可以导出为Excel或CSV格式。

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

## 打包为可执行文件

### Windows系统

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包为单个可执行文件
pyinstaller --onefile --windowed --name="目录扫描器" directory_scanner.py

# 可执行文件将生成在 dist/ 目录下
```

### Mac系统

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包为Mac应用程序
pyinstaller --onefile --windowed --name="目录扫描器" directory_scanner.py

# 应用程序将生成在 dist/ 目录下
```

### 高级打包选项

如果需要添加图标或其他资源：

```bash
# Windows (需要准备icon.ico文件)
pyinstaller --onefile --windowed --icon=icon.ico --name="目录扫描器" directory_scanner.py

# Mac (需要准备icon.icns文件)
pyinstaller --onefile --windowed --icon=icon.icns --name="目录扫描器" directory_scanner.py
```

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

## 版本历史

- v1.0 - 初始版本
  - 基本目录扫描功能
  - Excel和CSV导出
  - 跨平台GUI界面