# PaperReader 数据流程快速参考

## 📊 中间产物一览表

| # | 阶段 | 中间产物 | 格式 | 大小 | 持久化 | 位置 |
|---|------|---------|------|------|--------|------|
| 0 | 输入 | PDF文件 | 二进制 | 1-5 MB | ✅ | papers/ |
| 1 | 验证 | ValidationResult | dataclass | ~500 B | ❌ | 内存 |
| 2 | 提取 | paper_text | 字符串 | 50-200 KB | ❌ | 内存 |
| 2 | 提取 | sections | Dict | 10-50 KB | ❌ | 内存 |
| 2 | 提取 | PaperMetadata | dataclass | ~1 KB | ❌ | 内存 |
| 3 | 哈希 | pdf_hash | 字符串 | 32 B | ❌ | 内存 |
| 4 | AI分析 | PaperAnalysis | dataclass | 5-10 KB | ✅ | runtime/cache/ |
| 5 | 内容生成 | PresentationContent | dataclass | 10-20 KB | ✅ | runtime/cache/ |
| 6 | 缓存 | {hash}.json | JSON | 15-30 KB | ✅ | runtime/cache/ |
| 7 | 组织 | OrganizedPresentation | dataclass | 10-15 KB | ❌ | 内存 |
| 8 | 生成 | Markdown | 文本 | 20-40 KB | ✅ | outputs/markdown/ |
| 9 | 转换 | HTML/PDF | 文件 | 50KB-2MB | ✅ | outputs/slides/ |

## 🔄 数据流转示意图

```
PDF文件 (papers/example.pdf)
    │
    ├─→ [验证] → ValidationResult
    │
    ├─→ [提取] → paper_text (150K chars)
    │           sections (8-12个章节)
    │           metadata (title, authors, year)
    │
    ├─→ [哈希] → pdf_hash ("abc123...")
    │              │
    │              └─→ [缓存检查] → 缓存命中?
    │                                │
    │                                ├─ YES → 从缓存加载
    │                                │
    │                                └─ NO ↓
    │
    ├─→ [AI分析] → PaperAnalysis
    │    problem: "..."
    │    method: "..."
    │    innovations: [...]
    │    results: [...]
    │    pros: [...]
    │    cons: [...]
    │
    ├─→ [内容生成] → PresentationContent
    │    适合幻灯片的结构化内容
    │
    ├─→ [缓存保存] → runtime/cache/{hash}.json
    │
    ├─→ [组织] → OrganizedPresentation
    │    18个 SlideContent 对象
    │
    ├─→ [生成] → Markdown字符串
    │    包含Marp配置
    │
    └─→ [输出] → outputs/
         ├── markdown/example.md (20-40 KB)
         └── slides/example.html (50-100 KB)
```

## 📝 核心数据结构

### PaperAnalysis
```python
{
  "title": str,           # 论文标题
  "authors": List[str],   # 作者列表
  "problem": str,         # 研究问题 (2-3句)
  "motivation": str,      # 动机 (2-3句)
  "method": str,          # 方法描述 (4-6句)
  "innovations": List,    # 创新点 (3-5个)
  "experiments": str,     # 实验设置 (2-3句)
  "results": List,        # 主要结果 (3-5个)
  "pros": List,           # 优点 (3-5个)
  "cons": List,           # 缺点 (3-5个)
  "conclusions": str,     # 结论 (2-3句)
  "future_work": str      # 未来工作 (2-3句)
}
```

### PresentationContent
```python
{
  "title": str,                    # 演示标题
  "authors": str,                  # 作者（格式化）
  "venue": str,                    # 会议/期刊
  "year": str,                     # 年份
  "motivation": List[str],         # 动机要点
  "existing_problems": List[str],  # 现有问题
  "research_problem": str,         # 研究问题
  "method_overview": str,          # 方法概述
  "technical_details": List[str],  # 技术细节
  "innovations": List[str],        # 创新点
  "experimental_setup": str,       # 实验设置
  "main_results": List[str],       # 主要结果
  "result_analysis": str,          # 结果分析
  "discussion": str,               # 讨论
  "pros": List[str],               # 优点（带✓）
  "cons": List[str],               # 缺点（带✗）
  "future_work": List[str],        # 未来工作
  "conclusions": str               # 结论
}
```

### SlideContent
```python
{
  "title": str,            # 幻灯片标题
  "bullet_points": List,   # 要点列表
  "notes": str             # 演讲者备注
}
```

### 缓存文件结构
```json
{
  "hash": "abc123...",           // PDF文件MD5
  "timestamp": "2026-03-05...",  // 时间戳
  "analysis": {...},             // PaperAnalysis
  "presentation_content": {...}, // PresentationContent
  "metadata": {                  // 元数据
    "model": "claude-sonnet-4-6",
    "tokens_used": 87500,
    "cost": 0.0925
  }
}
```

