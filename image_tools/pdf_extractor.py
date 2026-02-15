"""
PDF 图片提取工具

使用 PyMuPDF (fitz) 实现 PDF 转图片和图片提取功能。
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Tuple


class PDFExtractor:
    """PDF 图片提取工具
    
    支持：
    1. 将 PDF 页面转换为图片
    2. 从 PDF 中提取嵌入的图片
    """
    
    def pages_to_images(self, pdf_path, output_folder, 
                       dpi=150, 
                       image_format='png',
                       page_range=None) -> List[str]:
        """
        将 PDF 页面转换为图片
        
        Args:
            pdf_path: PDF 文件路径
            output_folder: 输出文件夹
            dpi: 图片分辨率（DPI），默认 150
                 常用值: 72(屏幕), 150(一般), 300(高清), 600(印刷)
            image_format: 图片格式，'png' 或 'jpg'
            page_range: 页面范围，如 (0, 5) 表示第 1-5 页，None 表示全部
        
        Returns:
            list: 生成的图片路径列表
        """
        # 创建输出目录
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # 打开 PDF
        print(f"正在打开 PDF: {pdf_path}")
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        print(f"共 {total_pages} 页")
        
        # 确定页面范围
        if page_range:
            start_page, end_page = page_range
            start_page = max(0, start_page)
            end_page = min(total_pages, end_page)
        else:
            start_page, end_page = 0, total_pages
        
        # 计算缩放比例
        zoom = dpi / 72.0
        matrix = fitz.Matrix(zoom, zoom)
        
        image_paths = []
        
        # 转换每一页
        for page_num in range(start_page, end_page):
            page = doc[page_num]
            
            # 渲染页面为图片
            pix = page.get_pixmap(matrix=matrix)
            
            # 保存图片
            output_path = output_folder / f"page_{page_num + 1:04d}.{image_format}"
            
            if image_format.lower() == 'jpg':
                pix.save(str(output_path), "jpeg")
            else:
                pix.save(str(output_path))
            
            image_paths.append(str(output_path))
            print(f"✅ 已转换: 第 {page_num + 1}/{total_pages} 页 -> {output_path.name}")
        
        doc.close()
        
        print(f"\n完成！共生成 {len(image_paths)} 张图片")
        return image_paths
    
    def extract_images(self, pdf_path, output_folder, 
                      min_width=100, 
                      min_height=100) -> List[Tuple[str, dict]]:
        """
        从 PDF 中提取嵌入的图片
        
        Args:
            pdf_path: PDF 文件路径
            output_folder: 输出文件夹
            min_width: 最小宽度（像素），过滤小图片
            min_height: 最小高度（像素），过滤小图片
        
        Returns:
            list: 提取的图片信息列表，每项为 (路径, 信息字典)
        """
        # 创建输出目录
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # 打开 PDF
        print(f"正在打开 PDF: {pdf_path}")
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        print(f"共 {total_pages} 页")
        
        image_results = []
        image_count = 0
        
        # 遍历每一页
        for page_num in range(total_pages):
            page = doc[page_num]
            image_list = page.get_images()
            
            if image_list:
                print(f"\n第 {page_num + 1} 页: 发现 {len(image_list)} 张图片")
            
            # 提取每张图片
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image_width = base_image["width"]
                    image_height = base_image["height"]
                    
                    # 过滤小图片（通常是图标或背景）
                    if image_width < min_width or image_height < min_height:
                        print(f"  ⏭️  跳过小图片: {image_width}x{image_height}px")
                        continue
                    
                    image_count += 1
                    output_path = output_folder / f"image_{image_count:04d}.{image_ext}"
                    
                    # 保存图片
                    with open(output_path, "wb") as f:
                        f.write(image_bytes)
                    
                    # 记录信息
                    info = {
                        'page': page_num + 1,
                        'width': image_width,
                        'height': image_height,
                        'format': image_ext,
                        'size_bytes': len(image_bytes)
                    }
                    
                    image_results.append((str(output_path), info))
                    
                    print(f"  ✅ 已提取: {output_path.name} ({image_width}x{image_height}px, {len(image_bytes)//1024}KB)")
                
                except Exception as e:
                    print(f"  ❌ 提取失败: {str(e)}")
        
        doc.close()
        
        print(f"\n完成！共提取 {len(image_results)} 张图片")
        return image_results
    
    def get_pdf_info(self, pdf_path) -> dict:
        """
        获取 PDF 文件信息
        
        Args:
            pdf_path: PDF 文件路径
        
        Returns:
            dict: PDF 信息字典
        """
        doc = fitz.open(pdf_path)
        
        info = {
            'pages': len(doc),
            'title': doc.metadata.get('title', ''),
            'author': doc.metadata.get('author', ''),
            'subject': doc.metadata.get('subject', ''),
            'keywords': doc.metadata.get('keywords', ''),
            'creator': doc.metadata.get('creator', ''),
            'producer': doc.metadata.get('producer', ''),
            'creation_date': doc.metadata.get('creationDate', ''),
            'mod_date': doc.metadata.get('modDate', ''),
        }
        
        # 计算总图片数
        total_images = 0
        for page_num in range(len(doc)):
            page = doc[page_num]
            total_images += len(page.get_images())
        
        info['total_images'] = total_images
        
        doc.close()
        
        return info
    
    def convert_page_range(self, pdf_path, output_folder, 
                          start_page, end_page, 
                          dpi=150) -> List[str]:
        """
        转换指定范围的 PDF 页面为图片
        
        Args:
            pdf_path: PDF 文件路径
            output_folder: 输出文件夹
            start_page: 起始页码（从 1 开始）
            end_page: 结束页码（包含）
            dpi: 图片分辨率
        
        Returns:
            list: 生成的图片路径列表
        """
        # 转换为 0-based 索引
        page_range = (start_page - 1, end_page)
        return self.pages_to_images(
            pdf_path, 
            output_folder, 
            dpi=dpi, 
            page_range=page_range
        )


# 便捷函数
def pdf_to_images(pdf_path, output_folder, dpi=150):
    """
    快速将 PDF 转为图片（便捷函数）
    
    Args:
        pdf_path: PDF 文件路径
        output_folder: 输出文件夹
        dpi: 图片分辨率
    
    Returns:
        list: 生成的图片路径列表
    """
    extractor = PDFExtractor()
    return extractor.pages_to_images(pdf_path, output_folder, dpi=dpi)


def extract_pdf_images(pdf_path, output_folder):
    """
    快速从 PDF 提取图片（便捷函数）
    
    Args:
        pdf_path: PDF 文件路径
        output_folder: 输出文件夹
    
    Returns:
        list: 提取的图片信息列表
    """
    extractor = PDFExtractor()
    return extractor.extract_images(pdf_path, output_folder)


# 使用示例
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python pdf_extractor.py <PDF文件路径>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    # 创建提取器
    extractor = PDFExtractor()
    
    # 显示 PDF 信息
    print("=" * 60)
    print("PDF 文件信息")
    print("=" * 60)
    info = extractor.get_pdf_info(pdf_path)
    for key, value in info.items():
        if value:
            print(f"{key}: {value}")
    
    # 将 PDF 页面转为图片
    print("\n" + "=" * 60)
    print("转换 PDF 页面为图片")
    print("=" * 60)
    extractor.pages_to_images(pdf_path, "./output/pages", dpi=150)
    
    # 提取 PDF 中的图片
    print("\n" + "=" * 60)
    print("提取 PDF 中的图片")
    print("=" * 60)
    extractor.extract_images(pdf_path, "./output/images")
