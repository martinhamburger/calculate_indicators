"""
Command-line interface for image tools.

Provides a unified CLI for PDF extraction, web screenshots, and AI image generation.
"""

import argparse
import sys
from pathlib import Path

from .pdf_extractor import PDFExtractor
from .web_screenshot import WebScreenshot
from .ai_generator import AIGenerator


def cmd_extract_pdf(args):
    """Extract images from PDF."""
    extractor = PDFExtractor(args.pdf)
    
    if args.page is not None:
        # Extract specific page as image
        output = args.output or f"{Path(args.pdf).stem}_page{args.page}.png"
        extractor.extract_page_as_image(args.page, output, dpi=args.dpi)
        print(f"✓ Page extracted to: {output}")
    else:
        # Extract all images
        output_dir = args.output or './extracted_images'
        images = extractor.extract_all_images(output_dir)
        print(f"✓ Extracted {len(images)} images to: {output_dir}")


def cmd_screenshot(args):
    """Capture web screenshot."""
    screenshot = WebScreenshot(
        browser_type=args.browser,
        headless=not args.no_headless
    )
    
    viewport = None
    if args.width and args.height:
        viewport = {'width': args.width, 'height': args.height}
    
    if args.selector:
        # Capture specific element
        screenshot.capture_element(
            args.output,
            selector=args.selector,
            url=args.url,
            wait_time=args.wait * 1000
        )
    else:
        # Capture full page or viewport
        screenshot.capture(
            args.output,
            url=args.url,
            full_page=args.full_page,
            wait_time=args.wait * 1000,
            viewport=viewport
        )
    
    print(f"✓ Screenshot saved to: {args.output}")


def cmd_generate(args):
    """Generate AI image."""
    generator = AIGenerator(
        api_key=args.api_key,
        provider=args.provider,
        model=args.model
    )
    
    # Optimize prompt if requested
    prompt = args.prompt
    if args.optimize:
        prompt = generator.optimize_prompt(prompt)
        print(f"Optimized prompt: {prompt}")
    
    generator.generate(
        prompt,
        args.output,
        size=args.size,
        quality=args.quality,
        style=args.style
    )
    
    print(f"✓ Image generated and saved to: {args.output}")


def cmd_variations(args):
    """Generate image variations."""
    generator = AIGenerator(api_key=args.api_key)
    
    output_dir = args.output or './variations'
    variations = generator.generate_variations(
        args.image,
        output_dir,
        n=args.count,
        size=args.size
    )
    
    print(f"✓ Generated {len(variations)} variations in: {output_dir}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Image Tools for WeChat Public Account Articles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract images from PDF
  %(prog)s extract-pdf document.pdf
  %(prog)s extract-pdf document.pdf --page 0 --output page1.png
  
  # Capture web screenshot
  %(prog)s screenshot https://example.com -o page.png
  %(prog)s screenshot https://example.com --selector ".article" -o article.png
  
  # Generate AI image
  %(prog)s generate "a beautiful sunset over mountains" -o sunset.png
  %(prog)s generate "modern office interior" --model dall-e-3 --quality hd
  
  # Generate variations
  %(prog)s variations base_image.png -o ./variations --count 3
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # PDF extraction command
    pdf_parser = subparsers.add_parser('extract-pdf', help='Extract images from PDF')
    pdf_parser.add_argument('pdf', help='Path to PDF file')
    pdf_parser.add_argument('-o', '--output', help='Output path or directory')
    pdf_parser.add_argument('-p', '--page', type=int, help='Extract specific page as image (0-indexed)')
    pdf_parser.add_argument('--dpi', type=int, default=300, help='DPI for page extraction (default: 300)')
    
    # Screenshot command
    screenshot_parser = subparsers.add_parser('screenshot', help='Capture web screenshot')
    screenshot_parser.add_argument('url', help='URL to capture')
    screenshot_parser.add_argument('-o', '--output', default='screenshot.png', help='Output file path')
    screenshot_parser.add_argument('--selector', help='CSS selector for specific element')
    screenshot_parser.add_argument('--full-page', action='store_true', default=True, help='Capture full page')
    screenshot_parser.add_argument('--no-headless', action='store_true', help='Show browser window')
    screenshot_parser.add_argument('--wait', type=int, default=0, help='Wait time in seconds before capture')
    screenshot_parser.add_argument('--width', type=int, help='Viewport width')
    screenshot_parser.add_argument('--height', type=int, help='Viewport height')
    screenshot_parser.add_argument('--browser', choices=['chromium', 'firefox', 'webkit'], 
                                  default='chromium', help='Browser to use')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate AI image')
    generate_parser.add_argument('prompt', help='Text description of image to generate')
    generate_parser.add_argument('-o', '--output', default='generated_image.png', help='Output file path')
    generate_parser.add_argument('--api-key', help='API key (or set OPENAI_API_KEY env var)')
    generate_parser.add_argument('--provider', default='openai', choices=['openai'], help='AI provider')
    generate_parser.add_argument('--model', default='dall-e-3', choices=['dall-e-3', 'dall-e-2'], help='Model to use')
    generate_parser.add_argument('--size', default='1024x1024', help='Image size')
    generate_parser.add_argument('--quality', default='standard', choices=['standard', 'hd'], help='Image quality')
    generate_parser.add_argument('--style', choices=['vivid', 'natural'], help='Image style')
    generate_parser.add_argument('--optimize', action='store_true', help='Optimize prompt automatically')
    
    # Variations command
    variations_parser = subparsers.add_parser('variations', help='Generate image variations')
    variations_parser.add_argument('image', help='Base image path')
    variations_parser.add_argument('-o', '--output', help='Output directory')
    variations_parser.add_argument('--count', type=int, default=3, help='Number of variations')
    variations_parser.add_argument('--size', default='1024x1024', help='Image size')
    variations_parser.add_argument('--api-key', help='API key (or set OPENAI_API_KEY env var)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'extract-pdf':
            cmd_extract_pdf(args)
        elif args.command == 'screenshot':
            cmd_screenshot(args)
        elif args.command == 'generate':
            cmd_generate(args)
        elif args.command == 'variations':
            cmd_variations(args)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
