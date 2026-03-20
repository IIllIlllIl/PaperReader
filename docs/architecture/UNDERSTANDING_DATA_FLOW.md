# 📚 PaperReader 数据流程文档索引

这组文档描述当前推荐的 `pipeline` 主流程，以及调试时应关注的中间产物。

## 推荐阅读顺序

### 1. 先看整体流程
- **[PIPELINE_IMPLEMENTATION.md](PIPELINE_IMPLEMENTATION.md)**
  - 当前推荐命令
  - 8 个阶段 + 可选引用分析
  - CLI 参数与输出结构

### 2. 再看详细数据流
- **[DATA_FLOW.md](DATA_FLOW.md)**
  - 每个阶段的输入与输出
  - 中间产物与持久化位置
  - `PaperAnalysis` / `SlidePlan` / `OrganizedPresentation` 等关键对象

### 3. 日常速查
- **[DATA_FLOW_QUICK_REFERENCE.md](DATA_FLOW_QUICK_REFERENCE.md)**
  - 快速命令
  - 目录速查
  - 排查时优先检查的位置

### 4. 可视化理解
- **[DATA_VISUALIZATION.md](DATA_VISUALIZATION.md)**
  - 当前流水线的文本流程图
  - 关键目录与常见排查路径

## 当前推荐命令

```bash
python cli/main.py pipeline --paper papers/example.pdf
```

调试时保留中间文件：

```bash
python cli/main.py pipeline --paper papers/example.pdf --no-clean
```

启用引用分析：

```bash
python cli/main.py pipeline --paper papers/example.pdf --include-citations
```

## 常见问题对应文档

**“完整流程现在怎么跑？”**
→ 看 [PIPELINE_IMPLEMENTATION.md](PIPELINE_IMPLEMENTATION.md)

**“每个阶段会产出什么？”**
→ 看 [DATA_FLOW.md](DATA_FLOW.md)

**“输出文件现在放在哪？”**
→ 看 [DATA_FLOW_QUICK_REFERENCE.md](DATA_FLOW_QUICK_REFERENCE.md)

**“想快速理解整体结构？”**
→ 看 [DATA_VISUALIZATION.md](DATA_VISUALIZATION.md)

## 当前关键中间产物

| 产物 | 位置 |
|---|---|
| Slide plan | `outputs/intermediates/plans/{paper_name}_plan.json` |
| Slides markdown | `outputs/intermediates/markdown/{paper_name}.md` |
| Presentation script | `outputs/intermediates/scripts/{paper_name}_presentation_script.md` |
| Final PPTX | `outputs/slides/{paper_name}.pptx` |

## 调试时建议先看

1. `outputs/slides/`：最终 PPTX 是否生成
2. `outputs/intermediates/plans/`：slide plan 是否合理
3. `outputs/intermediates/markdown/`：markdown 幻灯片内容是否正确
4. `outputs/intermediates/scripts/`：讲稿是否和幻灯片一致
5. `runtime/cache/`：缓存是否命中，分析结果是否复用

## 说明

- 当前文档以 `src/core/pipeline.py` 为主流程事实来源
- 当前最终推荐输出是 `PPTX`
- 不要再把 `HTML/PDF`、`outputs/markdown/`、`tools/debug_data_flow.py` 当作当前主流程的一部分

---

**最后更新**: 2026-03-20
