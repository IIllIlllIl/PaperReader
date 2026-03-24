#!/usr/bin/env python3
"""
图形提取验证示例
演示如何验证PDF图形提取的完整性
"""
import sys
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parser.pdf_image_extractor import PDFImageExtractor
from src.parser.figure_validator import FigureValidator


def validate_and_extract(pdf_path: str, max_figures: int = 20):
    """
    提取并验证PDF图形

    Args:
        pdf_path: PDF文件路径
        max_figures: 最大提取图形数
    """
    print(f"📄 Processing: {pdf_path}")
    print("=" * 60)

    # 1. 先扫描预期图形
    print(f"\n🔍 Step 1: Scanning expected figures...")
    validator = FigureValidator(pdf_path)
    expected = validator.scan_captions()
    print(f"   Found: {len(expected)} expected figures/tables")

    if expected:
        print(f"\n   Expected list:")
        for fig in expected[:5]:  # 显示前5个
            icon = "📊" if fig.type == "table" else "📈"
            print(f"   {icon} {fig.type.upper()} {fig.number} (Page {fig.page}): {fig.caption[:50]}...")
        if len(expected) > 5:
            print(f"   ... and {len(expected) - 5} more")

    # 2. 提取图形
    print(f"\n📸 Step 2: Extracting figures...")
    extractor = PDFImageExtractor(output_dir="outputs/images")
    extracted = extractor.extract_key_figures(pdf_path, max_figures=max_figures)
    print(f"   Extracted: {len(extracted)} figures")

    # 分类
    caption_count = sum(1 for f in extracted if 'figure_' in f['image_path'])
    embedded_count = sum(1 for f in extracted if 'embedded_' in f['image_path'])
    print(f"   - Caption-based: {caption_count}")
    print(f"   - Embedded: {embedded_count}")

    # 3. 验证
    print(f"\n✅ Step 3: Validating extraction...")
    report = validator.validate_extraction(extracted)

    success_rate = len(report['extracted']) / len(expected) * 100 if expected else 0
    print(f"\n   Results:")
    print(f"   - Success: {len(report['extracted'])} / {len(expected)} ({success_rate:.1f}%)")
    print(f"   - Missing: {len(report['missing'])}")
    print(f"   - Extra: {len(report['extra'])}")

    # 4. 显示缺失
    if report['missing']:
        print(f"\n❌ Missing figures:")
        for fig in report['missing']:
            icon = "📊" if fig.type == "table" else "📈"
            print(f"   {icon} {fig.type.upper()} {fig.number} (Page {fig.page})")

    # 5. 保存报告
    report_path = Path("outputs") / f"validation_{Path(pdf_path).stem}.md"
    report_path.parent.mkdir(exist_ok=True)
    with open(report_path, "w") as f:
        f.write(validator.generate_report_markdown(report))
    print(f"\n📁 Validation report saved to: {report_path}")

    # 6. 清理
    validator.close()

    return report


def main():
    """主函数"""
    # 默认PDF
    pdf_path = "papers/Human-In-the-Loop.pdf"

    # 命令行参数
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]

    if not Path(pdf_path).exists():
        print(f"❌ Error: File not found: {pdf_path}")
        sys.exit(1)

    # 运行验证
    report = validate_and_extract(pdf_path)

    # 返回码
    if report['missing']:
        print(f"\n⚠️  Warning: {len(report['missing'])} figures are missing!")
        sys.exit(1)
    else:
        print(f"\n✅ Success: All expected figures extracted!")
        sys.exit(0)


if __name__ == "__main__":
    main()
