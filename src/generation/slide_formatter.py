#!/usr/bin/env python3
"""
Slide Formatter

Enforces design rules for research presentations:
- Max 5 bullets per slide
- Max 12 words per bullet
- Bold all numbers (**X%**)
- Mark key results with 🔥
"""

import re
import logging
from typing import List, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class FormattingStats:
    """Statistics about formatting changes"""
    original_bullets: int = 0
    formatted_bullets: int = 0
    bullets_removed: int = 0
    words_truncated: int = 0
    numbers_bolded: int = 0
    results_marked: int = 0


class SlideFormatter:
    """
    Formats slide content according to research presentation best practices
    """

    # Design rules
    MAX_BULLETS_PER_SLIDE = 5
    MAX_WORDS_PER_BULLET = 12

    # Keywords that indicate key results
    KEY_RESULT_KEYWORDS = [
        'achieved', 'improved', 'outperformed', 'demonstrated',
        'showed', 'reached', 'attained', 'scored', 'obtained',
        'increase', 'decrease', 'reduction', 'improvement',
        'approval', 'merge', 'success', 'accuracy', 'precision',
        'recall', 'f1', 'rate', 'score'
    ]

    def __init__(self, strict: bool = True):
        """
        Initialize formatter

        Args:
            strict: If True, enforce rules strictly. If False, log warnings but don't modify.
        """
        self.strict = strict
        self.stats = FormattingStats()

    def format_bullets(self, bullets: List[str]) -> Tuple[List[str], FormattingStats]:
        """
        Format bullet points according to design rules

        Args:
            bullets: List of bullet point strings

        Returns:
            Tuple of (formatted_bullets, stats)
        """
        self.stats = FormattingStats(original_bullets=len(bullets))

        # Step 1: limit bullets to max 5
        if len(bullets) > self.MAX_BULLETS_PER_SLIDE:
            logger.warning(f"Too many bullets ({len(bullets)}), limiting to {self.MAX_BULLETS_PER_SLIDE}")
            self.stats.bullets_removed = len(bullets) - self.MAX_BULLETS_PER_SLIDE
            if self.strict:
                bullets = bullets[:self.MAX_BULLETS_PER_SLIDE]

        # Step 2: Format each bullet
        formatted = []
        for bullet in bullets:
            formatted_bullet = self._format_bullet(bullet)
            formatted.append(formatted_bullet)

        self.stats.formatted_bullets = len(formatted)
        return formatted, self.stats

    def _format_bullet(self, bullet: str) -> str:
        """
        Format a single bullet point

        Steps:
        1. Limit to max words
        2. Bold numbers
        3. Add 🔥 for key results
        """
        # Clean up
        bullet = bullet.strip()
        if bullet.startswith('- ') or bullet.startswith('• '):
            bullet = bullet[2:]

        # Step 1: Limit words
        words = bullet.split()
        if len(words) > self.MAX_WORDS_PER_BULLET:
            logger.warning(f"Bullet too long ({len(words)} words): {bullet[:50]}...")
            if self.strict:
                bullet = ' '.join(words[:self.MAX_WORDS_PER_BULLET])
                self.stats.words_truncated += 1

        # Step 2: Bold numbers
        bullet = self._bold_numbers(bullet)

        # Step 3: Mark key results
        bullet = self._mark_key_result(bullet)

        return bullet

    def _bold_numbers(self, text: str) -> str:
        """
        Bold all numbers in text

        Examples:
            "82% approval" → "**82%** approval"
            "achieved 59%" → "achieved **59%**"
        """
        # Pattern to find numbers (with optional decimals and %)
        # Match: 82, 82.5, 82%, 82.5%
        pattern = r'(\d+(?:\.\d+)?)\s*(%)?'

        def replace_number(match):
            number = match.group(1)
            percent = match.group(2) or ''
            self.stats.numbers_bolded += 1
            return f'**{number}{percent}**'

        # Bold numbers that aren't already bolded
        # Skip if already in **X** format
        result = re.sub(r'(?<!\*)' + pattern + r'(?!.*\*)', replace_number, text)
        return result

    def _mark_key_result(self, text: str) -> str:
        """
        Add 🔥 emoji if this is a key result

        Key result indicators:
        - Contains key result keywords
        - Has numeric results
        - Shows improvement/achievement
        """
        text_lower = text.lower()

        # Check if already has 🔥
        if '🔥' in text:
            return text

        # Check if contains key result keywords
        has_keyword = any(kw in text_lower for kw in self.KEY_RESULT_KEYWORDS)

        # Check if contains numbers (already bolded)
        has_number = '**' in text and any(c.isdigit() for c in text)

        # If both conditions, mark as key result
        if has_keyword and has_number:
            self.stats.results_marked += 1
            return f"🔥 {text}"

        return text

    def format_slide_content(self, slide_content: dict) -> dict:
        """
        Format a complete slide content dictionary

        Args:
            slide_content: Dict with 'title', 'bullets', etc.

        Returns:
            Formatted slide content dict
        """
        if 'bullets' not in slide_content:
            return slide_content

        formatted_bullets, stats = self.format_bullets(slide_content['bullets'])

        return {
            **slide_content,
            'bullets': formatted_bullets,
            'formatting_stats': stats
        }

    def validate_bullets(self, bullets: List[str]) -> List[str]:
        """
        Validate bullets and return list of issues

        Returns:
            List of validation issue strings
        """
        issues = []

        # Check bullet count
        if len(bullets) > self.MAX_BULLETS_PER_SLIDE:
            issues.append(f"Too many bullets: {len(bullets)} > {self.MAX_BULLETS_PER_SLIDE}")

        # Check each bullet
        for i, bullet in enumerate(bullets, 1):
            word_count = len(bullet.split())
            if word_count > self.MAX_WORDS_PER_BULLET:
                issues.append(f"Bullet {i} too long: {word_count} words > {self.MAX_WORDS_PER_BULLET}")

        return issues

    def get_stats_summary(self) -> str:
        """Get human-readable stats summary"""
        return f"""
Formatting Statistics:
  Original bullets: {self.stats.original_bullets}
  Formatted bullets: {self.stats.formatted_bullets}
  Bullets removed: {self.stats.bullets_removed}
  Words truncated: {self.stats.words_truncated}
  Numbers bolded: {self.stats.numbers_bolded}
  Results marked: {self.stats.results_marked}
""".strip()


