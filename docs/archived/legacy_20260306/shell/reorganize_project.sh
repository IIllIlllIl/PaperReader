#!/bin/bash
#
# PaperReader 项目结构整理脚本
# 用途：将根目录的临时文档移动到 docs/ 目录下
#

set -e  # 遇到错误立即退出

PROJECT_ROOT="/Users/taoran.wang/Documents/PaperReader"
cd "$PROJECT_ROOT"

echo "📁 PaperReader 项目结构整理"
echo "================================"
echo ""

# 1. 创建新的文档目录结构
echo "1️⃣  创建文档目录结构..."
mkdir -p docs/project
mkdir -p docs/changelogs
mkdir -p docs/architecture
mkdir -p docs/testing
mkdir -p docs/user-guide

# 添加 .gitkeep 占位文件
touch docs/user-guide/.gitkeep

echo "   ✅ 目录创建完成"
echo ""

# 2. 移动现有的架构文档到 architecture/
echo "2️⃣  整理架构文档..."
if [ -f "docs/DATA_FLOW.md" ]; then
    mv docs/DATA_FLOW.md docs/architecture/
    echo "   ✅ DATA_FLOW.md → docs/architecture/"
fi

if [ -f "docs/DATA_FLOW_QUICK_REFERENCE.md" ]; then
    mv docs/DATA_FLOW_QUICK_REFERENCE.md docs/architecture/
    echo "   ✅ DATA_FLOW_QUICK_REFERENCE.md → docs/architecture/"
fi

if [ -f "docs/DATA_VISUALIZATION.md" ]; then
    mv docs/DATA_VISUALIZATION.md docs/architecture/
    echo "   ✅ DATA_VISUALIZATION.md → docs/architecture/"
fi

if [ -f "docs/UNDERSTANDING_DATA_FLOW.md" ]; then
    mv docs/UNDERSTANDING_DATA_FLOW.md docs/architecture/
    echo "   ✅ UNDERSTANDING_DATA_FLOW.md → docs/architecture/"
fi

if [ -f "docs/PROJECT_SUMMARY.md" ]; then
    mv docs/PROJECT_SUMMARY.md docs/architecture/
    echo "   ✅ PROJECT_SUMMARY.md → docs/architecture/"
fi

echo ""

# 3. 移动根目录的文档文件
echo "3️⃣  移动根目录文档..."

# 项目管理文档
if [ -f "PROJECT_STATUS.md" ]; then
    mv PROJECT_STATUS.md docs/project/
    echo "   ✅ PROJECT_STATUS.md → docs/project/"
fi

if [ -f "PROJECT_REORGANIZATION.md" ]; then
    mv PROJECT_REORGANIZATION.md docs/project/
    echo "   ✅ PROJECT_REORGANIZATION.md → docs/project/"
fi

# 变更日志
if [ -f "REFACTORING_COMPLETE.md" ]; then
    mv REFACTORING_COMPLETE.md docs/changelogs/
    echo "   ✅ REFACTORING_COMPLETE.md → docs/changelogs/"
fi

if [ -f "DOCUMENTATION_UPDATE_COMPLETE.md" ]; then
    mv DOCUMENTATION_UPDATE_COMPLETE.md docs/changelogs/
    echo "   ✅ DOCUMENTATION_UPDATE_COMPLETE.md → docs/changelogs/"
fi

# 测试文档
if [ -f "test_pptx_generation.md" ]; then
    mv test_pptx_generation.md docs/testing/
    echo "   ✅ test_pptx_generation.md → docs/testing/"
fi

echo ""

# 4. 创建文档索引
echo "4️⃣  创建文档索引..."
cat > docs/README.md << 'DOCEOF'
# 📚 PaperReader 文档中心

**欢迎来到 PaperReader 文档中心！**

---

## 🎯 快速导航

### 📋 项目管理
- [项目状态报告](project/PROJECT_STATUS.md) - 当前项目状态、进展和指标
- [项目重组计划](project/PROJECT_REORGANIZATION.md) - 项目重组方案和执行记录

### 🏗️ 架构设计
- [数据流详解](architecture/DATA_FLOW.md) - 完整的数据处理流程
- [数据可视化](architecture/DATA_VISUALIZATION.md) - 架构图和流程图
- [数据流快速参考](architecture/DATA_FLOW_QUICK_REFERENCE.md) - 快速查询手册
- [理解数据流](architecture/UNDERSTANDING_DATA_FLOW.md) - 数据流学习指南
- [项目摘要](architecture/PROJECT_SUMMARY.md) - 项目概览

### 📝 变更日志
- [重构完成报告](changelogs/REFACTORING_COMPLETE.md) - 代码重构总结
- [文档更新记录](changelogs/DOCUMENTATION_UPDATE_COMPLETE.md) - 文档变更历史

### 🧪 测试
- [PPTX 生成测试](testing/test_pptx_generation.md) - PPTX 功能测试报告

### 📖 用户指南
- *(待添加)* - 使用教程和示例

---

## 📂 文档结构说明

```
docs/
├── project/          # 项目管理文档
│   ├── PROJECT_STATUS.md
│   └── PROJECT_REORGANIZATION.md
├── architecture/     # 架构和技术文档
│   ├── DATA_FLOW.md
│   ├── DATA_VISUALIZATION.md
│   ├── DATA_FLOW_QUICK_REFERENCE.md
│   ├── UNDERSTANDING_DATA_FLOW.md
│   └── PROJECT_SUMMARY.md
├── changelogs/       # 变更日志和里程碑
│   ├── REFACTORING_COMPLETE.md
│   └── DOCUMENTATION_UPDATE_COMPLETE.md
├── testing/          # 测试报告
│   └── test_pptx_generation.md
└── user-guide/       # 用户使用指南
    └── (待添加)
```

---

## 🚀 快速开始

1. **了解项目**: 查看 [项目状态](project/PROJECT_STATUS.md)
2. **理解架构**: 阅读 [数据流详解](architecture/DATA_FLOW.md)
3. **开始使用**: 参考 [快速参考](architecture/DATA_FLOW_QUICK_REFERENCE.md)

---

## 📌 维护说明

- **添加新文档**: 根据文档类型放入对应子目录
- **更新索引**: 修改本文件的导航链接
- **命名规范**: 使用大写和下划线 (UPPERCASE_WITH_UNDERSCORES.md)

---

**最后更新**: 2026-03-05  
**维护者**: PaperReader Team
DOCEOF

echo "   ✅ docs/README.md 已创建"
echo ""

# 5. 显示整理结果
echo "5️⃣  整理完成！"
echo ""
echo "📊 整理统计:"
echo "   - 创建目录: 5 个"
echo "   - 移动文件: $(find docs -type f -name "*.md" | wc -l | tr -d ' ') 个文档文件"
echo ""
echo "📂 新的文档结构:"
tree docs -L 2 2>/dev/null || find docs -type f -name "*.md" | sort | sed 's/^/   /'
echo ""

# 6. 显示后续步骤
echo "📝 后续步骤:"
echo "   1. 检查 docs/README.md 确认文档索引正确"
echo "   2. 更新 CLAUDE.md 中的文档路径引用（如果有）"
echo "   3. 提交变更: git add . && git commit -m 'chore: reorganize project structure'"
echo "   4. 验证项目功能: python cli/main.py process --paper papers/Human-In-the-Loop.pdf"
echo ""
echo "✨ 整理完成！根目录现在更加整洁了。"
