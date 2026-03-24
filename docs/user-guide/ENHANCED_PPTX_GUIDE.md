# 🎯 PaperReader PPTX 生成指南

**版本**: 当前主流程
**更新日期**: 2026-03-20

---

## 概述

当前推荐使用 `pipeline` 命令，从论文 PDF 直接生成汇报用 `.pptx`，并在需要时保留 markdown、plan、script 等中间产物。

## 快速开始

```bash
python -m src.cli.main pipeline --paper papers/your-paper.pdf
```

常见变体：

```bash
# 保留中间文件用于调试
python -m src.cli.main pipeline --paper papers/your-paper.pdf --no-clean

# 启用引用分析
python -m src.cli.main pipeline --paper papers/your-paper.pdf --include-citations
```

## 输出文件

```text
outputs/
├── slides/
│   └── {paper_name}.pptx
└── intermediates/
    ├── markdown/
    │   └── {paper_name}.md
    ├── plans/
    │   └── {paper_name}_plan.json
    ├── scripts/
    │   └── {paper_name}_presentation_script.md
    ├── images/
    └── citations/
```

说明：

- 最终交付物是 `outputs/slides/{paper_name}.pptx`
- 默认成功后会清理中间文件
- 如需保留中间文件，请使用 `--no-clean`

## 当前主流程阶段

`src/core/pipeline.py` 当前执行：

1. Parse PDF
2. Extract structured sections
3. Run AI analysis
4. Optional citation analysis
5. Generate slide plan
6. Generate narrative
7. Generate slides markdown
8. Export PPTX
9. Generate presentation script

实现日志中可选引用分析显示为阶段 `3.5`。

## 默认演示结构

`src/planning/slide_planner.py` 默认使用结构化 10 页模板：

1. Title
2. Why Human-in-the-Loop?
3. Research Questions
4. HULA Framework Overview
5. Workflow: Human Feedback Integration
6. Three-Stage Evaluation
7. Offline & Online Results
8. User Survey Results
9. Discussion: Pros & Cons
10. Conclusions & Future Work

## 相关文档

- [Pipeline Implementation](../architecture/PIPELINE_IMPLEMENTATION.md)
- [Data Flow](../architecture/DATA_FLOW.md)
- [Quick Reference](../architecture/DATA_FLOW_QUICK_REFERENCE.md)

## 注意

- 当前推荐路径是 `python -m src.cli.main pipeline ...`
- 当前最终推荐输出是 `.pptx`
- 不要再把 `outputs/markdown/` 或旧的增强版脚本当作当前主路径
