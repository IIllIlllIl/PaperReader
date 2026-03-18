# 文件名冲突分析报告

**Date**: 2026-03-17
**Issue**: Caption-based和Embedded提取使用相同文件名导致覆盖

---

## 🔍 冲突位置分析

### 1. **Caption-based提取** (Line 130)

```python
# src/parser/pdf_image_extractor.py:130
image_name = f"{paper_name}_figure_{caption['figure_num']}.png"
# 结果: "Human-In-the-Loop_figure_1.png"
```

**特点**:
- 使用caption中的figure_num（从PDF文本中提取的编号）
- 例如：找到"Figure 1" → figure_num=1
- 输出高质量完整流程图 (1634x614)

### 2. **Embedded Image提取** (Line 203)

```python
# src/parser/pdf_image_extractor.py:202-203
figure_num = len(figures) + 1
image_filename = f"{paper_name}_figure_{figure_num}.{image_ext}"
# 结果: "Human-In-the-Loop_figure_1.png" (如果figures为空)
```

**特点**:
- 使用计数器生成编号（从1开始）
- 例如：第1个嵌入图片 → figure_num=1
- 输出嵌入的图标/小图 (512x512)

### 3. **冲突流程**

```
时间线：
1. Caption-based提取运行
   - 找到"Figure 1"
   - 保存: Human-In-the-Loop_figure_1.png (1634x614) ✅

2. Embedded extraction运行（fallback）
   - figures = [] (重新开始)
   - 第1个嵌入图片
   - 保存: Human-In-the-Loop_figure_1.png (512x512) ❌ 覆盖！

3. 最终结果
   - Human-In-the-Loop_figure_1.png → 512x512 (图标)
   - 原来的1634x614流程图被覆盖
```

---

## 💡 修复方案对比

### **方案A: 使用不同前缀** ⭐⭐⭐⭐⭐ (推荐)

```python
# Caption-based
image_name = f"{paper_name}_figure_{caption['figure_num']}.png"
# → Human-In-the-Loop_figure_1.png

# Embedded
image_filename = f"{paper_name}_embedded_{figure_num}.{image_ext}"
# → Human-In-the-Loop_embedded_1.png
```

**优点**:
- ✅ 最小改动（1行代码）
- ✅ 清晰区分来源
- ✅ 避免冲突
- ✅ 向后兼容（caption-based保持原名）

**缺点**:
- 需要文档说明两种文件的区别

**修改位置**: Line 203

---

### **方案B: 使用子目录** ⭐⭐⭐

```python
# Caption-based
output_path = Path(output_dir) / "caption" / image_name
# → outputs/images/caption/Human-In-the-Loop_figure_1.png

# Embedded
output_path = Path(output_dir) / "embedded" / image_filename
# → outputs/images/embedded/Human-In-the-Loop_figure_1.png
```

**优点**:
- ✅ 自动分类
- ✅ 避免冲突

**缺点**:
- ❌ 需要创建子目录
- ❌ 影响现有代码路径
- ❌ 破坏向后兼容

**修改位置**: Line 204, Line 434

---

### **方案C: 添加后缀** ⭐⭐⭐⭐

```python
# Caption-based
image_name = f"{paper_name}_figure_{caption['figure_num']}.png"
# → Human-In-the-Loop_figure_1.png

# Embedded
image_filename = f"{paper_name}_figure_{figure_num}_embedded.{image_ext}"
# → Human-In-the-Loop_figure_1_embedded.png
```

**优点**:
- ✅ 避免冲突
- ✅ 清晰标识来源

**缺点**:
- ❌ 文件名较长

**修改位置**: Line 203

---

## 🎯 推荐方案：方案A

### 修改内容

**文件**: `src/parser/pdf_image_extractor.py`

**Line 203** (修改前):
```python
image_filename = f"{paper_name}_figure_{figure_num}.{image_ext}"
```

