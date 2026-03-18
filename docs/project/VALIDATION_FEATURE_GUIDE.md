# 图形验证功能使用指南

**Date**: 2026-03-17
**Feature**: Figure/Table Extraction Validation

---

## 🎯 功能概述

验证PDF中的所有Figure和Table是否都被正确提取，生成详细的验证报告。

---

## 📋 使用方法

### 方法1: 命令行工具

```bash
# 验证单个PDF
python examples/figure_validation_demo.py papers/Human-In-the-Loop.pdf

# 查看报告
cat outputs/validation_Human-In-the-Loop.md
```

### 方法2: Python API

```python
from src.parser.pdf_image_extractor import PDFImageExtractor
from src.parser.figure_validator import FigureValidator

# 1. 提取图形
extractor = PDFImageExtractor(output_dir='outputs/images')
figures = extractor.extract_key_figures('papers/Human-In-the-Loop.pdf')

# 2. 验证
validator = FigureValidator('papers/Human-In-the-Loop.pdf')
validator.scan_captions()
report = validator.validate_extraction(figures)

# 3. 查看结果
print(f"Expected: {report['total_figures']}")
print(f"Extracted: {len(report['extracted'])}")
print(f"Missing: {len(report['missing'])}")

# 4. 保存报告
with open('outputs/validation_report.md', 'w') as f:
    f.write(validator.generate_report_markdown(report))

validator.close()
```

### 方法3: 便捷函数

```python
from src.parser.figure_validator import validate_pdf_figures

# 一行验证
report = validate_pdf_figures('papers/Human-In-the-Loop.pdf', extracted_figures)
```

---

## 📊 验证报告示例

```markdown
# Figure/Table Extraction Validation Report

**PDF**: `Human-In-the-Loop.pdf`
**Total Expected**: 9 figures/tables
**Success Rate**: 66.7%

## ✅ Extracted Successfully (6)
- 📈 **FIGURE 1** (Page 3): Fig. 1. An Overview of our Human-in-the-Loop...
- 📈 **FIGURE 2** (Page 3): Fig. 2. The user interface of our human-in-the-loop...
- ...

## ❌ Missing (3)
- 📈 **FIGURE 7** (Page 8): Figure 7 shows the analysis results...
- 📈 **FIGURE 8** (Page 8): Figure 8 presents the analysis results...
- 📈 **FIGURE 9** (Page 8): Figure 9 presents the analysis...

## 💡 Recommendations
1. Check if missing figures have non-standard captions
2. Verify if figures are on separate pages
3. Consider increasing `max_figures` parameter
```

---

## 🔍 当前验证结果

### Human-In-the-Loop.pdf

| 指标 | 值 |
|------|-----|
| 预期图形 | 9个 |
| 成功提取 | 6个 |
| 缺失 | 3个 (Figure 7, 8, 9) |
| 成功率 | 66.7% |

**缺失原因分析**:
- Figure 7, 8, 9在Page 8
- 可能是文中引用，而非实际的独立图形
- 或者标题格式不标准（如"Figure 7 shows..."而非"Fig. 7: ..."）

---

## 💡 优化建议

### 1. 增加max_figures参数

```python
# 如果有缺失，尝试增加提取数量
figures = extractor.extract_key_figures(pdf_path, max_figures=20)
```

### 2. 检查标题格式

```python
# 查看PDF中的实际标题格式
validator = FigureValidator(pdf_path)
expected = validator.scan_captions()

for fig in expected:
    print(f"{fig.type} {fig.number}: {fig.caption}")
```

### 3. 集成到PPT生成流程

```python
def generate_ppt_with_validation(pdf_path):
    # 1. 提取图形
    extractor = PDFImageExtractor()
    figures = extractor.extract_key_figures(pdf_path)

    # 2. 验证
    validator = FigureValidator(pdf_path)
    validator.scan_captions()
    report = validator.validate_extraction(figures)

    # 3. 如果有缺失，警告用户
    if report['missing']:
        print(f"⚠️  Warning: {len(report['missing'])} figures are missing!")
        for fig in report['missing']:
            print(f"  - {fig.type} {fig.number} (Page {fig.page})")

        # 可以选择继续或中止
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)

    # 4. 生成PPT
    ppt = generate_ppt(figures)
    return ppt
```

---

## 📚 API文档

### FigureValidator类

```python
class FigureValidator:
    def __init__(self, pdf_path: str):
        """初始化验证器"""

    def scan_captions(self) -> List[FigureInfo]:
        """扫描PDF中的所有Figure/Table标题"""

    def validate_extraction(self, extracted_figures: List[Dict]) -> Dict:
        """验证提取结果"""

    def generate_report_markdown(self, report: Dict) -> str:
        """生成Markdown格式报告"""

    def close(self):
        """关闭PDF文档"""
```

### FigureInfo类

```python
@dataclass
class FigureInfo:
    type: str          # 'figure' 或 'table'
    number: int        # 图形编号
    page: int          # 页码
    caption: str       # 标题文字
    extracted: bool    # 是否已提取
    image_path: str    # 图像路径
```

---

## ✅ 功能特点

1. **自动扫描** - 自动检测PDF中的所有Figure/Table标题
2. **智能匹配** - 支持多种标题格式（Figure X, Fig. X, FIGURE X）
3. **详细报告** - 生成Markdown格式验证报告
4. **缺失检测** - 准确识别未提取的图形
5. **易于集成** - 简单的API接口

---

## 🎯 最佳实践

1. **在提取后立即验证** - 及时发现缺失
2. **检查验证报告** - 了解提取质量
3. **调整参数** - 根据验证结果优化
4. **集成到CI/CD** - 自动化质量检查

---

## 📁 文件位置

- **模块**: `src/parser/figure_validator.py`
- **示例**: `examples/figure_validation_demo.py`
- **报告**: `outputs/validation_*.md`

---

**Status**: ✅ 功能已实现并测试
**Usage**: `python examples/figure_validation_demo.py <pdf_path>`
