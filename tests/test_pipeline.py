#!/usr/bin/env python3
"""
Test script for the PaperPresentationPipeline

Usage:
    python test_pipeline.py papers/example.pdf
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.pipeline import PaperPresentationPipeline
from src.utils import load_config, get_api_key, setup_logging


def main():
    """Test the pipeline"""

    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python test_pipeline.py <pdf_path>")
        print("\nExample:")
        print("  python test_pipeline.py papers/example.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]

    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    # Load config
    config = load_config('config.yaml')

    # Setup logging
    logger = setup_logging(config)

    # Get API key
    try:
        api_key = get_api_key(config)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Create pipeline
    pipeline = PaperPresentationPipeline(
        api_key=api_key,
        config=config,
        model=config['ai']['model']
    )

    # Run pipeline
    result = pipeline.run(pdf_path=pdf_path, output_dir='outputs')

    if result['success']:
        print("\n✅ Pipeline test completed successfully!")
        print(f"\nGenerated files:")
        for key, path in result['output_paths'].items():
            print(f"  {key}: {path}")
        sys.exit(0)
    else:
        print(f"\n❌ Pipeline test failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == '__main__':
    main()
