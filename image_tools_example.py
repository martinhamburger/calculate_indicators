#!/usr/bin/env python3
"""
Example usage of the image_tools package.

This script demonstrates basic usage of each tool.
"""

import os
import sys

# Add parent directory to path to import image_tools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def example_pdf_extraction():
    """Example: PDF image extraction."""
    print("=" * 60)
    print("PDF Image Extraction Example")
    print("=" * 60)
    
    try:
        from image_tools import PDFExtractor
        
        # Note: This is just a demonstration of the API
        # You would need an actual PDF file to run this
        print("\nAPI Usage:")
        print("  extractor = PDFExtractor('document.pdf')")
        print("  images = extractor.extract_all_images('./output')")
        print("  extractor.extract_page_as_image(0, 'page1.png')")
        print("\nCommand-line usage:")
        print("  python -m image_tools.cli extract-pdf document.pdf -o ./images")
        
    except Exception as e:
        print(f"Note: {e}")


def example_web_screenshot():
    """Example: Web screenshot."""
    print("\n" + "=" * 60)
    print("Web Screenshot Example")
    print("=" * 60)
    
    try:
        from image_tools import WebScreenshot
        
        print("\nAPI Usage:")
        print("  screenshot = WebScreenshot('https://example.com')")
        print("  screenshot.capture('page.png', full_page=True)")
        print("  screenshot.capture_element('elem.png', selector='.article')")
        print("\nCommand-line usage:")
        print("  python -m image_tools.cli screenshot https://example.com -o page.png")
        
    except Exception as e:
        print(f"Note: {e}")


def example_ai_generation():
    """Example: AI image generation."""
    print("\n" + "=" * 60)
    print("AI Image Generation Example")
    print("=" * 60)
    
    try:
        from image_tools import AIGenerator
        
        print("\nAPI Usage:")
        print("  generator = AIGenerator()")
        print("  generator.generate('a beautiful sunset', 'sunset.png')")
        print("  variations = generator.generate_variations('base.png', './variants')")
        print("\nCommand-line usage:")
        print("  python -m image_tools.cli generate 'a beautiful sunset' -o sunset.png")
        print("\nNote: Requires OPENAI_API_KEY environment variable")
        
    except Exception as e:
        print(f"Note: {e}")


def main():
    """Run all examples."""
    print("Image Tools - Usage Examples")
    print("=" * 60)
    print("\nThis script demonstrates the API for the image_tools package.")
    print("To actually use the tools, you need to:")
    print("  1. Install dependencies: pip install -r image_tools_requirements.txt")
    print("  2. Install Playwright browsers: playwright install chromium")
    print("  3. Set OpenAI API key (for AI generation): export OPENAI_API_KEY='your-key'")
    print()
    
    example_pdf_extraction()
    example_web_screenshot()
    example_ai_generation()
    
    print("\n" + "=" * 60)
    print("For more information, see image_tools/README.md")
    print("=" * 60)


if __name__ == '__main__':
    main()
