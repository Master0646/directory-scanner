# 目录扫描器开发工具
# 使用 make <命令> 执行常用操作

.PHONY: run debug test clean install build help

# 默认目标
help:
	@echo "🛠️  目录扫描器开发工具"
	@echo "可用命令:"
	@echo "  make run     - 🚀 直接运行程序"
	@echo "  make debug   - 🐛 调试模式运行"
	@echo "  make test    - 🧪 运行测试"
	@echo "  make install - 📦 安装依赖"
	@echo "  make build   - 🔨 快速构建"
	@echo "  make clean   - 🧹 清理文件"
	@echo "  make format  - 🎨 格式化代码"

# 直接运行
run:
	@echo "🚀 启动目录扫描器..."
	python directory_scanner.py

# 调试模式
debug:
	@echo "🐛 调试模式启动..."
	python debug_launcher.py

# 快速测试
test:
	@echo "🧪 运行快速测试..."
	python quick_debug.py

# 安装依赖
install:
	@echo "📦 安装依赖..."
	pip install -r requirements.txt

# 快速构建
build:
	@echo "🔨 快速构建..."
	python build_macos_optimized.py

# 清理文件
clean:
	@echo "🧹 清理构建文件..."
	rm -rf build/ dist/ *.spec __pycache__/ *.pyc
	@echo "✅ 清理完成"

# 格式化代码（如果安装了black）
format:
	@echo "🎨 格式化代码..."
	@if command -v black >/dev/null 2>&1; then 		black *.py; 	else 		echo "⚠️  black未安装，跳过格式化"; 	fi

# 完整开发环境检查
check:
	@echo "🔍 检查开发环境..."
	python setup_dev.py
