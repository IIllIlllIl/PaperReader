# PaperReader 项目规范

## 📁 目录结构黄金法则

根目录允许的文件：
```
├── CLAUDE.md           # 项目规范
├── README.md           # 项目说明
├── config.yaml         # 配置文件
├── requirements.txt    # 依赖文件
└── paperreader         # 可执行文件
```

其他所有文档必须放在：
```
└── docs/
    ├── project/        # 项目报告和文档
    ├── architecture/   # 架构文档
    ├── features/       # 功能文档
    └── testing/        # 测试文档
```

## 🚫 禁止提交的文件

- `.DS_Store`
- `*.pyc`
- `__pycache__/`
- `*.log`
- `*.tmp`
- `*.bak`
- `*~`

## 🔧 维护命令

```bash
# 检查项目健康状态
./scripts/health_check.sh

# 自动清理问题
./scripts/auto_clean.sh

# 提交前会自动检查（Git hook）
git commit -m "你的提交信息"
```

## 📋 Git 提交规范

提交前会自动检查：
- ✅ 根目录没有多余的 Markdown 文件
- ✅ 没有临时文件和缓存文件
- ✅ 文档组织符合规范

如果检查失败，请先运行：
```bash
./scripts/auto_clean.sh
```

## 🎯 最佳实践

1. **报告和文档**：所有项目报告、分析文档都应该放在 `docs/project/`
2. **功能文档**：功能相关的文档放在 `docs/features/`
3. **架构文档**：架构设计文档放在 `docs/architecture/`
4. **测试文档**：测试相关的文档放在 `docs/testing/`

## 🔄 定期维护

建议每周运行一次健康检查：
```bash
./scripts/health_check.sh
```

保持项目整洁，从规范开始！
