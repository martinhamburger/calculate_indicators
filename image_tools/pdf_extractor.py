"""
PDF Image Extractor

Extract images from PDF documents using PyMuPDF.
"""

import os
from pathlib import Path
from typing import List, Optional


class PDFExtractor:
    """Extract images from PDF documents."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize PDF extractor.
        
        Args:
            pdf_path: Path to the PDF file
        """
        self.pdf_path = pdf_path
        self.pdf_document = None
        
    def extract_all_images(self, output_dir: Optional[str] = None) -> List[str]:
        """
        Extract all images from the PDF.
        
        Args:
            output_dir: Directory to save extracted images. If None, uses './extracted_images'
            
        Returns:
            List of paths to extracted image files
        """
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError(
                "PyMuPDF is required for PDF extraction. "
                "Install it with: pip install PyMuPDF"
            )
        
        if output_dir is None:
            output_dir = './extracted_images'
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        extracted_files = []
        
        try:
            self.pdf_document = fitz.open(self.pdf_path)
            
            for page_num in range(len(self.pdf_document)):
                page = self.pdf_document[page_num]
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = self.pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # Generate filename
                    pdf_name = Path(self.pdf_path).stem
                    image_filename = os.path.join(
                        output_dir, 
                        f"{pdf_name}_page{page_num+1}_img{img_index+1}.{image_ext}"
                    )
                    
                    # Save image
                    with open(image_filename, "wb") as image_file:
                        image_file.write(image_bytes)
                    
                    extracted_files.append(image_filename)
                    print(f"Extracted: {image_filename}")
            
            return extracted_files
            
        finally:
            if self.pdf_document:
                self.pdf_document.close()
    
    def extract_page_as_image(self, page_num: int, output_path: str, 
                             dpi: int = 300) -> str:
        """
        Convert a PDF page to an image.
        
        Args:
            page_num: Page number (0-indexed)
            output_path: Path to save the image
            dpi: Resolution in DPI (default: 300)
            
        Returns:
            Path to the saved image
        """
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError(
                "PyMuPDF is required for PDF extraction. "
                "Install it with: pip install PyMuPDF"
            )
        
        try:
            self.pdf_document = fitz.open(self.pdf_path)
            
            if page_num >= len(self.pdf_document):
                raise ValueError(f"Page {page_num} does not exist in PDF")
            
            page = self.pdf_document[page_num]
            
            # Convert page to image
            zoom = dpi / 72  # 72 is the default DPI
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Save image
            pix.save(output_path)
            print(f"Saved page {page_num} to: {output_path}")
            
            return output_path
            
        finally:
            if self.pdf_document:
                self.pdf_document.close()
    
    def get_page_count(self) -> int:
        """
        Get the total number of pages in the PDF.
        
        Returns:
            Number of pages
        """
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError(
                "PyMuPDF is required for PDF extraction. "
                "Install it with: pip install PyMuPDF"
            )
        
        try:
            self.pdf_document = fitz.open(self.pdf_path)
            return len(self.pdf_document)
        finally:
            if self.pdf_document:
                self.pdf_document.close()


# Command-line usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_extractor.py <pdf_file> [output_dir]")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './extracted_images'
    
    extractor = PDFExtractor(pdf_file)
    
    print(f"Extracting images from: {pdf_file}")
    print(f"Output directory: {output_dir}")
    print(f"Total pages: {extractor.get_page_count()}")
    print()
    
    images = extractor.extract_all_images(output_dir)
    
    print()
    print(f"Extraction complete! Total images extracted: {len(images)}")
