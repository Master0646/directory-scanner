
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
