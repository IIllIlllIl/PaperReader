# 📊 PaperReader 数据流程可视化

## 当前推荐流程

```text
PDF
  ↓
[1/8] Parse PDF
  输出: paper_text, metadata
  ↓
[2/8] Extract structured sections
  输出: sections
  ↓
[3/8] Run AI analysis
  输出: PaperAnalysis
  ↓
[3.5/8] Analyze citations (optional)
  输出: citation_result
  ↓
[4/8] Plan slides
  输出: SlidePlan
  ↓
[5/8] Plan narrative
  输出: PresentationNarrative
  ↓
[6/8] Generate slides markdown
  输出: OrganizedPresentation + Markdown
  ↓
[7/8] Export PPTX
  输出: outputs/slides/{paper_name}.pptx
  ↓
[8/8] Generate presentation script
  输出: outputs/intermediates/scripts/{paper_name}_presentation_script.md
```

## 模块视角

```text
cli/main.py
  └─ pipeline command
      └─ src/core/pipeline.py
          ├─ src/parser/pdf_parser.py
          ├─ src/analysis/ai_analyzer.py
          ├─ src/analysis/citation_integration.py (optional)
          ├─ src/planning/slide_planner.py
          ├─ src/planning/narrative_planner.py
          ├─ src/analysis/content_extractor.py
          ├─ src/generation/ppt_generator.py
          └─ src/generation/pptx_exporter.py
```

## 当前输出目录

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

## 关键对象流转

```text
PDF
→ paper_text + metadata
→ PaperAnalysis
→ SlidePlan
→ PresentationNarrative
→ OrganizedPresentation
→ Markdown
→ PPTX
```

## 默认演示结构

`src/planning/slide_planner.py` 默认生成结构化 10 页：

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

## 运行与调试

```bash
# 推荐主流程
python cli/main.py pipeline --paper papers/example.pdf

# 保留中间文件
python cli/main.py pipeline --paper papers/example.pdf --no-clean

# 启用引用分析
python cli/main.py pipeline --paper papers/example.pdf --include-citations
```

排查问题时通常先看：

1. `outputs/slides/`
2. `outputs/intermediates/plans/`
3. `outputs/intermediates/markdown/`
4. `outputs/intermediates/scripts/`
5. `runtime/cache/`

## 注意

- 当前推荐路径是 `pipeline`，不是旧的 HTML/PDF 导出流程
- 当前最终交付物是 `.pptx`
- 若文档与实现冲突，以 `src/core/pipeline.py` 为准

---

**最后更新**: 2026-03-20