# Convenience functions
def format_bullet(bullet: str) -> str:
    """Format a single bullet (convenience function)"""
    formatter = SlideFormatter(strict=True)
    formatted, _ = formatter.format_bullets([bullet])
    return formatted[0]


def format_slide(bullets: List[str]) -> List[str]:
    """Format a list of bullets (convenience function)"""
    formatter = SlideFormatter(strict=True)
    formatted, _ = formatter.format_bullets(bullets)
    return formatted


# Example usage and testing
if __name__ == "__main__":
    print("=" * 70)
    print("SLIDE FORMATTER - EXAMPLE USAGE")
    print("=" * 70)

    formatter = SlideFormatter(strict=True)

    # Example 1: Too many bullets
    print("\n📝 Example 1: Too many bullets")
    print("-" * 70)

    bullets_long = [
        "First point about the problem",
        "Second point about the approach",
        "Third point about the method",
        "Fourth point about results",
        "Fifth point about implications",
        "Sixth point (should be removed)",
        "Seventh point (should be removed)"
    ]

    print(f"Original ({len(bullets_long)} bullets):")
    for i, b in enumerate(bullets_long, 1):
        print(f"  {i}. {b}")

    formatted, stats = formatter.format_bullets(bullets_long)

    print(f"\nFormatted ({len(formatted)} bullets):")
    for i, b in enumerate(formatted, 1):
        print(f"  {i}. {b}")

    print(f"\nStats: {stats.bullets_removed} bullets removed")

    # Example 2: Numbers and key results
    print("\n\n📝 Example 2: Bold numbers and mark key results")
    print("-" * 70)

    bullets_numbers = [
        "82% plan approval rate achieved",
        "59% merge rate shows strong trust",
        "Deployed to 2600 practitioners",
        "Outperformed baseline by 27%",
        "This is a regular bullet without numbers"
    ]

    print("Original:")
    for b in bullets_numbers:
        print(f"  • {b}")

    formatted, stats = formatter.format_bullets(bullets_numbers)

    print("\nFormatted:")
    for b in formatted:
        print(f"  • {b}")

    print(f"\nStats: {stats.numbers_bolded} numbers bolded, {stats.results_marked} results marked")

    # Example 3: Long bullets
    print("\n\n📝 Example 3: Truncate long bullets")
    print("-" * 70)

    bullets_verbose = [
        "This is an extremely long bullet point that contains way too many words and should definitely be truncated to meet the maximum word limit",
        "Another verbose bullet with unnecessary words that goes on and on without getting to the point quickly enough",
        "Short bullet"
    ]

    print("Original:")
    for b in bullets_verbose:
        words = len(b.split())
        print(f"  • [{words} words] {b}")

    formatted, stats = formatter.format_bullets(bullets_verbose)

    print("\nFormatted:")
    for b in formatted:
        words = len(b.split())
        print(f"  • [{words} words] {b}")

    print(f"\nStats: {stats.words_truncated} bullets truncated")

    # Example 4: Complete slide formatting
    print("\n\n📝 Example 4: Complete slide")
    print("-" * 70)

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

    print("Original slide:")
    print(f"  Title: {slide['title']}")
    print(f"  Bullets: {len(slide['bullets'])}")
    for b in slide['bullets']:
        print(f"    • {b}")

    formatted_slide = formatter.format_slide_content(slide)

    print("\nFormatted slide:")
    print(f"  Title: {formatted_slide['title']}")
    print(f"  Bullets: {len(formatted_slide['bullets'])}")
    for b in formatted_slide['bullets']:
        print(f"    • {b}")

    stats = formatted_slide['formatting_stats']
    print(f"\nStats:")
    print(f"  Bullets removed: {stats.bullets_removed}")
    print(f"  Numbers bolded: {stats.numbers_bolded}")
    print(f"  Results marked: {stats.results_marked}")

    print("\n" + "=" * 70)
    print("✅ FORMATTING COMPLETE")
    print("=" * 70)
