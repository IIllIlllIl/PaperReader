#!/bin/bash

echo "🧹 PaperReader 自动清理"
echo "======================"

# 1. 移动根目录的 .md 文件到 docs/project/
echo -n "移动根目录文档到 docs/project/... "
for f in $(find . -maxdepth 1 -name "*.md" ! -name "CLAUDE.md" ! -name "README.md"); do
    if [ -f "$f" ]; then
        mv "$f" docs/project/
        echo "已移动 $f"
    fi
done
echo "✅"

# 2. 清理临时文件
echo -n "清理临时文件... "
find . -name ".DS_Store" -delete 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
find . -name "*.log" -delete 2>/dev/null
find . -name "*.tmp" -delete 2>/dev/null
find . -name "*.bak" -delete 2>/dev/null
find . -name "*~" -delete 2>/dev/null
echo "✅"

# 3. 清理 Python 缓存
echo -n "清理 Python 缓存... "
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "✅"

# 4. 清理 outputs 临时文件
echo ""
if [ -f "./scripts/clean_outputs.sh" ]; then
    ./scripts/clean_outputs.sh
else
    echo "⚠️  未找到 clean_outputs.sh，跳过 outputs 清理"
fi

# 5. 检查结果
echo ""
./scripts/health_check.sh
