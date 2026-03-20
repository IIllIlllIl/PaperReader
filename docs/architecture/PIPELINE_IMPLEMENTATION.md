# Pipeline Implementation Summary

## Overview

`src/core/pipeline.py` 提供当前推荐的端到端流程：从 PDF 生成学术汇报用 PPTX，并在需要时保留可检查的中间产物。

主命令：

```bash
python cli/main.py pipeline --paper papers/example.pdf
```

---

## Pipeline Stages

```text
PDF
→ [1] Parse PDF
→ [2] Extract Sections
→ [3] AI Analysis
→ [3.5] Citation Analysis (optional)
→ [4] Slide Plan
→ [5] Narrative Plan
→ [6] Generate Slides Markdown
→ [7] Export PPTX
→ [8] Generate Script
```

---

## CLI Integration

`cli/main.py` 当前提供的主流程命令：

```bash
python cli/main.py pipeline --paper papers/example.pdf
python cli/main.py pipeline --paper papers/example.pdf --no-clean
python cli/main.py pipeline --paper papers/example.pdf --include-citations
```

主要参数：
- `--paper, -p`: 输入 PDF
- `--output, -o`: 输出目录，默认 `outputs`
- `--config`: 配置文件，默认 `config.yaml`
- `--verbose, -v`: 详细输出
- `--include-citations`: 启用引用分析
- `--citation-min-sources`: 每条引用最少验证来源数
- `--citation-limit`: 幻灯片展示的引用数量上限
- `--clean/--no-clean`: 成功后是否清理中间文件

---

## Stage Details

### Stage 1: Parse PDF
- 模块：`src/parser/pdf_parser.py`
- 输出：`paper_text`, `metadata`

### Stage 2: Extract Structured Sections
- 模块：`src/parser/pdf_parser.py`
- 输出：`sections`

### Stage 3: Run AI Analysis
- 模块：`src/analysis/ai_analyzer.py`
- 输出：`PaperAnalysis`

### Stage 3.5: Citation Analysis (optional)
- 模块：`src/analysis/citation_integration.py`
- 输出：`citation_result`

### Stage 4: Generate Slide Plan
- 模块：`src/planning/slide_planner.py`
- 输出：`SlidePlan`
- 当前默认：结构化 10 页模板

### Stage 5: Generate Narrative Plan
- 模块：`src/planning/narrative_planner.py`
- 输出：`PresentationNarrative`

### Stage 6: Generate Slides Markdown
- 模块：`src/analysis/content_extractor.py` + `src/generation/ppt_generator.py`
- 输出：`outputs/intermediates/markdown/{paper_name}.md`

### Stage 7: Export PPTX
- 模块：`src/generation/pptx_exporter.py`
- 输出：`outputs/slides/{paper_name}.pptx`

### Stage 8: Generate Presentation Script
- 模块：pipeline 内部脚本生成逻辑
- 输出：`outputs/intermediates/scripts/{paper_name}_presentation_script.md`

---

## Output Structure

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
- 最终交付物放在 `outputs/slides/`
- 规划、Markdown、讲稿、图片和引用缓存放在 `outputs/intermediates/`
- 默认会清理中间文件；使用 `--no-clean` 保留

---

## Slide Planning

`src/planning/slide_planner.py` 中的默认结构化模板为 10 页：

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

---

## Return Value

`PaperPresentationPipeline.run()` 返回：

```python
{
    "success": bool,
    "output_paths": {...},
    "stats": {...},
    "analysis": analysis,
    "slide_plan": slide_plan,
    "narrative": narrative,
}
```

其中 `output_paths` 与代码中的 `output_paths` 定义一致，是当前输出路径的最终依据。

---

## Notes

- 当前主流程以 PPTX 为最终输出，不再把 HTML/PDF 作为主路径。
- 若文档内容与实现不一致，请优先以 `src/core/pipeline.py` 为准。
- `process` 命令仍然存在，但当前推荐面向完整汇报生成的命令是 `pipeline`。
