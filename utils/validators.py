"""
工具类：输入验证
"""

import os
from typing import List


class PDFValidator:
    """PDF参数验证器"""
    
    @staticmethod
    def validate_input(input_pdf: str, page_breaks: List[int], output_dir: str) -> None:
        """验证输入参数"""
        if not os.path.exists(input_pdf):
            raise ValueError(f"输入文件不存在: {input_pdf}")
        
        if not input_pdf.lower().endswith('.pdf'):
            raise ValueError("输入文件必须是PDF格式")
        
        if not page_breaks:
            raise ValueError("必须提供至少一个分割点")
        
        if any(page <= 0 for page in page_breaks):
            raise ValueError("页码必须是正整数")
    
    @staticmethod
    def validate_page_ranges(page_breaks: List[int], total_pages: int) -> None:
        """验证页码范围"""
        if not page_breaks:
            return
            
        sorted_pages = sorted(page_breaks)
        if sorted_pages != page_breaks:
            raise ValueError("页码必须按升序排列")
        
        if sorted_pages[0] < 1:
            raise ValueError("页码必须大于0")
        
        if sorted_pages[-1] > total_pages:
            raise ValueError(f"分割点不能超过PDF总页数({total_pages})")