# 💬 PaperReader Prompt 建议和技巧

本文档提供高效的Prompt建议，帮助您更智能地使用PaperReader。

## 🎯 基础Prompt模式

### 模式1: 直接命令（最推荐）

**最简单**：
```
/paper
```

**指定文件**：
```
/paper attention.pdf
```

**指定格式**：
```
/paper attention.pdf --pdf
```

### 模式2: 自然语言 + Skill

Claude可以理解自然语言并调用skill：

```
帮我处理attention.pdf
```

Claude会自动识别并执行：
```bash
/paper attention.pdf
```

**更多示例**：
```
"处理这篇论文"         → /paper
"生成PPT"             → /ppt
"我要Markdown格式"    → /paper --md
"批量处理所有论文"     → /papers
```

### 模式3: 带上下文的请求

```
我刚下载了一篇关于Transformer的论文，帮我生成一个演示PPT
```

Claude会：
1. 检测 `papers/` 目录中的新论文
2. 执行 `/paper --html`
3. 提供输出位置

## 🚀 高效Prompt技巧

### 技巧1: 组合多个操作

**❌ 低效**：
```
/paper 1.pdf
/paper 2.pdf
/paper 3.pdf
```

**✅ 高效**：
```
批量处理这三篇论文
```

或直接：
```
/papers
```

### 技巧2: 智能格式选择

**根据用途选择格式**：

```
我要在会议上展示 → /paper --pdf
我要编辑内容     → /paper --md
我要快速查看     → /paper --html
```

### 技巧3: 利用详细输出调试

```
这篇论文处理失败了，帮我看看是什么问题
```

Claude会执行：
```
/paper xxx.pdf --verbose --no-cache
```

### 技巧4: 查询和统计

```
我处理了多少论文？花了多少钱？
```

Claude会执行：
```
/papers-stats
```

## 📝 实际场景Prompt示例

### 场景1: 日常论文阅读

**Prompt**：
```
处理papers目录中的最新论文，我需要Markdown格式以便编辑
```

**执行**：
```
/md
```

**或更详细**：
```
我刚下载了一篇新论文到papers/目录，帮我分析并生成Markdown摘要
```

### 场景2: 准备组会演示

**Prompt**：
```
帮我把这三篇论文都生成PPT，下周组会要用：
- attention.pdf
- transformer.pdf
- bert.pdf
```

**执行**：
```
/papers --pdf
```

或单独处理：
```
/paper attention.pdf --pdf
/paper transformer.pdf --pdf
/paper bert.pdf --pdf
```

### 场景3: 论文对比分析

**Prompt**：
```
帮我处理这两篇论文，然后对比它们的方法：
- paper1.pdf
- paper2.pdf
```

**执行**：
```
/paper paper1.pdf --md
/paper paper2.pdf --md
```

然后Claude会对比两篇论文的Markdown内容。

### 场景4: 成本控制

**Prompt**：
```
我想处理这篇论文，但想先知道成本
```

**执行**：
```
/paper-stats
```

然后Claude会告诉你：
- 缓存状态
- 预估成本
- 是否已有缓存

### 场景5: 重新分析不满意的结果

**Prompt**：
```
上次生成的PPT不太满意，重新分析一下这篇论文，这次要详细一点
```

**执行**：
```
/paper xxx.pdf --no-cache --verbose
```

## 🎨 Prompt模板库

### 模板1: 快速阅读

```
[论文文件名] 快速阅读模式
```

示例：
```
attention.pdf 快速阅读模式
```

执行：`/paper attention.pdf --html`

### 模板2: 深度分析

```
深度分析 [论文文件名] 并生成详细PPT
```

示例：
```
深度分析 transformer.pdf 并生成详细PPT
```

执行：`/paper transformer.pdf --pdf --verbose`

### 模板3: 批量准备

```
准备 [数量] 篇论文的演示材料，格式为 [格式]
```

示例：
```
准备 5 篇论文的演示材料，格式为PDF
```

执行：`/papers --pdf`

### 模板4: 查询统计

```
统计我的论文处理情况
```

执行：`/papers-stats`

## 🔧 高级Prompt技巧

### 技巧1: 条件处理

**Prompt**：
```
如果attention.pdf还没处理过，就帮我处理一下
```

