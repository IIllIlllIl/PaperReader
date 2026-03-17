# 🎯 PaperReader 增强版 PPTX 生成指南

**版本**: 2.0  
**更新日期**: 2026-03-06  

---

## 📖 概述

PaperReader 现在支持**增强版 PPTX 生成**，可以从学术论文自动生成包含 **30+ 张幻灯片**的详细演示文稿。

---

## 🚀 快速开始

### 使用增强版生成器

```bash
# 生成增强版 PPTX
python tools/generate_enhanced_pptx.py papers/your-paper.pdf
```

### 输出文件
- 📝 Markdown: `outputs/markdown/[PaperName]_enhanced.md`
- 📊 PPTX: `outputs/slides/[PaperName]_enhanced.pptx`

---

## 📊 版本对比

| 特性 | 标准版 | 增强版 |
|------|--------|--------|
| 幻灯片数量 | 16 | **30** |
| 内容详细度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| API 成本 | ~$0.06 | ~$0.11 |
| 适用场景 | 快速概览 | **学术演讲** |

**推荐使用增强版用于任何正式的学术演讲场合！**

---

## 💰 成本分析

- **API 成本**: $0.11 (~¥0.81)
- **处理时间**: ~2 分钟
- **性价比**: 优秀

---

**文件位置**:
- 增强版工具: `tools/generate_enhanced_pptx.py`
- 对比报告: `docs/testing/enhanced_pptx_comparison.md`
