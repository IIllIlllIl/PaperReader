#!/usr/bin/env python3
"""
数据流程追踪工具

使用此工具处理论文时会输出详细的中间产物信息，
帮助理解数据转换过程。

使用方法:
    python debug_data_flow.py papers/your_paper.pdf
"""

import sys
import json
from pathlib import Path
from typing import Any
import click

from src.utils import load_config, setup_logging, get_file_hash, get_api_key
from src.pdf_parser import PDFParser
from src.pdf_validator import PDFValidator
from src.ai_analyzer import AIAnalyzer
from src.content_extractor import ContentExtractor
from src.ppt_generator import PPTGenerator
from src.cache_manager import CacheManager


def print_section(title: str):
    """打印分节标题"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


def print_data(name: str, data: Any, max_length: int = 500):
    """打印数据（带截断）"""
    print(f"\n{name}:")
    print('-' * 70)

    if isinstance(data, str):
        if len(data) > max_length:
            print(data[:max_length])
            print(f"\n... [已截断，总长度: {len(data)} 字符]")
        else:
            print(data)
    elif isinstance(data, (dict, list)):
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        if len(json_str) > max_length:
            print(json_str[:max_length])
            print(f"\n... [已截断，总长度: {len(json_str)} 字符]")
        else:
            print(json_str)
    else:
        print(data)


@click.command()
@click.argument('paper_path', type=click.Path(exists=True))
@click.option('--skip-ai', is_flag=True, help='跳过AI分析（使用模拟数据）')
def debug_flow(paper_path: str, skip_ai: bool):
    """
    追踪论文处理的数据流程

    输出每个阶段的中间产物，帮助理解数据转换过程
    """

    print_section("PaperReader 数据流程追踪")
    print(f"论文路径: {paper_path}")
    print(f"模式: {'跳过AI分析（使用模拟数据）' if skip_ai else '完整流程'}")

    # 加载配置
    config = load_config()
    logger = setup_logging(config)

    # ========================================
    # 阶段1: PDF验证
    # ========================================
    print_section("阶段1: PDF验证与质量检测")

    validator = PDFValidator(paper_path)
    validation_result = validator.validate()

    print_data("验证结果", {
        "is_valid": validation_result.is_valid,
        "quality": validation_result.quality.value,
        "layout_type": validation_result.layout_type.value,
        "page_count": validation_result.page_count,
        "has_text": validation_result.has_text,
        "text_ratio": f"{validation_result.text_ratio:.2%}",
        "issues": validation_result.issues,
        "recommendations": validation_result.recommendations
    })

    if not validation_result.is_valid:
        print("\n❌ PDF验证失败，无法继续处理")
        sys.exit(1)

    # ========================================
    # 阶段2: PDF文本提取
    # ========================================
    print_section("阶段2: PDF文本提取")

    parser = PDFParser(paper_path)

    # 提取完整文本
    paper_text = parser.extract_text()
    print_data("提取的文本（前500字符）", paper_text, max_length=500)
    print(f"\n文本统计:")
    print(f"  总字符数: {len(paper_text):,}")
    print(f"  总单词数（估算）: {len(paper_text.split()):,}")
    print(f"  总行数: {len(paper_text.splitlines()):,}")

    # 提取章节
    sections = parser.extract_sections()
    print_data("识别的章节", list(sections.keys()))
    if sections:
        print("\n章节内容示例（第一个章节的前200字符）:")
        first_section = list(sections.keys())[0]
        print(f"  {first_section}: {sections[first_section][:200]}...")

    # 提取元数据
    metadata = parser.extract_metadata()
    print_data("提取的元数据", {
        "title": metadata.title,
        "authors": metadata.authors,
        "year": metadata.year,
        "venue": metadata.venue,
        "abstract": metadata.abstract[:200] + "..." if metadata.abstract and len(metadata.abstract) > 200 else metadata.abstract
    })

    # ========================================
    # 阶段3: 缓存检查
    # ========================================
    print_section("阶段3: 缓存检查")

    pdf_hash = get_file_hash(paper_path)
    print_data("PDF文件哈希", pdf_hash)

    cache_manager = CacheManager(cache_dir=config['cache']['cache_dir'])
    cached = cache_manager.get_cached_analysis(pdf_hash)

    if cached:
        print("\n✓ 找到缓存的分析结果")
        print(f"缓存包含以下内容: {list(cached.keys())}")
        print("使用缓存数据，跳过AI分析...")
        analysis_dict = cached['analysis']
        presentation_content_dict = cached['presentation_content']
    else:
        print("\n✗ 未找到缓存")
        print("将进行新的AI分析...")

    # ========================================
    # 阶段4: AI分析
    # ========================================
    if not cached and not skip_ai:
        print_section("阶段4: AI分析")

        try:
            api_key = get_api_key(config)
        except ValueError as e:
            print(f"\n❌ 错误: {e}")
            print("提示: 使用 --skip-ai 选项跳过AI分析")
            sys.exit(1)

        analyzer = AIAnalyzer(
            api_key=api_key,
            model=config['ai']['model']
        )

        print(f"\n开始AI分析...")
        print(f"使用模型: {config['ai']['model']}")

        analysis = analyzer.analyze_paper(paper_text, metadata.__dict__)

        print_data("AI分析结果", {
            "problem": analysis.problem,
            "motivation": analysis.motivation,
            "method": analysis.method[:300] + "...",
            "innovations": analysis.innovations,
            "results": analysis.results,
            "pros": analysis.pros,
            "cons": analysis.cons,
            "conclusions": analysis.conclusions[:300] + "..."
        }, max_length=1000)

        print(f"\nAI使用统计:")
        stats = analyzer.get_stats()
        print(f"  API调用次数: {stats['call_count']}")
        print(f"  总Token数: {stats['total_tokens']:,}")
        print(f"  总成本: ${stats['total_cost']:.4f}")

    elif skip_ai:
        print_section("阶段4: AI分析 (跳过 - 使用模拟数据)")

        # 使用模拟数据
        from examples.middle_products_example import paper_analysis_example
        analysis_dict = paper_analysis_example
        print("使用示例数据代替真实AI分析")
        print_data("模拟的分析结果", {
            "problem": analysis_dict['problem'][:200],
            "innovations": analysis_dict['innovations'][:3],
            "results": analysis_dict['results'][:3]
        })

    # ========================================
    # 阶段5: 演示内容生成
    # ========================================
    print_section("阶段5: 演示内容生成")

    if not cached and not skip_ai:
        # 从analysis对象生成
        presentation_content = analyzer.generate_presentation_content(analysis, metadata.__dict__)
        presentation_content_dict = presentation_content.__dict__
    elif skip_ai:
        # 使用示例数据
        from examples.middle_products_example import presentation_content_example
        presentation_content_dict = presentation_content_example

    print_data("演示内容（部分）", {
        "title": presentation_content_dict['title'],
        "authors": presentation_content_dict['authors'],
        "motivation": presentation_content_dict['motivation'],
        "innovations": presentation_content_dict['innovations'][:3],
        "main_results": presentation_content_dict['main_results'][:3],
        "pros": presentation_content_dict['pros'][:3],
        "cons": presentation_content_dict['cons'][:3]
    }, max_length=800)

    # ========================================
    # 阶段6: 缓存保存
    # ========================================
    if not cached:
        print_section("阶段6: 保存到缓存")

        cache_file = cache_manager.cache_dir / f"{pdf_hash}.json"
        print(f"缓存文件位置: {cache_file}")
        print(f"缓存内容: analysis + presentation_content")

        # 保存到缓存
        cache_manager.save_analysis(
            pdf_hash,
            analysis_dict if skip_ai else analysis.__dict__,
            metadata={'model': config['ai']['model']}
        )
        print("✓ 已保存到缓存")

    # ========================================
    # 阶段7: 幻灯片内容提取
    # ========================================
    print_section("阶段7: 幻灯片内容提取")

    content_extractor = ContentExtractor()

    # 如果使用真实analysis对象
    if not skip_ai and not cached:
        organized_presentation = content_extractor.extract_slide_content(
            analysis, presentation_content
        )
    else:
        # 使用字典数据构造对象
        from src.ai_analyzer import PaperAnalysis, PresentationContent
        from dataclasses import dataclass

        # 简化：直接使用示例中的organized_slides_example
        from examples.middle_products_example import organized_slides_example
        print("使用示例幻灯片数据")
        print_data("幻灯片列表（前5个）", organized_slides_example[:5])

    if not skip_ai and not cached:
        print(f"\n生成了 {organized_presentation.total_slides} 个幻灯片")
        print("\n幻灯片标题列表:")
        for i, slide in enumerate(organized_presentation.slides[:10], 1):
            print(f"  {i}. {slide.title}")
        if organized_presentation.total_slides > 10:
            print(f"  ... 还有 {organized_presentation.total_slides - 10} 个幻灯片")

    # ========================================
    # 阶段8: Markdown生成
    # ========================================
    print_section("阶段8: Markdown生成")

    ppt_generator = PPTGenerator()

    if not skip_ai and not cached:
        markdown = ppt_generator.generate_markdown(organized_presentation)
    else:
        from examples.middle_products_example import markdown_output_example
        markdown = markdown_output_example

    print_data("生成的Markdown（前800字符）", markdown, max_length=800)

    # 统计
    slide_count = markdown.count('---') - 1  # 减去front matter的分隔符
    print(f"\nMarkdown统计:")
    print(f"  总字符数: {len(markdown):,}")
    print(f"  总行数: {len(markdown.splitlines()):,}")
    print(f"  幻灯片数（估算）: {slide_count}")

    # ========================================
    # 阶段9: 文件保存
    # ========================================
    print_section("阶段9: 保存文件")

    paper_name = Path(paper_path).stem

    # 保存Markdown
    markdown_dir = Path(config['presentation']['output_dir']) / 'markdown'
    markdown_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = markdown_dir / f"{paper_name}_debug.md"

    ppt_generator.save_presentation(markdown, str(markdown_path))
    print(f"✓ Markdown已保存: {markdown_path}")

    # ========================================
    # 总结
    # ========================================
    print_section("数据流程追踪完成")

    print("\n📋 中间产物总结:")
    print("  1. PDF验证结果 ✓")
    print("  2. 提取的文本 ✓")
    print("  3. 论文元数据 ✓")
    print("  4. PDF文件哈希 ✓")
    print("  5. AI分析结果 ✓")
    print("  6. 演示内容 ✓")
    print("  7. 缓存文件 ✓")
    print("  8. 幻灯片组织 ✓")
    print("  9. Markdown输出 ✓")

    print("\n📁 输出文件:")
    print(f"  - {markdown_path}")

    print("\n💡 提示:")
    print("  - 所有中间产物已显示在上方")
    print("  - 要查看完整数据，请查看缓存文件:")
    print(f"    cache/{pdf_hash}.json")
    print("  - 要查看示例中间产物，请查看:")
    print("    examples/middle_products_example.py")


if __name__ == '__main__':
    debug_flow()
