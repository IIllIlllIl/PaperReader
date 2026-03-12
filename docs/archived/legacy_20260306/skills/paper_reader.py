# PaperReader Skill 设计方案

## 概述

为PaperReader设计一套skill命令，让用户可以在Claude对话框中用最简单的语言处理论文。

## 核心设计理念

1. **极简输入** - 最少只需1-2个词
2. **智能推断** - 自动检测最新PDF、智能选择格式
3. **灵活配置** - 支持简单模式和高级模式
4. **友好反馈** - 清晰的进度和结果提示

## Skill命令设计

### 1. 基础命令：`/paper`

**最简用法**：
```
/paper
```
- 自动处理 `papers/` 目录中最新的PDF
- 生成HTML格式PPT
- 使用默认配置

**指定文件**：
```
/paper attention.pdf
/paper papers/transformer.pdf
```

**指定格式**：
```
/paper --pdf
/paper attention.pdf --md
/paper transformer.pdf --html
```

### 2. 批量命令：`/papers`

**处理所有论文**：
```
/papers
```

**指定格式**：
```
/papers --pdf
/papers --md
```

### 3. 快速命令：`/ppt` 和 `/md`

**快速生成PPT**：
```
/ppt
/ppt attention.pdf
```

**快速生成Markdown**：
```
/md
/md transformer.pdf
```

### 4. 查询命令：`/papers-stats`

**查看统计**：
```
/papers-stats
```

## Skill配置文件

### 创建 `.claude/skills/paper_reader.yaml`

```yaml
name: paper_reader
description: Process academic papers and generate presentations
version: 1.0.0

commands:
  - name: paper
    description: Process a single paper
    usage: |
      /paper [filename] [--format=html|pdf|md] [--verbose] [--no-cache]

    arguments:
      - name: filename
        type: string
        optional: true
        description: PDF filename or path (defaults to latest in papers/)

      - name: format
        short: f
        type: choice
        choices: [html, pdf, md, markdown]
        default: html
        description: Output format

      - name: verbose
        short: v
        type: flag
        description: Show detailed progress

      - name: no-cache
        type: flag
        description: Disable cache for this run

    examples:
      - command: /paper
        description: Process latest PDF to HTML

      - command: /paper attention.pdf
        description: Process specific file

      - command: /paper --pdf
        description: Generate PDF output

      - command: /paper transformer.pdf --verbose
        description: Process with detailed output

  - name: papers
    description: Process all papers in papers/ directory
    usage: |
      /papers [--format=html|pdf|md]

    arguments:
      - name: format
        short: f
        type: choice
        choices: [html, pdf, md, markdown]
        default: html

    examples:
      - command: /papers
        description: Process all papers to HTML

      - command: /papers --pdf
        description: Process all papers to PDF

  - name: ppt
    description: Quick generate presentation (HTML format)
    usage: |
      /ppt [filename]

    arguments:
      - name: filename
        type: string
        optional: true

    examples:
      - command: /ppt
        description: Generate HTML presentation from latest PDF

      - command: /ppt attention.pdf
        description: Generate from specific file

  - name: md
    description: Quick generate Markdown only
    usage: |
      /md [filename]

    arguments:
      - name: filename
        type: string
        optional: true

    examples:
      - command: /md
        description: Generate Markdown from latest PDF

  - command: /md transformer.pdf
        description: Generate from specific file

  - name: papers-stats
    description: Show cache and processing statistics
    usage: |
      /papers-stats

# Skill execution handler
handler:
  type: python
  module: skills.paper_reader
  function: handle_paper_command

# Integration settings
integrations:
  - type: file_watcher
    path: papers/
    event: new_file
    action: suggest_processing

  - type: auto_complete
    triggers:
      - pattern: "/paper *.pdf"
        complete_from: papers/
      - pattern: "/ppt *.pdf"
        complete_from: papers/
      - pattern: "/md *.pdf"
        complete_from: papers/

# User preferences
preferences:
  default_format: html
  auto_open_result: true
  show_cost_warning: true
  cache_enabled: true
```

## Skill执行脚本

### 创建 `skills/paper_reader.py`

