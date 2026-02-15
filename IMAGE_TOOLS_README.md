# 公众号图片工具使用指南

## 简介

这是一个专为公众号内容创作设计的图片工具，提供网页截图和 PDF 处理功能。

## 安装

### 1. 安装 Python 依赖

```bash
pip install -r requirements_image.txt
```

### 2. 安装浏览器（用于网页截图）

```bash
playwright install chromium
```

## 快速开始

### 网页截图

#### 基本用法

```bash
# 截取整个网页
python image_cli.py screenshot https://example.com -o screenshot.png

# 仅截取可见区域
python image_cli.py screenshot https://example.com -o viewport.png --viewport-only

# 等待页面加载完成
python image_cli.py screenshot https://example.com -o page.png --wait 3

# 等待特定元素出现
python image_cli.py screenshot https://example.com -o page.png --wait-selector ".content"
```

#### 自定义视口大小

```bash
# 手机视口（iPhone 12）
python image_cli.py screenshot https://example.com -o mobile.png --width 390 --height 844

# 平板视口（iPad）
python image_cli.py screenshot https://example.com -o tablet.png --width 768 --height 1024

# 桌面视口（全高清）
python image_cli.py screenshot https://example.com -o desktop.png --width 1920 --height 1080
```

#### 批量截图

```bash
# 截取多个网页
python image_cli.py screenshot-batch https://example.com https://github.com -o ./screenshots
```

### PDF 处理

#### PDF 转图片

```bash
# 基本用法（默认 150 DPI）
python image_cli.py pdf-to-image document.pdf -o ./pages

# 高清输出（300 DPI）
python image_cli.py pdf-to-image document.pdf -o ./pages --dpi 300

# 输出 JPG 格式
python image_cli.py pdf-to-image document.pdf -o ./pages --format jpg

# 转换指定页面
python image_cli.py pdf-to-image document.pdf -o ./pages --pages 1-5
```

#### 从 PDF 提取图片

```bash
# 基本用法
python image_cli.py extract-images document.pdf -o ./images

# 只提取大图（过滤小图标）
python image_cli.py extract-images document.pdf -o ./images --min-width 200 --min-height 200
```

#### 查看 PDF 信息

```bash
python image_cli.py pdf-info document.pdf
```

## Python API 使用

### 网页截图

```python
from image_tools import WebScreenshot

# 方法 1: 使用上下文管理器
with WebScreenshot() as screenshot:
    screenshot.capture(
        url="https://example.com",
        output_path="screenshot.png",
        full_page=True
    )

# 方法 2: 使用便捷函数
from image_tools.screenshot import screenshot_url

screenshot_url("https://example.com", "screenshot.png")

# 方法 3: 批量截图
with WebScreenshot() as screenshot:
    urls = [
        "https://example.com",
        "https://github.com",
    ]
    screenshot.capture_batch(urls, "./screenshots")

# 方法 4: 截取特定元素
with WebScreenshot() as screenshot:
    screenshot.capture_element(
        url="https://example.com",
        selector=".main-content",
        output_path="element.png"
    )
```

### PDF 处理

```python
from image_tools import PDFExtractor

# 创建提取器
extractor = PDFExtractor()

# PDF 转图片
image_paths = extractor.pages_to_images(
    pdf_path="document.pdf",
    output_folder="./pages",
    dpi=150
)

# 提取 PDF 中的图片
images = extractor.extract_images(
    pdf_path="document.pdf",
    output_folder="./images",
    min_width=100,
    min_height=100
)

# 获取 PDF 信息
info = extractor.get_pdf_info("document.pdf")
print(f"总页数: {info['pages']}")
print(f"总图片数: {info['total_images']}")

# 转换指定页面范围
extractor.convert_page_range(
    pdf_path="document.pdf",
    output_folder="./pages",
    start_page=1,  # 从第 1 页开始
    end_page=5,    # 到第 5 页结束
    dpi=300
)
```

## 常见使用场景

### 场景 1: 公众号文章配图

从网页截取内容作为配图：

```bash
# 截取新闻页面
python image_cli.py screenshot https://news.example.com/article -o article.png --full-page

# 截取图表
python image_cli.py screenshot https://charts.example.com -o chart.png --width 800 --height 600
```

