# PaperReader 文档中心

欢迎来到PaperReader文档中心！这里包含了所有详细的项目文档。

## 📚 文档导航

### 🚀 快速开始

- **[项目总览](../README.md)** - 快速开始指南和安装说明
- **[开发者指南](../CLAUDE.md)** - 架构设计和开发指南

### 📊 数据流程文档

理解PaperReader如何处理论文的完整数据流程：

- **[数据流程详解](DATA_FLOW.md)** - 完整的9个阶段说明，每个中间产物的详细描述
- **[快速参考卡片](DATA_FLOW_QUICK_REFERENCE.md)** - 中间产物一览表、核心数据结构速查
- **[可视化流程图](DATA_VISUALIZATION.md)** - 完整的可视化流程图、时间成本分析
- **[理解数据流](UNDERSTANDING_DATA_FLOW.md)** - 学习路径、文档导航、实用命令

### 📈 项目信息

- **[项目总结](PROJECT_SUMMARY.md)** - 项目完成报告、统计数据、验收标准

### 🔧 Claude Skills

- **[Skills文档](../skills/README.md)** - Claude集成使用指南
- **[快速参考](../skills/docs/QUICK_REFERENCE.md)** - Skills命令速查
- **[Prompt建议](../skills/docs/PROMPT_SUGGESTIONS.md)** - 高效使用技巧

## 📖 文档结构

```
docs/
├── README.md                      # 本文件 - 文档导航
├── DATA_FLOW.md                   # 详细数据流程说明
├── DATA_FLOW_QUICK_REFERENCE.md   # 快速参考卡片
├── DATA_VISUALIZATION.md          # 可视化流程图
├── UNDERSTANDING_DATA_FLOW.md     # 学习指南
└── PROJECT_SUMMARY.md             # 项目总结
```

## 🎯 根据需求查找文档

### 我想了解...

**"整个系统是如何工作的？"**
→ 从 [DATA_VISUALIZATION.md](DATA_VISUALIZATION.md) 开始

**"AI分析输出了什么？"**
→ 查看 [DATA_FLOW.md](DATA_FLOW.md) 的阶段4和5

**"中间产物的格式是什么？"**
→ 查看 [DATA_FLOW_QUICK_REFERENCE.md](DATA_FLOW_QUICK_REFERENCE.md)

**"如何调试论文处理？"**
→ 查看 [UNDERSTANDING_DATA_FLOW.md](UNDERSTANDING_DATA_FLOW.md)

**"成本和时间消耗如何？"**
→ 查看 [DATA_VISUALIZATION.md](DATA_VISUALIZATION.md) 的成本分析

## 🛠️ 开发者文档

### 核心模块
- `src/pdf_parser.py` - PDF解析
- `src/ai_analyzer.py` - AI分析
- `src/ppt_generator.py` - PPT生成
- 详细说明见 [CLAUDE.md](../CLAUDE.md)

### 工具脚本
- `tools/debug_data_flow.py` - 数据流调试
- `tools/md_to_pptx.py` - Markdown转PPTX
- 详细说明见 [tools/](../tools/)

### 测试
- `tests/` - 测试套件
- 详细说明见 [CLAUDE.md](../CLAUDE.md)

## 📝 示例和演示

- **[示例代码](../examples/)** - 中间产物示例
- **[调试工具](../tools/)** - 数据流程追踪工具

## 💡 学习路径

### 初级（15分钟）
1. 阅读 [DATA_VISUALIZATION.md](DATA_VISUALIZATION.md) - 了解整体流程
2. 运行 `python tools/debug_data_flow.py papers/example.pdf --skip-ai`
3. 浏览 [DATA_FLOW_QUICK_REFERENCE.md](DATA_FLOW_QUICK_REFERENCE.md)

### 中级（1小时）
1. 查看 [examples/middle_products_example.py](../examples/middle_products_example.py)
2. 阅读 [DATA_FLOW.md](DATA_FLOW.md)
3. 真实处理一篇论文

### 高级（2小时）
1. 完成中级学习
2. 阅读源代码
3. 修改和实验

## 🔍 快速命令参考

```bash
# 处理论文
python cli/main.py process --paper papers/example.pdf

# 查看数据流程
python tools/debug_data_flow.py papers/example.pdf --skip-ai

# 转换为PPTX
python tools/md_to_pptx.py output/markdown/example.md

# 查看缓存
python cli/main.py stats
```

## 📞 获取帮助

- **使用问题**: 查看 [README.md](../README.md)
- **开发问题**: 查看 [CLAUDE.md](../CLAUDE.md)
- **Skills问题**: 查看 [skills/README.md](../skills/README.md)

---

**文档版本**: v1.0.0 | **更新日期**: 2026-03-05
