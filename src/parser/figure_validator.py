"""
图形清单验证模块
用于验证PDF中的所有Figure和Table是否都被提取
"""
import re
import fitz
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FigureInfo:
    """图形信息"""
    type: str  # 'figure' 或 'table'
    number: int
    page: int
    caption: str
    extracted: bool = False
    image_path: str = ""


class FigureValidator:
    """图形验证器"""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.figures: Dict[Tuple[str, int], FigureInfo] = {}

    def scan_captions(self) -> List[FigureInfo]:
        """
        扫描PDF中的所有Figure/Table标题
        返回应该存在的所有图形清单
        """
        # 更精确的模式：必须跟标点符号（.或:），表示独立标题
        patterns = {
            'figure': [
                r'Fig\.?\s*(\d+)[.:]\s+',      # "Fig. 1:" or "Fig 1."
                r'Figure\s+(\d+)[.:]\s+',      # "Figure 1:" or "Figure 1."
                r'FIGURE\s+(\d+)[.:]\s+',      # "FIGURE 1:"
            ],
            'table': [
                r'Table\s+(\d+)[.:]\s+',       # "Table 1:" or "Table 1."
                r'TABLE\s+(\d+)[.:]\s+',       # "TABLE 1:"
                r'Tbl\.?\s*(\d+)[.:]\s+',      # "Tbl. 1:"
            ]
        }

        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text()

            for fig_type, fig_patterns in patterns.items():
                for pattern in fig_patterns:
                    matches = list(re.finditer(pattern, text))

                    for match in matches:
                        number = int(match.group(1))

                        # 提取完整标题
                        caption = self._extract_caption(text, match)

                        # 创建图形信息
                        fig_info = FigureInfo(
                            type=fig_type,
                            number=number,
                            page=page_num + 1,
                            caption=caption
                        )

                        # 存入字典（避免重复）
                        key = (fig_type, number)
                        if key not in self.figures:
                            self.figures[key] = fig_info

        return list(self.figures.values())

    def _extract_caption(self, text: str, match) -> str:
        """提取完整的标题文字"""
        # 找到匹配位置所在的行
        start = match.start()
        lines_before = text[:start].split('\n')

        # 获取当前行
        if lines_before:
            current_line_start = start - len(lines_before[-1])
            remaining_text = text[current_line_start:]
            current_line = remaining_text.split('\n')[0]
            return current_line.strip()

        return match.group(0)

    def validate_extraction(self, extracted_figures: List[Dict]) -> Dict:
        """
        验证提取结果

        Args:
            extracted_figures: extract_key_figures() 返回的列表

        Returns:
            验证报告
        """
        # 标记已提取的图形
        extracted_numbers = set()
        for fig in extracted_figures:
            fig_num = fig.get('figure_num')
            if fig_num:
                extracted_numbers.add(fig_num)
                # 检查是否在预期清单中
                if ('figure', fig_num) in self.figures:
                    self.figures[('figure', fig_num)].extracted = True
                    self.figures[('figure', fig_num)].image_path = fig.get('image_path', '')

        # 生成报告
        report = {
            'total_figures': len(self.figures),
            'extracted': [],
            'missing': [],
            'extra': []  # 提取了但不在清单中的
        }

        # 检查每个预期图形
        for (fig_type, num), info in self.figures.items():
            if info.extracted:
                report['extracted'].append(info)
            else:
                report['missing'].append(info)

        # 检查额外提取的（编号不在预期中）
        for fig_num in extracted_numbers:
            if ('figure', fig_num) not in self.figures:
                report['extra'].append(fig_num)

        return report

    def generate_report_markdown(self, report: Dict) -> str:
        """生成Markdown格式的报告"""
        lines = []
        lines.append(f"# Figure/Table Extraction Validation Report\n")
        lines.append(f"**PDF**: `{Path(self.pdf_path).name}`\n")
        lines.append(f"**Total Expected**: {report['total_figures']} figures/tables\n")

        # 统计
        success_rate = len(report['extracted']) / report['total_figures'] * 100 if report['total_figures'] > 0 else 0
        lines.append(f"**Success Rate**: {success_rate:.1f}%\n")

        # 提取成功
        lines.append(f"\n## ✅ Extracted Successfully ({len(report['extracted'])})\n")
        if report['extracted']:
            for fig in sorted(report['extracted'], key=lambda x: (x.type, x.number)):
                icon = "📊" if fig.type == "table" else "📈"
                lines.append(f"- {icon} **{fig.type.upper()} {fig.number}** (Page {fig.page}): {fig.caption[:60]}...")
        else:
            lines.append("- *None extracted*\n")

        # 缺失
        lines.append(f"\n## ❌ Missing ({len(report['missing'])})\n")
        if report['missing']:
            for fig in sorted(report['missing'], key=lambda x: (x.type, x.number)):
                icon = "📊" if fig.type == "table" else "📈"
                lines.append(f"- {icon} **{fig.type.upper()} {fig.number}** (Page {fig.page}): {fig.caption[:60]}...")
        else:
            lines.append("- *None - All figures extracted!* 🎉\n")

        # 额外提取的
        lines.append(f"\n## ⚠️ Extra Extractions ({len(report['extra'])})\n")
        if report['extra']:
            for fig_num in report['extra']:
                lines.append(f"- Figure {fig_num} (not in expected list)")
        else:
            lines.append("- *None*\n")

        # 建议
        lines.append(f"\n## 💡 Recommendations\n")
        if report['missing']:
            lines.append("1. Check if missing figures have non-standard captions")
            lines.append("2. Verify if figures are on separate pages")
            lines.append("3. Consider increasing `max_figures` parameter")
        else:
            lines.append("✅ All expected figures have been extracted successfully!")

        return "\n".join(lines)

    def close(self):
        """关闭PDF文档"""
        if self.doc:
            self.doc.close()


def validate_pdf_figures(pdf_path: str, extracted_figures: List[Dict]) -> Dict:
    """
    便捷函数：验证PDF图形提取

    Args:
        pdf_path: PDF文件路径
        extracted_figures: extract_key_figures() 的返回值

    Returns:
        验证报告
    """
    validator = FigureValidator(pdf_path)
    try:
        validator.scan_captions()
        return validator.validate_extraction(extracted_figures)
    finally:
        validator.close()


# 命令行接口
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        print(f"📄 Validating: {pdf_path}")
        print("=" * 60)

        # 需要先提取图形
        try:
            from pdf_image_extractor import PDFImageExtractor
        except ImportError:
            from src.parser.pdf_image_extractor import PDFImageExtractor

        # 提取
        extractor = PDFImageExtractor()
        figures = extractor.extract_key_figures(pdf_path)
        print(f"\n✅ Extracted: {len(figures)} figures")

        # 验证
        validator = FigureValidator(pdf_path)
        expected = validator.scan_captions()
        print(f"📋 Expected: {len(expected)} figures")

        report = validator.validate_extraction(figures)

        # 输出报告
        print("\n" + validator.generate_report_markdown(report))

        # 保存报告
        report_path = f"outputs/validation_{Path(pdf_path).stem}.md"
        Path("outputs").mkdir(exist_ok=True)
        with open(report_path, "w") as f:
            f.write(validator.generate_report_markdown(report))
        print(f"\n📁 Report saved to: {report_path}")

        validator.close()
    else:
        print("Usage: python figure_validator.py <pdf_path>")
