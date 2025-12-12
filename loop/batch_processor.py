"""
重复层：批量处理PDF分割任务
职责：循环执行任务、采样、批处理、重试逻辑
"""

import logging
from typing import List, Tuple, Callable

logger = logging.getLogger(__name__)


class BatchPDFProcessor:
    """批量PDF处理器"""
    
    @staticmethod
    def process_split_ranges(page_breaks: List[int], total_pages: int, 
                           process_func: Callable) -> List[str]:
        """
        处理所有分割区间
        
        Args:
            page_breaks: 分割点页码列表
            total_pages: PDF总页数
            process_func: 处理函数
            
        Returns:
            生成的PDF文件路径列表
        """
        output_files = []
        ranges = BatchPDFProcessor._generate_ranges(page_breaks, total_pages)
        
        for i, (start, end) in enumerate(ranges):
            logger.info(f"处理分割区间 {i+1}: {start}-{end}")
            
            # 重试逻辑
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    output_file = process_func(start, end, i)
                    output_files.append(output_file)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"分割区间 {start}-{end} 处理失败: {str(e)}")
                        raise
                    logger.warning(f"第{attempt+1}次尝试失败，重试...")
                    
        return output_files
    
    @staticmethod
    def _generate_ranges(page_breaks: List[int], total_pages: int) -> List[Tuple[int, int]]:
        """生成分割区间列表 - 修正后的逻辑"""
        ranges = []
        
        # 如果没有分割点，返回空列表
        if not page_breaks:
            return ranges
            
        # 排序页码
        sorted_breaks = sorted(page_breaks)
        
        # 生成相邻分割点的区间
        for i in range(len(sorted_breaks)-1):
            start = sorted_breaks[i]
            end = sorted_breaks[i+1]
            if end > total_pages:
                end = total_pages
            if start < end:
                ranges.append((start, end))
        
        # 处理最后一个分割点到文档末尾
        if sorted_breaks[-1] < total_pages:
            ranges.append((sorted_breaks[-1], total_pages))
            
        return ranges