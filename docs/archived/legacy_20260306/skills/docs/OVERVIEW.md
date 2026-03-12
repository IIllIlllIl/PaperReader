# PaperReader Skills 目录

本目录包含PaperReader的Claude Skill集成系统，让您可以在Claude对话框中用最简单的命令处理学术论文。

## 📁 文件说明

### 核心文件

| 文件 | 说明 | 必需 |
|------|------|------|
| `paper_reader.yaml` | Skill配置文件 | ✅ |
| `paper_reader.py` | Skill执行处理器 | ✅ |
| `install_skill.sh` | 自动安装脚本 | ✅ |

### 文档文件

| 文件 | 说明 |
|------|------|
| `README.md` | 完整使用指南 |
| `QUICK_REFERENCE.md` | 快速参考卡片 |
| `PROMPT_SUGGESTIONS.md` | Prompt技巧和建议 |

## 🚀 快速开始

### 1. 安装

```bash
# 自动安装（推荐）
./tools/install_skill.sh

# 或手动安装
mkdir -p ~/.claude/skills
cp paper_reader.yaml paper_reader.py ~/.claude/skills/
```

### 2. 配置API密钥

```bash
# 编辑项目根目录的 .env 文件
echo "ANTHROPIC_API_KEY=your-key-here" > ../.env
```

### 3. 使用

在Claude对话框中：

```
/paper                    # 处理最新PDF
/paper attention.pdf      # 处理指定文件
/papers                   # 批量处理
```

## 📖 文档导航

### 新手入门
1. 阅读 [README.md](README.md) - 了解所有命令和功能
2. 查看 [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 快速参考
3. 学习 [PROMPT_SUGGESTIONS.md](PROMPT_SUGGESTIONS.md) - 提高效率

### 快速查询
- 命令语法 → QUICK_REFERENCE.md
- 使用示例 → README.md
- Prompt技巧 → PROMPT_SUGGESTIONS.md

## 🎯 核心命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `/paper` | 处理单篇论文 | `/paper file.pdf` |
| `/papers` | 批量处理 | `/papers` |
| `/ppt` | 快速PPT | `/ppt` |
| `/md` | 快速MD | `/md file.pdf` |
| `/papers-stats` | 查看统计 | `/papers-stats` |

## 💡 最常用操作

### 场景1: 日常阅读
```bash
# 1. 下载论文到 papers/
# 2. 在Claude中输入:
/paper
# 3. 查看输出: output/slides/xxx.html
```

### 场景2: 批量准备
```bash
# 1. 放置所有论文到 papers/
# 2. 在Claude中输入:
/papers --pdf
# 3. 所有PPT在 output/slides/
```

### 场景3: 快速编辑
```bash
# 生成可编辑的Markdown
/md attention.pdf
# 编辑 output/markdown/attention.md
```

## 🔧 配置选项

### 默认配置
- 输出格式: HTML
- 缓存: 启用（7天TTL）
- 进度显示: 启用
- 成本警告: 启用

### 自定义配置
编辑 `~/.claude/skills/paper_reader.yaml`：

```yaml
preferences:
  default_format: pdf      # 改为PDF
  cache_enabled: true      # 启用缓存
  show_cost_warning: true  # 显示成本
```

## 📊 性能参考

| 操作 | 首次处理 | 缓存命中 | 成本 |
|------|---------|---------|------|
| 单篇 | 15-30s | 2-5s | $0.05-0.10 |
| 批量(10篇) | 3-5min | 30s | $0.50-1.00 |
| 缓存节省 | - | 100% | 70% |

## 🔍 故障排除

### 常见问题

**Q: 命令无法识别**
```bash
# 检查skill是否安装
ls ~/.claude/skills/paper_reader.*

# 重新安装
./tools/install_skill.sh
```

**Q: PDF未找到**
```bash
# 检查文件位置
ls ../papers/*.pdf

# 使用完整路径
/paper /path/to/paper.pdf
```

**Q: API密钥错误**
```bash
# 检查.env文件
cat ../.env

# 设置密钥
echo "ANTHROPIC_API_KEY=sk-ant-..." > ../.env
```

**Q: Marp未找到**
```bash
# 安装Marp CLI
npm install -g @marp-team/marp-cli

# 或使用Markdown格式
/paper --md
```

## 📚 相关文档

### 项目文档
- [主README](../README.md) - 项目总览
- [数据流程](../UNDERSTANDING_DATA_FLOW.md) - 理解中间产物
- [开发文档](../CLAUDE.md) - 开发者指南

### 示例和工具
- [中间产物示例](../examples/middle_products_example.py)
- [数据流程调试](../debug_data_flow.py)

## 🎓 学习路径

### 第1天：基础
- [ ] 安装skill
- [ ] 处理第一篇论文
- [ ] 查看输出结果

### 第2天：进阶
- [ ] 尝试不同格式
- [ ] 批量处理
- [ ] 查看统计信息

### 第3天：高级
- [ ] 自定义配置
- [ ] Prompt技巧
- [ ] 故障排除

## 💬 获取帮助

### 文档帮助
- 快速参考: `QUICK_REFERENCE.md`
- 完整指南: `README.md`
- Prompt技巧: `PROMPT_SUGGESTIONS.md`

### 命令帮助
```
/paper --help
```

### 项目支持
- Issues: github.com/paperreader/issues
- Email: support@paperreader.com

## 🎉 快速测试

```bash
# 1. 安装
./tools/install_skill.sh

# 2. 配置
echo "ANTHROPIC_API_KEY=test" > ../.env

# 3. 测试
python3 -c "from skills.paper_reader import handle_paper_command; print('✓ Skill已就绪')"

# 4. 在Claude中使用
/paper
```

## 📝 更新日志

### v1.0.0 (2026-03-05)
- ✅ 初始版本发布
- ✅ 5个核心命令
- ✅ 自动补全支持
- ✅ 文件监控集成
- ✅ 完整文档

## 🚧 开发计划

### v1.1.0 (计划中)
- [ ] Web界面集成
- [ ] 更多输出格式
- [ ] 自定义模板
- [ ] OCR支持

### v1.2.0 (计划中)
- [ ] 多语言支持
- [ ] 图表提取
- [ ] 协作功能

## 🤝 贡献

欢迎贡献代码、文档或建议！

## 📄 许可证

MIT License

---

**Happy Paper Reading! 📚✨**

**版本**: v1.0.0 | **更新**: 2026-03-05 | **维护**: PaperReader Team
