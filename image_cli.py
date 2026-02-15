#!/usr/bin/env python3
"""
公众号图片工具命令行接口

提供网页截图、PDF 转图片等功能的命令行工具。
"""

import argparse
import sys
from pathlib import Path


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='公众号图片工具 - 网页截图和 PDF 处理',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 网页截图
  python image_cli.py screenshot https://example.com -o screenshot.png
  
  # PDF 转图片
  python image_cli.py pdf-to-image document.pdf -o ./pages
  
  # 提取 PDF 中的图片
  python image_cli.py extract-images document.pdf -o ./images
  
  # 查看 PDF 信息
  python image_cli.py pdf-info document.pdf
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # ========== 网页截图命令 ==========
    screenshot_parser = subparsers.add_parser(
        'screenshot',
        help='网页截图'
    )
    screenshot_parser.add_argument(
        'url',
        help='目标网址（如 https://example.com）'
    )
    screenshot_parser.add_argument(
        '-o', '--output',
        default='screenshot.png',
        help='输出文件路径（默认: screenshot.png）'
    )
    screenshot_parser.add_argument(
        '--full-page',
        action='store_true',
        help='截取整个页面（默认）'
    )
    screenshot_parser.add_argument(
        '--viewport-only',
        action='store_true',
        help='仅截取可见区域'
    )
    screenshot_parser.add_argument(
        '--width',
        type=int,
        default=1920,
        help='视口宽度（像素，默认: 1920）'
    )
    screenshot_parser.add_argument(
        '--height',
        type=int,
        default=1080,
        help='视口高度（像素，默认: 1080）'
    )
    screenshot_parser.add_argument(
        '--wait',
        type=int,
        default=0,
        help='等待时间（秒，默认: 0）'
    )
    screenshot_parser.add_argument(
        '--wait-selector',
        help='等待特定元素出现（CSS 选择器）'
    )
    screenshot_parser.add_argument(
        '--show-browser',
        action='store_true',
        help='显示浏览器窗口（用于调试）'
    )
    
    # ========== 批量截图命令 ==========
    batch_parser = subparsers.add_parser(
        'screenshot-batch',
        help='批量截图多个网页'
    )
    batch_parser.add_argument(
        'urls',
        nargs='+',
        help='目标网址列表'
    )
    batch_parser.add_argument(
        '-o', '--output',
        default='./screenshots',
        help='输出文件夹（默认: ./screenshots）'
    )
    batch_parser.add_argument(
        '--full-page',
        action='store_true',
        default=True,
        help='截取整个页面'
    )
    
    # ========== PDF 转图片命令 ==========
    pdf_parser = subparsers.add_parser(
        'pdf-to-image',
        help='将 PDF 页面转换为图片'
    )
    pdf_parser.add_argument(
        'pdf',
        help='PDF 文件路径'
    )
    pdf_parser.add_argument(
        '-o', '--output',
        default='./output/pages',
        help='输出文件夹（默认: ./output/pages）'
    )
    pdf_parser.add_argument(
        '--dpi',
        type=int,
        default=150,
        choices=[72, 150, 300, 600],
        help='图片分辨率 DPI（默认: 150）'
    )
    pdf_parser.add_argument(
        '--format',
        choices=['png', 'jpg'],
        default='png',
        help='图片格式（默认: png）'
    )
    pdf_parser.add_argument(
        '--pages',
        help='页面范围（如 "1-5" 或 "1,3,5"）'
    )
    
    # ========== 提取 PDF 图片命令 ==========
    extract_parser = subparsers.add_parser(
        'extract-images',
        help='从 PDF 中提取嵌入的图片'
    )
    extract_parser.add_argument(
        'pdf',
        help='PDF 文件路径'
    )
    extract_parser.add_argument(
        '-o', '--output',
        default='./output/images',
        help='输出文件夹（默认: ./output/images）'
    )
    extract_parser.add_argument(
        '--min-width',
        type=int,
        default=100,
        help='最小宽度（像素，默认: 100）'
    )
    extract_parser.add_argument(
        '--min-height',
        type=int,
        default=100,
        help='最小高度（像素，默认: 100）'
    )
    
    # ========== PDF 信息命令 ==========
    info_parser = subparsers.add_parser(
        'pdf-info',
        help='查看 PDF 文件信息'
    )
    info_parser.add_argument(
        'pdf',
        help='PDF 文件路径'
    )
    
    # 解析参数
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 执行命令
    try:
        if args.command == 'screenshot':
            from image_tools.screenshot import WebScreenshot
            
            full_page = not args.viewport_only
            headless = not args.show_browser
            
            print(f"📷 正在截图: {args.url}")
            print(f"   输出: {args.output}")
            print(f"   模式: {'整页' if full_page else '可见区域'}")
            
            with WebScreenshot(headless=headless) as screenshot:
                screenshot.capture(
                    url=args.url,
                    output_path=args.output,
                    full_page=full_page,
                    viewport_width=args.width,
                    viewport_height=args.height,
                    wait_time=args.wait,
                    wait_for_selector=args.wait_selector
                )
        
        elif args.command == 'screenshot-batch':
            from image_tools.screenshot import WebScreenshot
            
            print(f"📷 批量截图: {len(args.urls)} 个网页")
            print(f"   输出文件夹: {args.output}")
            
            with WebScreenshot() as screenshot:
                screenshot.capture_batch(
                    urls=args.urls,
                    output_folder=args.output,
                    full_page=args.full_page
                )
        
        elif args.command == 'pdf-to-image':
            from image_tools.pdf_extractor import PDFExtractor
            
            # 解析页面范围
            page_range = None
            if args.pages:
                if '-' in args.pages:
                    start, end = args.pages.split('-')
                    page_range = (int(start) - 1, int(end))
                else:
                    # TODO: 支持离散页码
                    print("暂不支持离散页码，请使用范围格式（如 1-5）")
                    return
            
            print(f"📄 PDF 转图片: {args.pdf}")
            print(f"   输出文件夹: {args.output}")
            print(f"   分辨率: {args.dpi} DPI")
            print(f"   格式: {args.format}")
            
            extractor = PDFExtractor()
            extractor.pages_to_images(
                pdf_path=args.pdf,
                output_folder=args.output,
                dpi=args.dpi,
                image_format=args.format,
                page_range=page_range
            )
        
        elif args.command == 'extract-images':
            from image_tools.pdf_extractor import PDFExtractor
            
            print(f"🖼️  提取 PDF 图片: {args.pdf}")
            print(f"   输出文件夹: {args.output}")
            print(f"   最小尺寸: {args.min_width}x{args.min_height}px")
            
            extractor = PDFExtractor()
            extractor.extract_images(
                pdf_path=args.pdf,
                output_folder=args.output,
                min_width=args.min_width,
                min_height=args.min_height
            )
        
        elif args.command == 'pdf-info':
            from image_tools.pdf_extractor import PDFExtractor
            
            print(f"📋 PDF 信息: {args.pdf}")
            print("=" * 60)
            
            extractor = PDFExtractor()
            info = extractor.get_pdf_info(args.pdf)
            
            for key, value in info.items():
                if value:
                    label = key.replace('_', ' ').title()
                    print(f"{label:20s}: {value}")
        
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\n\n⚠️  操作已取消")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
