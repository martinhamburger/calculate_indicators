#!/bin/bash
# 自动创建新仓库的脚本
# 用于将图片工具从 calculate_indicators 独立出来

set -e

REPO_NAME="wechat-image-tools"
REPO_DESC="公众号图片工具 - 网页截图和PDF处理"
SOURCE_DIR="../calculate_indicators"

echo "================================================"
echo "  创建新仓库: $REPO_NAME"
echo "================================================"

# 检查源目录
if [ ! -d "$SOURCE_DIR" ]; then
    echo "❌ 错误: 找不到源目录 $SOURCE_DIR"
    exit 1
fi

# 创建新目录
echo "📁 创建新目录: $REPO_NAME"
mkdir -p "$REPO_NAME"
cd "$REPO_NAME"

# 初始化 Git
echo "🔧 初始化 Git 仓库"
git init

# 复制核心文件
echo "📋 复制核心文件..."
cp -r "$SOURCE_DIR/image_tools" ./ 2>/dev/null || echo "  ⚠️  image_tools 目录不存在"
cp "$SOURCE_DIR/image_cli.py" ./ 2>/dev/null || echo "  ⚠️  image_cli.py 不存在"
cp "$SOURCE_DIR/demo_image_tools.py" ./ 2>/dev/null || echo "  ⚠️  demo_image_tools.py 不存在"
cp "$SOURCE_DIR/requirements_image.txt" ./requirements.txt 2>/dev/null || echo "  ⚠️  requirements_image.txt 不存在"
cp "$SOURCE_DIR/.gitignore" ./ 2>/dev/null || echo "  ⚠️  .gitignore 不存在"

# 创建 README.md
echo "📝 创建 README.md"
cat > README.md << 'EOF'
# 公众号图片工具 (WeChat Image Tools)

专为公众号内容创作设计的图片处理工具，支持网页截图和 PDF 处理。

## ✨ 功能特点

- 🌐 **网页截图**：支持全页面、可见区域、特定元素截图
- 📄 **PDF 处理**：PDF 转图片、提取 PDF 中的图片
- 🎯 **批量处理**：支持批量截图和转换
- 💻 **双接口**：命令行工具和 Python API
- 🔧 **灵活配置**：自定义 DPI、视口大小、输出格式

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/wechat-image-tools.git
cd wechat-image-tools

# 安装依赖
pip install -r requirements.txt

# 安装浏览器（用于网页截图）
playwright install chromium
```

### 命令行使用

```bash
# 网页截图
python image_cli.py screenshot https://example.com -o screenshot.png

# 截取整个页面
python image_cli.py screenshot https://example.com -o fullpage.png --full-page

# PDF 转图片
python image_cli.py pdf-to-image document.pdf -o ./pages --dpi 300

# 从 PDF 提取图片
python image_cli.py extract-images document.pdf -o ./images

# 批量截图
python image_cli.py screenshot-batch https://example.com https://github.com -o ./screenshots
```

### Python API 使用

```python
from image_tools import WebScreenshot, PDFExtractor

# 网页截图
with WebScreenshot() as screenshot:
    screenshot.capture(
        url="https://example.com",
        output_path="screenshot.png",
        full_page=True
    )

# PDF 处理
extractor = PDFExtractor()
extractor.pages_to_images(
    pdf_path="document.pdf",
    output_folder="./pages",
    dpi=150
)
```

## 📖 文档

- [详细使用指南](https://github.com/YOUR_USERNAME/wechat-image-tools)
- [API 文档](https://github.com/YOUR_USERNAME/wechat-image-tools)
- [常见问题](https://github.com/YOUR_USERNAME/wechat-image-tools)

## 🛠️ 技术栈

- [Playwright](https://playwright.dev/) - 现代化网页自动化
- [PyMuPDF](https://pymupdf.readthedocs.io/) - 高性能 PDF 处理
- Python 3.8+

## 📋 依赖

```
playwright>=1.40.0
PyMuPDF>=1.23.0
Pillow>=10.0.0
```

## 💡 使用场景

1. **公众号配图**：从网页截取内容作为配图
2. **文档处理**：将 PDF 报告转为图片
3. **批量处理**：批量截取多个网页或处理多个 PDF
4. **自动化**：集成到内容创作工作流

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

本项目基于以下优秀的开源项目：
- [Playwright](https://github.com/microsoft/playwright)
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF)

---

如有问题或建议，欢迎提 Issue！
EOF

# 创建 LICENSE
echo "📜 创建 LICENSE"
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# 创建 .gitignore（如果不存在）
if [ ! -f .gitignore ]; then
    echo "🚫 创建 .gitignore"
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Test outputs
screenshots/
pages/
images/
demo_output/
output/
*.log
EOF
fi

# 创建目录结构
echo "📂 创建目录结构"
mkdir -p examples tests docs

# 创建示例文件
echo "📝 创建示例文件"
cat > examples/screenshot_example.py << 'EOF'
"""网页截图示例"""
from image_tools import WebScreenshot

def main():
    with WebScreenshot() as screenshot:
        # 基本截图
        screenshot.capture(
            url="https://example.com",
            output_path="example.png"
        )
        
        # 手机视口
        screenshot.capture(
            url="https://example.com",
            output_path="mobile.png",
            viewport_width=390,
            viewport_height=844
        )

if __name__ == "__main__":
    main()
EOF

cat > examples/pdf_example.py << 'EOF'
"""PDF 处理示例"""
from image_tools import PDFExtractor

def main():
    extractor = PDFExtractor()
    
    # PDF 转图片
    extractor.pages_to_images(
        pdf_path="document.pdf",
        output_folder="./pages",
        dpi=150
    )
    
    # 提取图片
    extractor.extract_images(
        pdf_path="document.pdf",
        output_folder="./images"
    )

if __name__ == "__main__":
    main()
EOF

# 初始提交
echo "💾 创建初始提交"
git add .
git commit -m "Initial commit: WeChat Image Tools

Features:
- Web page screenshot using Playwright
- PDF processing using PyMuPDF
- Command-line interface
- Python API
- Demo scripts and documentation"

# 显示下一步操作
echo ""
echo "================================================"
echo "  ✅ 新仓库创建成功！"
echo "================================================"
echo ""
echo "📍 位置: $(pwd)"
echo ""
echo "🎯 下一步操作："
echo ""
echo "1. 在 GitHub 上创建新仓库："
echo "   https://github.com/new"
echo ""
echo "2. 连接到远程仓库："
echo "   cd $REPO_NAME"
echo "   git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
echo ""
echo "3. 推送到 GitHub："
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "================================================"