**Line 203** (修改后):
```python
image_filename = f"{paper_name}_embedded_{figure_num}.{image_ext}"
```

### 修改命令

```bash
# 使用sed进行修改
sed -i '' '203s/figure_/embedded_/' src/parser/pdf_image_extractor.py

# 验证修改
sed -n '200,210p' src/parser/pdf_image_extractor.py | grep -A2 -B2 "image_filename"
```

### 预期结果

修改后，提取会生成两类文件：

```
outputs/images/
  ├── Human-In-the-Loop_figure_1.png      (1634x614, 完整流程图)
  ├── Human-In-the-Loop_figure_2.png      (完整图表)
  ├── Human-In-the-Loop_figure_3.png      (完整图表)
  ├── Human-In-the-Loop_embedded_1.png    (512x512, 图标)
  ├── Human-In-the-Loop_embedded_2.png    (图标)
  └── ...
```

---

## 📊 验证测试

### 测试脚本

```python
from src.parser.pdf_image_extractor import PDFImageExtractor
import os

# 测试修复后的提取器
extractor = PDFImageExtractor(output_dir='outputs/test_fix')
figures = extractor.extract_key_figures('papers/Human-In-the-Loop.pdf', max_figures=5)

print("提取结果:")
for fig in figures:
    print(f"  {fig['image_path']}")
    print(f"    尺寸: {fig['width']}x{fig['height']}")
    print(f"    类型: {fig['caption'][:50]}...")
    print()

# 检查文件
import glob
caption_files = glob.glob('outputs/test_fix/*_figure_*.png')
embedded_files = glob.glob('outputs/test_fix/*_embedded_*.png')

print(f"\n文件分类:")
print(f"  Caption-based: {len(caption_files)} 个")
print(f"  Embedded: {len(embedded_files)} 个")

# 检查figure_1的尺寸
figure_1_path = 'outputs/test_fix/Human-In-the-Loop_figure_1.png'
if os.path.exists(figure_1_path):
    from PIL import Image
    img = Image.open(figure_1_path)
    print(f"\n✅ figure_1.png 尺寸: {img.size[0]}x{img.size[1]}")
    if img.size[0] > 1000:
        print("✅ 修复成功！这是完整的流程图")
    else:
        print("❌ 仍然有问题，尺寸太小")
```

---

## 📝 后续工作

### 1. 更新文档

```bash
# 创建说明文档
cat > docs/features/FIGURE_NAMING.md << 'EOF'
# 图形文件命名规则

## 文件类型

### figure_X.png
- 来源：Caption-based提取
- 特点：基于Figure标题定位的完整图形
- 用途：流程图、架构图、大型图表
- 质量：高分辨率，包含所有元素

### embedded_X.png
- 来源：Embedded image提取
- 特点：直接从PDF提取的嵌入图片
- 用途：图标、小图、独立图表
- 质量：原始分辨率

## 使用建议

在PPT生成时，优先使用 `figure_X.png`，因为它们通常是论文中的主要图表。
EOF
```

### 2. 更新代码注释

在 `_extract_embedded_figures` 方法中添加注释：

```python
def _extract_embedded_figures(self, pdf_path: str, max_figures: int) -> List[dict]:
    """Fallback strategy: extract embedded images that look like figures.

    Note: Uses 'embedded_' prefix to avoid conflicts with caption-based figures.
    """
```

---

## ✅ 检查清单

修复完成后，验证：

- [ ] Line 203已修改为使用 `embedded_` 前缀
- [ ] 运行测试脚本，figure_1.png尺寸 > 1000px
- [ ] 检查outputs/test_fix/目录，两类文件都存在
- [ ] 文档已更新
- [ ] 代码注释已添加

---

## 🔗 相关文件

- 主文件: `src/parser/pdf_image_extractor.py`
- 备份: `src/parser/pdf_image_extractor.py.bak`
- 测试输出: `outputs/test_fix/`
- 文档: `docs/features/FIGURE_NAMING.md`
