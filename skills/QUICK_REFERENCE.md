# PaperReader Skill 快速参考卡片

## 🚀 快速命令

| 命令 | 说明 | 最简形式 |
|------|------|---------|
| `/paper` | 处理论文 | `/paper` |
| `/ppt` | 快速PPT | `/ppt` |
| `/md` | 快速MD | `/md` |
| `/papers` | 批量处理 | `/papers` |
| `/papers-stats` | 查看统计 | `/papers-stats` |

## 📝 命令格式

### 基础
```bash
/paper                    # 处理最新PDF
/paper attention.pdf      # 处理指定文件
```

### 格式
```bash
/paper --html            # HTML格式（默认）
/paper --pdf             # PDF格式
/paper --md              # Markdown格式
```

### 选项
```bash
/paper --verbose         # 详细输出
/paper --no-cache        # 强制重新分析
```

### 组合
```bash
/paper attention.pdf --pdf --verbose
```

## 💡 最常用场景

### 场景1: 快速处理新论文
```bash
# 1. 下载论文到 papers/
# 2. 运行:
/paper
# 3. 查看输出: output/slides/xxx.html
```

### 场景2: 批量准备材料
```bash
/papers --pdf
# 所有论文 → PDF格式
```

### 场景3: 快速Markdown
```bash
/md attention.pdf
# 生成可编辑的Markdown
```

## ⚡ 性能对比

| 操作 | 首次 | 缓存命中 |
|------|------|---------|
| 单篇 | 15-30s | 2-5s |
| 批量（10篇） | 3-5min | 30s |
| 成本 | $0.05-0.10 | $0.00 |

## 🔍 故障排除

| 问题 | 解决 |
|------|------|
| PDF未找到 | 检查 `papers/` 目录 |
| API密钥错误 | 编辑 `.env` 文件 |
| Marp未找到 | 使用 `--md` 或安装Marp |
| 处理很慢 | 使用 `--verbose` 查看 |

## 📊 输出位置

```
output/
├── markdown/  # Markdown文件
└── slides/    # HTML/PDF文件
```

## 🎯 最佳实践

1. ✅ 利用缓存（默认启用）
2. ✅ 批量处理更高效
3. ✅ Markdown格式最快
4. ✅ 定期清理缓存

## 📚 完整文档

- 使用指南: `skills/README.md`
- 项目文档: `README.md`
- 数据流程: `UNDERSTANDING_DATA_FLOW.md`

---

**版本**: v1.0.0 | **更新**: 2026-03-05
