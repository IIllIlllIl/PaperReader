# 示例和中间产物

这个目录包含了PaperReader处理论文时产生的中间产物示例。

## 文件说明

### middle_products_example.py

包含所有主要中间产物的完整示例数据：

- **PDF验证结果** - PDF质量评估
- **提取的文本** - 从PDF提取的原始文本
- **论文元数据** - 标题、作者、年份等
- **AI分析结果** - Claude AI的结构化分析
- **演示内容** - 适合幻灯片的内容
- **组织的幻灯片** - 16个完整的幻灯片示例
- **Markdown输出** - 最终生成的Markdown
- **缓存文件内容** - 保存到cache的JSON结构

### 使用方法

```bash
# 查看所有示例
python examples/middle_products_example.py

# 在Python中导入
from examples.middle_products_example import paper_analysis_example
print(paper_analysis_example['problem'])
```

### 示例论文

示例数据基于论文 **"Attention Is All You Need"** (Vaswani et al., 2017)。

这是一个经典的深度学习论文，非常适合展示PaperReader的功能。

## 调试工具

### debug_data_flow.py

追踪真实论文处理的数据流程：

```bash
# 使用示例数据（不需要API密钥）
python tools/debug_data_flow.py papers/your_paper.pdf --skip-ai

# 真实处理（需要API密钥）
python tools/debug_data_flow.py papers/your_paper.pdf
```

输出包括：
1. PDF验证结果
2. 提取的文本统计
3. 识别的章节
4. 提取的元数据
5. PDF文件哈希
6. AI分析结果
7. 演示内容
8. 组织的幻灯片
9. 生成的Markdown
10. 缓存信息

## 中间产物概览

| 产物 | 大小 | 描述 |
|------|------|------|
| PDF文件 | 1-5 MB | 原始输入 |
| 提取文本 | 50-200 KB | 纯文本内容 |
| AI分析 | 5-10 KB | 结构化分析结果 |
| 演示内容 | 10-20 KB | 幻灯片友好格式 |
| 缓存文件 | 15-30 KB | JSON格式 |
| Markdown | 20-40 KB | Marp格式 |
| HTML/PDF | 50KB-2MB | 最终输出 |

## 学习路径

1. **查看示例数据**
   ```bash
   python examples/middle_products_example.py
   ```

2. **追踪真实论文**（使用示例数据）
   ```bash
   python tools/debug_data_flow.py papers/your_paper.pdf --skip-ai
   ```

3. **查看详细文档**
   - 阅读 DATA_FLOW.md
   - 阅读 DATA_FLOW_QUICK_REFERENCE.md

4. **真实处理**
   ```bash
   python cli/main.py process --paper papers/your_paper.pdf --verbose
   ```

5. **检查输出**
   ```bash
   cat output/markdown/your_paper.md
   open output/slides/your_paper.html
   ```

## 相关文档

- [DATA_FLOW.md](../DATA_FLOW.md) - 详细的数据流程
- [DATA_FLOW_QUICK_REFERENCE.md](../DATA_FLOW_QUICK_REFERENCE.md) - 快速参考
- [README.md](../README.md) - 使用指南
