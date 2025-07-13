# 🐳 Docker Windows 构建指南

使用 Docker 构建真正可用的 Windows 可执行文件

## 📋 概述

本项目提供了完整的 Docker 解决方案，可以在真实的 Windows 容器环境中构建可执行文件，解决了跨平台编译的兼容性问题。

## 🚀 快速开始

### 方法 1: 一键构建 (推荐)

```bash
python build_with_docker.py
```

这个脚本会自动:
- ✅ 检查 Docker 环境
- ✅ 构建 Windows 容器镜像
- ✅ 运行构建过程
- ✅ 输出可执行文件到 `dist/` 目录

### 方法 2: 手动构建

```bash
# 1. 构建 Docker 镜像
docker build -f Dockerfile.windows -t directory-scanner-windows .

# 2. 运行构建容器
docker run --rm -v ${PWD}/dist:/app/dist directory-scanner-windows
```

### 方法 3: 使用 Docker Compose

```bash
# 构建并运行
docker-compose -f docker-compose.windows.yml up --build

# 清理资源
docker-compose -f docker-compose.windows.yml down --rmi all
```

## 🔧 前置要求

### Windows 系统

1. **安装 Docker Desktop**:
   - 下载: [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
   - 安装并启动 Docker Desktop

2. **切换到 Windows 容器**:
   - 右键 Docker Desktop 系统托盘图标
   - 选择 "Switch to Windows containers"
   - 等待切换完成

3. **验证环境**:
   ```cmd
   docker --version
   docker system info
   ```

### macOS/Linux 系统

**注意**: macOS 和 Linux 无法直接运行 Windows 容器。需要以下方案之一:

1. **远程 Windows Docker 主机**
2. **GitHub Actions** (推荐)
3. **Windows 虚拟机**

## 📁 文件结构

```
├── Dockerfile.windows          # Windows 容器构建文件
├── build_windows_docker.py     # 容器内构建脚本
├── docker-compose.windows.yml  # Docker Compose 配置
├── build_with_docker.py        # 本地 Docker 管理脚本
└── dist/                       # 输出目录
    └── 目录扫描器.exe          # 生成的可执行文件
```

## 🔍 构建过程详解

### 1. Docker 镜像构建

基于 `mcr.microsoft.com/windows/servercore:ltsc2022`:
- 📦 安装 Python 3.11.7
- 📦 安装 PyInstaller 和依赖
- 📦 复制项目文件
- 📦 配置构建环境

### 2. 容器构建过程

在 Windows 容器中执行:
- 🔍 环境检查
- 🧹 清理构建目录
- 📝 创建版本信息
- 🔨 PyInstaller 打包
- ✅ 验证输出文件

### 3. 输出结果

- 📁 位置: `dist/目录扫描器.exe`
- 📏 大小: ~30-35 MB
- 🎯 兼容性: Windows 7+ (x64)
- 🔒 签名: 未签名 (正常现象)

## 🛠️ 故障排除

### 常见问题

#### 1. Docker 未安装或未运行

```
❌ Docker 未安装或无法访问
```

**解决方案**:
- 安装 Docker Desktop
- 启动 Docker 服务
- 检查 Docker 是否在 PATH 中

#### 2. 容器模式错误

```
❌ Docker 当前为 linux 容器模式
```

**解决方案**:
- 右键 Docker Desktop 图标
- 选择 "Switch to Windows containers"
- 等待切换完成

#### 3. 内存不足

```
❌ 构建过程中内存不足
```

**解决方案**:
- 增加 Docker 内存限制 (推荐 4GB+)
- 关闭其他占用内存的应用
- 清理 Docker 缓存: `docker system prune`

#### 4. 网络连接问题

```
❌ 无法下载 Python 安装包
```

**解决方案**:
- 检查网络连接
- 配置 Docker 代理设置
- 使用国内镜像源

### 调试技巧

#### 1. 查看详细日志

```bash
# 构建时显示详细输出
docker build -f Dockerfile.windows -t directory-scanner-windows . --progress=plain
```

#### 2. 进入容器调试

```bash
# 交互式运行容器
docker run -it --rm directory-scanner-windows cmd
```

#### 3. 检查容器状态

```bash
# 查看运行中的容器
docker ps

# 查看容器日志
docker logs <container_id>
```

## 🔧 高级配置

### 自定义构建参数

编辑 `build_windows_docker.py` 中的 PyInstaller 参数:

```python
cmd = [
    'pyinstaller',
    '--onefile',
    '--windowed',
    '--name=目录扫描器',
    # 添加自定义参数
    '--add-data', 'custom_file.txt;.',
    '--hidden-import', 'custom_module',
    'directory_scanner.py'
]
```

### 优化镜像大小

在 `Dockerfile.windows` 中添加清理步骤:

```dockerfile
# 清理缓存
RUN pip cache purge && \
    del /q /s %TEMP%\* && \
    del /q /s %LOCALAPPDATA%\pip\cache\*
```

### 多阶段构建

```dockerfile
# 构建阶段
FROM mcr.microsoft.com/windows/servercore:ltsc2022 AS builder
# ... 构建步骤 ...

# 运行阶段
FROM mcr.microsoft.com/windows/nanoserver:ltsc2022
COPY --from=builder C:\\app\\dist C:\\app
```

## 📊 性能对比

| 构建方法 | 构建时间 | 文件大小 | 兼容性 | 难度 |
|---------|---------|---------|--------|------|
| Docker | 10-15分钟 | ~32MB | 完美 | 中等 |
| GitHub Actions | 5-10分钟 | ~32MB | 完美 | 简单 |
| 本地 macOS | 2-3分钟 | ~32MB | 不兼容 | 简单 |
| Windows VM | 3-5分钟 | ~32MB | 完美 | 复杂 |

## 🔗 相关资源

- 📖 [Windows 兼容性指南](WINDOWS_COMPATIBILITY_GUIDE.md)
- 🚀 [GitHub Actions 构建](.github/workflows/build.yml)
- 🛠️ [构建脚本说明](BUILD_GUIDE.md)
- 🐳 [Docker 官方文档](https://docs.docker.com/)
- 📦 [PyInstaller 文档](https://pyinstaller.readthedocs.io/)

## 💡 最佳实践

1. **优先使用 GitHub Actions**: 最简单可靠
2. **Docker 作为备选**: 需要本地 Windows 环境
3. **定期清理**: 避免磁盘空间不足
4. **版本固定**: 确保构建一致性
5. **测试验证**: 在真实 Windows 系统上测试

## 🆘 获取帮助

如果遇到问题:

1. 📖 查看 [故障排除](#故障排除) 部分
2. 🔍 检查 [GitHub Issues](https://github.com/Master0646/directory-scanner/issues)
3. 📧 提交新的 Issue 描述问题
4. 💬 在项目讨论区寻求帮助

---

**注意**: Docker Windows 容器需要 Windows 10/11 或 Windows Server 2016+ 系统支持。