#!/bin/bash
# 废弃文件清理脚本
# 基于 ABANDONED_FILES_ANALYSIS_REPORT.md
# 生成时间: 2026-03-17

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         PaperReader 废弃文件清理脚本                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Phase 1: 安全清理
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Phase 1: 安全清理 (无风险)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "1. 删除 .DS_Store 文件..."
count=$(find . -name ".DS_Store" 2>/dev/null | wc -l | xargs)
if [ "$count" -gt 0 ]; then
    find . -name ".DS_Store" -delete
    echo -e "${GREEN}✓${NC} 已删除 $count 个 .DS_Store 文件"
else
    echo -e "${GREEN}✓${NC} 没有找到 .DS_Store 文件"
fi

echo ""
echo "2. 删除 pytest 缓存..."
if [ -d ".pytest_cache" ]; then
    rm -rf .pytest_cache/
    echo -e "${GREEN}✓${NC} 已删除 .pytest_cache/"
else
    echo -e "${GREEN}✓${NC} 没有找到 .pytest_cache/"
fi

echo ""
echo -e "${GREEN}✅ Phase 1 完成！${NC}"
echo ""

# Phase 2: 谨慎清理
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Phase 2: 谨慎清理 (需要确认)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 3. 删除临时审计文件
if [ -f "project_audit_20260316.txt" ]; then
    echo "3. 发现临时审计文件:"
    echo "   project_audit_20260316.txt ($(du -h project_audit_20260316.txt | cut -f1))"
    echo ""
    echo "   这是 2026-03-16 生成的项目健康度审计报告"
    echo "   建议: 如果不再需要，可以删除"
    echo ""
    read -p "删除这个审计文件? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm project_audit_20260316.txt
        echo -e "${GREEN}✓${NC} 已删除 project_audit_20260316.txt"
    else
        echo -e "${YELLOW}⊘${NC} 跳过删除"
    fi
else
    echo -e "${GREEN}✓${NC} 没有找到临时审计文件"
fi

echo ""

# 4. 删除 Claude worktrees
if [ -d ".claude/worktrees/agent-a5b5cd7e" ]; then
    echo "4. 发现 Claude worktree:"
    echo "   .claude/worktrees/agent-a5b5cd7e/ (4.1MB)"
    echo ""
    echo "   这是 Claude Code Agent 的工作树，包含嵌套的 git 仓库"
    echo "   警告: 如果 Agent 会话还在使用，删除可能影响 Agent 状态"
    echo ""
    echo "   检查 worktree 状态..."
    git_worktrees=$(git worktree list 2>/dev/null | wc -l)
    echo "   当前 git worktree 数量: $git_worktrees"
    echo ""
    read -p "删除 Claude worktree? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .claude/worktrees/agent-a5b5cd7e/
        echo -e "${GREEN}✓${NC} 已删除 .claude/worktrees/agent-a5b5cd7e/"
    else
        echo -e "${YELLOW}⊘${NC} 跳过删除"
    fi
else
    echo -e "${GREEN}✓${NC} 没有找到 Claude worktree"
fi

echo ""
echo -e "${GREEN}✅ Phase 2 完成！${NC}"
echo ""

# 统计
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "清理统计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✓ Phase 1 (安全): 已完成"
echo "✓ Phase 2 (谨慎): 已完成"
echo ""
echo "项目现在是完全干净的状态！"
echo ""
