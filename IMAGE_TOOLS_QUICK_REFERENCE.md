# 微信公众号图片工具 - 快速参考指南

## 安装

```bash
# 1. 安装Python依赖
pip install -r image_tools_requirements.txt

# 2. 安装Playwright浏览器
playwright install chromium

# 3. 设置OpenAI API Key（用于AI生成图片）
export OPENAI_API_KEY='your-api-key-here'
```

## 常用命令

### 📄 从PDF提取图片

```bash
# 提取所有图片
python -m image_tools.cli extract-pdf 文档.pdf -o ./图片

# 转换特定页面为图片（高清）
python -m image_tools.cli extract-pdf 文档.pdf --page 0 --dpi 600 -o 页面1.png
```

### 🌐 网页截图

```bash
# 截取完整网页
python -m image_tools.cli screenshot https://example.com -o 网页.png

# 截取特定元素
python -m image_tools.cli screenshot https://example.com --selector ".article" -o 文章.png

# 等待页面加载完成
python -m image_tools.cli screenshot https://example.com --wait 3 -o 网页.png
```

### 🎨 AI生成图片

```bash
# 基础生成
python -m image_tools.cli generate "日落美景" -o 日落.png

# 高质量生成
python -m image_tools.cli generate "现代办公室内景" \
  --model dall-e-3 --quality hd -o 办公室.png

# 生成变体
python -m image_tools.cli variations 基础图片.png -o ./变体 --count 3
```

## Python API

### PDF提取

```python
from image_tools import PDFExtractor

extractor = PDFExtractor('文档.pdf')
images = extractor.extract_all_images('./输出')
```

### 网页截图

```python
from image_tools import WebScreenshot

screenshot = WebScreenshot('https://example.com')
screenshot.capture('网页.png', full_page=True)
```

### AI生成

```python
from image_tools import AIGenerator

generator = AIGenerator()
generator.generate('美丽的日落', '日落.png')
```

## 实用场景

### 1. 技术文档配图

```bash
# 从技术文档提取图表
python -m image_tools.cli extract-pdf 技术文档.pdf -o ./图表

# 生成概念图
python -m image_tools.cli generate "云计算架构图，简洁专业" -o 架构.png
```

### 2. 网页内容引用

```bash
# 截取新闻文章
python -m image_tools.cli screenshot https://news.example.com/article \
  --selector "article" --wait 2 -o 新闻.png

# 截取数据图表
python -m image_tools.cli screenshot https://data.example.com/chart \
  --selector "#chart" -o 图表.png
```

### 3. 社交媒体配图

```bash
# 生成文章封面
python -m image_tools.cli generate \
  "科技感背景，蓝色调，简约现代风格" \
  --quality hd -o 封面.png

# 生成多个候选
python -m image_tools.cli generate "商务会议场景" -o base.png
python -m image_tools.cli variations base.png -o ./候选 --count 4
```

## 故障排除

### 问题：PyMuPDF安装失败
**解决**：安装C++编译器
- Windows: 安装 Visual Studio Build Tools
- Linux: `sudo apt-get install python3-dev`
- macOS: `xcode-select --install`

### 问题：Playwright浏览器未安装
**解决**：运行 `playwright install chromium`

### 问题：API key错误
**解决**：检查环境变量
```bash
echo $OPENAI_API_KEY  # 查看是否设置
export OPENAI_API_KEY='sk-...'  # 设置API key
```

### 问题：截图不完整
**解决**：增加等待时间
```bash
python -m image_tools.cli screenshot URL --wait 5 -o output.png
```

## 费用参考

### OpenAI DALL-E 定价
- DALL-E 3 标准: $0.040/张
- DALL-E 3 高清: $0.080/张
- DALL-E 2: $0.020/张

其他功能（PDF提取、网页截图）完全免费。

## 获取帮助

```bash
# 查看总体帮助
python -m image_tools.cli --help

# 查看具体命令帮助
python -m image_tools.cli extract-pdf --help
python -m image_tools.cli screenshot --help
python -m image_tools.cli generate --help
```

## 完整文档

- **详细使用说明**: [image_tools/README.md](image_tools/README.md)
- **可行性分析**: [IMAGE_INSERTION_FEASIBILITY_ANALYSIS.md](IMAGE_INSERTION_FEASIBILITY_ANALYSIS.md)
- **使用示例**: 运行 `python image_tools_example.py`

---

**提示**: 所有工具都可以直接在Claude Code环境中使用！
