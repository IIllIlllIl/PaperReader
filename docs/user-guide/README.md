# 用户指南

本目录包含面向日常使用者的说明文档。

## 推荐入口

- **[ENHANCED_PPTX_GUIDE.md](ENHANCED_PPTX_GUIDE.md)** - 当前 `pipeline` 主流程的快速使用说明

## 推荐命令

```bash
python cli/main.py pipeline --paper papers/example.pdf
```

常见变体：

```bash
# 保留中间文件
python cli/main.py pipeline --paper papers/example.pdf --no-clean

# 启用引用分析
python cli/main.py pipeline --paper papers/example.pdf --include-citations
```

## 说明

- 最终输出位于 `outputs/slides/`
- 中间产物位于 `outputs/intermediates/`
- 完整流程说明见 `docs/architecture/PIPELINE_IMPLEMENTATION.md`

---

**最后更新**: 2026-03-20
