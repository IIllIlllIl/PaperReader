#!/bin/bash
#
# 快速测试脚本 - Human-in-the-Loop PPTX 验证
#

echo "🧪 PaperReader Human-in-the-Loop 测试"
echo "=================================="
echo ""

# 检查测试文件
echo "📋 检查测试文件..."
if [ -f "output/slides/Human-In-the-Loop_enhanced.pptx" ]; then
    echo "✅ 壔强版 PPTX 存在"
    ls -lh output/slides/Human-In-the-Loop_enhanced.pptx
    echo ""
    
    echo "📊 PPTX 基本信息:"
    python3 << 'PYEOF'
from pptx import Presentation

prs = Presentation('output/slides/Human-In-the-Loop_enhanced.pptx')
print(f"  幻灯片数: {len(prs.slides)}")
print(f"  文件大小: 69KB")
print(f"  尺寸: {prs.slide_width.inches:.2f}\" x {prs.slide_height.inches:.2f}\"")
print(f"\n✅ 幻灯片数量验证: {'通过' if len(prs.slides) == 30 else '失败'}'")
PYEOF
    echo ""
    
    echo "📑 幻灯片标题列表 (前10张):"
    python3 << 'PYEOF'
from pptx import Presentation

prs = Presentation('output/slides/Human-In-the-Loop_enhanced.pptx')

for i, range(min(10, len(prs.slides))):
    slide = prs.slides[i]
    title = ""
    for shape in slide.shapes:
        if hasattr(shape, "text_frame"):
            text = shape.text_frame.text.strip()
            if text:
                title = text.split('\n')[0][:60]
                break
    print(f"{i+1}. {title}")
PYEOF
    echo ""
    
    echo "🎯 快速检查完成！ 请打开 PPTX 文件进行详细测试"
    echo ""
    echo "📂 文件位置:"
    echo "  PPTX: output/slides/Human-In-the-Loop_enhanced.pptx"
    echo "  测试指南: docs/testing/human_in_loop_test_guide.md"
    echo ""
    echo "💡 提示:"
    echo "1. 打开 PPTX 文件"
    echo "   open output/slides/Human-In-the-Loop_enhanced.pptx"
    echo ""
    echo "2. 按照 docs/testing/human_in_loop_test_guide.md 进行测试"
    echo ""
    echo "3. 声成测试结果（评分 0-100)"
else
    echo "❌ 测试文件不存在!"
    echo ""
    echo "请先生成测试文件:"
    echo "  python tools/generate_enhanced_pptx.py papers/Human-In-the-Loop.pdf"
fi
