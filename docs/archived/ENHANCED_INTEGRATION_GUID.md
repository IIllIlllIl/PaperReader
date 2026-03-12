# 🎯 增强版 PPTX 集成指南

## 快速开始

### 方法 1: 使用增强版一键生成 (推荐)

```bash
# 生成增强版 PPTX (30 slides, ~$0.11)
python tools/generate_enhanced_pptx.py papers/your-paper.pdf
```

### 方法 2: 标准工作流 + 手动转换

```bash
# 1. 生成增强版 Markdown
PYTHONPATH=. python cli/main.py process --paper papers/your-paper.pdf --format markdown --enhanced

# 2. 转换为 PPTX
python tools/md_to_pptx.py output/markdown/your-paper_enhanced.md
```

## 推荐用法

对于任何正式的学术演讲， **强烈推荐使用方法 1 (增强版一键生成)**！

这个方法会：
- ✅ 生成 30 张详细幻灯片
- ✅ 包含完整的技术细节
- ✅ 成本约 $0.11/篇论文
- ✅ 自动转换为 PPTX

## 文件位置

- **增强版工具**: `tools/generate_enhanced_pptx.py`
- **标准版工具**: `cli/main.py` (支持 `--enhanced` 标志)
- **PPTX 转换**: `tools/md_to_pptx.py`

## 总结

由于集成工作流需要更多测试, 目前建议使用独立的增强版工具 (`tools/generate_enhanced_pptx.py`), 它已经过充分测试并验证可以生成高质量的 30 张幻灯片 PPTX。
