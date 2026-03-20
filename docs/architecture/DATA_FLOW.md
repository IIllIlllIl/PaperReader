# PaperReader 数据流程和中间产物详解

## 总览

推荐命令是 `python cli/main.py pipeline --paper <pdf>`。

当前主流程由 `src/core/pipeline.py` 协调，默认执行 8 个阶段，并在启用引用分析时插入可选的 `3.5` 阶段：

1. 解析 PDF
2. 提取结构化章节
3. 运行 AI 分析
3.5. 可选：引用分析
4. 生成 Slide Plan
5. 生成 Narrative
6. 生成 Markdown 幻灯片
7. 导出 PPTX
8. 生成讲稿脚本

默认会在成功后清理中间文件；使用 `--no-clean` 可保留中间产物用于调试。

---

## 完整流程

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
[4/8] Planning slides
  输出: SlidePlan
  ↓
[5/8] Planning narrative
  输出: PresentationNarrative
  ↓
[6/8] Generating slides
  输出: OrganizedPresentation + Markdown
  ↓
[7/8] Exporting PPTX
  输出: outputs/slides/{paper_name}.pptx
  ↓
[8/8] Generating presentation script
  输出: outputs/intermediates/scripts/{paper_name}_presentation_script.md
```

---

## 每个阶段的输入与输出

### 阶段 1：Parse PDF
- 模块：`src/parser/pdf_parser.py`
- 输入：PDF 文件路径
- 输出：
  - `paper_text`
  - `metadata`
- 说明：提取全文、元数据和页数等基础信息。

### 阶段 2：Extract structured sections
- 模块：`src/parser/pdf_parser.py`
- 输入：PDF 文件路径
- 输出：`sections` 字典
- 说明：抽取 abstract、introduction、method、results 等结构化章节。

### 阶段 3：Run AI analysis
- 模块：`src/analysis/ai_analyzer.py`
- 输入：`paper_text` + `metadata`
- 输出：`PaperAnalysis`
- 说明：得到问题定义、方法、结果、优缺点、结论等结构化分析。

### 阶段 3.5：Analyze citations（可选）
- 模块：`src/analysis/citation_integration.py`
- 触发方式：`--include-citations`
- 输出：`citation_result`
- 说明：为演示内容补充可验证引用信息。

### 阶段 4：Planning slides
- 模块：`src/planning/slide_planner.py`
- 输入：`PaperAnalysis`
- 输出：`SlidePlan`
- 说明：默认使用结构化模板，生成 10 页主线演示结构。

### 阶段 5：Planning narrative
- 模块：`src/planning/narrative_planner.py`
- 输入：`PaperAnalysis`
- 输出：`PresentationNarrative`
- 说明：提炼讲述主线，供最终讲稿使用。

### 阶段 6：Generating slides
- 模块：`src/analysis/content_extractor.py` + `src/generation/ppt_generator.py`
- 输入：`PaperAnalysis` + `SlidePlan` + figures + optional citations
- 输出：
  - `OrganizedPresentation`
  - `outputs/intermediates/markdown/{paper_name}.md`
- 说明：生成 Markdown 幻灯片内容，并保存到中间目录。

### 阶段 7：Exporting PPTX
- 模块：`src/generation/pptx_exporter.py`
- 输入：Markdown 文件
- 输出：`outputs/slides/{paper_name}.pptx`
- 说明：这是当前推荐流程的最终演示文件。

### 阶段 8：Generating presentation script
- 模块：`src/core/pipeline.py` 内部脚本生成逻辑
- 输入：`PresentationNarrative` + `SlidePlan`
- 输出：`outputs/intermediates/scripts/{paper_name}_presentation_script.md`
- 说明：生成与幻灯片结构对齐的讲稿。

---

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

说明：
- `slides/` 保存最终产物。
- `intermediates/` 保存可复查的中间产物。
- 默认清理策略会在成功后删除中间文件；如需排查，使用 `--no-clean`。

---

## 关键数据结构

### `PaperAnalysis`
来自 AI 分析阶段，包含：
- `problem`
- `motivation`
- `method`
- `innovations`
- `experiments`
- `results`
- `pros`
- `cons`
- `conclusions`
- `future_work`

### `SlidePlan`
来自规划阶段，描述每页要讲什么。

默认结构化模板为 10 页：
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

### `OrganizedPresentation`
来自内容生成阶段，表示最终 Markdown/PPTX 使用的幻灯片集合。

---

## 常用调试方式

### 保留中间产物
```bash
python cli/main.py pipeline --paper papers/example.pdf --no-clean
```

### 查看缓存统计
```bash
python cli/main.py stats
```

### 查看关键中间文件
```bash
ls outputs/intermediates/markdown
ls outputs/intermediates/plans
ls outputs/intermediates/scripts
```

---

## 与旧文档的区别

当前代码库已经不再把 `HTML/PDF` 作为主流程输出，也不再以 `outputs/markdown/`、`outputs/scripts/`、`outputs/plans/` 作为主路径。排查问题时，请以 `src/core/pipeline.py` 中定义的 `output_paths` 为准。

---

## 相关文件

- `src/core/pipeline.py`
- `src/planning/slide_planner.py`
- `src/analysis/content_extractor.py`
- `src/generation/pptx_exporter.py`
- `README.md`
