# Outputs 清理指南

## 📊 问题分析

### 清理前状态
- **总大小**: 15M
- **总文件数**: 249 个
- **问题**: 大量测试/调试目录占用空间

### 清理后状态
- **总大小**: 1.3M (减少 87%)
- **总文件数**: 38 个 (减少 85%)
- **清理目录**: 19 个

---

## 🎯 输出分类

### ✅ 永久输出（应保留）
```
outputs/slides/      # PPT 幻灯片 (.pptx)
outputs/images/      # 提取的图片 (.png, .jpg)
outputs/markdown/    # 生成的 Markdown 文档
outputs/plans/       # 幻灯片规划文件
outputs/charts/      # 生成的图表
```

### ❌ 临时输出（应清理）
```
outputs/test_*/              # 所有测试目录
outputs/debug_*/             # 所有调试目录
outputs/*_old_*/             # 旧备份目录
outputs/*_backup_*/          # 备份目录
outputs/validation_*.md      # 验证报告（可选）
```

---

## 🛠️ 清理工具

### 1. **专用清理脚本** (推荐)

```bash
# 预览模式（不实际删除，只显示将要清理的内容）
DRY_RUN=true ./scripts/clean_outputs.sh

# 执行清理
./scripts/clean_outputs.sh
```

**特点**：
- ✅ 清理所有测试/调试/备份目录
- ✅ 清理空目录
- ✅ 显示详细统计信息
- ✅ 支持 dry-run 预览
- ✅ 保留所有永久输出

### 2. **自动清理脚本** (完整清理)

```bash
./scripts/auto_clean.sh
```

**功能**：
1. 移动根目录文档到 `docs/project/`
2. 清理临时文件 (.DS_Store, *.pyc, *.log, *.tmp, *.bak)
3. 清理 Python 缓存 (__pycache__)
4. **调用 clean_outputs.sh 清理 outputs/**
5. 运行健康检查

### 3. **健康检查脚本**

```bash
./scripts/health_check.sh
```

**检查项**：
- 根目录文档位置
- 临时文件
- Python 缓存
- 文档索引完整性
- **outputs 临时目录**

---

## 📋 使用建议

### 日常使用

#### 开发完成后
```bash
# 运行完整清理
./scripts/auto_clean.sh
```

#### 只清理 outputs
```bash
# 先预览
DRY_RUN=true ./scripts/clean_outputs.sh

# 确认无误后执行
./scripts/clean_outputs.sh
```

#### 提交代码前
```bash
# 检查项目健康状态
./scripts/health_check.sh

# 如有问题，运行自动修复
./scripts/auto_clean.sh
```

### 定期维护

#### 每周一次
```bash
# 检查项目状态
./scripts/health_check.sh

# 如果有临时输出，运行清理
./scripts/clean_outputs.sh
```

---

## 🔧 工具集成

### 与 Pipeline 集成

在 Pipeline 运行完成后自动清理临时输出：

```python
# 在 src/core/pipeline.py 中添加

def run(self, clean_temp_outputs: bool = False):
    """Run the pipeline.

    Args:
        clean_temp_outputs: Whether to clean temporary outputs after completion
    """
    try:
        # ... existing pipeline code ...

        if clean_temp_outputs:
            self._clean_temp_outputs()

    finally:
        pass

def _clean_temp_outputs(self):
    """Clean temporary output directories."""
    import subprocess
    logger.info("Cleaning temporary outputs...")
    subprocess.run(["./scripts/clean_outputs.sh"], check=False)
```

### 与测试脚本集成

在 `tools/manual_tests/` 中的测试脚本使用临时目录：

```python
# 使用固定的测试输出目录
output_dir = "outputs/test_latest"  # 而不是 test_fix1, test_fix2...

# 或者在测试结束后清理
import shutil
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
```

---

## ⚙️ 配置选项

### 环境变量

```bash
# Dry-run 模式（只预览，不删除）
export DRY_RUN=true

# 详细模式
export VERBOSE=true
```

### 自定义清理模式

编辑 `scripts/clean_outputs.sh` 中的 `TEMP_PATTERNS` 数组：

```bash
TEMP_PATTERNS=(
    "outputs/test_*"
    "outputs/debug_*"
    "outputs/*_old_*"
    "outputs/*_backup_*"
    "outputs/validation_*.md"
    # 添加你自己的模式
    # "outputs/temp_*"
)
```

---

## 📊 .gitignore 更新

已将临时输出添加到 `.gitignore`：

```gitignore
# Temporary outputs (test/debug/backup)
outputs/test_*/
outputs/debug_*/
outputs/*_old_*/
outputs/*_backup_*/
outputs/validation_*.md
```

这样可以防止临时文件被提交到 Git。

---

## 🚨 注意事项

### 清理前确认

1. **检查是否有重要的测试结果**
   ```bash
   # 查看将要清理的内容
   find outputs/ -maxdepth 1 -type d -name "test_*" -o -name "debug_*"
   ```

2. **使用 dry-run 预览**
   ```bash
   DRY_RUN=true ./scripts/clean_outputs.sh
   ```

### 不应清理的目录

以下目录**永远不会被清理脚本删除**：
- `outputs/slides/`
- `outputs/images/`
- `outputs/markdown/`
- `outputs/plans/`
- `outputs/charts/`

### 手动清理

如果需要手动清理特定目录：

```bash
# 只清理测试目录
rm -rf outputs/test_*

# 只清理调试目录
rm -rf outputs/debug_*

# 只清理备份目录
rm -rf outputs/*_old_*
```

---

## 📈 效果统计

### 单次清理效果
- **减少空间**: 15M → 1.3M (87% reduction)
- **减少文件**: 249 → 38 (85% reduction)
- **清理目录**: 19 个

### 清理的目录类型
- `test_*`: 15 个目录 (10M)
- `debug_*`: 3 个目录 (3M)
- `*_old_*`: 1 个目录 (912K)
- 空目录: 5 个

---

## 🆘 故障排除

### 问题：脚本没有执行权限

```bash
chmod +x scripts/clean_outputs.sh
chmod +x scripts/auto_clean.sh
chmod +x scripts/health_check.sh
```

### 问题：找不到脚本

确保在项目根目录运行：
```bash
cd /path/to/PaperReader
./scripts/clean_outputs.sh
```

### 问题：清理了不想删除的文件

恢复方法：
1. 检查 Git 历史：`git checkout outputs/your_file`
2. 使用 Time Machine 或其他备份恢复

**预防措施**：始终先用 `DRY_RUN=true` 预览

---

## 📝 总结

1. **定期运行** `./scripts/health_check.sh` 检查项目状态
2. **需要清理时** 运行 `./scripts/auto_clean.sh`
3. **只清理 outputs** 使用 `./scripts/clean_outputs.sh`
4. **不确定时** 先用 `DRY_RUN=true` 预览

**推荐工作流**：
```bash
# 1. 开发完成后
./scripts/auto_clean.sh

# 2. 提交代码前
./scripts/health_check.sh

# 3. 定期维护（每周）
./scripts/auto_clean.sh
```
