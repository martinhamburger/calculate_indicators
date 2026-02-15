"""
公众号图片工具模块

提供网页截图、PDF 转图片等功能，用于公众号内容创作。
"""

__version__ = '1.0.0'
__all__ = []

# 尝试导入网页截图功能
try:
    from .screenshot import WebScreenshot
    __all__.append('WebScreenshot')
except ImportError as e:
    import warnings
    warnings.warn(f"网页截图功能不可用，需要安装 playwright: {e}")
    WebScreenshot = None

# 尝试导入 PDF 处理功能
try:
    from .pdf_extractor import PDFExtractor
    __all__.append('PDFExtractor')
except ImportError as e:
    import warnings
    warnings.warn(f"PDF 处理功能不可用，需要安装 PyMuPDF: {e}")
    PDFExtractor = None
