"""
执行层：PDF文件操作原子化功能
职责：PDF读取、页面切割、文件保存等基础操作
"""

import PyPDF2
from typing import List


class PDFOperator:
    """PDF操作执行类"""
    
    @staticmethod
    def read_pdf(file_path: str) -> PyPDF2.PdfReader:
        """
        读取PDF文件
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            PdfReader对象
            
        Raises:
            FileNotFoundError: 文件不存在
            PyPDF2.PdfReadError: PDF读取错误
        """
        try:
            # 使用二进制模式打开文件，并保持文件打开状态
            file_obj = open(file_path, 'rb')
            return PyPDF2.PdfReader(file_obj)
        except FileNotFoundError:
            raise FileNotFoundError(f"PDF文件不存在: {file_path}")
        except Exception as e:
            raise PyPDF2.PdfReadError(f"PDF读取失败: {str(e)}")
    
    @staticmethod
    def extract_pages(reader: PyPDF2.PdfReader, start_page: int, end_page: int) -> PyPDF2.PdfWriter:
        """
        提取指定页面范围
        
        Args:
            reader: PDF读取器
            start_page: 起始页码(0-based)
            end_page: 结束页码(0-based, 不包含)
            
        Returns:
            PdfWriter对象包含提取的页面
            
        Raises:
            ValueError: 页码范围无效
        """
        if start_page < 0 or end_page > len(reader.pages) or start_page >= end_page:
            raise ValueError(f"无效的页面范围: {start_page}-{end_page}")
            
        writer = PyPDF2.PdfWriter()
        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])
            
        return writer
    
    @staticmethod
    def save_pdf(writer: PyPDF2.PdfWriter, output_path: str) -> None:
        """
        保存PDF文件
        
        Args:
            writer: PDF写入器
            output_path: 输出文件路径
            
        Raises:
            IOError: 文件保存失败
        """
        try:
            with open(output_path, 'wb') as file:
                writer.write(file)
        except Exception as e:
            raise IOError(f"PDF保存失败: {str(e)}")