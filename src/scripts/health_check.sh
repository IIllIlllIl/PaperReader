#!/bin/bash

echo "🏥 PaperReader 项目健康检查"
echo "=========================="
echo ""

ISSUES=0

# 1. 根目录检查
echo -n "📁 根目录文档检查... "
ROOT_MDS=$(find . -maxdepth 1 -name "*.md" ! -name "CLAUDE.md" ! -name "README.md" | wc -l)
if [ $ROOT_MDS -eq 0 ]; then
    echo "✅"
else
    echo "❌"
    find . -maxdepth 1 -name "*.md" ! -name "CLAUDE.md" ! -name "README.md" | while read f; do
        echo "   - 应移动到 docs/project/: $f"
    done
    ISSUES=$((ISSUES + 1))
fi

# 2. 临时文件检查
echo -n "📄 临时文件检查... "
TEMP_FILES=$(find . -name ".DS_Store" -o -name "*.pyc" -o -name "*.log" -o -name "*.tmp" -o -name "*.bak" -o -name "*~" | grep -v "^\./\.git/" | wc -l)
if [ $TEMP_FILES -eq 0 ]; then
    echo "✅"
else
    echo "❌"
    find . -name ".DS_Store" -o -name "*.pyc" -o -name "*.log" -o -name "*.tmp" -o -name "*.bak" -o -name "*~" | grep -v "^\./\.git/" | head -5
    echo "   ... 共 $TEMP_FILES 个临时文件"
    ISSUES=$((ISSUES + 1))
fi

# 3. Python 缓存检查
echo -n "🐍 Python 缓存检查... "
PYCACHE=$(find . -type d -name "__pycache__" 2>/dev/null | wc -l)
PYFILES=$(find . -name "*.pyc" 2>/dev/null | wc -l)
if [ $PYCACHE -eq 0 ] && [ $PYFILES -eq 0 ]; then
    echo "✅"
else
    echo "❌"
    [ $PYCACHE -gt 0 ] && echo "   - 发现 $PYCACHE 个 __pycache__ 目录"
    [ $PYFILES -gt 0 ] && echo "   - 发现 $PYFILES 个 .pyc 文件"
    ISSUES=$((ISSUES + 1))
fi

# 4. 文档索引检查
echo -n "📚 文档索引完整性... "
MISSING_INDEX=0
for dir in docs/*/ ; do
    if [ -d "$dir" ] && [ ! -f "${dir}README.md" ]; then
        MISSING_INDEX=$((MISSING_INDEX + 1))
    fi
done
if [ $MISSING_INDEX -eq 0 ]; then
    echo "✅"
else
    echo "❌ 发现 $MISSING_INDEX 个目录缺少 README.md"
    ISSUES=$((ISSUES + 1))
fi

# 5. outputs 临时文件检查
echo -n "🗂️  outputs 临时文件检查... "
TEMP_OUTPUTS=$(find outputs/ -maxdepth 1 -type d \( -name "test_*" -o -name "debug_*" -o -name "*_old_*" -o -name "*_backup_*" \) 2>/dev/null | wc -l | tr -d ' ')
if [ "$TEMP_OUTPUTS" -eq 0 ]; then
    echo "✅"
else
    echo "❌"
    find outputs/ -maxdepth 1 -type d \( -name "test_*" -o -name "debug_*" -o -name "*_old_*" -o -name "*_backup_*" \) 2>/dev/null | while read dir; do
        size=$(du -sh "$dir" 2>/dev/null | cut -f1)
        files=$(find "$dir" -type f 2>/dev/null | wc -l | tr -d ' ')
        echo "   - $dir ($size, $files 个文件)"
    done
    echo "   ... 共 $TEMP_OUTPUTS 个临时目录"
    ISSUES=$((ISSUES + 1))
fi

echo ""
echo "=========================="
if [ $ISSUES -eq 0 ]; then
    echo "🎉 项目健康！一切正常"
    exit 0
else
    echo "⚠️  发现 $ISSUES 个问题需要处理"
    echo ""
    echo "运行以下命令自动修复："
    echo "  ./scripts/auto_clean.sh"
    echo ""
    echo "或者单独清理 outputs："
    echo "  ./scripts/clean_outputs.sh"
    echo "  DRY_RUN=true ./scripts/clean_outputs.sh  # 预览模式"
    exit 1
fi
