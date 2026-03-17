#!/bin/bash
# 文档重组执行脚本
# 基于 DOCUMENTATION_ANALYSIS_REPORT.md 的优化方案
# 生成时间: 2026-03-17

set -e  # 遇到错误立即退出

echo "====================================="
echo "文档位置优化脚本"
echo "====================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 确认执行
echo -e "${YELLOW}警告: 此脚本将重组文档结构${NC}"
echo "建议先阅读 DOCUMENTATION_ANALYSIS_REPORT.md"
echo ""
read -p "是否继续? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "已取消"
    exit 1
fi

echo ""
echo "=== Phase 1: 高优先级修复 ==="
echo ""

# 1.1 移动根目录临时文档
echo "步骤 1/7: 移动根目录临时文档..."
if [ -f "CLEANUP_REPORT.md" ]; then
    mv CLEANUP_REPORT.md docs/project/CLEANUP_REPORT_20260316.md
    echo -e "${GREEN}✓${NC} CLEANUP_REPORT.md → docs/project/CLEANUP_REPORT_20260316.md"
fi

if [ -f "CLEANUP_EXECUTION_REPORT.md" ]; then
    mv CLEANUP_EXECUTION_REPORT.md docs/project/CLEANUP_EXECUTION_20260317.md
    echo -e "${GREEN}✓${NC} CLEANUP_EXECUTION_REPORT.md → docs/project/CLEANUP_EXECUTION_20260317.md"
fi

if [ -f "UNUSED_CODE_ANALYSIS_REPORT.md" ]; then
    mv UNUSED_CODE_ANALYSIS_REPORT.md docs/project/CODE_ANALYSIS_20260317.md
    echo -e "${GREEN}✓${NC} UNUSED_CODE_ANALYSIS_REPORT.md → docs/project/CODE_ANALYSIS_20260317.md"
fi

if [ -f "EXAMPLES_ARCHIVED.md" ]; then
    mv EXAMPLES_ARCHIVED.md docs/project/EXAMPLES_ARCHIVED_20260317.md
    echo -e "${GREEN}✓${NC} EXAMPLES_ARCHIVED.md → docs/project/EXAMPLES_ARCHIVED_20260317.md"
fi

echo ""

# 1.2 重命名 testing/README.md
echo "步骤 2/7: 重命名 testing/README.md..."
if [ -f "docs/testing/README.md" ]; then
    mv docs/testing/README.md docs/testing/IMAGE_SUPPORT_ACCEPTANCE_COMPLETE.md
    echo -e "${GREEN}✓${NC} testing/README.md → testing/IMAGE_SUPPORT_ACCEPTANCE_COMPLETE.md"
fi

echo ""

# 1.3 归档过时文档
echo "步骤 3/7: 归档过时文档..."
mkdir -p docs/archived
if [ -f "docs/project/PROJECT_REORGANIZATION.md" ]; then
    mv docs/project/PROJECT_REORGANIZATION.md docs/archived/PROJECT_REORGANIZATION_DEPRECATED.md
    echo -e "${GREEN}✓${NC} PROJECT_REORGANIZATION.md → archived/PROJECT_REORGANIZATION_DEPRECATED.md"
fi

echo ""

# 1.4 修复 UNDERSTANDING_DATA_FLOW.md 中的链接
echo "步骤 4/7: 修复失效链接..."
if [ -f "docs/architecture/UNDERSTANDING_DATA_FLOW.md" ]; then
    # 使用 sed 替换链接
    sed -i.bak 's|\[examples/README\.md\](examples/README\.md)|[EXAMPLES_ARCHIVED](../project/EXAMPLES_ARCHIVED_20260317.md)|g' \
        docs/architecture/UNDERSTANDING_DATA_FLOW.md
    rm -f docs/architecture/UNDERSTANDING_DATA_FLOW.md.bak
    echo -e "${GREEN}✓${NC} 修复了 UNDERSTANDING_DATA_FLOW.md 中的链接"
fi

echo ""
echo "=== Phase 2: 完善索引 ==="
echo ""

# 2.1 创建 docs/features/README.md
echo "步骤 5/7: 创建子目录索引文件..."

cat > docs/features/README.md << 'EOF'
# Features Documentation

This directory contains documentation for specific features of PaperReader.

---

## Available Features

