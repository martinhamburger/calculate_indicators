#!/usr/bin/env python3
"""
公众号图片工具示例

演示如何使用图片工具进行公众号内容创作。
"""

import os
from pathlib import Path


def demo_screenshot():
    """演示网页截图功能"""
    print("=" * 60)
    print("示例 1: 网页截图")
    print("=" * 60)
    
    try:
        from image_tools import WebScreenshot
        
        output_folder = Path("./demo_output/screenshots")
        output_folder.mkdir(parents=True, exist_ok=True)
        
        with WebScreenshot() as screenshot:
            # 示例 1: 基本截图
            print("\n1. 截取示例网页...")
            screenshot.capture(
                url="https://example.com",
                output_path=output_folder / "example.png",
                full_page=True
            )
            
            print("\n✅ 截图完成！查看输出: demo_output/screenshots/")
    
    except ImportError:
        print("\n⚠️  需要先安装依赖:")
        print("   pip install playwright")
        print("   playwright install chromium")
    
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")


def demo_pdf_processing():
    """演示 PDF 处理功能"""
    print("\n" + "=" * 60)
    print("示例 2: PDF 处理")
    print("=" * 60)
    
    try:
        from image_tools import PDFExtractor
        
        # 检查是否有测试 PDF
        test_pdf = "test.pdf"
        if not os.path.exists(test_pdf):
            print(f"\n⚠️  请准备一个测试 PDF 文件并命名为 '{test_pdf}'")
            print("   然后重新运行此示例")
            return
        
        output_folder = Path("./demo_output")
        
        extractor = PDFExtractor()
        
        # 示例 1: 显示 PDF 信息
        print(f"\n1. 读取 PDF 信息: {test_pdf}")
        info = extractor.get_pdf_info(test_pdf)
        print(f"   页数: {info['pages']}")
        print(f"   图片数: {info['total_images']}")
        
        # 示例 2: PDF 转图片
        print("\n2. 将 PDF 页面转为图片...")
        pages_folder = output_folder / "pdf_pages"
        extractor.pages_to_images(
            pdf_path=test_pdf,
            output_folder=pages_folder,
            dpi=150
        )
        
        # 示例 3: 提取图片
        if info['total_images'] > 0:
            print("\n3. 提取 PDF 中的图片...")
            images_folder = output_folder / "pdf_images"
            extractor.extract_images(
                pdf_path=test_pdf,
                output_folder=images_folder
            )
        
        print("\n✅ PDF 处理完成！查看输出: demo_output/")
    
    except ImportError:
        print("\n⚠️  需要先安装依赖:")
        print("   pip install PyMuPDF")
    
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")


def demo_batch_processing():
    """演示批量处理"""
    print("\n" + "=" * 60)
    print("示例 3: 批量处理多个网页")
    print("=" * 60)
    
    try:
        from image_tools import WebScreenshot
        
        output_folder = Path("./demo_output/batch")
        output_folder.mkdir(parents=True, exist_ok=True)
        
        urls = [
            "https://example.com",
            "https://www.wikipedia.org",
        ]
        
        print(f"\n批量截图 {len(urls)} 个网页...")
        
        with WebScreenshot() as screenshot:
            results = screenshot.capture_batch(
                urls=urls,
                output_folder=output_folder,
                full_page=True
            )
        
        print("\n✅ 批量处理完成！查看输出: demo_output/batch/")
    
    except ImportError:
        print("\n⚠️  需要先安装依赖:")
        print("   pip install playwright")
        print("   playwright install chromium")
    
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")


def demo_api_usage():
    """演示 Python API 使用"""
    print("\n" + "=" * 60)
    print("示例 4: Python API 使用")
    print("=" * 60)
    
    print("\n# 网页截图 API")
    print("""
from image_tools import WebScreenshot

with WebScreenshot() as screenshot:
    # 基本截图
    screenshot.capture(
        url="https://example.com",
        output_path="screenshot.png"
    )
    
    # 自定义视口（手机）
    screenshot.capture(
        url="https://example.com",
        output_path="mobile.png",
        viewport_width=390,
        viewport_height=844
    )
    
    # 等待元素加载
    screenshot.capture(
        url="https://example.com",
        output_path="loaded.png",
        wait_for_selector=".content"
    )
""")
    
    print("\n# PDF 处理 API")
    print("""
from image_tools import PDFExtractor

extractor = PDFExtractor()

# PDF 转图片
extractor.pages_to_images(
    pdf_path="document.pdf",
    output_folder="./pages",
    dpi=150
)

# 提取 PDF 图片
extractor.extract_images(
    pdf_path="document.pdf",
    output_folder="./images"
)

# 获取 PDF 信息
info = extractor.get_pdf_info("document.pdf")
print(f"总页数: {info['pages']}")
""")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("公众号图片工具示例演示")
    print("=" * 60)
    print("\n本示例将演示以下功能:")
    print("1. 网页截图")
    print("2. PDF 处理（需要测试 PDF 文件）")
    print("3. 批量处理")
    print("4. Python API 使用方法")
    
    # 检查依赖
    print("\n" + "=" * 60)
    print("检查依赖")
    print("=" * 60)
    
    dependencies = {
        'playwright': False,
        'fitz': False,  # PyMuPDF
    }
    
    try:
        import playwright
        dependencies['playwright'] = True
        print("✅ Playwright 已安装")
    except ImportError:
        print("❌ Playwright 未安装")
        print("   安装: pip install playwright && playwright install chromium")
    
    try:
        import fitz
        dependencies['fitz'] = True
        print("✅ PyMuPDF 已安装")
    except ImportError:
        print("❌ PyMuPDF 未安装")
        print("   安装: pip install PyMuPDF")
    
    # 运行演示
    if dependencies['playwright']:
        demo_screenshot()
        demo_batch_processing()
    
    if dependencies['fitz']:
        demo_pdf_processing()
    
    # 显示 API 使用方法
    demo_api_usage()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    print("\n更多使用方法请查看:")
    print("- IMAGE_TOOLS_README.md - 详细使用指南")
    print("- IMAGE_INSERTION_FEASIBILITY.md - 可行性分析")
    print("\n命令行工具:")
    print("  python image_cli.py --help")


if __name__ == "__main__":
    main()
