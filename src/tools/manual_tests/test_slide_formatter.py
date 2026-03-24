#!/usr/bin/env python3
"""
Test Slide Formatter

Tests the slide formatting rules:
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.generation.slide_formatter import SlideFormatter


def test_basic_formatting():
    """Test basic bullet formatting"""
    print("\n" + "=" * 70)
    print("TEST 1: Basic Formatting")
    print("=" * 70)

    formatter = SlideFormatter(strict=True)
    bullets = [
        "82% plan approval rate achieved in our deployment",
        "59% merge rate demonstrates strong developer trust",
        "Deployed to 2600 practitioners at Atlassian",
        "Outperformed SWE-agent baseline by 27% on resolution",
        "This is a fifth point about the results",
        "This sixth point should be removed due to limit"
    ]

    formatted, stats = formatter.format_bullets(bullets)

    print("\nOriginal:")
    for i, b in enumerate(bullets, 1):
        print(f"  {i}. {b}")

    print("\nFormatted:")
    for i, b in enumerate(formatted, 1):
        print(f"  {i}. {b}")

    print(f"\nStats:")
    print(f"  Original bullets: {stats.original_bullets}")
    print(f"  Formatted bullets: {stats.formatted_bullets}")
    print(f"  Bullets removed: {stats.bullets_removed}")
    print(f"  Numbers bolded: {stats.numbers_bolded}")
    print(f"  Results marked: {stats.results_marked}")

    # Assertions
    assert len(formatted) == 5, "Should limit to 5 bullets"
    assert stats.bullets_removed == 1, "Should remove 1 bullet"
    assert stats.numbers_bolded >= 4, "Should bold numbers"
    assert stats.results_marked >= 2, "Should mark key results"

    # Check formatting
    assert "🔥" in formatted[0], "First bullet should have 🔥"
    assert "**82%**" in formatted[0], "First bullet should bold numbers"

    print("\n✅ Test passed")


def test_word_limit():
    """Test word limit enforcement"""
    print("\n" + "=" * 70)
    print("TEST 2: Word Limit")
    print("=" * 70)

    formatter = SlideFormatter(strict=True)
    bullets = [
        "this is an extremely long bullet point that contains way too many words and should definitely be truncated to meet the maximum word limit",
        "short bullet"
    ]

    formatted, stats = formatter.format_bullets(bullets)

    print("\nOriginal:")
    for i, b in enumerate(bullets, 1):
        word_count = len(b.split())
        print(f"  {i}. ({word_count} words) {b}")

    print("\nFormatted:")
    for i, b in enumerate(formatted, 1):
        word_count = len(b.split())
        print(f"  {i}. ({word_count} words) {b}")

    assert len(formatted[0].split()) <= 13, "Long bullet should be truncated"
    assert stats.words_truncated >= 1, "Should track truncated words"

    print("\n✅ Test passed")


def test_number_formatting():
    """Test number bolding"""
    print("\n" + "=" * 70)
    print("TEST 3: Number Formatting")
    print("=" * 70)

    formatter = SlideFormatter(strict=True)
    bullets = [
        "Achieved 82% approval rate",
        "Score of 95.5 points",
        "improved by 27%",
        "processed 1500 samples"
        "reduced time by 50%"
    ]

    formatted, stats = formatter.format_bullets(bullets)

    print("\nOriginal → Formatted:")
    for orig, fmt in zip(bullets, formatted):
        print(f"  {orig}")
        print(f"  → {fmt}")

    # All should have bold numbers
    assert all("**" in b for b in formatted), "All bullets should have bold numbers"

    print("\n✅ Test passed")


def test_result_marking():
    """Test key result marking with 🔥"""
    print("\n" + "=" * 70)
    print("TEST 4: Result Marking")
    print("=" * 70)

    formatter = SlideFormatter(strict=True)
    bullets = [
        "achieved 82% approval rate",
        "the dataset has 1500 samples",
        "improved performance by 27%",
        "baseline approach",
        "demonstrated strong results"
    ]

    formatted, stats = formatter.format_bullets(bullets)

    print("\nOriginal → Formatted:")
    for orig, fmt in zip(bullets, formatted):
        print(f"  {orig}")
        print(f"  → {fmt}")

    # Check which bullets have 🔥
    has_fire = ["🔥" in b for b in formatted]
    num_with_fire = sum(has_fire)
    print(f"\nBullets with 🔥: {num_with_fire}/{len(formatted)}")

    # Bullets with key result keywords should have 🔥
    assert num_with_fire >= 2, "At least 2 bullets should have 🔥"

    print("\n✅ Test passed")


def test_slide_formatting():
    """Test complete slide formatting"""
    print("\n" + "=" * 70)
    print("TEST 5: Complete Slide Formatting")
    print("=" * 70)

    formatter = SlideFormatter(strict=True)
    slide = {
        'title': 'Results',
        'bullets': [
            '82% plan approval rate achieved in our deployment',
            '59% merge rate demonstrates strong developer trust',
            'Deployed to 2600 practitioners at Atlassian',
            'Outperformed SWE-agent baseline by 27% on resolution',
            'This is a fifth point about the results',
            'This sixth point should be removed due to limit'
        ]
    }

    formatted_slide = formatter.format_slide_content(slide)
    formatted = formatted_slide['bullets']
    stats = formatted_slide['formatting_stats']

    print("\nOriginal slide:")
    print(f"  Title: {slide['title']}")
    print(f"  Bullets: {len(slide['bullets'])}")
    for b in slide['bullets']:
        print(f"    • {b}")

    print("\nFormatted slide:")
    print(f"  Title: {formatted_slide['title']}")
    print(f"  Bullets: {len(formatted_slide['bullets'])}")
    for b in formatted_slide['bullets']:
        print(f"    • {b}")

    print(f"\nFormatting stats:")
    print(f"  Original bullets: {stats.original_bullets}")
    print(f"  Formatted bullets: {stats.formatted_bullets}")
    print(f"  Bullets removed: {stats.bullets_removed}")
    print(f"  Numbers bolded: {stats.numbers_bolded}")
    print(f"  Results marked: {stats.results_marked}")

    assert len(formatted_slide['bullets']) == 5, "Should limit to 5 bullets"

    print("\n✅ Test passed")


def test_validation():
    """Test validation"""
    print("\n" + "=" * 70)
    print("TEST 6: Validation")
    print("=" * 70)

    formatter = SlideFormatter(strict=True)

    # Good bullets
    good_bullets = [
        "🔥 **82%** approval rate",
        "🔥 **59%** merge rate",
        "Deployed to **2600** practitioners",
        "🔥 **27%** improvement over baseline",
        "Outperformed **SWE-agent**"
    ]

    issues = formatter.validate_bullets(good_bullets)
    print(f"\nGood bullets: {len(issues)} issues")
    assert len(issues) == 0, "Good bullets should have no issues"

    # Bad bullets (too many)
    bad_bullets = good_bullets + ["Sixth bullet", "Seventh bullet"]
    issues = formatter.validate_bullets(bad_bullets)
    print(f"\nBad bullets (7 bullets): {len(issues)} issues")
    assert len(issues) > 0, "Too many bullets should have issues"

    # Long bullets
    long_bullets = [
        "this is a very long bullet that has way too many words and exceeds the limit",
    ]
    issues = formatter.validate_bullets(long_bullets)
    print(f"\nLong bullets: {len(issues)} issues")
    assert len(issues) > 0, "Long bullets should have issues"

    print("\n✅ Test passed")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🧪 RUNNING ALL TESTS")
    print("=" * 70)

    try:
        test_basic_formatting()
        test_word_limit()
        test_number_formatting()
        test_result_marking()
        test_slide_formatting()
        test_validation()

        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
