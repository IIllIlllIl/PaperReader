#!/bin/bash
# PaperReader - 文档路径更新脚本
# 在项目重构后，更新所有文档中的命令引用

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "🔧 Updating documentation paths after refactoring..."
echo ""

# 1. Update python main.py -> python cli/main.py
echo "📝 Updating python main.py references..."
find . -name "*.md" -not -path "./.git/*" -type f | while read file; do
    if grep -q "python main.py" "$file" 2>/dev/null; then
        sed -i '' 's|python main.py |python cli/main.py |g' "$file"
        sed -i '' 's|python main.py$|python cli/main.py|g' "$file"
        echo "  ✓ Updated: $file"
    fi
done

# 2. Update ./install_skill.sh -> ./tools/install_skill.sh
echo ""
echo "📝 Updating install_skill.sh references..."
find . -name "*.md" -not -path "./.git/*" -type f | while read file; do
    if grep -q "./install_skill.sh" "$file" 2>/dev/null; then
        sed -i '' 's|./install_skill.sh|./tools/install_skill.sh|g' "$file"
        echo "  ✓ Updated: $file"
    fi
done

# 3. Update ./test_skill.sh -> ./tools/test_skill.sh
echo ""
echo "📝 Updating test_skill.sh references..."
find . -name "*.md" -not -path "./.git/*" -type f | while read file; do
    if grep -q "./test_skill.sh" "$file" 2>/dev/null; then
        sed -i '' 's|./test_skill.sh|./tools/test_skill.sh|g' "$file"
        echo "  ✓ Updated: $file"
    fi
done

# 4. Update debug_data_flow.py path
echo ""
echo "📝 Updating debug_data_flow.py references..."
find . -name "*.md" -not -path "./.git/*" -type f | while read file; do
    if grep -q "debug_data_flow.py" "$file" 2>/dev/null; then
        sed -i '' 's|python debug_data_flow.py|python tools/debug_data_flow.py|g' "$file"
        echo "  ✓ Updated: $file"
    fi
done

# 5. Update md_to_pptx.py path
echo ""
echo "📝 Updating md_to_pptx.py references..."
find . -name "*.md" -not -path "./.git/*" -type f | while read file; do
    if grep -q "md_to_pptx.py" "$file" 2>/dev/null; then
        sed -i '' 's|python md_to_pptx.py|python tools/md_to_pptx.py|g' "$file"
        echo "  ✓ Updated: $file"
    fi
done

echo ""
echo "✅ Documentation update complete!"
echo ""
echo "📊 Summary of changes:"
echo "  • python main.py → python cli/main.py"
echo "  • ./install_skill.sh → ./tools/install_skill.sh"
echo "  • ./test_skill.sh → ./tools/test_skill.sh"
echo "  • python debug_data_flow.py → python tools/debug_data_flow.py"
echo "  • python md_to_pptx.py → python tools/md_to_pptx.py"
echo ""
echo "💡 Run 'git diff' to see all changes"
