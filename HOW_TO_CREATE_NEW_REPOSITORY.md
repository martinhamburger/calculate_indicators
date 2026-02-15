# 如何创建新的 GitHub 仓库

## 重要说明

当前的图片工具功能已经在 `calculate_indicators` 仓库中实现。如果您希望将图片工具独立为一个新的仓库，请按照以下步骤操作。

## 方案一：通过 GitHub 网页创建新仓库

### 1. 在 GitHub 上创建新仓库

1. 登录 GitHub (https://github.com)
2. 点击右上角的 "+" 按钮
3. 选择 "New repository"
4. 填写仓库信息：
   - **Repository name**: 例如 `wechat-image-tools` 或 `image-tools`
   - **Description**: "公众号图片工具 - 网页截图和 PDF 处理"
   - **Public/Private**: 选择公开或私有
   - **Initialize with README**: 可选
5. 点击 "Create repository"

### 2. 复制图片工具文件到新仓库

```bash
# 创建新的本地目录
mkdir wechat-image-tools
cd wechat-image-tools

# 初始化 Git
git init

# 连接到你的新仓库（替换为你的仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/wechat-image-tools.git

# 从当前仓库复制相关文件
# 假设你在 calculate_indicators 目录的上一级
cp -r ../calculate_indicators/image_tools ./
cp ../calculate_indicators/image_cli.py ./
cp ../calculate_indicators/demo_image_tools.py ./
cp ../calculate_indicators/requirements_image.txt ./requirements.txt
cp ../calculate_indicators/IMAGE_TOOLS_README.md ./README.md
cp ../calculate_indicators/IMAGE_INSERTION_FEASIBILITY.md ./
cp ../calculate_indicators/.gitignore ./

# 创建初始提交
git add .
git commit -m "Initial commit: WeChat image tools"

# 推送到 GitHub
git branch -M main
git push -u origin main
```

## 方案二：使用 GitHub CLI

如果你安装了 GitHub CLI (`gh`)：

```bash
# 创建新仓库
gh repo create wechat-image-tools --public --description "公众号图片工具"

# 克隆新仓库
gh repo clone YOUR_USERNAME/wechat-image-tools
cd wechat-image-tools

# 复制文件（同上）
```

## 方案三：Fork 并修改当前仓库

如果你想基于当前仓库创建新的独立项目：

```bash
# 在 GitHub 上 Fork martinhamburger/calculate_indicators

# 克隆你的 fork
git clone https://github.com/YOUR_USERNAME/calculate_indicators.git
cd calculate_indicators

# 删除不需要的财务计算功能，只保留图片工具
# 重命名仓库（在 GitHub 设置中）
```

## 推荐的新仓库结构

```
wechat-image-tools/
├── README.md                    # 主要文档
├── requirements.txt             # 依赖列表
├── .gitignore                   # Git 忽略文件
├── LICENSE                      # 许可证
├── image_tools/                 # 核心模块
│   ├── __init__.py
│   ├── screenshot.py
│   └── pdf_extractor.py
├── image_cli.py                 # 命令行工具
├── demo_image_tools.py          # 示例脚本
├── examples/                    # 示例目录（新增）
│   ├── screenshot_example.py
│   └── pdf_example.py
├── tests/                       # 测试目录（新增）
│   ├── test_screenshot.py
│   └── test_pdf_extractor.py
└── docs/                        # 文档目录（新增）
    ├── installation.md
    ├── usage.md
    └── api.md
```

## 新仓库的 README.md 模板

```markdown
# 公众号图片工具 (WeChat Image Tools)

专为公众号内容创作设计的图片处理工具，支持网页截图和 PDF 处理。

## 功能特点

- 🌐 网页截图：支持全页面、可见区域、特定元素截图
- 📄 PDF 处理：PDF 转图片、提取 PDF 中的图片
- 🎯 批量处理：支持批量截图和转换
- 💻 双接口：命令行工具和 Python API
- 🔧 灵活配置：自定义 DPI、视口大小、输出格式

## 快速开始

### 安装

\`\`\`bash
pip install -r requirements.txt
playwright install chromium
\`\`\`

### 使用

**命令行：**
\`\`\`bash
# 网页截图
python image_cli.py screenshot https://example.com -o screenshot.png

# PDF 转图片
python image_cli.py pdf-to-image document.pdf -o ./pages
\`\`\`

**Python API：**
\`\`\`python
from image_tools import WebScreenshot, PDFExtractor

# 网页截图
with WebScreenshot() as screenshot:
    screenshot.capture("https://example.com", "screenshot.png")

# PDF 处理
extractor = PDFExtractor()
extractor.pages_to_images("document.pdf", "./pages")
\`\`\`

## 文档

- [安装指南](docs/installation.md)
- [使用说明](docs/usage.md)
- [API 文档](docs/api.md)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
\`\`\`

## 新仓库的 requirements.txt

```
# 网页截图
playwright>=1.40.0

# PDF 处理
PyMuPDF>=1.23.0

# 图片处理
Pillow>=10.0.0
```

## 后续步骤

创建新仓库后，你可以：

1. **添加 CI/CD**：设置 GitHub Actions 进行自动测试
2. **发布到 PyPI**：让用户可以通过 `pip install wechat-image-tools` 安装
3. **添加测试**：使用 pytest 编写单元测试
4. **完善文档**：使用 Sphinx 或 MkDocs 生成文档网站
5. **添加示例**：创建更多使用示例

## 为什么要创建新仓库？

将图片工具独立为新仓库的优点：

- ✅ 专注于单一功能
- ✅ 更容易维护和更新
- ✅ 用户可以单独安装使用
- ✅ 可以独立发版本
- ✅ 更清晰的项目定位

## 需要帮助？

如果你在创建新仓库时遇到问题：

1. 参考 [GitHub 文档](https://docs.github.com/cn/repositories/creating-and-managing-repositories/creating-a-new-repository)
2. 查看 [Git 教程](https://git-scm.com/book/zh/v2)
3. 在原仓库提出 Issue

## 注意事项

- 创建新仓库后，记得更新所有文档中的仓库链接
- 如果要保留 Git 历史，使用 `git filter-branch` 或 `git subtree`
- 确保新仓库有适当的 LICENSE 文件
- 考虑添加 CODE_OF_CONDUCT.md 和 CONTRIBUTING.md

## 自动化脚本

我们提供了一个自动化脚本来帮助你创建新仓库：

```bash
#!/bin/bash
# create_new_repo.sh

REPO_NAME="wechat-image-tools"
REPO_DESC="公众号图片工具 - 网页截图和PDF处理"

# 创建新目录
mkdir $REPO_NAME
cd $REPO_NAME

# 初始化 Git
git init

# 复制文件
cp -r ../calculate_indicators/image_tools ./
cp ../calculate_indicators/image_cli.py ./
cp ../calculate_indicators/demo_image_tools.py ./
cp ../calculate_indicators/requirements_image.txt ./requirements.txt
cp ../calculate_indicators/IMAGE_TOOLS_README.md ./README.md
cp ../calculate_indicators/IMAGE_INSERTION_FEASIBILITY.md ./FEASIBILITY.md
cp ../calculate_indicators/.gitignore ./

# 创建新文件
echo "# $REPO_NAME" > README_NEW.md
echo "$REPO_DESC" >> README_NEW.md
cat README.md >> README_NEW.md
mv README_NEW.md README.md

# 创建 LICENSE
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

# 初始提交
git add .
git commit -m "Initial commit: WeChat Image Tools

Features:
- Web page screenshot using Playwright
- PDF processing using PyMuPDF
- Command-line interface
- Python API
- Demo scripts and documentation"

echo "✅ 新仓库已准备完毕！"
echo "下一步："
echo "1. 在 GitHub 上创建新仓库"
echo "2. 运行: git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
echo "3. 运行: git push -u origin main"
```

保存为 `create_new_repo.sh`，然后运行：

```bash
chmod +x create_new_repo.sh
./create_new_repo.sh
```

## 总结

创建新仓库是一个简单的过程，只需要：
1. 在 GitHub 上创建新仓库
2. 复制相关文件
3. 提交并推送

如果你需要更详细的帮助，请告诉我具体遇到了什么问题！
