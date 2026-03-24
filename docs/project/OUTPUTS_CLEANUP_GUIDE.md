# Outputs 清理指南

## 概述

当前推荐的 PaperReader 主流程是：

```bash
python -m src.cli.main pipeline --paper papers/example.pdf
```

该流程的最终交付物是 `outputs/slides/{paper_name}.pptx`。
中间产物统一位于 `outputs/intermediates/`，并且默认在成功后自动清理；如需保留，请使用 `--no-clean`。

---

## 当前输出分类

### 最终交付物

```text
outputs/slides/
└── {paper_name}.pptx
```

### 中间产物（默认成功后清理）

```text
outputs/intermediates/
├── markdown/
├── plans/
├── scripts/
├── images/
└── citations/
```

说明：
- `outputs/slides/` 应视为最终交付目录。
- `outputs/intermediates/` 应视为调试、排查、复查目录。
- 如果不使用 `--no-clean`，成功运行后中间产物通常不会保留在工作区。

---

## 推荐清理方式

### 1. 默认自动清理

```bash
python -m src.cli.main pipeline --paper papers/example.pdf
```

这是推荐方式。流程成功后会自动清理中间文件。

### 2. 调试时保留中间文件

```bash
python -m src.cli.main pipeline --paper papers/example.pdf --no-clean
```

适合以下场景：
- 检查 slide plan
- 检查 markdown 幻灯片内容
- 检查 presentation script
- 检查图片提取或引用分析结果

### 3. 手动检查保留的中间产物

```text
outputs/intermediates/plans/
outputs/intermediates/markdown/
outputs/intermediates/scripts/
outputs/intermediates/images/
outputs/intermediates/citations/
```

---

## 提交代码前的清理建议

提交前优先检查：

1. 是否误改了 `outputs/` 下的生成结果
2. 是否保留了 `.claude/worktrees/` 等本地工作区产物
3. 是否有只用于本地调试的中间文件或报告

建议流程：

```bash
# 查看当前工作区
git status --short

# 如需保留中间文件进行排查，先这样运行
python -m src.cli.main pipeline --paper papers/example.pdf --no-clean

# 排查完成后，重新运行默认流程或手动清理不需要的生成物
python -m src.cli.main pipeline --paper papers/example.pdf
```

---

## 当前应保留与不应提交的内容

### 推荐保留

- 源代码改动
- 测试代码
- 真实需要更新的文档
- 必要的配置调整

### 通常不应提交

- `.claude/worktrees/` 下的本地工作区产物
- `outputs/intermediates/` 下的调试中间文件
- 旧目录结构中的本地生成物，例如：
  - `outputs/markdown/`
  - `outputs/plans/`
  - `outputs/scripts/`
  - `outputs/citations/`
  - `outputs/images/citations/`
- 只用于本地验证的临时报告

如需保留中间结果做分析，请在本地使用，不要默认把这些文件作为最终交付物提交。

---

## 调试建议

当你怀疑问题出在流程中间阶段时：

```bash
python -m src.cli.main pipeline --paper papers/example.pdf --verbose --no-clean
```

然后按顺序检查：

1. `outputs/intermediates/plans/`
2. `outputs/intermediates/markdown/`
3. `outputs/intermediates/scripts/`
4. `outputs/slides/`

---

## 与当前实现保持一致的原则

为避免文档再次过时，请遵循以下约定：

- 当前推荐入口是 `python -m src.cli.main pipeline ...`
- 当前推荐最终输出是 `.pptx`
- 当前中间产物主路径是 `outputs/intermediates/...`
- 不要再把 `outputs/markdown/`、`outputs/plans/`、`outputs/scripts/` 当作主路径
- 若文档与代码不一致，以 `src/cli/main.py` 和 `src/core/pipeline.py` 为准

---

## 相关文档

- `README.md`
- `docs/user-guide/ENHANCED_PPTX_GUIDE.md`
- `docs/architecture/PIPELINE_IMPLEMENTATION.md`
- `docs/architecture/DATA_FLOW.md`
- `docs/project/PROJECT_STATUS.md`
