"""
能力层：PDF分割业务逻辑
职责：输入校验、业务逻辑组合、错误处理
"""

import os
from typing import List
from execution.pdf_operations import PDFOperator
from loop.batch_processor import BatchPDFProcessor
from utils.validators import PDFValidator


class PDFSplitService:
    """PDF分割服务"""
    
    def __init__(self):
        self.validator = PDFValidator()
        self.pdf_operator = PDFOperator()
        self.processor = BatchPDFProcessor()
    
    def split_pdf_by_pages(self, input_pdf: str, page_breaks: List[int], 
                          output_dir: str = "output") -> List[str]:
        """
        根据页码分割PDF
        
        Args:
            input_pdf: 输入PDF文件路径
            page_breaks: 分割点页码列表
            output_dir: 输出目录
            
        Returns:
            生成的PDF文件路径列表
            
        Raises:
            ValueError: 输入参数无效
            Exception: 分割处理失败
        """
        # 输入校验
        self.validator.validate_input(input_pdf, page_breaks, output_dir)
        
        # 读取PDF
        pdf_reader = self.pdf_operator.read_pdf(input_pdf)
        total_pages = len(pdf_reader.pages)
        
        # 校验页码范围
        self.validator.validate_page_ranges(page_breaks, total_pages)
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 处理分割
        def process_split(start: int, end: int, index: int) -> str:
            output_file = os.path.join(output_dir, f"split_{index+1}.pdf")
            writer = self.pdf_operator.extract_pages(pdf_reader, start, end)
            self.pdf_operator.save_pdf(writer, output_file)
            return output_file
        
        # 批量处理
        output_files = self.processor.process_split_ranges(
            page_breaks, total_pages, process_split
        )
        
        return output_files