Claude会：
1. 检查缓存
2. 如果未处理：执行 `/paper attention.pdf`
3. 如果已处理：告知缓存信息

### 技巧2: 智能建议

**Prompt**：
```
papers目录里有5篇论文，哪篇最适合我下次汇报？
```

Claude会：
1. 列出所有论文
2. 根据文件名和修改时间
3. 建议最新的或最相关的

### 技巧3: 自定义输出

**Prompt**：
```
处理这篇论文，但我只关心方法和结果部分
```

Claude会：
1. 执行 `/paper xxx.pdf --md`
2. 在生成后高亮方法和结果部分
3. 提供聚焦建议

### 技巧4: 后处理请求

**Prompt**：
```
生成PPT后，帮我总结这篇论文的三个主要贡献
```

Claude会：
1. 执行 `/paper xxx.pdf`
2. 阅读生成的分析结果
3. 提炼三个主要贡献

## 💡 效率提升技巧

### 技巧1: 使用别名

创建自己的命令别名：

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
alias ppr='/paper'
alias ppp='/ppt'
alias pmd='/md'
```

### 技巧2: 自动补全

在Claude中，输入 `/` 后会自动提示可用的skill命令。

### 技巧3: 历史记录

使用上下箭头键查看之前执行过的命令。

### 技巧4: 批量命名

统一命名论文文件：
```
2024_author_topic.pdf
```

这样更容易识别和管理。

## 📊 Prompt效率对比

| Prompt类型 | 字符数 | 执行时间 | 推荐度 |
|-----------|--------|---------|--------|
| `/paper` | 6 | 最快 | ⭐⭐⭐⭐⭐ |
| 自然语言 | 20-50 | 快 | ⭐⭐⭐⭐ |
| 详细描述 | 100+ | 慢 | ⭐⭐⭐ |

## 🎯 最佳实践总结

### DO ✅

1. **使用skill命令** - 最快最直接
   ```
   /paper attention.pdf
   ```

2. **利用缓存** - 避免重复处理
   ```
   /paper attention.pdf  # 第二次运行会使用缓存
   ```

3. **批量处理** - 一次性处理多篇
   ```
   /papers
   ```

4. **指定格式** - 一步到位
   ```
   /paper --pdf  # 而不是生成HTML后再转换
   ```

### DON'T ❌

1. **不要重复指定参数**
   ```
   ❌ /paper attention.pdf file.pdf
   ✅ /paper attention.pdf
   ```

2. **不要过度描述**
   ```
   ❌ 请帮我使用PaperReader工具处理papers目录中的attention.pdf文件，生成HTML格式的演示文稿...
   ✅ /paper attention.pdf
   ```

3. **不要忽略缓存**
   ```
   ❌ 总是使用 --no-cache
   ✅ 只在必要时使用 --no-cache
   ```

## 🔍 故障排除Prompt

### 问题诊断

**Prompt**：
```
处理这篇论文时出错了，帮我看看是什么问题
```

Claude会执行：
```
/paper xxx.pdf --verbose
```

并分析错误信息。

### 格式转换失败

**Prompt**：
```
PDF生成失败，但Markdown可以，怎么办？
```

Claude会建议：
1. 安装Marp CLI
2. 或使用在线转换工具
3. 或使用HTML格式

### 成本过高

**Prompt**：
```
处理成本太高了，有什么节省办法？
```

Claude会建议：
1. 启用缓存
2. 批量处理
3. 使用Markdown格式
4. 查看统计信息

## 📚 学习路径

### 初级（今天掌握）
1. 基础命令：`/paper`, `/ppt`, `/md`
2. 查看统计：`/papers-stats`
3. 批量处理：`/papers`

### 中级（本周掌握）
1. 自然语言调用
2. 条件处理
3. 故障排除

### 高级（持续优化）
1. 自定义配置
2. 集成工作流
3. 批量自动化

## 🎉 总结

**最高效的使用方式**：
```
/paper [文件名] [选项]
```

**最自然的交互方式**：
```
帮我处理这篇论文
```

**最适合你的方式**：
- 快速处理 → Skill命令
- 复杂需求 → 自然语言描述
- 批量任务 → `/papers` 命令

---

**记住**: `/paper` 是你的好朋友！🚀

**文档版本**: v1.0.0 | **更新**: 2026-03-05
