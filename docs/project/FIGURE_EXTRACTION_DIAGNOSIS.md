# Figure Extraction 诊断报告

**Date**: 2026-03-17
**Issue**: 提取的 `figure_1.png` 是512x512图标，而非完整的流程图

---

## 🔍 问题诊断

### 现状分析

#### 1. **当前提取的文件**

```bash
outputs/images/Human-In-the-Loop_figure_1.png
  Size: 512x512 (15KB)
  Type: 嵌入图片（图标：人使用电脑）
  Status: ❌ 不是完整的Figure 1流程图
```

#### 2. **PDF结构（Page 4）**

```
Page 4: 612 x 792 points
  - 嵌入图片: 18个（图标：human, computer, etc.）
  - 绘图路径: 79个（vector图形：boxes, arrows）
  - Figure 1标题: "Fig. 1. An Overview of our Human-in-the-Loop..."
  - 类型: 混合图形（vector + raster）
```

#### 3. **当前提取器策略**

`src/parser/pdf_image_extractor.py` 使用**两阶段策略**：

1. **Caption-based extraction** (主要策略)
   - 查找Figure标题（"Fig. 1", "Figure 1"）
   - 确定图形区域（标题上方的区域）
   - 使用pdf2image渲染整个区域
   - ✅ **成功提取**: 1634x614 (完整流程图)

2. **Embedded image extraction** (fallback策略)
   - 提取PDF中的嵌入图片
   - 过滤小图片和重复图片
   - ❌ **覆盖文件**: 512x512 (图标)

### 根本原因

**文件名冲突导致覆盖！**

```python
# Caption-based extraction
image_name = f"{paper_name}_figure_{caption['figure_num']}.png"
# -> "Human-In-the-Loop_figure_1.png"

# Embedded image extraction (fallback)
image_name = f"{paper_name}_figure_{idx + 1}.png"
# -> "Human-In-the-Loop_figure_1.png" (覆盖!)
```

**时间线：**
1. Caption-based提取 → `figure_1.png` (1634x614) ✅
2. Embedded image提取 → `figure_1.png` (512x512) ❌ 覆盖
3. 最终文件 → 512x512图标

---

## 📊 测试数据对比

### PyMuPDF测试结果

| 方法 | 输出文件 | 尺寸 | 文件大小 | 质量 |
|------|---------|------|----------|------|
| Full page render | `page4_full.png` | 1224x1584 | 372KB | ⭐⭐⭐⭐⭐ |
| Caption-based (实际) | `figure_1.png` | 1634x614 | ? | ⭐⭐⭐⭐⭐ |
| Graphics paths | `page4_all_graphics.png` | 1224x1313 | 327KB | ⭐ (无文字) |
| Embedded image | `figure_1.png` (当前) | 512x512 | 15KB | ⭐⭐⭐ (仅图标) |

### PDF页面分析

```
Page 4 (Figure 1所在页):
  ✅ Caption found: "Fig. 1. An Overview of..."
  ✅ Caption-based extraction: 成功 (1634x614)
  ✅ Embedded images: 18个 (512x512 icons)
  ✅ Graphics paths: 79个 (vector图形)

  问题: 文件名冲突 → 正确提取的文件被覆盖
```

---

## 💡 解决方案

### 方案1: **修复文件名冲突** (推荐)

```python
# src/parser/pdf_image_extractor.py

def extract_key_figures(self, pdf_path: str, max_figures: int = 5) -> List[dict]:
    # Phase 1: Caption-based extraction
    caption_figures = self.extract_figures_by_caption(...)

    # Phase 2: Embedded image extraction (仅填充剩余配额)
    if len(caption_figures) < max_figures:
        embedded_limit = max_figures - len(caption_figures)
        # 使用不同的文件名前缀
        embedded_figures = self._extract_embedded_figures(
            pdf_path,
            embedded_limit,
            start_index=len(caption_figures) + 1  # 避免冲突
        )
```

**优点**:
- ✅ Caption-based提取优先（完整流程图）
- ✅ 避免文件名冲突
- ✅ 保持向后兼容

### 方案2: **提高Caption-based提取优先级**

```python
def _merge_figure_results(self, caption_figures, embedded_figures):
    # Caption-based figures优先
    # Embedded images仅作为补充
    # 使用set去重（基于figure_num）
```

### 方案3: **改进区域检测算法**

当前的`_determine_figure_region`已经工作良好（1634x614），无需改进。

---

## 🎯 推荐行动

### 立即行动

1. **修复文件名冲突**
   - Caption-based和Embedded使用不同的命名空间
   - 或者在merge时去重

2. **验证提取效果**
   ```bash
   # 重新运行提取器（修复后）
   python3 -c "
   from parser.pdf_image_extractor import PDFImageExtractor
   extractor = PDFImageExtractor('outputs/test_fixed')
   figures = extractor.extract_key_figures('papers/Human-In-the-Loop.pdf', max_figures=11)
   "

   # 检查figure_1.png尺寸
   file outputs/test_fixed/Human-In-the-Loop_figure_1.png
   ```

### 可选优化

3. **添加图片质量评估**
   - 大图片优先（完整流程图 > 图标）
   - 基于尺寸/面积的排序

4. **改进日志**
   - 记录每个提取阶段的文件名和尺寸
   - 帮助调试覆盖问题

---

## 📈 PyMuPDF vs Current Approach

| 维度 | PyMuPDF Full Page | Current (pdf2image + PyMuPDF) |
|------|-------------------|------------------------------|
| **Caption-based提取** | 需要手动实现 | ✅ 已实现并工作良好 |
| **质量** | Excellent | Excellent (1634x614) |
| **速度** | Fast | Fast |
| **文件大小** | 372KB (full page) | ~50-150KB (cropped) |
| **Vector graphics** | ✅ 支持 | ✅ 支持 (via pdf2image) |
| **Text overlay** | ✅ 包含 | ✅ 包含 |

**结论**: **当前方案已经很好，只需要修复文件名冲突bug！**

---

## 🔧 快速修复代码

```python
# src/parser/pdf_image_extractor.py

def _extract_embedded_figures(
    self,
    pdf_path: str,
    max_figures: int,
    start_index: int = 0  # 新增参数
) -> List[dict]:
    """Fallback strategy: extract embedded images that look like figures."""
    pdf_doc = fitz.open(pdf_path)
    figures = []
    paper_name = Path(pdf_path).stem

    try:
        for page_num in range(len(pdf_doc)):
            page = pdf_doc[page_num]
            image_list = page.get_images(full=True)
            page_rect = page.rect

            for img in image_list:
                if len(figures) >= max_figures:
                    break

                # ... (existing validation code)

                # 修改文件名，避免与caption-based冲突
                idx = len(figures) + start_index
                image_name = f"{paper_name}_embedded_{idx + 1}.png"

                # ... (rest of the code)
```

---

## 📝 总结

### 关键发现

1. ✅ **Caption-based提取已经工作** (1634x614)
2. ❌ **文件被Embedded image覆盖** (512x512)
3. ✅ **PyMuPDF测试验证了当前方案的可行性**
4. ❌ **PyMuPDF的graphics path提取无法使用** (缺少文字)

### 行动项

- [ ] 修复文件名冲突（方案1）
- [ ] 重新运行提取器验证
- [ ] 添加图片质量评估逻辑
- [ ] 更新日志以追踪覆盖问题

### 结论

**无需切换到纯PyMuPDF方案！**

当前的pdf2image + PyMuPDF混合方案已经很好，只需要修复文件名冲突bug即可正确提取完整流程图。
