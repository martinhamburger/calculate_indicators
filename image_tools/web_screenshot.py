"""
Web Screenshot Tool

Capture screenshots of web pages using Playwright.
"""

import os
from typing import Optional, Dict, Any


class WebScreenshot:
    """Capture screenshots of web pages."""
    
    def __init__(self, url: Optional[str] = None, 
                 browser_type: str = 'chromium',
                 headless: bool = True):
        """
        Initialize web screenshot tool.
        
        Args:
            url: URL to capture (optional, can be set later)
            browser_type: Browser to use ('chromium', 'firefox', 'webkit')
            headless: Run browser in headless mode
        """
        self.url = url
        self.browser_type = browser_type
        self.headless = headless
    
    def capture(self, output_path: str, 
                url: Optional[str] = None,
                full_page: bool = True,
                wait_time: int = 0,
                viewport: Optional[Dict[str, int]] = None) -> str:
        """
        Capture a screenshot of a web page.
        
        Args:
            output_path: Path to save the screenshot
            url: URL to capture (overrides init URL)
            full_page: Capture full scrollable page (default: True)
            wait_time: Time to wait before capturing in milliseconds
            viewport: Viewport size dict with 'width' and 'height'
            
        Returns:
            Path to the saved screenshot
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise ImportError(
                "Playwright is required for web screenshots. "
                "Install it with: pip install playwright && playwright install"
            )
        
        target_url = url or self.url
        if not target_url:
            raise ValueError("URL must be provided")
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        with sync_playwright() as p:
            # Launch browser
            if self.browser_type == 'chromium':
                browser = p.chromium.launch(headless=self.headless)
            elif self.browser_type == 'firefox':
                browser = p.firefox.launch(headless=self.headless)
            elif self.browser_type == 'webkit':
                browser = p.webkit.launch(headless=self.headless)
            else:
                raise ValueError(f"Unsupported browser type: {self.browser_type}")
            
            try:
                # Create page with optional viewport
                page_options = {}
                if viewport:
                    page_options['viewport'] = viewport
                
                page = browser.new_page(**page_options)
                
                # Navigate to URL
                print(f"Loading: {target_url}")
                page.goto(target_url, wait_until='networkidle')
                
                # Optional wait time
                if wait_time > 0:
                    page.wait_for_timeout(wait_time)
                
                # Take screenshot
                print(f"Capturing screenshot to: {output_path}")
                page.screenshot(path=output_path, full_page=full_page)
                
                return output_path
                
            finally:
                browser.close()
    
    def capture_element(self, output_path: str,
                       selector: str,
                       url: Optional[str] = None,
                       wait_time: int = 0) -> str:
        """
        Capture a screenshot of a specific element.
        
        Args:
            output_path: Path to save the screenshot
            selector: CSS selector for the element
            url: URL to capture (overrides init URL)
            wait_time: Time to wait before capturing in milliseconds
            
        Returns:
            Path to the saved screenshot
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise ImportError(
                "Playwright is required for web screenshots. "
                "Install it with: pip install playwright && playwright install"
            )
        
        target_url = url or self.url
        if not target_url:
            raise ValueError("URL must be provided")
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            
            try:
                page = browser.new_page()
                
                # Navigate to URL
                print(f"Loading: {target_url}")
                page.goto(target_url, wait_until='networkidle')
                
                # Optional wait time
                if wait_time > 0:
                    page.wait_for_timeout(wait_time)
                
                # Find element and take screenshot
                element = page.locator(selector)
                print(f"Capturing element '{selector}' to: {output_path}")
                element.screenshot(path=output_path)
                
                return output_path
                
            finally:
                browser.close()
    
    def capture_multiple_pages(self, urls: list, output_dir: str,
                              full_page: bool = True) -> list:
        """
        Capture screenshots of multiple URLs.
        
        Args:
            urls: List of URLs to capture
            output_dir: Directory to save screenshots
            full_page: Capture full scrollable page
            
        Returns:
            List of paths to saved screenshots
        """
        os.makedirs(output_dir, exist_ok=True)
        
        screenshots = []
        for i, url in enumerate(urls):
            filename = f"screenshot_{i+1:03d}.png"
            output_path = os.path.join(output_dir, filename)
            
            try:
                self.capture(output_path, url=url, full_page=full_page)
                screenshots.append(output_path)
            except Exception as e:
                print(f"Error capturing {url}: {e}")
        
        return screenshots


# Command-line usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python web_screenshot.py <url> [output_file]")
        print("Example: python web_screenshot.py https://example.com screenshot.png")
        sys.exit(1)
    
    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'screenshot.png'
    
    screenshot = WebScreenshot(url)
    
    print(f"Capturing screenshot of: {url}")
    result = screenshot.capture(output_file)
    
    print(f"\nScreenshot saved to: {result}")
