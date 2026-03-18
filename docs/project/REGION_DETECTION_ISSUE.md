# 区域检测精度问题分析报告

**Date**: 2026-03-17
**Issue**: 提取的图形包含了不该包含的左右两侧文字
**Root Cause**: Graphic regions合并时包含了超出页面边界的元素

---

## 🔍 问题诊断

### 现象

```
提取的Figure 1:
  宽度: 1634px (PDF中817 points)
  页面宽度: 612 points
  问题: 提取区域占96.1%页面宽度，包含了左右两侧的文字列
```

### 根本原因

**Page 4 的graphic regions分析**:

```
找到 39 个graphic regions
所有graphics的边界:
  X: -74.7 - 831.2 (宽度: 905.9)  ← 超出页面宽度！
  Y: 165.9 - 891.1

计算的bbox:
  X: 12.0 - 600.0 (宽度: 588.0)
  页面宽度百分比: 96.1%  ← 太宽了！
```

**问题链条**:

1. `_collect_graphic_regions()` 收集所有绘图路径
   - 包括79个绘图路径
   - 其中有些路径的坐标**超出页面边界**（X: -74.7 到 831.2）
   - 页面宽度只有612.0

2. `_merge_regions()` 合并所有regions
   - 简单地取所有regions的最小/最大边界
   - 结果：X范围 = -74.7 到 831.2

3. `_determine_figure_region()` 裁剪到页面范围
   ```python
   bbox = (
       max(12, bbox[0] - 12),  # 裁剪左边界
       ...
       min(page_width - 12, bbox[2] + 12),  # 裁剪右边界
   )
   ```
   - 结果：12.0 - 600.0 (96.1%页面宽度)

4. 最终提取区域包含了左右两侧的文字

---

## 📊 PDF布局分析

### Page 4 文本分布

```
页面宽度: 612 points
页面中心: 306 points

左侧文本 (37个):  x < 214
  - {Jira issue}, {Code repository}, Human Agent, etc.

中间文本 (27个):  214 < x < 398
  - Generate a Plan, Review a Plan, {Relevant files}, etc.

右侧文本 (32个):  x > 398
  - Generate a Code Refine a Code, {Code change}, {Pull Request}, etc.
```

### 实际Figure 1的范围

根据文本布局，Figure 1应该在：
- **X范围**: 约 50 - 560 (中间区域)
- **当前提取**: 12 - 600 (太宽)

---

## 💡 修复方案

### 方案1: 过滤超出边界的Graphic Regions ⭐⭐⭐⭐⭐ (推荐)

**原理**: 在收集graphic regions时，过滤掉超出页面合理范围的元素

```python
def _collect_graphic_regions(
    self,
    page,
    page_height: float,
) -> List[Tuple[float, float, float, float]]:
    """Collect image and vector graphic bounds on a page in PDF coordinates."""
    regions = []
    seen = set()

    for image in page.get_images(full=True):
        xref = image[0]
        for rect in page.get_image_rects(xref):
            region = self._fitz_rect_to_pdf_bbox(rect, page_height)
            key = tuple(round(value, 1) for value in region)
            if key not in seen:
                regions.append(region)
                seen.add(key)

    for drawing in page.get_drawings():
        rect = drawing.get("rect")
        if not rect:
            continue

        region = self._fitz_rect_to_pdf_bbox(rect, page_height)

        # ✅ 新增：过滤超出页面边界的regions
        page_width = page.rect.width
        margin = page_width * 0.15  # 允许15%的边距

        if region[0] < -margin or region[2] > page_width + margin:
            # 超出页面范围太多，可能是装饰元素
            continue

        key = tuple(round(value, 1) for value in region)
        if key not in seen:
            regions.append(region)
            seen.add(key)

    return regions
```

**优点**:
- ✅ 直接过滤异常元素
- ✅ 防止超出边界的regions影响合并结果
- ✅ 逻辑清晰，易于理解

**预期效果**:
- 过滤掉 X < -74.7 和 X > 831.2 的异常regions
- 合并后的bbox更接近实际图形范围
- 提取宽度从96%降低到70-80%

---

### 方案2: 改进合并算法 - 使用聚类 ⭐⭐⭐⭐

**原理**: 不是简单合并所有regions，而是聚类找出主要的图形区域

```python
def _merge_regions(self, regions: List[Tuple]) -> Tuple:
    """Merge multiple regions, excluding outliers."""
    if not regions:
        return (0, 0, 0, 0)

    # 计算X坐标的分布
    x_centers = [(r[0] + r[2]) / 2 for r in regions]
    x_widths = [r[2] - r[0] for r in regions]

    # 找出X坐标的中心聚类
    from statistics import median
    median_x = median(x_centers)

    # 过滤掉离中心太远的regions（异常值）
    threshold = page_width * 0.4  # 允许40%的偏离
    filtered_regions = [
        r for r in regions
        if abs((r[0] + r[2]) / 2 - median_x) < threshold
    ]

    # 合并过滤后的regions
    x0 = min(r[0] for r in filtered_regions)
    y0 = min(r[1] for r in filtered_regions)
    x1 = max(r[2] for r in filtered_regions)
    y1 = max(r[3] for r in filtered_regions)

    return (x0, y0, x1, y1)
```

