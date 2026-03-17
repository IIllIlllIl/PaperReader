# 未调用代码和长时间未更新文件分析报告

**生成时间**: 2026-03-16
**分析范围**: 代码调用关系、文件更新时间、文档位置合理性

---

## 第一部分：代码调用关系分析

### 1. templates/ 目录分析

**状态**: ✅ **正在使用，必须保留**

**引用位置**:
- `src/generation/ppt_generator.py:26` - 作为默认模板路径

**结论**:
- `templates/ppt_template.md` 被 PPTGenerator 类使用
- 是核心功能的一部分
- **建议**: 保留

---

### 2. runtime/ 目录分析

**状态**: ✅ **正在使用，必须保留**

**引用位置**:
- `src/core/cache_manager.py:21` - 默认缓存目录
- `tools/refactor_repository.py` - 重构工具引用（辅助）

**当前内容**:
```
runtime/
├── cache/    (缓存文件)
└── logs/     (日志文件)
```

**结论**:
- 是缓存系统的核心目录
- **建议**: 保留

---

### 3. examples/ 目录分析

**状态**: ⚠️ **部分失效，需要清理**

**README.md 引用**:
- Line 327: `[Examples](examples/middle_products_example.py)`

**实际问题**:
- `examples/middle_products_example.py` - **已被删除** (git status: D)
- `examples/README.md` - 存在，但引用了不存在的文件

**examples/README.md 内容**:
- 描述了 `middle_products_example.py` 的功能
- 引用了 `tools/debug_data_flow.py`（也已删除）
- 提供了学习路径，但链接失效

**结论**:
- examples/ 目录当前只有 README.md
- README.md 引用的文件不存在
- **建议**:
  1. **选项A**: 删除 examples/ 目录（推荐）
  2. **选项B**: 更新 examples/README.md，移除失效链接，作为文档目录保留

---

### 4. tools/test_*.py 测试脚本分析

**状态**: ⚠️ **独立脚本，未被导入**

**发现的测试脚本**:
```
tools/test_chart_generation.py       4.5K
tools/test_narrative_planner.py      3.8K
tools/test_phd_meeting_v2.py         6.6K
tools/test_research_meeting.py       3.7K
tools/test_slide_formatter.py        7.6K
tools/test_slide_planner.py          4.2K
```

**引用分析**:
- **没有任何 Python 文件导入这些模块**
- 它们是独立的可执行测试脚本

**脚本功能**:
1. `test_narrative_planner.py` - 测试叙事提取流程
2. `test_slide_formatter.py` - 测试幻灯片格式化规则
3. `test_chart_generation.py` - 测试图表生成
4. `test_slide_planner.py` - 测试幻灯片规划
5. `test_research_meeting.py` - 测试研究会议模式
6. `test_phd_meeting_v2.py` - 测试博士会议模式 V2

**结论**:
- 这些是**手动测试工具**，不是单元测试
- 可能用于功能验证和演示
- **建议**:
  1. **选项A**: 移动到 `tools/manual_tests/` 子目录，明确分类
  2. **选项B**: 如果有对应的 pytest 测试，可以删除
  3. **选项C**: 保留在 tools/，在 README 中说明用途

---

## 第二部分：长时间未更新文件分析

### 文件修改时间统计

**根目录文件**:
```
.env                  2026-03-05  (11天前)
.env.example          2026-03-04  (12天前)
.gitignore            2026-03-13  (3天前)
CLAUDE.md             2026-03-16  (今天)
CLEANUP_REPORT.md     2026-03-16  (今天)
IMPROVEMENTS_SUMMARY.md  2026-03-13  (3天前)
PIPELINE_IMPLEMENTATION.md  2026-03-13  (3天前)
README.md             2026-03-16  (今天)
config.yaml           2026-03-13  (3天前)
paperreader           2026-03-05  (11天前)
project_audit_20260316.txt  2026-03-16  (今天)
requirements.txt      2026-03-16  (今天)
```

**顶级目录最新修改时间**:
```
.claude/      2026-03-16 16:44  (活跃)
.pytest_cache/  2026-03-16 12:48  (活跃)
cli/          2026-03-13 15:53
docs/         2026-03-13 13:53
examples/     2026-03-13 13:08
outputs/      2026-03-16 14:53  (活跃)
papers/       2026-03-04 16:07  (12天前)
runtime/      2026-03-05 15:20  (11天前)
scripts/      2026-03-13 12:52
src/          2026-03-16 15:23  (活跃)
templates/    2026-03-05 13:57  (11天前)
tests/        2026-03-16 12:47  (活跃)
tools/        2026-03-16 12:41  (活跃)
```

