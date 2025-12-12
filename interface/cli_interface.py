"""
接口层：命令行接口
职责：参数解析、用户交互、结果显示
"""

import argparse
import sys
from typing import List
from service.pdf_service import PDFSplitService


class CLInterface:
    """命令行接口处理"""
    
    @staticmethod
    def parse_arguments() -> argparse.Namespace:
        """解析命令行参数"""
        parser = argparse.ArgumentParser(description="PDF文档分割工具")
        parser.add_argument("input_pdf", help="输入PDF文件路径")
        parser.add_argument("pages", nargs="+", type=int, 
                          help="分割点页码列表，如: 2 4 6 8 10")
        parser.add_argument("-o", "--output", default="output", 
                          help="输出目录 (默认: output)")
        
        return parser.parse_args()
    
    @staticmethod
    def run_cli() -> None:
        """运行命令行接口"""
        try:
            args = CLInterface.parse_arguments()
            CLInterface.start_split(args.input_pdf, args.pages, args.output)
        except Exception as e:
            print(f"错误: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    @staticmethod
    def start_split(input_pdf: str, page_breaks: List[int], output_dir: str) -> None:
        """
        启动PDF分割流程
        
        Args:
            input_pdf: 输入PDF路径
            page_breaks: 分割页码列表
            output_dir: 输出目录
        """
        service = PDFSplitService()
        
        print(f"开始分割PDF: {input_pdf}")
        print(f"分割点: {page_breaks}")
        print(f"输出目录: {output_dir}")
        print("-" * 50)
        
        output_files = service.split_pdf_by_pages(input_pdf, page_breaks, output_dir)
        
        print("分割完成!")
        print("生成的文件:")
        for i, file_path in enumerate(output_files, 1):
            print(f"  {i}. {file_path}")


def main():
    """主函数"""
    CLInterface.run_cli()


if __name__ == "__main__":
    main()