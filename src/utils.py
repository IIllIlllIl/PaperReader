"""
Utility functions for PaperReader
"""

import os
import hashlib
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from dotenv import load_dotenv


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def setup_logging(config: Dict[str, Any]) -> logging.Logger:
    """Setup logging based on configuration"""
    log_dir = Path(config['logging']['file']).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config['logging']['level']),
        format=config['logging']['format'],
        handlers=[
            logging.FileHandler(config['logging']['file']),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def get_file_hash(file_path: str) -> str:
    """Calculate MD5 hash of a file for caching purposes"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def ensure_dir(directory: str) -> Path:
    """Ensure directory exists, create if not"""
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_api_key(config: Dict[str, Any]) -> str:
    """Get API key from environment variable"""
    load_dotenv()

    api_key_env = config['ai']['api_key_env']
    api_key = os.getenv(api_key_env)

    if not api_key:
        raise ValueError(
            f"API key not found. Please set {api_key_env} environment variable "
            f"or create a .env file with your API key."
        )

    return api_key


def scan_papers(input_dir: str) -> list:
    """Scan directory for PDF papers"""
    paper_dir = Path(input_dir)
    if not paper_dir.exists():
        raise FileNotFoundError(f"Paper directory not found: {input_dir}")

    pdf_files = list(paper_dir.glob("*.pdf"))
    return [str(pdf) for pdf in pdf_files]


def format_time(seconds: float) -> str:
    """Format seconds into human-readable time string"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max_length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

