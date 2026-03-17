# Examples Directory Archived

**Date**: 2026-03-17
**Action**: Archived to `trash/cleanup_20260317/examples_archived/`

## Reason for Archival

The `examples/` directory was archived because:

1. **Only contained README.md** - No actual example files remained
2. **Referenced deleted files** - README.md linked to `middle_products_example.py` which was deleted
3. **Outdated content** - Examples referenced deprecated tools and workflows

## What Was Moved

```
examples/
└── README.md (only file remaining)
```

Moved to: `trash/cleanup_20260317/examples_archived/`

## Alternative Resources

For intermediate products and data flow examples, see:

- **[Data Flow Guide](../architecture/DATA_FLOW.md)** - Detailed explanation with examples
- **[Quick Reference](../architecture/DATA_FLOW_QUICK_REFERENCE.md)** - Quick reference card
- **[Project Improvements](IMPROVEMENTS_SUMMARY.md)** - Recent pipeline improvements
- **[Pipeline Implementation](../architecture/PIPELINE_IMPLEMENTATION.md)** - Architecture overview

## Recovery

If you need to restore the examples directory:

```bash
mv trash/cleanup_20260317/examples_archived/ examples/
```

---

*This file documents the cleanup action taken on 2026-03-17.*
