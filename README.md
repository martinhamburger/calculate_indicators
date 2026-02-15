# 产品净值计算器

产品净值业绩指标计算工具，支持单个文件或批量处理目录下所有Excel文件。

## 功能模块

### 1. 净值计算器
- 计算年化收益率、波动率、夏普比率、最大回撤等指标
- 支持年度、月度多维度分析
- 详见 [使用说明.md](./使用说明.md)

### 2. 公众号图片工具 🆕
- **网页截图**: 支持全页面截图、元素截图
- **PDF 处理**: PDF 转图片、提取 PDF 中的图片
- **命令行工具**: 简单易用的 CLI 界面
- 详见 [IMAGE_TOOLS_README.md](./IMAGE_TOOLS_README.md)
- 可行性分析: [IMAGE_INSERTION_FEASIBILITY.md](./IMAGE_INSERTION_FEASIBILITY.md)

## 快速开始

### 净值计算

```bash
# 安装依赖
pip install pandas openpyxl

# 处理单个文件
python calculate.py -f 产品净值.xlsx

# 批量处理目录
python calculate.py -d ./净值列表
```

### 图片工具

```bash
# 安装依赖
pip install -r requirements_image.txt
playwright install chromium

# 网页截图
python image_cli.py screenshot https://example.com -o screenshot.png

# PDF 转图片
python image_cli.py pdf-to-image document.pdf -o ./pages
```

## 项目结构

```
calculate_indicators/
├── calculate.py              # 净值计算主程序
├── buy_avg_return.py         # 买入平均收益计算
├── periodic_buy.py           # 周期性买入计算
├── merge_excel.py            # Excel 合并工具
├── image_cli.py              # 图片工具命令行接口 🆕
├── utils/                    # 工具类
├── image_tools/              # 图片工具模块 🆕
│   ├── screenshot.py         # 网页截图
│   └── pdf_extractor.py      # PDF 处理
├── frontend/                 # 前端界面
├── backend/                  # 后端 API
└── 使用说明.md               # 详细使用说明
```

## 文档

- [使用说明](./使用说明.md) - 净值计算器详细说明
- [图片工具使用指南](./IMAGE_TOOLS_README.md) - 公众号图片工具使用说明
- [可行性分析](./IMAGE_INSERTION_FEASIBILITY.md) - 图片功能可行性分析
- [Excel 合并说明](./MERGE_EXCEL_README.md) - Excel 文件合并工具
- [GitHub Pages 部署](./GITHUB_PAGES_DEPLOYMENT.md) - 部署指南

## 依赖

### 核心依赖
```
pandas
openpyxl
```

### 图片工具依赖
```
playwright
PyMuPDF
Pillow
```

## 许可证

MIT License
