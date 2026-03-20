# Quick Start Examples

## Basic Usage (Recommended)

```bash
python cli/main.py pipeline --paper papers/example.pdf
```

默认成功后会保留最终 PPTX，并清理中间文件。

### 最终输出

- `outputs/slides/example.pptx` - 最终汇报文件

### 调试时保留中间文件

```bash
python cli/main.py pipeline --paper papers/example.pdf --no-clean
```

此时可检查：
- `outputs/intermediates/markdown/example.md`
- `outputs/intermediates/plans/example_plan.json`
- `outputs/intermediates/scripts/example_presentation_script.md`
- `outputs/intermediates/images/`
- `outputs/intermediates/citations/`

---

## 常用命令

### 启用引用分析

```bash
python cli/main.py pipeline --paper papers/example.pdf --include-citations
```

### 查看详细日志

```bash
python cli/main.py pipeline --paper papers/example.pdf --verbose
```

### 缓存管理

```bash
python cli/main.py stats
python cli/main.py cleanup
python cli/main.py clear-cache
```

### 手动清理中间文件

```bash
python scripts/clean_intermediates.py
python scripts/clean_intermediates.py --execute
```

---

## 推荐工作流

```bash
# 1. 放入论文
cp ~/Downloads/my-paper.pdf papers/

# 2. 生成 PPTX
python cli/main.py pipeline --paper papers/my-paper.pdf

# 3. 查看结果
open outputs/slides/my-paper.pptx

# 4. 如需排查，保留中间文件重新运行
python cli/main.py pipeline --paper papers/my-paper.pdf --no-clean
```

---

## 相关文档

- `README.md`
- `docs/user-guide/ENHANCED_PPTX_GUIDE.md`
- `docs/BEST_PRACTICES.md`
- `docs/architecture/PIPELINE_IMPLEMENTATION.md`
