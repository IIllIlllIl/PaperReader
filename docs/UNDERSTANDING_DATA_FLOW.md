# 📚 PaperReader 数据流程文档索引

本项目的数据流程文档已经齐全，帮助您深入理解系统的每个环节。

## 📖 文档导航

### 1. 快速入门
- **[DATA_VISUALIZATION.md](DATA_VISUALIZATION.md)** ⭐ **从这里开始**
  - 完整的流程图可视化
  - 时间和成本分析
  - 关键决策点
  - 适合快速了解整体流程

### 2. 详细参考
- **[DATA_FLOW.md](DATA_FLOW.md)**
  - 详细的9个阶段说明
  - 每个中间产物的完整描述
  - 数据格式和结构
  - 真实案例演示
  - 适合深入理解每个细节

- **[DATA_FLOW_QUICK_REFERENCE.md](DATA_FLOW_QUICK_REFERENCE.md)**
  - 快速参考卡片
  - 中间产物一览表
  - 核心数据结构
  - 调试技巧
  - 适合日常查阅

### 3. 示例代码
- **[examples/middle_products_example.py](examples/middle_products_example.py)**
  - 所有中间产物的完整示例
  - 基于"Attention Is All You Need"论文
  - 可直接运行查看
  - 适合学习数据格式

- **[examples/README.md](examples/README.md)**
  - 示例文件使用指南
  - 学习路径建议

### 4. 调试工具
- **[debug_data_flow.py](debug_data_flow.py)**
  - 交互式数据流程追踪
  - 实时显示中间产物
  - 支持示例数据模式
  - 适合调试和学习

## 🎯 学习路径推荐

### 路径1: 快速理解（15分钟）
```
1. 阅读 DATA_VISUALIZATION.md (5分钟)
   └─> 了解整体流程和关键概念

2. 运行 debug_data_flow.py --skip-ai (5分钟)
   └─> 查看真实论文的中间产物

3. 浏览 DATA_FLOW_QUICK_REFERENCE.md (5分钟)
   └─> 掌握关键数据结构
```

### 路径2: 深入学习（1小时）
```
1. 阅读路径1的所有内容 (15分钟)

2. 运行 middle_products_example.py (5分钟)
   └─> 查看完整示例数据

3. 阅读 DATA_FLOW.md (20分钟)
   └─> 理解每个阶段的详细处理

4. 真实处理一篇论文 (15分钟)
   python cli/main.py process -p papers/example.pdf -v

5. 检查缓存文件 (5分钟)
   cat cache/{hash}.json | jq .
```

### 路径3: 开发者深入（2小时）
```
1. 完成路径2的所有内容 (1小时)

2. 阅读源代码 (30分钟)
   ├─ src/pdf_parser.py
   ├─ src/ai_analyzer.py
   └─ src/ppt_generator.py

3. 修改和实验 (30分钟)
   └─ 调整prompt、模板等
```

## 🔍 按需求查找

### 我想了解...

**"整个系统是如何工作的？"**
→ 从 [DATA_VISUALIZATION.md](DATA_VISUALIZATION.md) 开始

**"AI分析输出了什么？"**
→ 查看 [DATA_FLOW.md](DATA_FLOW.md) 的阶段4和5

**"中间产物的格式是什么？"**
→ 运行 `python examples/middle_products_example.py`

**"缓存文件里有什么？"**
→ 查看 [DATA_FLOW.md](DATA_FLOW.md) 的缓存文件示例

**"如何调试我的论文处理？"**
→ 运行 `python tools/debug_data_flow.py papers/your_paper.pdf`

**"成本和时间消耗如何？"**
→ 查看 [DATA_VISUALIZATION.md](DATA_VISUALIZATION.md) 的成本分析

**"数据在内存中如何流转？"**
→ 查看 [DATA_FLOW.md](DATA_FLOW.md) 的数据流图

**"如何查看真实案例？"**
→ 运行 `python tools/debug_data_flow.py papers/example.pdf --skip-ai`

## 📊 核心中间产物速查

