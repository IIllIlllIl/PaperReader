# PaperReader 项目摘要

## 当前状态

PaperReader 当前提供一条以 `pipeline` 命令为核心的论文到汇报生成流程：

```bash
python cli/main.py pipeline --paper papers/example.pdf
```

该流程从 PDF 出发，完成解析、AI 分析、slide planning、narrative planning、markdown 生成、PPTX 导出，以及讲稿生成。

## 当前主流程

`src/core/pipeline.py` 协调的推荐流程为：

1. Parse PDF
2. Extract structured sections
3. Run AI analysis
4. Optional citation analysis
5. Generate slide plan
6. Generate narrative
7. Generate slides markdown
8. Export PPTX
9. Generate presentation script

实现中可选引用分析会显示为阶段 `3.5`。

## 当前关键模块

- `cli/main.py`：CLI 入口与 `pipeline` 命令
- `src/core/pipeline.py`：端到端主流程编排
- `src/parser/pdf_parser.py`：PDF 文本与章节提取
- `src/analysis/ai_analyzer.py`：论文结构化分析
- `src/analysis/citation_integration.py`：引用分析集成（可选）
- `src/planning/slide_planner.py`：slide planning
- `src/planning/narrative_planner.py`：讲述主线规划
- `src/analysis/content_extractor.py`：生成幻灯片内容
- `src/generation/ppt_generator.py`：markdown 生成
- `src/generation/pptx_exporter.py`：PPTX 导出

## 当前输出结构

```text
outputs/
├── slides/
│   └── {paper_name}.pptx
└── intermediates/
    ├── markdown/
    ├── plans/
    ├── scripts/
    ├── images/
    └── citations/
```

说明：

- `outputs/slides/` 保存最终交付物
- `outputs/intermediates/` 保存排查和复查需要的中间产物
- 默认成功后会清理中间文件；使用 `--no-clean` 可保留

## 默认演示结构

当前默认由 `src/planning/slide_planner.py` 生成结构化 10 页模板：

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

## 当前建议使用方式

```bash
# 标准运行
python cli/main.py pipeline --paper papers/example.pdf

# 调试模式：保留中间文件
python cli/main.py pipeline --paper papers/example.pdf --no-clean

# 启用引用分析
python cli/main.py pipeline --paper papers/example.pdf --include-citations

# 查看缓存统计
python cli/main.py stats

# 清理过期缓存
python cli/main.py cleanup
```

## 注意

- 当前主流程以 PPTX 为最终输出
- 不要再把 HTML/PDF 视为当前推荐输出路径
- 不要再把 `outputs/markdown/`、`outputs/plans/`、`outputs/scripts/` 当作主路径
- 若文档与实现不一致，以 `src/core/pipeline.py` 和 `cli/main.py` 为准

---

**最后更新**: 2026-03-20
