# 🚀 PaperReader Skill 使用指南

## 快速安装

### 方法1: 自动安装（推荐）

```bash
# 在项目根目录运行
./install_skill.sh
```

### 方法2: 手动安装

```bash
# 1. 创建Claude配置目录
mkdir -p ~/.claude/skills

# 2. 复制skill文件
cp skills/paper_reader.yaml ~/.claude/skills/
cp skills/paper_reader.py ~/.claude/skills/

# 3. 重启Claude或重新加载配置
```

## 基本使用

### 1. 最简单的方式

```
/paper
```

- 自动处理 `papers/` 目录中最新的PDF
- 生成HTML格式演示文稿
- 所有输出都在 `output/` 目录

### 2. 指定文件

```
/paper attention.pdf
/paper papers/transformer.pdf
```

### 3. 指定格式

```
/paper --pdf          # 生成PDF格式
/paper --md           # 只生成Markdown
/paper --html         # 生成HTML（默认）
```

### 4. 详细输出

```
/paper attention.pdf --verbose
```

显示：
- 处理进度
- API调用统计
- 成本信息
- 详细日志

## 命令速查表

| 命令 | 说明 | 示例 |
|------|------|------|
| `/paper` | 处理单篇论文 | `/paper attention.pdf` |
| `/papers` | 批量处理 | `/papers` |
| `/ppt` | 快速生成PPT | `/ppt` |
| `/md` | 快速生成MD | `/md paper.pdf` |
| `/papers-stats` | 查看统计 | `/papers-stats` |

## 完整命令详解

### `/paper` - 处理单篇论文

**语法**：
```
/paper [filename] [--format=FORMAT] [--verbose] [--no-cache]
```

**参数**：
- `filename` - PDF文件名（可选，默认使用最新的）
- `--format` / `-f` - 输出格式：`html`（默认）、`pdf`、`md`
- `--verbose` / `-v` - 显示详细进度
- `--no-cache` - 强制重新分析（不使用缓存）

**示例**：

```bash
# 最简单：处理最新PDF
/paper

# 指定文件
/paper attention.pdf

# 生成PDF格式
/paper attention.pdf --pdf

# 详细输出
/paper attention.pdf --verbose

# 强制重新分析
/paper attention.pdf --no-cache

# 只生成Markdown
/paper attention.pdf -f md
```

### `/papers` - 批量处理

**语法**：
```
/papers [--format=FORMAT]
```

**示例**：
```bash
# 处理所有论文（HTML格式）
/papers

# 全部生成PDF
/papers --pdf
```

### `/ppt` - 快速生成PPT

**语法**：
```
/ppt [filename]
```

**说明**：等同于 `/paper [filename] --format=html`

**示例**：
```bash
# 最新PDF生成PPT
/ppt

# 指定文件
/ppt attention.pdf
```

### `/md` - 快速生成Markdown

**语法**：
```
/md [filename]
```

**说明**：等同于 `/paper [filename] --format=md`

**示例**：
```bash
# 最新PDF生成MD
/md

# 指定文件
/md transformer.pdf
```

### `/papers-stats` - 查看统计

**语法**：
```
/papers-stats
```

**输出**：
```
Cache Statistics:
  Total files: 15
  Valid files: 12
  Expired files: 3
  Total size: 0.35 MB
```

## 使用场景

### 场景1: 快速浏览新论文

```bash
# 1. 下载论文到papers/目录
# 2. 打开Claude对话框
# 3. 输入：
/paper

# 4. 等待处理完成（15-30秒）
# 5. 查看output/slides/xxx.html
```

### 场景2: 批量准备组会材料

```bash
# 1. 将所有论文放入papers/
# 2. 运行：
/papers --pdf

# 3. 所有PPT都在output/slides/目录
```

### 场景3: 快速生成Markdown（用于编辑）

```bash
# 生成可编辑的Markdown
/md attention.pdf

# 编辑output/markdown/attention.md
# 然后手动调整内容
```

### 场景4: 重新分析论文

```bash
# 如果AI分析结果不满意，强制重新处理
/paper attention.pdf --no-cache --verbose
```

## 工作流程示例

### 典型的一天

```
早晨：
  📥 下载了3篇新论文 → papers/

Claude对话框：
  👤 /papers --verbose

  🤖 Processing papers...
     ✓ attention.pdf (15s, $0.08)
     ✓ transformer.pdf (12s, $0.06)
     ✓ bert.pdf (18s, $0.09)

  📊 Summary:
     Total time: 45s
     Total cost: $0.23
     Output: output/slides/

下午：
  📂 打开output/slides/attention.html
  📊 准备组会演示
```

## 高级用法

### 1. 结合自然语言