### Narrative Planning
- **[NARRATIVE_PLANNER.md](NARRATIVE_PLANNER.md)** - Narrative extraction and planning system
- **[NARRATIVE_QUICKSTART.md](NARRATIVE_QUICKSTART.md)** - Quick start guide for narrative planning
- **[NARRATIVE_INTEGRATION_GUIDE.md](NARRATIVE_INTEGRATION_GUIDE.md)** - How to integrate narrative planning

### Slide Formatting
- **[SLIDE_FORMATTER.md](SLIDE_FORMATTER.md)** - Slide formatting rules and validation
- **[SLIDE_FORMATTER_QUICKSTART.md](SLIDE_FORMATTER_QUICKSTART.md)** - Quick start guide for slide formatting

### Chart Generation
- **[CHART_GENERATION.md](CHART_GENERATION.md)** - Chart generation from data

---

## Feature Development Lifecycle

1. **Design** → Architecture documents in `docs/architecture/`
2. **Implement** → Code in `src/`
3. **Document** → Feature guides in this directory
4. **Test** → Test reports in `docs/testing/`

---

## Related Documentation

- [Architecture Overview](../architecture/PROJECT_SUMMARY.md)
- [Pipeline Implementation](../architecture/PIPELINE_IMPLEMENTATION.md)
- [User Guide](../user-guide/ENHANCED_PPTX_GUIDE.md)

---

**Last Updated**: 2026-03-17
EOF

echo -e "${GREEN}✓${NC} 创建了 docs/features/README.md"

# 2.2 创建 docs/project/README.md

cat > docs/project/README.md << 'EOF'
# Project Management Documentation

This directory contains project management documents, status reports, and cleanup history.

---

## Current Status

- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Current project status and roadmap
- **[IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md)** - Recent pipeline improvements (2026-03-13)

---

## Cleanup History

- **[CLEANUP_HISTORY.md](CLEANUP_HISTORY.md)** - Complete cleanup and reorganization history

### Cleanup Reports

- **[CLEANUP_REPORT_20260316.md](CLEANUP_REPORT_20260316.md)** - Major project cleanup (March 16, 2026)
- **[CLEANUP_EXECUTION_20260317.md](CLEANUP_EXECUTION_20260317.md)** - Code cleanup execution (March 17, 2026)
- **[CODE_ANALYSIS_20260317.md](CODE_ANALYSIS_20260317.md)** - Unused code analysis report
- **[EXAMPLES_ARCHIVED_20260317.md](EXAMPLES_ARCHIVED_20260317.md)** - Examples directory archival

---

## Historical Documents

- **[PROJECT_REORGANIZATION.md](PROJECT_REORGANIZATION.md)** - Original reorganization plan

> Note: For historical reorganization plans, see `docs/archived/`

---

## Cleanup Guidelines

### When to Clean Up

- Monthly: Review and remove obsolete files
- After major features: Archive completed feature documentation
- Before releases: Ensure all documentation is up to date

### How to Document Cleanup

1. Create analysis report before cleanup
2. Get user approval
3. Move files to `trash/cleanup_YYYYMMDD/`
4. Update this history file
5. Verify no broken links

---

## Related Documentation

- [Architecture](../architecture/) - Technical design
- [Testing](../testing/) - Test reports
- [Main README](../../README.md) - Project overview

---

**Last Updated**: 2026-03-17
EOF

echo -e "${GREEN}✓${NC} 创建了 docs/project/README.md"

# 2.3 创建 docs/testing/README.md

cat > docs/testing/README.md << 'EOF'
# Testing Documentation

This directory contains test reports, acceptance documents, and validation results.

---

## Test Reports

### Feature Tests

- **[TEST_PPTX_GENERATION.md](TEST_PPTX_GENERATION.md)** - PPTX generation functionality tests
- **[ENHANCED_PPTX_COMPARISON.md](ENHANCED_PPTX_COMPARISON.md)** - Standard vs Enhanced PPTX comparison
- **[HUMAN_IN_LOOP_TEST_GUIDE.md](HUMAN_IN_LOOP_TEST_GUIDE.md)** - Human-in-the-loop testing guide
- **[HUMAN_IN_LOOP_V3_REVIEW_PACKAGE.md](HUMAN_IN_LOOP_V3_REVIEW_PACKAGE.md)** - V3 review package

### Meeting Mode Tests

- **[PHD_MEETING_V2_COMPLETE.md](PHD_MEETING_V2_COMPLETE.md)** - PhD meeting mode V2 completion report
- **[RESEARCH_MEETING_UPGRADE.md](RESEARCH_MEETING_UPGRADE.md)** - Research meeting pipeline upgrade

