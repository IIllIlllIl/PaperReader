# 📚 PaperReader 文档中心

欢迎来到 PaperReader 文档中心。

---

## 快速导航

### 架构设计
- [架构索引](architecture/README.md)
- [数据流详解](architecture/DATA_FLOW.md)
- [数据流快速参考](architecture/DATA_FLOW_QUICK_REFERENCE.md)
- [数据流可视化](architecture/DATA_VISUALIZATION.md)
- [理解数据流](architecture/UNDERSTANDING_DATA_FLOW.md)
- [Slide Planning Layer](architecture/SLIDE_PLANNING_LAYER.md)
- [Pipeline Implementation](architecture/PIPELINE_IMPLEMENTATION.md)
- [项目摘要](architecture/PROJECT_SUMMARY.md)

### 功能文档
- [功能索引](features/README.md)
- [Narrative Planner](features/NARRATIVE_PLANNER.md)
- [Slide Formatter](features/SLIDE_FORMATTER.md)
- [Chart Generation](features/CHART_GENERATION.md)

### 测试与验收
- [测试索引](testing/README.md)
- [PHD Meeting V2 完成报告](testing/PHD_MEETING_V2_COMPLETE.md)
- [Research Meeting 升级报告](testing/RESEARCH_MEETING_UPGRADE.md)
- [Deployment Checklist](testing/DEPLOYMENT_CHECKLIST.md)

### 项目管理
- [项目索引](project/README.md)
- [项目状态](project/PROJECT_STATUS.md)
- [改进总结](project/IMPROVEMENTS_SUMMARY.md)
- [清理历史](project/CLEANUP_HISTORY.md)

### 用户指南
- [用户指南索引](user-guide/README.md)
- [增强版 PPTX 生成指南](user-guide/ENHANCED_PPTX_GUIDE.md)

---

## 文档结构

```text
docs/
├── architecture/   # 架构、数据流与实现说明
├── features/       # 功能说明
├── project/        # 项目状态、分析报告、清理记录
├── testing/        # 测试、验收与发布检查
├── user-guide/     # 使用指南
└── archived/       # 已归档历史文档
```

为避免索引过时，本页不再维护子目录文件数量。

---

## 建议阅读顺序

1. 先看 [README.md](../README.md) 了解安装和主命令
2. 再看 [Pipeline Implementation](architecture/PIPELINE_IMPLEMENTATION.md) 了解完整流水线
3. 需要排查输出时看 [数据流详解](architecture/DATA_FLOW.md)
4. 需要快速查命令和产物时看 [数据流快速参考](architecture/DATA_FLOW_QUICK_REFERENCE.md)

---

## 维护说明

- 活跃文档放在 `architecture/`、`features/`、`project/`、`testing/`、`user-guide/`
- 历史材料移到 `docs/archived/`
- 新增或删除活跃文档时同步更新本页链接
- 尽量避免在索引中写死文件数量、旧命令名或已删除脚本

---

**最后更新**: 2026-03-20