**30天未更新文件**: **无**

**结论**:
- ✅ 项目处于**活跃维护状态**
- ✅ 所有关键目录都在近期有更新
- ✅ 没有长期废弃的文件

---

## 第三部分：文档位置合理性分析

### 根目录 .md 文件分类

| 文件 | 当前位置 | 建议位置 | 理由 |
|------|---------|---------|------|
| CLAUDE.md | 根目录 | ✅ **保留根目录** | Claude Code 配置文件，标准位置 |
| README.md | 根目录 | ✅ **保留根目录** | 项目主文档，标准位置 |
| CLEANUP_REPORT.md | 根目录 | ⚠️ **可选** | 最近清理记录，可在根目录或移到 docs/project/ |
| IMPROVEMENTS_SUMMARY.md | 根目录 | ❌ **应移到 docs/** | 改进总结，属于文档 |
| PIPELINE_IMPLEMENTATION.md | 根目录 | ❌ **应移到 docs/architecture/** | 架构设计文档 |

### docs/ 目录结构分析

**当前结构**:
```
docs/
├── architecture/      (13个文件) - 架构设计
├── features/          (5个文件) - 功能文档
├── project/           (2个文件) - 项目管理
├── testing/           (13个文件) - 测试文档
└── user-guide/        (1个文件) - 用户指南
```

**建议的文档调整**:

1. **IMPROVEMENTS_SUMMARY.md** → `docs/project/IMPROVEMENTS_SUMMARY.md`
   - 与 PROJECT_STATUS.md 放在一起

2. **PIPELINE_IMPLEMENTATION.md** → `docs/architecture/PIPELINE_IMPLEMENTATION.md`
   - 与其他架构文档放在一起

3. **CLEANUP_REPORT.md**:
   - **选项A**: 保留根目录（方便查看最近清理）
   - **选项B**: 移到 `docs/project/CLEANUP_REPORT.md`

---

## 第四部分：清理建议清单

### 1. 可安全移动到 trash 的目录/文件

#### A. examples/ 目录（推荐删除）

**建议**: 🗑️ **删除整个 examples/ 目录**

**理由**:
- 目录只包含一个 README.md
- README.md 引用的所有文件都已删除
- 没有实际代码或数据
- 删除风险：**低**

**命令**:
```bash
mv examples/ trash/cleanup_20260316/examples/
```

#### B. 临时审计文件（可选删除）

**文件**: `project_audit_20260316.txt`

**建议**: ⚠️ **可选删除**

**理由**:
- 这是今天生成的审计文件
- 内容可能已整合到其他报告
- 如果不再需要可以删除

**命令**:
```bash
mv project_audit_20260316.txt trash/cleanup_20260316/
```

---

### 2. 需要移动到 docs/ 的文档清单

#### 优先级 1: 必须移动

```bash
# 移动改进总结到项目文档
mv IMPROVEMENTS_SUMMARY.md docs/project/

# 移动架构文档到架构目录
mv PIPELINE_IMPLEMENTATION.md docs/architecture/
```

#### 优先级 2: 可选移动

```bash
# 可选：移动清理报告到项目文档
mv CLEANUP_REPORT.md docs/project/
```

**移动后需要更新**:
- 检查 README.md 是否有引用这些文件
- 如果有，更新链接

---

### 3. 需要整合的测试脚本清单

#### tools/test_*.py 处理建议

**当前状态**: 6个独立测试脚本，共 30.4 KB

**推荐方案**: 创建 `tools/manual_tests/` 子目录

```bash
# 创建目录
mkdir -p tools/manual_tests

# 移动测试脚本
mv tools/test_chart_generation.py tools/manual_tests/
mv tools/test_narrative_planner.py tools/manual_tests/
mv tools/test_phd_meeting_v2.py tools/manual_tests/
mv tools/test_research_meeting.py tools/manual_tests/
mv tools/test_slide_formatter.py tools/manual_tests/
mv tools/test_slide_planner.py tools/manual_tests/

# 创建 README 说明
cat > tools/manual_tests/README.md << 'EOF'
# Manual Test Scripts

These scripts are used for manual testing and demonstration purposes.

## Usage

Run any script directly:

```bash
python tools/manual_tests/test_slide_formatter.py
```

## Scripts

- `test_chart_generation.py` - Test chart generation
- `test_narrative_planner.py` - Test narrative extraction
- `test_phd_meeting_v2.py` - Test PhD meeting mode V2
- `test_research_meeting.py` - Test research meeting mode
- `test_slide_formatter.py` - Test slide formatting rules
- `test_slide_planner.py` - Test slide planning
EOF
```

**替代方案**: 如果这些脚本不再使用，可以移动到 `archive/manual_tests/`

---

### 4. 需要保留但可归档的目录建议

#### 无需归档的目录

**以下目录都在活跃使用，不建议归档**:
- ✅ `templates/` - 被 PPTGenerator 使用
- ✅ `runtime/` - 被缓存管理器使用
- ✅ `scripts/` - 可能包含实用脚本
- ✅ `papers/` - 输入论文目录（即使为空）

---

### 5. README.md 失效链接修复

#### 需要修复的链接

**README.md Line 327**:
```markdown
当前: - **[Project Improvements](IMPROVEMENTS_SUMMARY.md)** - Recent pipeline improvements
```

**修复方案 1**: 删除该行（如果删除 examples/ 目录）
```markdown
# 删除整行
```

**修复方案 2**: 更新链接（如果保留 examples/README.md）
```markdown
修改为: - **[Examples](examples/README.md)** - Examples and intermediate products documentation
```

---

## 第五部分：执行建议

### 推荐执行顺序

#### Phase 1: 低风险清理（立即执行）

```bash
# 1. 移动文档到正确位置
mv IMPROVEMENTS_SUMMARY.md docs/project/
mv PIPELINE_IMPLEMENTATION.md docs/architecture/

# 2. 整理测试脚本
mkdir -p tools/manual_tests
mv tools/test_*.py tools/manual_tests/

# 3. 创建测试脚本说明
# (如上所示的 README.md)
```

#### Phase 2: 中等风险清理（需确认）

```bash
# 4. 删除 examples/ 目录
mv examples/ trash/cleanup_20260316/examples/

# 5. 修复 README.md 失效链接
# 手动编辑 README.md，移除 Line 327 或更新链接
```

#### Phase 3: 可选清理

```bash
# 6. 移动清理报告（可选）
mv CLEANUP_REPORT.md docs/project/

# 7. 删除临时审计文件（可选）
mv project_audit_20260316.txt trash/cleanup_20260316/
```

---

## 第六部分：风险评估

### 低风险操作 ✅

- 移动文档到 docs/ 子目录
- 整理测试脚本到子目录
- 删除 examples/ 目录（只有 README.md）

### 中等风险操作 ⚠️

- 修改 README.md（需要检查引用）
- 删除 project_audit_20260316.txt（可能需要保留）

### 无风险 ✅

- 所有操作都可以通过 trash/ 恢复
- 没有删除任何正在使用的代码

---

## 第七部分：总结

### 关键发现

1. **✅ 没有长期未更新的文件** - 项目维护良好
2. **✅ 核心目录都在使用** - templates/, runtime/ 必须保留
3. **⚠️ examples/ 目录失效** - 只有 README.md，引用的文件已删除
4. **⚠️ 6个独立测试脚本** - 未被导入，建议整理到子目录
5. **⚠️ 根目录文档散乱** - 2个文档应移到 docs/

### 推荐操作

**立即执行**:
1. 移动 `IMPROVEMENTS_SUMMARY.md` → `docs/project/`
2. 移动 `PIPELINE_IMPLEMENTATION.md` → `docs/architecture/`
3. 创建 `tools/manual_tests/` 并移动测试脚本

**可选执行**:
4. 删除 `examples/` 目录
5. 修复 `README.md` 失效链接

### 预期效果

- ✅ 清晰的文档组织结构
- ✅ 明确的测试脚本分类
- ✅ 移除失效的目录和链接
- ✅ 保持项目活跃状态

---

## 附录：命令速查表

### 快速清理命令

```bash
# Phase 1: 文档整理
mv IMPROVEMENTS_SUMMARY.md docs/project/
mv PIPELINE_IMPLEMENTATION.md docs/architecture/

# Phase 2: 测试脚本整理
mkdir -p tools/manual_tests
mv tools/test_*.py tools/manual_tests/

# Phase 3: 清理失效目录
mv examples/ trash/cleanup_20260316/examples/

# Phase 4: 更新 README.md
# 手动编辑，移除或更新 Line 327
```

### 验证命令

```bash
# 验证文档移动
ls -la docs/project/
ls -la docs/architecture/

# 验证测试脚本移动
ls -la tools/manual_tests/

# 验证 examples/ 删除
ls -la examples/ 2>&1  # 应该报错

# 验证 README.md 链接
grep "examples/" README.md
```

---

**报告生成时间**: 2026-03-16 16:45
**分析工具**: Claude Code
**下一步**: 等待用户确认后执行清理操作
