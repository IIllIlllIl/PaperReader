#!/bin/bash

# PaperReader Outputs 清理脚本
# 用途：清理 outputs/ 目录中的测试、调试和临时文件

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置选项
DRY_RUN=${DRY_RUN:-false}  # 默认执行删除，设置为 true 则只显示
VERBOSE=${VERBOSE:-false}

# 计数器
CLEANED_DIRS=0
CLEANED_SIZE="0K"

echo "🧹 PaperReader Outputs 清理工具"
echo "================================"
echo ""

# 显示当前状态
echo "📊 当前 outputs/ 状态："
TOTAL_SIZE=$(du -sh outputs/ 2>/dev/null | cut -f1)
TOTAL_FILES=$(find outputs/ -type f 2>/dev/null | wc -l | tr -d ' ')
echo "   总大小: ${TOTAL_SIZE}"
echo "   总文件数: ${TOTAL_FILES}"
echo ""

# 定义要清理的模式
TEMP_PATTERNS=(
    "outputs/test_*"
    "outputs/debug_*"
    "outputs/*_old_*"
    "outputs/*_backup_*"
    "outputs/validation_*.md"
)

# 函数：计算目录大小
calc_size() {
    local dir=$1
    if [ -d "$dir" ]; then
        du -sh "$dir" 2>/dev/null | cut -f1
    else
        echo "0K"
    fi
}

# 函数：统计文件数
count_files() {
    local dir=$1
    if [ -d "$dir" ]; then
        find "$dir" -type f 2>/dev/null | wc -l | tr -d ' '
    else
        echo "0"
    fi
}

# 函数：清理目录
clean_dir() {
    local dir=$1
    local size=$2
    local files=$3

    if [ "$DRY_RUN" = true ]; then
        echo -e "   ${YELLOW}[预览]${NC} 将删除: $dir ($size, $files 个文件)"
    else
        echo -n "   删除 $dir... "
        rm -rf "$dir"
        echo -e "${GREEN}✓${NC} ($size, $files 个文件)"
    fi

    CLEANED_DIRS=$((CLEANED_DIRS + 1))
}

echo "🗑️  清理临时输出目录："
echo ""

# 清理匹配的目录
for pattern in "${TEMP_PATTERNS[@]}"; do
    # 使用 shell 通配符展开
    for dir in $pattern; do
        if [ -d "$dir" ]; then
            size=$(calc_size "$dir")
            files=$(count_files "$dir")
            clean_dir "$dir" "$size" "$files"
        fi
    done
done

# 清理空目录
echo ""
echo "🧽 清理空目录："
EMPTY_DIRS=$(find outputs/ -type d -empty 2>/dev/null | grep -v "^outputs/$")
if [ -n "$EMPTY_DIRS" ]; then
    echo "$EMPTY_DIRS" | while read dir; do
        if [ "$DRY_RUN" = true ]; then
            echo -e "   ${YELLOW}[预览]${NC} 将删除空目录: $dir"
        else
            echo -n "   删除空目录: $dir... "
            rmdir "$dir" 2>/dev/null || true
            echo -e "${GREEN}✓${NC}"
        fi
        CLEANED_DIRS=$((CLEANED_DIRS + 1))
    done
else
    echo "   无空目录"
fi

# 显示结果
echo ""
echo "================================"
if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}预览模式完成${NC}"
    echo ""
    echo "要执行实际清理，运行："
    echo "  DRY_RUN=false ./scripts/clean_outputs.sh"
else
    # 重新计算状态
    NEW_SIZE=$(du -sh outputs/ 2>/dev/null | cut -f1)
    NEW_FILES=$(find outputs/ -type f 2>/dev/null | wc -l | tr -d ' ')

    echo -e "${GREEN}清理完成！${NC}"
    echo ""
    echo "📊 清理后状态："
    echo "   总大小: ${NEW_SIZE} (之前: ${TOTAL_SIZE})"
    echo "   总文件数: ${NEW_FILES} (之前: ${TOTAL_FILES})"
    echo "   清理目录: ${CLEANED_DIRS} 个"
fi

echo ""
echo "✅ 保留的输出："
echo "   - outputs/slides/      (PPT幻灯片)"
echo "   - outputs/images/      (提取的图片)"
echo "   - outputs/markdown/    (Markdown文档)"
echo "   - outputs/plans/       (规划文件)"
echo "   - outputs/charts/      (图表)"