### Feature Acceptance

- **[IMAGE_SUPPORT_ACCEPTANCE_COMPLETE.md](IMAGE_SUPPORT_ACCEPTANCE_COMPLETE.md)** - Image support feature - Complete acceptance
- **[IMAGE_SUPPORT_ACCEPTANCE_REPORT.md](IMAGE_SUPPORT_ACCEPTANCE_REPORT.md)** - Detailed test results
- **[ACCEPTANCE_EXECUTIVE_SUMMARY.md](ACCEPTANCE_EXECUTIVE_SUMMARY.md)** - Executive summary
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Deployment checklist

### Refactoring Tests

- **[REFACTOR_TEST_REPORT.md](REFACTOR_TEST_REPORT.md)** - Repository refactoring validation
- **[V3_IMPLEMENTATION_SUMMARY.md](V3_IMPLEMENTATION_SUMMARY.md)** - V3 implementation summary

---

## Testing Categories

### 1. Functional Testing
Tests that verify specific features work as expected.

### 2. Acceptance Testing
Tests that verify features meet requirements and are ready for production.

### 3. Comparison Testing
Tests that compare different versions or approaches.

### 4. Integration Testing
Tests that verify different components work together.

---

## Test Status Overview

| Feature | Status | Report |
|---------|--------|--------|
| Image Support | ✅ APPROVED | [IMAGE_SUPPORT_ACCEPTANCE_COMPLETE.md](IMAGE_SUPPORT_ACCEPTANCE_COMPLETE.md) |
| PhD Meeting V2 | ✅ COMPLETE | [PHD_MEETING_V2_COMPLETE.md](PHD_MEETING_V2_COMPLETE.md) |
| Research Meeting | ✅ UPGRADED | [RESEARCH_MEETING_UPGRADE.md](RESEARCH_MEETING_UPGRADE.md) |
| V3 Implementation | ✅ COMPLETE | [V3_IMPLEMENTATION_SUMMARY.md](V3_IMPLEMENTATION_SUMMARY.md) |

---

## Related Documentation

- [Architecture](../architecture/) - Technical design documents
- [User Guide](../user-guide/) - How to use tested features
- [Main README](../../README.md) - Project overview

---

**Last Updated**: 2026-03-17
EOF

echo -e "${GREEN}✓${NC} 创建了 docs/testing/README.md"

echo ""

# 2.4 更新 docs/README.md
echo "步骤 6/7: 更新主索引 docs/README.md..."

cat > docs/README.md << 'EOF'
# 📚 PaperReader 文档中心

**欢迎来到 PaperReader 文档中心！**

---

## 🎯 快速导航

### 🏗️ 架构设计
- **[数据流详解](architecture/DATA_FLOW.md)** - 完整的数据处理流程
- **[数据可视化](architecture/DATA_VISUALIZATION.md)** - 架构图和流程图
- **[数据流快速参考](architecture/DATA_FLOW_QUICK_REFERENCE.md)** - 快速查询手册
- **[理解数据流](architecture/UNDERSTANDING_DATA_FLOW.md)** - 数据流学习指南
- **[项目摘要](architecture/PROJECT_SUMMARY.md)** - 项目概览
- **[Prompt Engineering V3](architecture/PROMPT_ENGINEERING_V3.md)** - 提示词设计规范
- **[Slide Planning Layer](architecture/SLIDE_PLANNING_LAYER.md)** - 两阶段 slide 规划架构
- **[Pipeline Implementation](architecture/PIPELINE_IMPLEMENTATION.md)** - Pipeline 架构实现

### ✨ 功能文档
- **[功能索引](features/README.md)** - 所有功能文档导航
- **[Narrative Planner](features/NARRATIVE_PLANNER.md)** - 叙事提取系统
- **[Slide Formatter](features/SLIDE_FORMATTER.md)** - 幻灯片格式化规则
- **[Chart Generation](features/CHART_GENERATION.md)** - 图表生成功能

### 🧪 测试与验收
- **[测试索引](testing/README.md)** - 所有测试文档导航
- **[PPTX 生成测试](testing/TEST_PPTX_GENERATION.md)** - PPTX 功能测试报告
- **[增强版对比报告](testing/ENHANCED_PPTX_COMPARISON.md)** - 标准版与增强版对比
- **[PhD Meeting V2 完成报告](testing/PHD_MEETING_V2_COMPLETE.md)** - PhD 组会 pipeline 升级结果
- **[Research Meeting 升级报告](testing/RESEARCH_MEETING_UPGRADE.md)** - Research meeting pipeline 说明

