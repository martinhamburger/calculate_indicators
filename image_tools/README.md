# Image Tools for WeChat Public Account Articles

一套用于微信公众号文章图片准备的工具集，支持从PDF提取图片、网页截图和AI图片生成。

## 功能特性

- 📄 **PDF图片提取**：从PDF文档中提取嵌入的图片，或将PDF页面转换为图片
- 🌐 **网页截图**：捕获完整网页或特定元素的截图
- 🎨 **AI图片生成**：使用OpenAI DALL-E生成AI图片
- 🔧 **命令行工具**：提供便捷的CLI接口
- 🐍 **Python API**：可在代码中直接调用

## 安装依赖

### 基础依赖

```bash
pip install PyMuPDF playwright openai pillow requests
```

### Playwright浏览器安装

```bash
playwright install chromium
```

如果需要其他浏览器：
```bash
playwright install firefox
playwright install webkit
```

## 快速开始

### 1. PDF图片提取

#### 命令行使用

```bash
# 提取PDF中所有图片
python -m image_tools.cli extract-pdf document.pdf

# 指定输出目录
python -m image_tools.cli extract-pdf document.pdf -o ./images

# 将PDF页面转换为图片
python -m image_tools.cli extract-pdf document.pdf --page 0 -o page1.png

# 高分辨率输出
python -m image_tools.cli extract-pdf document.pdf --page 0 --dpi 600 -o page1_hd.png
```

#### Python API

```python
from image_tools import PDFExtractor

# 创建提取器
extractor = PDFExtractor('document.pdf')

# 提取所有图片
images = extractor.extract_all_images('./output')
print(f"提取了 {len(images)} 张图片")

# 将页面转换为图片
extractor.extract_page_as_image(0, 'page1.png', dpi=300)

# 获取PDF页数
page_count = extractor.get_page_count()
```

### 2. 网页截图

#### 命令行使用

```bash
# 捕获完整网页
python -m image_tools.cli screenshot https://example.com -o page.png

# 捕获特定元素
python -m image_tools.cli screenshot https://example.com --selector ".article" -o article.png

# 设置视口大小
python -m image_tools.cli screenshot https://example.com --width 1920 --height 1080 -o page.png

# 等待页面加载
python -m image_tools.cli screenshot https://example.com --wait 3 -o page.png

# 使用不同浏览器
python -m image_tools.cli screenshot https://example.com --browser firefox -o page.png
```

#### Python API

```python
from image_tools import WebScreenshot

# 创建截图工具
screenshot = WebScreenshot('https://example.com')

# 捕获完整页面
screenshot.capture('page.png', full_page=True)

# 捕获特定元素
screenshot.capture_element('element.png', selector='.article')

# 设置视口
screenshot.capture('page.png', viewport={'width': 1920, 'height': 1080})

# 批量截图
urls = ['https://site1.com', 'https://site2.com']
screenshots = screenshot.capture_multiple_pages(urls, './screenshots')
```

### 3. AI图片生成

#### 设置API Key

```bash
export OPENAI_API_KEY='your-api-key-here'
```

或在代码中直接传入。

#### 命令行使用

```bash
# 基础生成
python -m image_tools.cli generate "a beautiful sunset over mountains" -o sunset.png

# 使用DALL-E 3高质量模式
python -m image_tools.cli generate "modern office interior" \
  --model dall-e-3 --quality hd --size 1792x1024 -o office.png

# 自动优化提示词
python -m image_tools.cli generate "cat" --optimize -o cat.png

# 生成变体
python -m image_tools.cli variations base_image.png -o ./variations --count 3
```

#### Python API

```python
from image_tools import AIGenerator

# 创建生成器（API key可通过环境变量设置）
generator = AIGenerator()

# 或直接传入API key
generator = AIGenerator(api_key='your-key')

# 生成图片
generator.generate(
    prompt="a beautiful sunset over mountains",
    output_path="sunset.png",
    size="1024x1024",
    quality="standard"
)

# 生成变体
variations = generator.generate_variations(
    base_image_path="base.png",
    output_dir="./variations",
    n=3
)

# 优化提示词
optimized = generator.optimize_prompt("cat")
```

## 命令行工具详细说明

### extract-pdf - PDF图片提取

```bash
python -m image_tools.cli extract-pdf <pdf_file> [options]
```

**选项：**
- `-o, --output`: 输出路径或目录
- `-p, --page`: 提取特定页面为图片（从0开始）
- `--dpi`: 页面转换DPI（默认：300）

### screenshot - 网页截图

```bash
python -m image_tools.cli screenshot <url> [options]
```

**选项：**
- `-o, --output`: 输出文件路径（默认：screenshot.png）
- `--selector`: 捕获特定元素的CSS选择器
- `--full-page`: 捕获完整页面（默认：true）
- `--no-headless`: 显示浏览器窗口
- `--wait`: 捕获前等待时间（秒）
- `--width`: 视口宽度
- `--height`: 视口高度
- `--browser`: 使用的浏览器（chromium/firefox/webkit）

### generate - AI图片生成

```bash
python -m image_tools.cli generate <prompt> [options]
```

