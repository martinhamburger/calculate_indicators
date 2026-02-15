"""
网页截图工具

使用 Playwright 实现网页自动化截图功能。
"""

from typing import Optional, List
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from pathlib import Path
import time


class WebScreenshot:
    """网页截图工具
    
    支持全页面截图、元素截图等功能。
    使用 Playwright 实现，支持 JavaScript 渲染的现代网页。
    """
    
    def __init__(self, headless: bool = True, browser_type: str = 'chromium') -> None:
        """
        初始化截图工具
        
        Args:
            headless: 是否使用无头模式（不显示浏览器窗口）
            browser_type: 浏览器类型，可选 'chromium', 'firefox', 'webkit'
        """
        self.headless = headless
        self.browser_type = browser_type
        self.playwright = None
        self.browser = None
    
    def __enter__(self):
        """上下文管理器入口"""
        self.playwright = sync_playwright().start()
        browser_launcher = getattr(self.playwright, self.browser_type)
        self.browser = browser_launcher.launch(headless=self.headless)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def capture(self, url: str, output_path: str, 
                full_page: bool = True, 
                viewport_width: int = 1920, 
                viewport_height: int = 1080,
                wait_time: int = 0,
                wait_for_selector: Optional[str] = None) -> str:
        """
        截取网页
        
        Args:
            url: 目标网址
            output_path: 输出文件路径
            full_page: 是否截取整个页面（默认 True）
            viewport_width: 视口宽度（像素）
            viewport_height: 视口高度（像素）
            wait_time: 等待时间（秒），用于等待页面加载完成
            wait_for_selector: 等待特定元素出现（CSS 选择器）
        
        Returns:
            str: 截图保存的路径
        
        Raises:
            PlaywrightTimeout: 页面加载超时
        """
        if not self.browser:
            raise RuntimeError("请使用 with 语句或先调用 __enter__() 方法")
        
        # 创建输出目录
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建页面
        page = self.browser.new_page(
            viewport={"width": viewport_width, "height": viewport_height}
        )
        
        try:
            # 访问网页
            print(f"正在访问: {url}")
            page.goto(url, wait_until="networkidle", timeout=30000)
            
            # 等待特定元素
            if wait_for_selector:
                print(f"等待元素: {wait_for_selector}")
                page.wait_for_selector(wait_for_selector, timeout=10000)
            
            # 额外等待时间
            if wait_time > 0:
                print(f"等待 {wait_time} 秒...")
                time.sleep(wait_time)
            
            # 截图
            print(f"正在截图...")
            page.screenshot(path=str(output_path), full_page=full_page)
            print(f"✅ 截图已保存到: {output_path}")
            
            return str(output_path)
        
        finally:
            page.close()
    
    def capture_element(self, url, selector, output_path, 
                       viewport_width=1920, 
                       viewport_height=1080,
                       wait_time=0):
        """
        截取网页中的特定元素
        
        Args:
            url: 目标网址
            selector: CSS 选择器
            output_path: 输出文件路径
            viewport_width: 视口宽度（像素）
            viewport_height: 视口高度（像素）
            wait_time: 等待时间（秒）
        
        Returns:
            str: 截图保存的路径
        """
        if not self.browser:
            raise RuntimeError("请使用 with 语句或先调用 __enter__() 方法")
        
        # 创建输出目录
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建页面
        page = self.browser.new_page(
            viewport={"width": viewport_width, "height": viewport_height}
        )
        
        try:
            # 访问网页
            print(f"正在访问: {url}")
            page.goto(url, wait_until="networkidle", timeout=30000)
            
            # 等待元素出现
            print(f"等待元素: {selector}")
            element = page.wait_for_selector(selector, timeout=10000)
            
            # 额外等待时间
            if wait_time > 0:
                print(f"等待 {wait_time} 秒...")
                time.sleep(wait_time)
            
            # 截取元素
            print(f"正在截取元素...")
            element.screenshot(path=str(output_path))
            print(f"✅ 截图已保存到: {output_path}")
            
            return str(output_path)
        
        finally:
            page.close()
    
    def capture_batch(self, urls: List[str], output_folder: str, 
                     full_page: bool = True,
                     viewport_width: int = 1920,
                     viewport_height: int = 1080) -> List[Optional[str]]:
        """
        批量截取多个网页
        
        Args:
            urls: URL 列表
            output_folder: 输出文件夹
            full_page: 是否截取整个页面
            viewport_width: 视口宽度（像素）
            viewport_height: 视口高度（像素）
        
        Returns:
            list: 所有截图的路径列表
        """
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        
        results = []
        for i, url in enumerate(urls, 1):
            try:
                # 生成文件名
                filename = f"screenshot_{i}.png"
                output_path = output_folder / filename
                
                print(f"\n[{i}/{len(urls)}] 处理: {url}")
                path = self.capture(
                    url, 
                    output_path, 
                    full_page=full_page,
                    viewport_width=viewport_width,
                    viewport_height=viewport_height
                )
                results.append(path)
            
            except Exception as e:
                print(f"❌ 失败: {url}")
                print(f"   错误: {str(e)}")
                results.append(None)
        
        success_count = sum(1 for r in results if r is not None)
        print(f"\n✅ 完成: {success_count}/{len(urls)} 个网页截图成功")
        
        return results


# 便捷函数
def screenshot_url(url, output_path, full_page=True, headless=True):
    """
    快速截图单个网页（便捷函数）
    
    Args:
        url: 目标网址
        output_path: 输出文件路径
        full_page: 是否截取整个页面
        headless: 是否使用无头模式
    
    Returns:
        str: 截图保存的路径
    """
    with WebScreenshot(headless=headless) as screenshot:
        return screenshot.capture(url, output_path, full_page=full_page)


# 使用示例
if __name__ == "__main__":
    # 示例 1: 基本用法
    with WebScreenshot() as screenshot:
        screenshot.capture(
            url="https://example.com",
            output_path="example.png",
            full_page=True
        )
    
    # 示例 2: 使用便捷函数
    screenshot_url("https://example.com", "example2.png")
    
    # 示例 3: 批量截图
    with WebScreenshot() as screenshot:
        urls = [
            "https://example.com",
            "https://github.com",
        ]
        screenshot.capture_batch(urls, "./screenshots")
