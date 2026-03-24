#!/usr/bin/env python3
"""
Verification script for directory structure refactoring.

This script checks:
1. All modules use correct output paths
2. Intermediate artifacts go to outputs/intermediates/
3. Final artifacts go to outputs/slides/ and outputs/reports/
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parser.pdf_image_extractor import PDFImageExtractor
from src.analysis.citation_analyzer import CitationAnalyzer
from src.analysis.citation_integration import CitationIntegrator
from src.core.pipeline import PaperPresentationPipeline


def check_path_setting(obj, attr_name, expected_suffix):
    """Check if an object's path attribute has the expected suffix."""
    actual = str(getattr(obj, attr_name))
    if expected_suffix in actual:
        print(f"  ✅ {attr_name}: {actual}")
        return True
    else:
        print(f"  ❌ {attr_name}: {actual} (expected: {expected_suffix})")
        return False


def verify_pdf_image_extractor():
    """Verify PDFImageExtractor uses correct path."""
    print("\n1. PDFImageExtractor")
    extractor = PDFImageExtractor()
    return check_path_setting(extractor, 'output_dir', 'intermediates/images')


def verify_citation_analyzer():
    """Verify CitationAnalyzer uses correct path."""
    print("\n2. CitationAnalyzer")
    analyzer = CitationAnalyzer()
    return check_path_setting(analyzer, 'cache_dir', 'intermediates/citations')


def verify_citation_integrator():
    """Verify CitationIntegrator uses correct paths."""
    print("\n3. CitationIntegrator")
    integrator = CitationIntegrator()
    chart_output = integrator.chart_generator.output_dir
    expected = 'intermediates/images/citations'

    if expected in str(chart_output):
        print(f"  ✅ chart_generator.output_dir: {chart_output}")
        return True
    else:
        print(f"  ❌ chart_generator.output_dir: {chart_output} (expected: {expected})")
        return False


def verify_pipeline():
    """Verify PaperPresentationPipeline output paths."""
    print("\n4. PaperPresentationPipeline")

    # Check pipeline path definitions
    import inspect
    source = inspect.getsource(PaperPresentationPipeline.run)

    checks = {
        'intermediates/markdown': "'intermediates' / 'markdown'" in source or "intermediates' / 'markdown'" in source,
        'intermediates/scripts': "'intermediates' / 'scripts'" in source or "intermediates' / 'scripts'" in source,
        'intermediates/plans': "'intermediates' / 'plans'" in source or "intermediates' / 'plans'" in source,
        'slides/': "'slides'" in source,
    }

    all_passed = True
    for path, passed in checks.items():
        if passed:
            print(f"  ✅ {path} reference found")
        else:
            print(f"  ❌ {path} reference NOT found")
            all_passed = False

    return all_passed


def main():
    """Run all verification checks."""
    print("="*70)
    print("Directory Structure Verification")
    print("="*70)

    results = {
        'PDFImageExtractor': verify_pdf_image_extractor(),
        'CitationAnalyzer': verify_citation_analyzer(),
        'CitationIntegrator': verify_citation_integrator(),
        'Pipeline': verify_pipeline(),
    }

    print("\n" + "="*70)
    print("Verification Summary")
    print("="*70)

    all_passed = all(results.values())

    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")

    print("="*70)

    if all_passed:
        print("\n✅ All checks passed! Directory structure is correct.")
        return 0
    else:
        print("\n❌ Some checks failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