| 产物 | 查看方式 | 文档位置 |
|------|---------|---------|
| PDF验证结果 | debug_data_flow.py | DATA_FLOW.md#阶段1 |
| 提取的文本 | debug_data_flow.py | DATA_FLOW.md#阶段2 |
| 论文元数据 | debug_data_flow.py | DATA_FLOW.md#阶段2 |
| PDF哈希 | cache目录文件名 | DATA_FLOW.md#阶段3 |
| AI分析结果 | cache/{hash}.json | DATA_FLOW.md#阶段4 |
| 演示内容 | cache/{hash}.json | DATA_FLOW.md#阶段5 |
| 组织的幻灯片 | debug_data_flow.py | DATA_FLOW.md#阶段7 |
| Markdown | output/markdown/ | DATA_FLOW.md#阶段8 |
| 最终PPT | output/slides/ | DATA_FLOW.md#阶段9 |

## 🛠️ 实用命令

```bash
# 查看完整的数据流程（使用示例数据）
python tools/debug_data_flow.py papers/example.pdf --skip-ai

# 查看完整的数据流程（真实AI分析）
python tools/debug_data_flow.py papers/example.pdf

# 查看示例中间产物
python examples/middle_products_example.py

# 查看缓存内容
cat cache/*.json | jq .

# 查看生成的Markdown
cat output/markdown/*.md

# 统计信息
python cli/main.py stats
```

## 📚 文档关系图

```
                    ┌─────────────────────┐
                    │  README.md          │
                    │  (使用指南)          │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                  │
    ┌─────────▼──────────┐          ┌──────────▼──────────┐
    │ DATA_VISUALIZATION │          │    CLAUDE.md        │
    │     (流程可视化)    │          │   (开发指南)         │
    └─────────┬──────────┘          └─────────────────────┘
              │
    ┌─────────┴──────────────────────────────┐
    │                                         │
┌───▼──────────────┐              ┌──────────▼──────────┐
│   DATA_FLOW.md   │              │  DATA_FLOW_QUICK_   │
│   (详细流程)      │              │  REFERENCE.md       │
└───┬──────────────┘              │  (快速参考)          │
    │                              └─────────────────────┘
    │
┌───┴──────────────────────────────────────────────┐
│                                                   │
│          examples/                                │
│          ├─ middle_products_example.py           │
│          └─ README.md                             │
│                                                   │
│          debug_data_flow.py                       │
│          (调试工具)                                │
└───────────────────────────────────────────────────┘
```

## 🎓 关键概念

### 数据流
1. **PDF** → 验证 → 提取 → **文本**
2. **文本** → AI分析 → **PaperAnalysis**
3. **PaperAnalysis** → 内容生成 → **PresentationContent**
4. **PresentationContent** → 组织 → **Slides**
5. **Slides** → Markdown生成 → **输出文件**

### 核心对象
- `ValidationResult` - PDF质量评估
- `PaperMetadata` - 论文元数据
- `PaperAnalysis` - AI分析结果（10个字段）
- `PresentationContent` - 演示内容（17个字段）
- `SlideContent` - 单个幻灯片
- `OrganizedPresentation` - 完整演示（15-20个幻灯片）

### 关键优化
- **缓存** - 基于文件哈希，7天TTL
- **分段分析** - 快速浏览 + 深度分析
- **错误重试** - 指数退避，最多3次
- **成本追踪** - 实时统计API使用

## 💡 提示

1. **第一次使用**：先阅读 DATA_VISUALIZATION.md，了解整体流程
2. **调试问题**：使用 debug_data_flow.py 查看中间产物
3. **理解格式**：运行 middle_products_example.py 查看示例
4. **日常参考**：使用 DATA_FLOW_QUICK_REFERENCE.md 快速查找
5. **深入学习**：阅读 DATA_FLOW.md 了解每个细节

## 📞 获取帮助

- **文档问题**：查看对应的文档文件
- **代码问题**：查看源代码注释
- **使用问题**：查看 README.md
- **开发问题**：查看 CLAUDE.md

---

**文档版本**: v1.0
**最后更新**: 2026-03-05
**维护者**: PaperReader Team
