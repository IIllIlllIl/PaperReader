#!/bin/bash
# 归档开发遗留文件
# 日期: 2026-03-06

ARCHIVE_DIR="docs/archived/legacy_$(date +%Y%m%d)"
mkdir -p "$ARCHIVE_DIR"

echo "📦 开始归档遗留文件..."
echo ""

# 1. Python脚本
echo "Python脚本:"
mkdir -p "$ARCHIVE_DIR/scripts"

if [ -f "main.py" ]; then
    mv main.py "$ARCHIVE_DIR/scripts/"
    echo "  ✓ main.py (兼容性包装器)"
fi

if [ -f "cli/main_backup_enhanced_version.py" ]; then
    mv cli/main_backup_enhanced_version.py "$ARCHIVE_DIR/scripts/"
    echo "  ✓ cli/main_backup_enhanced_version.py (备份文件)"
fi

if [ -f "tools/debug_data_flow.py" ]; then
    mv tools/debug_data_flow.py "$ARCHIVE_DIR/scripts/"
    echo "  ✓ tools/debug_data_flow.py (调试工具)"
fi

if [ -f "examples/middle_products_example.py" ]; then
    mv examples/middle_products_example.py "$ARCHIVE_DIR/scripts/"
    echo "  ✓ examples/middle_products_example.py (示例文件)"
fi

# 2. Shell脚本
echo ""
echo "Shell脚本:"
mkdir -p "$ARCHIVE_DIR/shell"

if [ -f "tools/reorganize_project.sh" ]; then
    mv tools/reorganize_project.sh "$ARCHIVE_DIR/shell/"
    echo "  ✓ tools/reorganize_project.sh (一次性重组脚本)"
fi

if [ -f "tools/update_docs_after_refactor.sh" ]; then
    mv tools/update_docs_after_refactor.sh "$ARCHIVE_DIR/shell/"
    echo "  ✓ tools/update_docs_after_refactor.sh (一次性更新脚本)"
fi

if [ -f "tools/install_skill.sh" ]; then
    mv tools/install_skill.sh "$ARCHIVE_DIR/shell/"
    echo "  ✓ tools/install_skill.sh (skill安装脚本)"
fi

if [ -f "tools/test_skill.sh" ]; then
    mv tools/test_skill.sh "$ARCHIVE_DIR/shell/"
    echo "  ✓ tools/test_skill.sh (skill测试脚本)"
fi

if [ -f "tools/quick_test.sh" ]; then
    mv tools/quick_test.sh "$ARCHIVE_DIR/shell/"
    echo "  ✓ tools/quick_test.sh (快速测试脚本)"
fi

# 3. Skills目录
echo ""
echo "Skills目录:"
if [ -d "skills" ]; then
    mv skills "$ARCHIVE_DIR/"
    echo "  ✓ skills/ (skill功能目录)"
fi

# 4. 重复文档
echo ""
echo "重复文档:"
mkdir -p "$ARCHIVE_DIR/docs"

if [ -f "PROJECT_SUMMARY.md" ]; then
    mv PROJECT_SUMMARY.md "$ARCHIVE_DIR/docs/"
    echo "  ✓ PROJECT_SUMMARY.md (与docs/重复)"
fi

if [ -f "FINAL_SUMMARY.md" ]; then
    mv FINAL_SUMMARY.md "$ARCHIVE_DIR/docs/"
    echo "  ✓ FINAL_SUMMARY.md (临时总结)"
fi

# 5. 调试输出文件
echo ""
echo "调试输出:"
if [ -f "output/markdown/Human-In-the-Loop_debug.md" ]; then
    mv output/markdown/Human-In-the-Loop_debug.md "$ARCHIVE_DIR/docs/"
    echo "  ✓ Human-In-the-Loop_debug.md (调试文件)"
fi

# 6. Examples目录
echo ""
echo "Examples目录:"
if [ -d "examples" ]; then
    # 检查是否为空
    if [ -z "$(ls -A examples 2>/dev/null)" ]; then
        rmdir examples
        echo "  ✓ examples/ (空目录已删除)"
    fi
fi

# 创建归档说明
cat > "$ARCHIVE_DIR/README.md" << 'EOFREADME'
# Legacy Files Archive

This directory contains archived files that are no longer used in the main workflow.

## Archive Date
$(date +%Y-%m-%d)

## Archived Files

### Scripts
- `main.py` - Compatibility wrapper (replaced by cli/main.py)
- `cli/main_backup_enhanced_version.py` - Backup file
- `tools/debug_data_flow.py` - Debug tool
- `examples/middle_products_example.py` - Example file

### Shell Scripts
- `tools/reorganize_project.sh` - One-time reorganization script
- `tools/update_docs_after_refactor.sh` - One-time update script
- `tools/install_skill.sh` - Skill installation script
- `tools/test_skill.sh` - Skill testing script
- `tools/quick_test.sh` - Quick test script

### Skills Directory
- `skills/` - Complete skill functionality directory (not part of main workflow)

### Documentation
- `PROJECT_SUMMARY.md` - Duplicate of docs/architecture/PROJECT_SUMMARY.md
- `FINAL_SUMMARY.md` - Temporary summary document
- `Human-In-the-Loop_debug.md` - Debug output file

## Current Main Workflow

### Entry Points
- **Standard**: `python cli/main.py process --paper <file.pdf>`
- **Enhanced**: `python tools/generate_enhanced_pptx.py <file.pdf>`

### Core Modules
- `src/ai_analyzer_enhanced.py` - Enhanced AI analyzer (V3)
- `src/content_extractor_enhanced.py` - Enhanced content extractor (V3)
- `src/ppt_generator_enhanced.py` - Enhanced PPT generator (V3)
- `src/pdf_parser.py` - PDF text extraction
- `src/cache_manager.py` - Analysis caching
- `src/resilience.py` - Retry logic
- `src/progress_reporter.py` - Progress bars
- `src/utils.py` - Utilities

### Tools
- `tools/generate_enhanced_pptx.py` - One-click enhanced PPTX generation
- `tools/md_to_pptx.py` - Markdown to PPTX converter

### Tests
- `tests/test_*.py` - Unit tests

## Reason for Archival
These files were used during development or are experimental features that are not part of the current main workflow. They are archived for reference but should not be used in production.
EOFREADME

echo ""
echo "✅ 归档完成！"
echo ""
echo "归档位置: $ARCHIVE_DIR"
echo ""
echo "归档内容总结:"
echo "  - Python脚本: 4个"
echo "  - Shell脚本: 5个"
echo "  - Skills目录: 1个"
echo "  - 重复文档: 3个"
echo ""
echo "💡 提示: 归档文件已移至 $ARCHIVE_DIR，可随时恢复"
