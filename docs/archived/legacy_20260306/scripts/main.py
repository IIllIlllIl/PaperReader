#!/usr/bin/env python3
"""
PaperReader Compatibility Wrapper

This script provides backward compatibility after project reorganization.
All commands are forwarded to the new CLI location at cli/main.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and delegate to new CLI
from cli.main import cli

if __name__ == '__main__':
    cli()
