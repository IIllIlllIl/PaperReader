# 📊 PaperReader 项目状态报告

**更新时间**: 2026-03-20
**项目状态**: ✅ 活跃开发中

---

## 当前重点

当前仓库的推荐使用方式已经收敛到 `pipeline` 主流程：

```bash
python -m src.cli.main pipeline --paper papers/example.pdf
```

该流程会生成最终 `.pptx`，并在需要时保留 `outputs/intermediates/` 下的中间产物用于排查。

---

## 当前项目结构（概览）

```text
PaperReader/
├── docs/                   # 项目文档
├── outputs/                # 生成结果
├── papers/                 # 输入 PDF
├── runtime/                # cache / logs
├── src/                    # 核心源代码
│   ├── cli/                # CLI 入口
│   ├── parser/             # PDF 解析
│   ├── analysis/           # AI 分析
│   ├── planning/           # Slide 规划
│   ├── generation/         # PPTX 生成
│   ├── scripts/            # 工具脚本
│   ├── templates/          # 模板
│   └── tools/              # 工具集
├── tests/                  # 测试
├── CLAUDE.md               # 项目协作说明
├── README.md               # 项目主文档
├── config.yaml             # 配置文件
└── requirements.txt        # Python 依赖
```

说明：

- 当前文档不再维护容易过时的“文件数/目录数”统计
- 具体模块分布请以当前源码目录为准

---

## 当前主流程

`src/core/pipeline.py` 协调的推荐流程：

1. Parse PDF
2. Extract structured sections
3. Run AI analysis
4. Optional citation analysis
5. Generate slide plan
6. Generate narrative
7. Generate slides markdown
8. Export PPTX
9. Generate presentation script

实现日志中可选引用分析会显示为 `3.5` 阶段。

---

## 当前关键模块

- `src/cli/main.py`：CLI 命令入口
- `src/core/pipeline.py`：端到端流程编排
- `src/parser/pdf_parser.py`：PDF 解析
- `src/parser/pdf_image_extractor.py`：图片提取
- `src/analysis/ai_analyzer.py`：AI 分析
- `src/analysis/content_extractor.py`：内容生成
- `src/analysis/citation_integration.py`：引用分析集成
- `src/planning/slide_planner.py`：slide planning
- `src/planning/narrative_planner.py`：讲述主线规划
- `src/generation/pptx_exporter.py`：PPTX 导出

---

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

- 最终交付物在 `outputs/slides/`
- 中间产物在 `outputs/intermediates/`
- 默认成功后清理中间文件；调试时使用 `--no-clean`

---

## 当前默认演示结构

当前默认由 `src/planning/slide_planner.py` 生成结构化 10 页：

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

## 常用命令

```bash
# 推荐主流程
python -m src.cli.main pipeline --paper papers/example.pdf

# 保留中间文件
python -m src.cli.main pipeline --paper papers/example.pdf --no-clean

# 启用引用分析
python -m src.cli.main pipeline --paper papers/example.pdf --include-citations

# 缓存统计
python -m src.cli.main stats

# 清理过期缓存
python -m src.cli.main cleanup
```

`process` 命令仍然存在，但当前推荐用于完整汇报生成的命令是 `pipeline`。

---

## 文档状态

近期已更新的活跃文档重点聚焦：

- 推荐命令统一为 `python -m src.cli.main pipeline ...`
- 最终输出统一为 `.pptx`
- 中间产物路径统一为 `outputs/intermediates/...`
- slide planning 默认结构统一为 10 slides

若文档与代码不一致，以 `src/core/pipeline.py`、`src/cli/main.py`、`src/planning/slide_planner.py` 为准。

---

## 维护建议

- 修改主流程后，同步检查 `README.md` 与 `docs/architecture/`
- 避免在文档中写死文件数量、过时命令名或已删除脚本
- 把 `outputs/slides/` 视为最终产物目录，把 `outputs/intermediates/` 视为排查目录

---

**最后更新**: 2026-03-20
