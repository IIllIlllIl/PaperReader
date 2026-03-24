# PaperReader 数据流程快速参考

## 当前推荐命令

```bash
python -m src.cli.main pipeline --paper papers/example.pdf
```

保留中间文件用于调试：

```bash
python -m src.cli.main pipeline --paper papers/example.pdf --no-clean
```

启用引用分析：

```bash
python -m src.cli.main pipeline --paper papers/example.pdf --include-citations
```

---

## 阶段速查

| 阶段 | 名称 | 主要输出 | 持久化位置 |
|---|---|---|---|
| 1 | Parse PDF | `paper_text`, `metadata` | 内存 |
| 2 | Extract sections | `sections` | 内存 |
| 3 | AI analysis | `PaperAnalysis` | 内存 |
| 3.5 | Citation analysis（可选） | `citation_result` | 内存 / 中间目录 |
| 4 | Slide planning | `SlidePlan` | `outputs/intermediates/plans/` |
| 5 | Narrative planning | `PresentationNarrative` | 内存 |
| 6 | Generate slides | Markdown + `OrganizedPresentation` | `outputs/intermediates/markdown/` |
| 7 | Export PPTX | `.pptx` | `outputs/slides/` |
| 8 | Generate script | 讲稿 Markdown | `outputs/intermediates/scripts/` |

---

## 输出目录速查

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

默认成功后会清理中间文件；如需保留，请使用 `--no-clean`。

---

## 当前默认演示结构

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

---

## 核心对象

### `PaperAnalysis`
AI 对论文的结构化分析结果，包含问题、方法、结果、优缺点和结论。

### `SlidePlan`
规划层输出，定义每页幻灯片的主题、关键点和类型。

### `OrganizedPresentation`
内容层输出，表示最终 Markdown/PPTX 使用的幻灯片集合。

---

## 常用命令

```bash
# 主流程
python -m src.cli.main pipeline --paper papers/example.pdf

# 保留中间文件
python -m src.cli.main pipeline --paper papers/example.pdf --no-clean

# 启用引用分析
python -m src.cli.main pipeline --paper papers/example.pdf --include-citations

# 查看缓存统计
python -m src.cli.main stats

# 清理过期缓存
python -m src.cli.main cleanup
```

---

## 排查时最先看什么

1. `outputs/slides/`：最终 PPTX 是否生成
2. `outputs/intermediates/plans/`：规划结果是否合理
3. `outputs/intermediates/markdown/`：Markdown 幻灯片是否正确
4. `outputs/intermediates/scripts/`：讲稿是否与幻灯片对齐
5. `runtime/cache/`：AI 分析缓存是否命中

---

## 注意

- 当前主流程文档以 `pipeline` 命令为准。
- 不要再把 `HTML/PDF` 视为当前推荐输出。
- 不要再把 `outputs/markdown/`、`outputs/scripts/`、`outputs/plans/` 当作主路径。