### 📋 项目管理
- **[项目索引](project/README.md)** - 项目管理文档导航
- **[项目状态](project/PROJECT_STATUS.md)** - 当前项目状态
- **[改进总结](project/IMPROVEMENTS_SUMMARY.md)** - 最近的改进
- **[清理历史](project/CLEANUP_HISTORY.md)** - 清理和重组历史

### 📖 用户指南
- **[增强版 PPTX 生成指南](user-guide/ENHANCED_PPTX_GUIDE.md)** - 增强版使用说明

---

## 📂 文档结构说明

```text
docs/
├── architecture/     # 架构和技术文档 (13个文件)
├── features/         # 功能文档 (6个文件)
├── project/          # 项目管理和历史 (8个文件)
├── testing/          # 测试、验收和评审报告 (12个文件)
└── user-guide/       # 用户使用指南 (1个文件)
```

归档的历史文档位于 `docs/archived/`。

---

## 🚀 快速开始

1. **理解架构**: 阅读 [数据流详解](architecture/DATA_FLOW.md)
2. **查看功能**: 浏览 [功能索引](features/README.md)
3. **开始使用**: 参考 [增强版 PPTX 生成指南](user-guide/ENHANCED_PPTX_GUIDE.md)
4. **查看验证结果**: 打开 [测试索引](testing/README.md)

---

## 📌 维护说明

- **新增活跃文档**: 仅放入 `architecture/`、`features/`、`project/`、`testing/` 或 `user-guide/`
- **归档历史内容**: 放入 `docs/archived/`
- **更新索引**: 修改本文件中的导航链接
- **命名规范**: 使用 `UPPERCASE_WITH_UNDERSCORES.md`

---

**最后更新**: 2026-03-17
**维护者**: PaperReader Team
EOF

echo -e "${GREEN}✓${NC} 更新了 docs/README.md"

echo ""
echo "=== Phase 3: 统一命名（可选） ==="
echo ""

read -p "是否统一 testing/ 目录的文件命名? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "步骤 7/7: 统一 testing/ 文件命名..."

    cd docs/testing
    [ -f "enhanced_pptx_comparison.md" ] && mv enhanced_pptx_comparison.md ENHANCED_PPTX_COMPARISON.md && echo -e "${GREEN}✓${NC} enhanced_pptx_comparison.md → ENHANCED_PPTX_COMPARISON.md"
    [ -f "human_in_loop_test_guide.md" ] && mv human_in_loop_test_guide.md HUMAN_IN_LOOP_TEST_GUIDE.md && echo -e "${GREEN}✓${NC} human_in_loop_test_guide.md → HUMAN_IN_LOOP_TEST_GUIDE.md"
    [ -f "human_in_loop_v3_review_package.md" ] && mv human_in_loop_v3_review_package.md HUMAN_IN_LOOP_V3_REVIEW_PACKAGE.md && echo -e "${GREEN}✓${NC} human_in_loop_v3_review_package.md → HUMAN_IN_LOOP_V3_REVIEW_PACKAGE.md"
    [ -f "test_pptx_generation.md" ] && mv test_pptx_generation.md TEST_PPTX_GENERATION.md && echo -e "${GREEN}✓${NC} test_pptx_generation.md → TEST_PPTX_GENERATION.md"
    [ -f "v3_implementation_summary.md" ] && mv v3_implementation_summary.md V3_IMPLEMENTATION_SUMMARY.md && echo -e "${GREEN}✓${NC} v3_implementation_summary.md → V3_IMPLEMENTATION_SUMMARY.md"
    cd ../..

    echo ""
else
    echo "跳过命名统一"
    echo ""
fi

echo "====================================="
echo -e "${GREEN}✅ 文档重组完成！${NC}"
echo "====================================="
echo ""
echo "📊 统计:"
echo "  - 移动文档: 4个"
echo "  - 重命名文档: 1个"
echo "  - 创建索引: 4个"
echo "  - 归档文档: 1个"
echo ""
echo "📁 根目录现在只有:"
ls -1 *.md 2>/dev/null | grep -E "^(CLAUDE|README)\.md$" || echo "  - CLAUDE.md"
echo ""
echo "✨ 下一步:"
echo "  1. 检查 docs/README.md 确保索引正确"
echo "  2. 运行链接检查确保没有失效链接"
echo "  3. 提交更改到 git"
echo ""