**选项：**
- `-o, --output`: 输出文件路径（默认：generated_image.png）
- `--api-key`: API密钥（或设置环境变量）
- `--provider`: AI提供商（目前仅支持openai）
- `--model`: 使用的模型（dall-e-3或dall-e-2）
- `--size`: 图片尺寸（如1024x1024）
- `--quality`: 图片质量（standard或hd）
- `--style`: 图片风格（vivid或natural）
- `--optimize`: 自动优化提示词

### variations - 图片变体生成

```bash
python -m image_tools.cli variations <image_file> [options]
```

**选项：**
- `-o, --output`: 输出目录
- `--count`: 生成数量（默认：3）
- `--size`: 图片尺寸
- `--api-key`: API密钥

## 使用示例

### 场景1：从技术文档提取图表

```bash
# 1. 提取PDF中的所有图片
python -m image_tools.cli extract-pdf technical_doc.pdf -o ./doc_images

# 2. 或者将特定页面转为高清图片
python -m image_tools.cli extract-pdf technical_doc.pdf --page 5 --dpi 600 -o diagram.png
```

### 场景2：截取网页内容

```bash
# 1. 截取整个文章
python -m image_tools.cli screenshot https://blog.example.com/article --wait 2 -o article.png

# 2. 只截取文章主体
python -m image_tools.cli screenshot https://blog.example.com/article --selector "article" -o content.png

# 3. 设置合适的视口尺寸
python -m image_tools.cli screenshot https://blog.example.com --width 1200 --height 800 -o preview.png
```

### 场景3：生成配图

```bash
# 设置API key
export OPENAI_API_KEY='sk-...'

# 1. 生成文章配图
python -m image_tools.cli generate "professional office meeting, modern style" \
  --model dall-e-3 --quality hd -o meeting.png

# 2. 生成多个变体选择最佳
python -m image_tools.cli generate "technology concept illustration" -o base.png
python -m image_tools.cli variations base.png -o ./variants --count 4
```

### 场景4：批量处理（Python脚本）

```python
from image_tools import PDFExtractor, WebScreenshot, AIGenerator

# 批量提取多个PDF
pdfs = ['doc1.pdf', 'doc2.pdf', 'doc3.pdf']
for pdf in pdfs:
    extractor = PDFExtractor(pdf)
    extractor.extract_all_images(f'./output/{pdf[:-4]}')

# 批量截图
urls = ['https://site1.com', 'https://site2.com']
screenshot = WebScreenshot()
screenshot.capture_multiple_pages(urls, './screenshots')

# 批量生成AI图片
generator = AIGenerator()
prompts = [
    "modern technology",
    "business meeting",
    "data analysis"
]
for i, prompt in enumerate(prompts):
    generator.generate(prompt, f'image_{i+1}.png')
```

## 高级功能

### 自定义截图选项

```python
from image_tools import WebScreenshot

screenshot = WebScreenshot(
    browser_type='firefox',  # 使用Firefox
    headless=False  # 显示浏览器窗口用于调试
)

# 等待JavaScript加载
screenshot.capture(
    'dynamic_page.png',
    url='https://example.com',
    wait_time=5000,  # 等待5秒
    full_page=True
)
```

### AI图片生成最佳实践

```python
from image_tools import AIGenerator

generator = AIGenerator(model='dall-e-3')

# 使用详细的提示词获得更好的结果
detailed_prompt = """
A modern, minimalist office interior with large windows,
natural lighting, wooden desk, ergonomic chair,
plants, and laptop. Professional photography style,
high quality, 4K resolution.
"""

generator.generate(
    detailed_prompt,
    'office_interior.png',
    quality='hd',  # 使用高质量模式
    style='natural'  # 自然风格
)
```

## 常见问题

### Q: PyMuPDF安装失败？
A: 确保已安装C++编译器。Windows用户可能需要安装Visual Studio Build Tools。

### Q: Playwright提示浏览器未安装？
A: 运行 `playwright install chromium` 安装浏览器。

### Q: AI生成失败提示API key错误？
A: 检查环境变量 `OPENAI_API_KEY` 是否设置正确。

### Q: 截图显示不完整？
A: 尝试增加 `--wait` 参数，等待页面完全加载。

### Q: PDF提取的图片质量不好？
A: 使用 `--page` 和 `--dpi` 参数将整个页面转换为高分辨率图片。

## API费用说明

### OpenAI DALL-E定价（截至2024年）

- DALL-E 3 标准质量: $0.040/张
- DALL-E 3 高清质量: $0.080/张  
- DALL-E 2: $0.020/张

更多信息请查看：https://openai.com/pricing

## 依赖说明

- **PyMuPDF**: PDF处理 (MIT License)
- **Playwright**: 浏览器自动化 (Apache 2.0 License)
- **OpenAI**: AI图片生成 (需要API密钥)
- **Pillow**: 图片处理 (PIL License)
- **Requests**: HTTP请求 (Apache 2.0 License)

## 项目结构

```
image_tools/
├── __init__.py          # 包初始化
├── pdf_extractor.py     # PDF图片提取
├── web_screenshot.py    # 网页截图
├── ai_generator.py      # AI图片生成
├── cli.py              # 命令行接口
└── README.md           # 本文档
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 相关资源

- [PyMuPDF文档](https://pymupdf.readthedocs.io/)
- [Playwright Python文档](https://playwright.dev/python/)
- [OpenAI API文档](https://platform.openai.com/docs)
- [可行性分析报告](../IMAGE_INSERTION_FEASIBILITY_ANALYSIS.md)
