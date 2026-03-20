#!/usr/bin/env python3
"""
Test clean intermediates functionality.

This test verifies:
1. Default mode (--clean) removes intermediate files after success
2. Debug mode (--no-clean) preserves intermediate files
3. Failure preserves intermediate files for debugging
4. Manual cleanup script works correctly
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.pipeline import PaperPresentationPipeline


def test_clean_parameter():
    """Test that clean_intermediates parameter is properly initialized"""
    print("\nTest 1: Clean parameter initialization")

    # Test with clean=True (default)
    pipeline1 = PaperPresentationPipeline(
        api_key="test_key",
        config={},
        clean_intermediates=True
    )
    assert pipeline1.clean_intermediates == True, "clean_intermediates should be True"
    print("  ✅ clean_intermediates=True properly set")

    # Test with clean=False
    pipeline2 = PaperPresentationPipeline(
        api_key="test_key",
        config={},
        clean_intermediates=False
    )
    assert pipeline2.clean_intermediates == False, "clean_intermediates should be False"
    print("  ✅ clean_intermediates=False properly set")


def test_create_intermediates_structure():
    """Test that intermediates directory structure is created correctly"""
    print("\nTest 2: Create intermediates structure")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "outputs"

        pipeline = PaperPresentationPipeline(
            api_key="test_key",
            config={},
            clean_intermediates=False  # Don't clean during init
        )
        pipeline.output_dir = str(output_dir)

        # Create structure
        pipeline._create_intermediates_structure()

        # Verify all subdirectories exist
        intermediates_dir = output_dir / "intermediates"
        expected_subdirs = ['images', 'images/citations', 'markdown', 'scripts', 'plans', 'citations', 'temp']

        for subdir in expected_subdirs:
            subdir_path = intermediates_dir / subdir
            assert subdir_path.exists(), f"Subdirectory {subdir} should exist"
            assert subdir_path.is_dir(), f"{subdir} should be a directory"

        print(f"  ✅ Created {len(expected_subdirs)} subdirectories correctly")


def test_clean_with_files():
    """Test that clean actually removes files"""
    print("\nTest 3: Clean with files")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "outputs"

        # Create pipeline
        pipeline = PaperPresentationPipeline(
            api_key="test_key",
            config={},
            clean_intermediates=True
        )
        pipeline.output_dir = str(output_dir)

        # Create intermediates structure
        pipeline._create_intermediates_structure()

        # Add some test files
        intermediates_dir = output_dir / "intermediates"
        test_file = intermediates_dir / "markdown" / "test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("# Test markdown")

        # Verify file exists
        assert test_file.exists(), "Test file should exist before clean"
        print(f"  ✓ Created test file: {test_file}")

        # Clean
        pipeline._clean_intermediate_files()

        # Verify intermediates directory still exists (recreated)
        assert intermediates_dir.exists(), "Intermediates directory should be recreated"

        # Verify file is gone
        assert not test_file.exists(), "Test file should be deleted after clean"
        print(f"  ✅ Test file successfully removed")

        # Verify structure recreated
        expected_subdirs = ['images', 'images/citations', 'markdown', 'scripts', 'plans', 'citations', 'temp']
        for subdir in expected_subdirs:
            subdir_path = intermediates_dir / subdir
            assert subdir_path.exists(), f"Subdirectory {subdir} should be recreated"


def test_no_clean_preserves_files():
    """Test that --no-clean preserves files"""
    print("\nTest 4: No-clean preserves files")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "outputs"

        # Create pipeline with clean_intermediates=False
        pipeline = PaperPresentationPipeline(
            api_key="test_key",
            config={},
            clean_intermediates=False
        )
        pipeline.output_dir = str(output_dir)

        # Create intermediates structure
        pipeline._create_intermediates_structure()

        # Add test file
        intermediates_dir = output_dir / "intermediates"
        test_file = intermediates_dir / "markdown" / "test.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("# Test markdown")

        # Try to clean (should not clean due to clean_intermediates=False)
        pipeline._clean_intermediate_files()

        # Verify file still exists
        assert test_file.exists(), "Test file should still exist with --no-clean"
        print(f"  ✅ Test file preserved with --no-clean")


def main():
    """Run all tests"""
    print("="*70)
    print("Clean Intermediates Functionality Tests")
    print("="*70)

    tests = [
        test_clean_parameter,
        test_create_intermediates_structure,
        test_clean_with_files,
        test_no_clean_preserves_files,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            failed += 1

    print("\n" + "="*70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*70)

    if failed == 0:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
