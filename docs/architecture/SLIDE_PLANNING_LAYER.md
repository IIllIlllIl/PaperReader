# Slide Planning Layer

## 概述

Slide Planning Layer 是当前主流程中的规划层，负责决定每页幻灯片应该覆盖什么主题，再由后续内容层把这些主题扩展为实际的幻灯片内容。

在当前实现中：

- 规划层入口：`src/planning/slide_planner.py`
- 主流程调用位置：`src/core/pipeline.py`
- 规划层输出：`SlidePlan`

## 在主流程中的位置

```text
PDF
→ Parse
→ AI Analysis
→ Slide Planning
→ Narrative Planning
→ Content Extraction
→ Markdown Generation
→ PPTX Export
```

在 `src/core/pipeline.py` 中，规划层位于 AI analysis 之后、narrative planning 之前。

## 当前实现

`SlidePlanner.plan_slides(..., use_structured_template=True)` 默认启用结构化模板，因此当前主流程默认不会走旧的自由规划分支，而是直接生成稳定的结构化 `SlidePlan`。

相关实现可参考：

- `src/planning/slide_planner.py`
- `src/planning/models.py`
- `src/core/pipeline.py`

## 当前默认模板

当前默认模板为结构化 10 页：

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

如有引用分析数据，规划层还可以在讨论部分之前插入引用相关页面。

## `SlidePlan` 的作用

`SlidePlan` 是内容生成前的结构化规划结果，用来定义：

- 每页的标题
- 每页的关键点
- 每页的 slide type
- 内容层应该如何组织后续幻灯片

这让规划层与内容层职责分离：

- Planning layer：决定 **讲什么**
- Content layer：决定 **怎么讲**

## 设计价值

### 1. 结构稳定

默认模板让最终演示结构更稳定，避免页数和主题大幅波动。

### 2. 更易调试

主流程会把 `SlidePlan` 持久化到：

```text
outputs/intermediates/plans/{paper_name}_plan.json
```

因此可以在不看最终 PPTX 的情况下先检查规划结果。

### 3. 更易扩展

未来若要调整演示结构，可以优先修改 `SlidePlanner`，而不必先改 markdown 或 PPTX 导出逻辑。

## 与内容层的关系

主流程中这两个阶段是连续的：

1. `SlidePlanner` 生成 `SlidePlan`
2. `ContentExtractor` 根据 `SlidePlan` 生成 `OrganizedPresentation`

随后 `PPTGenerator` 生成 markdown，`pptx_exporter` 导出最终 `.pptx`。

## 调试建议

运行：

```bash
python -m src.cli.main pipeline --paper papers/example.pdf --no-clean
```

然后优先检查：

1. `outputs/intermediates/plans/`
2. `outputs/intermediates/markdown/`
3. `outputs/slides/`

## 注意

- 当前默认模板是 **10 slides**，不是 11 slides
- 当前推荐主流程是 `pipeline`
- 若文档与代码不一致，以 `src/planning/slide_planner.py` 为准

---

**最后更新**: 2026-03-20
