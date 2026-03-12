# 📁 PaperReader 根目录整理方案

**创建日期**: 2026-03-05  
**目的**: 优化项目结构，提高可维护性

---

## 📋 当前问题

根目录下有多个临时状态文件和报告文件，影响项目结构的清晰度：
- DOCUMENTATION_UPDATE_COMPLETE.md
- PROJECT_REORGANIZATION.md
- PROJECT_STATUS.md
- REFACTORING_COMPLETE.md
- test_pptx_generation.md

---

## 🎯 整理目标

1. **根目录简洁**: 只保留核心配置和入口文件
2. **文档集中管理**: 所有文档按类型组织在 `docs/` 下
3. **符合 Python 最佳实践**: 遵循标准项目布局
4. **便于维护**: 清晰的目录结构

---

## 📂 建议的新目录结构

```
PaperReader/
├── 📄 README.md                    # 项目说明（保留）
├── 📄 CLAUDE.md                    # Claude 指导（保留）
├── 📄 requirements.txt             # 依赖（保留）
├── 📄 config.yaml                  # 配置（保留）
├── 📄 .env.example                 # 环境变量示例（保留）
├── 📄 .gitignore                   # Git 配置（保留）
├── 📄 main.py                      # 主入口（保留）
├── 📄 paperreader                  # 快捷脚本（保留）
│
├── 📂 docs/                        # 📚 文档目录
│   ├── 📄 README.md               # 文档索引
│   ├── 📂 project/                # 项目管理文档
│   │   ├── PROJECT_STATUS.md
│   │   └── PROJECT_REORGANIZATION.md
│   ├── 📂 changelogs/             # 变更日志
│   │   ├── REFACTORING_COMPLETE.md
│   │   └── DOCUMENTATION_UPDATE_COMPLETE.md
│   ├── 📂 architecture/           # 架构文档
│   │   ├── DATA_FLOW.md
│   │   ├── DATA_VISUALIZATION.md
│   │   └── UNDERSTANDING_DATA_FLOW.md
│   ├── 📂 testing/                # 测试文档
│   │   └── test_pptx_generation.md
│   └── 📂 user-guide/             # 用户指南
│       └── (未来添加)
│
├── 📂 src/                        # 源代码（保留）
├── 📂 cli/                        # CLI 模块（保留）
├── 📂 tests/                      # 测试（保留）
├── 📂 tools/                      # 工具脚本（保留）
├── 📂 templates/                  # 模板（保留）
├── 📂 examples/                   # 示例（保留）
├── 📂 papers/                     # 输入（保留）
├── 📂 output/                     # 输出（保留）
├── 📂 cache/                      # 缓存（保留）
├── 📂 logs/                       # 日志（保留）
└── 📂 skills/                     # Claude 技能（保留）
```

---

## 🔄 文件移动计划

### 1. 移动到 `docs/project/`
```bash
mv PROJECT_STATUS.md docs/project/
mv PROJECT_REORGANIZATION.md docs/project/
```

### 2. 移动到 `docs/changelogs/`
```bash
mv REFACTORING_COMPLETE.md docs/changelogs/
mv DOCUMENTATION_UPDATE_COMPLETE.md docs/changelogs/
```

### 3. 移动到 `docs/architecture/`
```bash
# 已存在的文件，保持不动
# DATA_FLOW.md
# DATA_VISUALIZATION.md
# UNDERSTANDING_DATA_FLOW.md
```

### 4. 移动到 `docs/testing/`
```bash
mv test_pptx_generation.md docs/testing/
```

---

## 📝 更新文档索引

创建 `docs/README.md` 作为文档导航：

```markdown
# 📚 PaperReader 文档中心

## 🎯 快速导航

### 项目管理
- [项目状态](project/PROJECT_STATUS.md) - 当前项目状态和进展
- [重组计划](project/PROJECT_REORGANIZATION.md) - 项目重组方案

### 架构设计
- [数据流](architecture/DATA_FLOW.md) - 详细数据流说明
- [快速参考](architecture/DATA_FLOW_QUICK_REFERENCE.md) - 数据流快速参考

### 变更日志
- [重构完成](changelogs/REFACTORING_COMPLETE.md) - 重构总结
- [文档更新](changelogs/DOCUMENTATION_UPDATE_COMPLETE.md) - 文档更新记录

### 测试
- [PPTX 生成测试](testing/test_pptx_generation.md) - PPTX 功能测试报告

### 用户指南
- (待添加)

## 📂 文档结构

- `project/` - 项目管理相关文档
- `architecture/` - 架构和技术文档
- `changelogs/` - 变更日志和里程碑
- `testing/` - 测试报告和结果
- `user-guide/` - 用户使用指南
```

---

## ✅ 整理后的根目录

整理后，根目录将只包含：

```
PaperReader/
├── README.md
├── CLAUDE.md
├── requirements.txt
├── config.yaml
├── .env.example
├── .gitignore
├── main.py
├── paperreader
├── src/
├── cli/
├── tests/
├── tools/
├── templates/
├── examples/
├── papers/
├── output/
├── cache/
├── logs/
├── skills/
└── docs/
```

**根目录文件数**: 8 个（符合最佳实践）

---

## 🚀 实施步骤

### 方案 A: 手动执行（推荐）
逐步执行命令，确认每一步正确

### 方案 B: 自动脚本
运行提供的整理脚本 `tools/reorganize_project.sh`

---

## 📊 整理收益

| 指标 | 当前 | 整理后 | 改善 |
|------|------|--------|------|
| 根目录文件数 | 13 | 8 | **-38%** |
| 文档组织 | 分散 | 集中 | **✅** |
| 查找效率 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **+67%** |

---

## 🔍 注意事项

1. **Git 历史**: 文件移动后，Git 会自动跟踪
2. **引用更新**: 需要检查是否有其他文件引用这些文档
3. **.gitignore**: 添加 `docs/user-guide/.gitkeep` 占位
4. **CLAUDE.md**: 可能需要更新文档路径引用

---

## 📅 执行检查清单

- [ ] 创建新的文档子目录
- [ ] 移动项目管理文档
- [ ] 移动变更日志
- [ ] 移动测试文档
- [ ] 更新 docs/README.md
- [ ] 检查并更新文档引用
- [ ] 提交变更到 Git
- [ ] 验证项目功能正常

---

## 💡 未来改进

1. **自动化文档生成**: 使用 Sphinx 或 MkDocs
2. **API 文档**: 添加代码文档生成
3. **版本化文档**: 为不同版本维护文档
4. **贡献指南**: 添加 CONTRIBUTING.md