**优点**:
- ✅ 更智能的region选择
- ✅ 自动排除异常值

**缺点**:
- ❌ 增加复杂度
- ❌ 可能误删有效regions

---

### 方案3: 添加宽度约束 ⭐⭐⭐

**原理**: 在`_determine_figure_region`中检查合并后的宽度

```python
def _determine_figure_region(self, ...):
    # ... existing code ...

    if candidate_regions:
        bbox = self._merge_regions(candidate_regions)

        # ✅ 新增：检查宽度是否合理
        width = bbox[2] - bbox[0]
        max_reasonable_width = page_width * 0.85  # 不应超过85%

        if width > max_reasonable_width:
            # 宽度过大，可能是包含了异常regions
            # 使用fallback
            logger.warning(f"Figure region too wide ({width/page_width*100:.1f}%), using fallback")
            bbox = self._calculate_fallback_bbox(...)

        bbox = (
            max(12, bbox[0] - 12),
            ...
        )
        return self._clamp_bbox(bbox, page_width, page_height)
```

**优点**:
- ✅ 简单直接
- ✅ 有fallback机制

**缺点**:
- ❌ Fallback bbox仍然可能过宽

---

### 方案4: 使用文本列检测 ⭐⭐⭐

**原理**: 分析文本布局，避免包含文字列

```python
def _detect_text_columns(self, page) -> List[Tuple[float, float]]:
    """Detect text column boundaries to avoid including them in figures."""
    blocks = page.get_text('dict')['blocks']

    # 统计X坐标分布
    x_positions = []
    for block in blocks:
        if 'lines' in block:
            for line in block['lines']:
                bbox = line['bbox']
                x_positions.append(bbox[0])

    # 找出主要的文本列边界
    # ... 聚类算法 ...

    return column_boundaries
```

**优点**:
- ✅ 智能避开文字列
- ✅ 适合多栏布局

**缺点**:
- ❌ 复杂度高
- ❌ 可能误判

---

## 🎯 推荐方案

**推荐：方案1（过滤超出边界的regions）**

### 修改位置

**文件**: `src/parser/pdf_image_extractor.py`
**方法**: `_collect_graphic_regions`
**行数**: ~Line 370

### 修改代码

```python
# 在 Line 370-377 之间添加过滤逻辑

for drawing in page.get_drawings():
    rect = drawing.get("rect")
    if not rect:
        continue

    region = self._fitz_rect_to_pdf_bbox(rect, page_height)

    # ✅ 新增：过滤超出页面边界的regions
    page_width = page.rect.width
    margin = page_width * 0.15  # 允许15%边距

    if region[0] < -margin or region[2] > page_width + margin:
        # 超出页面范围，跳过
        logger.debug(f"Skipping out-of-bounds region: {region}")
        continue

    key = tuple(round(value, 1) for value in region)
    if key not in seen:
        regions.append(region)
        seen.add(key)
```

---

## 📊 预期效果

### 修改前

```
Graphic regions: X: -74.7 - 831.2
合并后bbox: X: 12.0 - 600.0 (96.1%)
提取宽度: 1634px
问题: 包含左右两侧文字
```

### 修改后（预期）

```
Graphic regions: X: 50 - 560 (过滤后)
合并后bbox: X: 38 - 572 (87.3%)
提取宽度: ~1200px
效果: 仅包含流程图，不含文字列
```

---

## ✅ 测试验证

修改后，需要验证：

```bash
# 重新提取Figure 1
python3 -c "
from src.parser.pdf_image_extractor import PDFImageExtractor
e = PDFImageExtractor('outputs/test_fix3')
f = e.extract_key_figures('papers/Human-In-the-Loop.pdf', max_figures=1)
"

# 检查提取宽度
python3 -c "
from PIL import Image
img = Image.open('outputs/test_fix3/Human-In-the-Loop_figure_1.png')
print(f'宽度: {img.width}px (PDF: {img.width/2:.1f} points)')
print(f'页面宽度: 612 points')
print(f'占比: {img.width/2/612*100:.1f}%')

if img.width/2/612 < 0.85:
    print('✅ 宽度合理')
else:
    print('❌ 仍然过宽')
"
```

---

## 📝 总结

### 问题本质

- Graphic regions包含超出页面边界的元素
- 简单的合并算法导致bbox过宽
- 最终提取区域包含了不该包含的文字列

### 修复方案

- **方案1**（推荐）: 过滤超出边界的regions
- **方案2**: 改进合并算法（聚类）
- **方案3**: 添加宽度约束
- **方案4**: 文本列检测

### 下一步

1. [ ] 实施方案1（过滤异常regions）
2. [ ] 测试验证效果
3. [ ] 如果仍有问题，考虑组合方案1+方案3

---

**Priority**: High
**Complexity**: Medium
**Impact**: Improves figure extraction quality significantly