## 🎯 关键转换点

### 转换1: PDF → 文本
- **输入**: PDF二进制文件
- **处理**: PyMuPDF逐页提取
- **输出**: 纯文本字符串
- **复杂度**: O(页数 × 每页复杂度)

### 转换2: 文本 → AI分析
- **输入**: paper_text (可能150K+ 字符)
- **处理**: Claude API分析
- **输出**: 结构化PaperAnalysis
- **成本**: ~$0.05-0.10

### 转换3: 分析 → 演示内容
- **输入**: PaperAnalysis
- **处理**: 内容重组和格式化
- **输出**: PresentationContent
- **复杂度**: O(1) 本地处理

### 转换4: 演示内容 → 幻灯片
- **输入**: PresentationContent
- **处理**: 按标准结构组织
- **输出**: 15-20个SlideContent
- **复杂度**: O(1) 本地处理

### 转换5: 幻灯片 → Markdown
- **输入**: OrganizedPresentation
- **处理**: 应用模板生成
- **输出**: Markdown字符串
- **复杂度**: O(幻灯片数)

### 转换6: Markdown → HTML/PDF
- **输入**: Markdown字符串
- **处理**: Marp CLI转换
- **输出**: HTML或PDF文件
- **复杂度**: 依赖外部工具

## 💾 存储策略

### 内存存储（临时）
- ValidationResult
- paper_text, sections, metadata
- PaperAnalysis, PresentationContent
- OrganizedPresentation
- Markdown字符串

### 磁盘存储（持久）
- **papers/**: 原始PDF文件
- **runtime/cache/**: AI分析结果（7天TTL）
- **outputs/markdown/**: Markdown文件
- **outputs/slides/**: 最终演示文件

### 缓存策略
- **键**: PDF文件MD5哈希
- **值**: analysis + presentation_content
- **TTL**: 7天（可配置）
- **命中**: 节省$0.05-0.10 + 10-30秒

## 📈 性能指标

| 指标 | 典型值 | 说明 |
|------|--------|------|
| PDF解析时间 | 1-5秒 | 取决于页数 |
| AI分析时间 | 10-30秒 | 取决于论文长度 |
| 内容生成 | <1秒 | 本地处理 |
| Markdown生成 | <1秒 | 本地处理 |
| 格式转换 | 2-5秒 | Marp CLI |
| **总处理时间** | 15-45秒 | 首次处理 |
| **缓存命中** | 2-5秒 | 仅文件操作 |

## 🔍 调试技巧

### 查看中间产物
```bash
# 追踪数据流程（使用示例数据）
python tools/debug_data_flow.py papers/example.pdf --skip-ai

# 查看缓存内容
cat runtime/cache/{hash}.json | jq .

# 查看生成的Markdown
cat outputs/markdown/example.md
```

### 验证数据完整性
```python
# 检查缓存文件
from src.core.cache_manager import CacheManager
cache = CacheManager()
stats = cache.get_cache_stats()
print(stats)

# 检查AI分析结果
from src.analysis.ai_analyzer import AIAnalyzer
stats = analyzer.get_stats()
print(f"Cost: ${stats['total_cost']:.4f}")
```

## 🎨 数据流向可视化

```
┌─────────────────────────────────────────────────────────┐
│                    PaperReader Pipeline                  │
└─────────────────────────────────────────────────────────┘

   输入层          解析层         分析层        输出层
  ┌─────┐        ┌─────┐       ┌─────┐      ┌─────┐
  │ PDF │───────→│验证 │──────→│ AI  │─────→│  .md│
  └─────┘        └─────┘       └─────┘      └─────┘
                    │             │            │
                    ↓             ↓            ↓
                 ┌─────┐      ┌─────┐      ┌─────┐
                 │文本  │      │分析  │      │.html│
                 └─────┘      └─────┘      └─────┘
                    │             │            │
                    ↓             ↓            ↓
                 ┌─────┐      ┌─────┐      ┌─────┐
                 │元数据│      │缓存  │      │.pdf │
                 └─────┘      └─────┘      └─────┘

  大小: 1-5MB    大小: 50-200KB 大小: 15KB   大小: 50KB-2MB
  时间: 0s       时间: 1-5s     时间: 10-30s 时间: 2-5s
```

## 📚 相关文档

- **详细流程**: DATA_FLOW.md
- **示例数据**: examples/middle_products_example.py
- **调试工具**: debug_data_flow.py
- **使用指南**: README.md
- **开发文档**: CLAUDE.md

## 🚀 快速开始

```bash
# 1. 追踪数据流程（使用示例）
python tools/debug_data_flow.py papers/example.pdf --skip-ai

# 2. 真实处理
python cli/main.py process --paper papers/example.pdf --verbose

# 3. 查看输出
ls outputs/
cat outputs/markdown/example.md
open outputs/slides/example.html
```