```python
"""
PaperReader Skill Handler

Handles /paper, /papers, /ppt, /md commands
"""

import os
import sys
from pathlib import Path
from typing import Optional, List
import subprocess
import json

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def handle_paper_command(command: str, args: dict) -> dict:
    """
    Main handler for paper reader commands

    Args:
        command: Command name (paper, papers, ppt, md)
        args: Command arguments

    Returns:
        Response dict with status and message
    """
    try:
        if command == 'paper':
            return handle_single_paper(args)
        elif command == 'papers':
            return handle_batch_papers(args)
        elif command == 'ppt':
            return handle_quick_ppt(args)
        elif command == 'md':
            return handle_quick_md(args)
        elif command == 'papers-stats':
            return handle_stats()
        else:
            return {
                'status': 'error',
                'message': f'Unknown command: {command}'
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}'
        }


def handle_single_paper(args: dict) -> dict:
    """Handle /paper command"""

    # Get filename
    filename = args.get('filename')

    if not filename:
        # Find latest PDF
        filename = find_latest_pdf()
        if not filename:
            return {
                'status': 'error',
                'message': 'No PDF files found in papers/ directory'
            }

    # Resolve path
    pdf_path = resolve_pdf_path(filename)
    if not pdf_path:
        return {
            'status': 'error',
            'message': f'PDF not found: {filename}'
        }

    # Get format
    format = args.get('format', 'html')

    # Build command
    cmd = build_command(pdf_path, format, args)

    # Execute
    return execute_command(cmd, pdf_path, format)


def handle_batch_papers(args: dict) -> dict:
    """Handle /papers command"""

    format = args.get('format', 'html')

    cmd = ['python', str(PROJECT_ROOT / 'main.py'), 'process', '--all', '-f', format]

    if args.get('verbose'):
        cmd.append('--verbose')

    # Execute
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT))

    if result.returncode == 0:
        return {
            'status': 'success',
            'message': f'Batch processing completed!\n\n{result.stdout}',
            'action': 'display'
        }
    else:
        return {
            'status': 'error',
            'message': f'Batch processing failed:\n{result.stderr}'
        }


def handle_quick_ppt(args: dict) -> dict:
    """Handle /ppt command (quick HTML generation)"""

    args['format'] = 'html'
    return handle_single_paper(args)


def handle_quick_md(args: dict) -> dict:
    """Handle /md command (quick Markdown generation)"""

    args['format'] = 'markdown'
    return handle_single_paper(args)


def handle_stats() -> dict:
    """Handle /papers-stats command"""

    cmd = ['python', str(PROJECT_ROOT / 'main.py'), 'stats']
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT))

    return {
        'status': 'success',
        'message': f'Cache Statistics:\n\n{result.stdout}',
        'action': 'display'
    }


def find_latest_pdf() -> Optional[str]:
    """Find the most recently modified PDF in papers/ directory"""

    papers_dir = PROJECT_ROOT / 'papers'
    if not papers_dir.exists():
        return None

    pdf_files = list(papers_dir.glob('*.pdf'))
    if not pdf_files:
        return None

    # Sort by modification time, get latest
    latest = max(pdf_files, key=lambda p: p.stat().st_mtime)
    return str(latest)


def resolve_pdf_path(filename: str) -> Optional[str]:
    """Resolve PDF path from filename"""

    # Try as absolute path
    if Path(filename).is_absolute() and Path(filename).exists():
        return filename

    # Try in papers/ directory
    papers_path = PROJECT_ROOT / 'papers' / filename
    if papers_path.exists():
        return str(papers_path)

    # Try as relative path from project root
    root_path = PROJECT_ROOT / filename
    if root_path.exists():
        return str(root_path)

    # Try adding .pdf extension
    if not filename.endswith('.pdf'):
        return resolve_pdf_path(filename + '.pdf')

    return None


def build_command(pdf_path: str, format: str, args: dict) -> List[str]:
    """Build main.py command"""

    cmd = [
        'python',
        str(PROJECT_ROOT / 'main.py'),
        'process',
        '--paper', pdf_path,
        '--format', format
    ]

    if args.get('verbose'):
        cmd.append('--verbose')

    if args.get('no-cache'):
        cmd.append('--no-cache')

    return cmd


def execute_command(cmd: List[str], pdf_path: str, format: str) -> dict:
    """Execute processing command and return result"""

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT)
    )

    if result.returncode == 0:
        # Determine output file
        pdf_name = Path(pdf_path).stem
        output_dir = PROJECT_ROOT / 'output'

        if format == 'markdown':
            output_file = output_dir / 'markdown' / f'{pdf_name}.md'
        elif format == 'pdf':
            output_file = output_dir / 'slides' / f'{pdf_name}.pdf'
        else:  # html
            output_file = output_dir / 'slides' / f'{pdf_name}.html'

        message = f'✅ Paper processed successfully!\n\n'
        message += f'📄 Input: {Path(pdf_path).name}\n'
        message += f'📊 Output: {output_file.relative_to(PROJECT_ROOT)}\n\n'
        message += f'Details:\n{result.stdout}'

        return {
            'status': 'success',
            'message': message,
            'action': 'display',
            'output_file': str(output_file)
        }
    else:
        return {
            'status': 'error',
            'message': f'Processing failed:\n{result.stderr}'
        }


# Command line testing
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['paper', 'papers', 'ppt', 'md', 'stats'])
    parser.add_argument('--filename', '-f', help='PDF filename')
    parser.add_argument('--format', choices=['html', 'pdf', 'md'], default='html')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--no-cache', action='store_true')

    cli_args = parser.parse_args()

    if cli_args.command == 'stats':
        result = handle_stats()
    else:
        args_dict = {
            'filename': cli_args.filename,
            'format': cli_args.format,
            'verbose': cli_args.verbose,
            'no-cache': cli_args.no_cache
        }

        if cli_args.command == 'paper':
            result = handle_single_paper(args_dict)
        elif cli_args.command == 'papers':
            result = handle_batch_papers(args_dict)
        elif cli_args.command == 'ppt':
            result = handle_quick_ppt(args_dict)
        elif cli_args.command == 'md':
            result = handle_quick_md(args_dict)

    print(result['message'])