### 场景 2: 从 PDF 报告提取图表

```bash
# 将 PDF 报告的每一页转为图片
python image_cli.py pdf-to-image report.pdf -o ./report_pages --dpi 300

# 提取 PDF 中的图表
python image_cli.py extract-images report.pdf -o ./charts --min-width 300 --min-height 200
```

### 场景 3: 批量处理多个来源

```python
from image_tools import WebScreenshot, PDFExtractor

# 截取网页
with WebScreenshot() as screenshot:
    screenshot.capture("https://example.com", "web_source.png")

# 处理 PDF
extractor = PDFExtractor()
extractor.pages_to_images("document.pdf", "./pdf_pages", dpi=150)
```

## 参数说明

### 网页截图参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | 目标网址 | - |
| `output_path` | 输出文件路径 | - |
| `full_page` | 截取整个页面 | `True` |
| `viewport_width` | 视口宽度（像素） | `1920` |
| `viewport_height` | 视口高度（像素） | `1080` |
| `wait_time` | 等待时间（秒） | `0` |
| `wait_for_selector` | 等待特定元素（CSS 选择器） | `None` |

### PDF 处理参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `pdf_path` | PDF 文件路径 | - |
| `output_folder` | 输出文件夹 | - |
| `dpi` | 图片分辨率 | `150` |
| `image_format` | 图片格式（png/jpg） | `png` |
| `min_width` | 最小宽度（提取时） | `100` |
| `min_height` | 最小高度（提取时） | `100` |

### DPI 选择建议

| DPI | 用途 | 文件大小 |
|-----|------|----------|
| 72 | 屏幕显示 | 小 |
| 150 | 一般用途（推荐） | 中等 |
| 300 | 高清打印 | 大 |
| 600 | 专业印刷 | 很大 |

## 常见问题

### Q1: 网页截图显示不完整？

**A:** 尝试增加等待时间或等待特定元素：

```bash
python image_cli.py screenshot https://example.com -o page.png --wait 5
```

### Q2: PDF 转图片不清晰？

**A:** 提高 DPI 设置：

```bash
python image_cli.py pdf-to-image document.pdf -o ./pages --dpi 300
```

### Q3: 提取的 PDF 图片太多？

**A:** 设置更大的最小尺寸来过滤小图：

```bash
python image_cli.py extract-images document.pdf -o ./images --min-width 300 --min-height 300
```

### Q4: 如何截取移动端网页？

**A:** 设置移动端视口大小：

```bash
python image_cli.py screenshot https://example.com -o mobile.png --width 390 --height 844
```

### Q5: 网页截图时浏览器报错？

**A:** 确保已安装浏览器引擎：

```bash
playwright install chromium
```

## 高级用法

### 自定义 Python 脚本

```python
from image_tools import WebScreenshot, PDFExtractor
import os

def process_content_sources(web_urls, pdf_files, output_folder):
    """处理多种内容来源"""
    os.makedirs(output_folder, exist_ok=True)
    
    # 处理网页
    with WebScreenshot() as screenshot:
        for i, url in enumerate(web_urls, 1):
            output_path = f"{output_folder}/web_{i}.png"
            screenshot.capture(url, output_path)
    
    # 处理 PDF
    extractor = PDFExtractor()
    for i, pdf_file in enumerate(pdf_files, 1):
        folder = f"{output_folder}/pdf_{i}"
        extractor.pages_to_images(pdf_file, folder, dpi=150)

# 使用
web_urls = [
    "https://example.com/article1",
    "https://example.com/article2",
]
pdf_files = [
    "report1.pdf",
    "report2.pdf",
]

process_content_sources(web_urls, pdf_files, "./output")
```

## 技术支持

如有问题或建议，请查看：
- [可行性分析文档](./IMAGE_INSERTION_FEASIBILITY.md)
- [Playwright 文档](https://playwright.dev/python/)
- [PyMuPDF 文档](https://pymupdf.readthedocs.io/)

## 许可证

本工具基于开源项目开发：
- Playwright: Apache 2.0 License
- PyMuPDF: GNU AGPL v3 License
