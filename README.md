# Calculate Indicators

A comprehensive toolkit for financial indicator calculation and image preparation for WeChat public account articles.

## Features

This repository contains two main components:

### 1. Financial Indicators Calculator (财务指标计算器)

Calculate performance metrics for financial products, including:
- Annual returns and volatility
- Sharpe ratio
- Maximum drawdown
- Monthly and yearly analysis

For detailed documentation in Chinese, see [使用说明.md](使用说明.md)

### 2. Image Tools for WeChat Articles (微信公众号图片工具) 🆕

A complete toolkit for preparing images for WeChat public account articles:
- **PDF Image Extraction**: Extract images from PDF documents or convert PDF pages to images
- **Web Screenshots**: Capture full web pages or specific elements
- **AI Image Generation**: Generate images using OpenAI DALL-E

For detailed documentation, see [image_tools/README.md](image_tools/README.md)

## Quick Start

### Financial Indicators Calculator

```bash
# Calculate indicators from Excel files
python calculate.py -d ./净值列表

# Calculate buy average returns
python buy_avg_return.py -f 买入平均收益_净值列表/日度净值.xlsx

# Calculate periodic buy returns
python periodic_buy.py -f 买入平均收益_净值列表/日度净值.xlsx --rule friday
```

### Image Tools

```bash
# Install dependencies
pip install -r image_tools_requirements.txt
playwright install chromium

# Extract images from PDF
python -m image_tools.cli extract-pdf document.pdf -o ./images

# Capture web screenshot
python -m image_tools.cli screenshot https://example.com -o page.png

# Generate AI image (requires OPENAI_API_KEY)
export OPENAI_API_KEY='your-key'
python -m image_tools.cli generate "a beautiful sunset" -o sunset.png
```

## Project Structure

```
calculate_indicators/
├── image_tools/                    # Image tools for WeChat articles (NEW)
│   ├── __init__.py
│   ├── pdf_extractor.py           # PDF image extraction
│   ├── web_screenshot.py          # Web screenshot tool
│   ├── ai_generator.py            # AI image generator
│   ├── cli.py                     # Command-line interface
│   └── README.md                  # Detailed documentation
├── utils/                          # Financial calculation utilities
├── frontend/                       # Web interface
├── backend/                        # Backend services
├── calculate.py                    # Main calculator
├── buy_avg_return.py              # Buy average return calculator
├── periodic_buy.py                # Periodic buy calculator
├── 使用说明.md                     # Chinese documentation
├── IMAGE_INSERTION_FEASIBILITY_ANALYSIS.md  # Feasibility analysis
└── image_tools_requirements.txt    # Image tools dependencies
```

## Documentation

### Financial Indicators
- [使用说明.md](使用说明.md) - Complete guide in Chinese
- [MERGE_EXCEL_README.md](MERGE_EXCEL_README.md) - Excel merging guide

### Image Tools
- [image_tools/README.md](image_tools/README.md) - Complete image tools guide
- [IMAGE_INSERTION_FEASIBILITY_ANALYSIS.md](IMAGE_INSERTION_FEASIBILITY_ANALYSIS.md) - Feasibility analysis report

### Deployment
- [GITHUB_PAGES_SETUP_COMPLETE.md](GITHUB_PAGES_SETUP_COMPLETE.md) - GitHub Pages setup
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Deployment checklist

## Dependencies

### Financial Calculator
```bash
pip install pandas openpyxl
```

### Image Tools
```bash
pip install -r image_tools_requirements.txt
playwright install chromium
```

## Use Cases

### Financial Analysis
1. Calculate product performance metrics from Excel files
2. Analyze buy-and-hold returns over time
3. Evaluate periodic investment strategies
4. Generate performance reports

### WeChat Article Preparation
1. Extract charts and diagrams from PDF documents
2. Capture screenshots of web content for articles
3. Generate AI illustrations for article headers
4. Batch process images from multiple sources

## Examples

### Financial Calculator Example

```python
from utils import ProductNetValueCalculator

calculator = ProductNetValueCalculator(
    file_path="产品净值.xlsx",
    risk_free_rate=0.02
)

calculator.run_all_calculations()
calculator.save_to_excel("产品净值_结果.xlsx")
```

### Image Tools Example

```python
from image_tools import PDFExtractor, WebScreenshot, AIGenerator

# Extract images from PDF
extractor = PDFExtractor('document.pdf')
images = extractor.extract_all_images('./output')

# Capture web screenshot
screenshot = WebScreenshot('https://example.com')
screenshot.capture('page.png')

# Generate AI image
generator = AIGenerator()
generator.generate('a beautiful sunset', 'sunset.png')
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Related Projects

For similar image processing tools, check out:
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) - PDF processing
- [Playwright](https://github.com/microsoft/playwright-python) - Browser automation
- [shot-scraper](https://github.com/simonw/shot-scraper) - Website screenshots

## Acknowledgments

This project uses several open-source libraries:
- PyMuPDF for PDF processing
- Playwright for web automation
- OpenAI API for AI image generation
- Pandas and openpyxl for Excel processing

## Contact

For questions or issues, please open an issue on GitHub.

---

**Note**: The image tools module was added to support WeChat public account article preparation. See [IMAGE_INSERTION_FEASIBILITY_ANALYSIS.md](IMAGE_INSERTION_FEASIBILITY_ANALYSIS.md) for the detailed feasibility analysis.