```
👤: 帮我处理attention.pdf，我想要PDF格式

🤖: 我来帮你处理这篇论文。
    运行: /paper attention.pdf --pdf

    ✅ 处理完成！
    输出: output/slides/attention.pdf
```

### 2. 批量处理特定前缀

虽然skill不支持通配符，但可以这样：

```python
# 在Claude中运行Python代码
import glob
files = glob.glob('papers/arxiv_*.pdf')
print(f"Found {len(files)} papers")
for f in files:
    print(f"/paper {f}")
```

然后复制粘贴输出的命令。

### 3. 检查处理状态

```
/papers-stats

如果有3个缓存文件：
  - 说明已处理3篇论文
  - 可以快速重新生成
  - 不需要重新调用API
```

## 自定义配置

### 修改默认格式

编辑 `~/.claude/skills/paper_reader.yaml`：

```yaml
preferences:
  default_format: pdf  # 改为PDF
```

### 禁用成本警告

```yaml
preferences:
  show_cost_warning: false
```

### 更改缓存时间

```yaml
preferences:
  cache_ttl_days: 30  # 延长到30天
```

## 性能优化建议

### 1. 利用缓存

- 相同论文只分析一次
- 7天内重复处理免费
- 缓存命中率通常>60%

### 2. 选择合适格式

| 格式 | 速度 | 优点 | 缺点 |
|------|------|------|------|
| Markdown | ⚡⚡⚡ 最快 | 可编辑 | 需要Marp转换 |
| HTML | ⚡⚡ 快 | 即用 | 依赖Marp |
| PDF | ⚡ 慢 | 通用 | 需要Chrome |

### 3. 批量处理

```bash
# 比单独处理更快
/papers

# 而不是
/paper 1.pdf
/paper 2.pdf
/paper 3.pdf
```

## 故障排除

### 问题1: "PDF not found"

**原因**: 文件不在papers/目录

**解决**:
```bash
# 检查文件位置
ls papers/

# 使用完整路径
/paper /path/to/paper.pdf
```

### 问题2: "API key not found"

**原因**: 未设置ANTHROPIC_API_KEY

**解决**:
```bash
# 创建.env文件
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# 或设置环境变量
export ANTHROPIC_API_KEY=sk-ant-...
```

### 问题3: "Marp CLI not found"

**原因**: 未安装Marp

**解决**:
```bash
npm install -g @marp-team/marp-cli

# 或使用Markdown格式（不需要Marp）
/paper --md
```

### 问题4: 处理很慢

**原因**: 可能是首次处理或网络问题

**解决**:
```bash
# 使用verbose查看进度
/paper --verbose

# 检查网络连接
# 检查API状态
```

### 问题5: 缓存失效

**原因**: PDF文件被修改或缓存过期

**解决**:
```bash
# 检查缓存状态
/papers-stats

# 清理过期缓存
python main.py cleanup
```

## 与其他工具集成

### 1. 与文件管理器集成

MacOS Finder / Windows Explorer:
- 右键PDF文件
- 选择"Services" → "Process with PaperReader"

### 2. 与编辑器集成

VS Code / Vim:
```bash
# 打开Markdown预览
code output/markdown/attention.md

# 实时编辑
```

### 3. 自动化脚本

```bash
# 监控papers/目录，自动处理新文件
./watch_and_process.sh
```

## 成本控制

### 单篇论文成本

- **首次处理**: $0.05-0.10
- **缓存命中**: $0.00
- **平均成本**: $0.02-0.05（考虑缓存）

### 成本估算

```
10篇论文（无缓存）: ~$0.50-1.00
10篇论文（50%缓存）: ~$0.25-0.50
100篇论文（70%缓存）: ~$3.00-6.00
```

### 节省成本技巧

1. ✅ 启用缓存（默认启用）
2. ✅ 批量处理（避免重复）
3. ✅ 使用Markdown格式（最快）
4. ❌ 避免频繁使用 `--no-cache`

## 最佳实践

### 1. 论文组织

```
papers/
├── 2024-01/
│   ├── attention.pdf
│   └── transformer.pdf
├── 2024-02/
│   └── bert.pdf
└── to_read/
    └── new_paper.pdf
```

### 2. 命名规范

```bash
# 好的命名
2024_vaswani_attention.pdf
2024_devlin_bert.pdf

# 避免
paper1.pdf
download.pdf
```

### 3. 定期维护

```bash
# 每周运行一次
python main.py cleanup  # 清理过期缓存
python main.py stats    # 检查使用情况
```

## 反馈和支持

- 📧 Email: support@paperreader.com
- 💬 Issues: github.com/paperreader/issues
- 📖 文档: README.md, CLAUDE.md

---

**Skill版本**: v1.0.0
**更新日期**: 2026-03-05
