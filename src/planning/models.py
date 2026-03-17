"""
Slide Planning Models

Data structures for the slide planning layer.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class SlideTopic:
    """
    Represents a single slide's topic and key points

    This is a planning structure - it contains WHAT should be covered,
    not the full text content.
    """
    title: str
    key_points: List[str] = field(default_factory=list)
    slide_type: str = "content"  # content, title, table, discussion, figure
    notes: str = ""  # Brief description of what this slide should accomplish


@dataclass
class PresentationNarrative:
    """
    Research narrative structure for storytelling

    This represents the STORY arc of the presentation,
    following a compelling research narrative structure.
    """
    # Hook: Captures audience attention (1-2 sentences)
    hook: str = ""

    # Problem: What problem does this research address?
    problem: str = ""

    # Limitations: What's wrong with previous approaches?
    limitations_of_prior_work: str = ""

    # Key Idea: Main contribution in ONE sentence
    key_idea: str = ""

    # Method: Brief method overview (2-3 sentences)
    method: str = ""

    # Evidence: Key results that support the idea
    evidence: str = ""

    # Implications: What does this mean for the future?
    implications: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "hook": self.hook,
            "problem": self.problem,
            "limitations_of_prior_work": self.limitations_of_prior_work,
            "key_idea": self.key_idea,
            "method": self.method,
            "evidence": self.evidence,
            "implications": self.implications
        }


@dataclass
class SlidePlan:
    """
    Complete slide plan for a presentation

    This represents the HIGH-LEVEL structure of the presentation,
    before detailed content is generated.
    """
    slides: List[SlideTopic] = field(default_factory=list)
    total_slides: int = 0
    narrative: PresentationNarrative = field(default_factory=PresentationNarrative)

    def __post_init__(self):
        self.total_slides = len(self.slides)

    def get_slide(self, index: int) -> SlideTopic:
        """Get slide by index"""
        if 0 <= index < len(self.slides):
            return self.slides[index]
        raise IndexError(f"Slide index {index} out of range")

    def get_slide_by_title(self, title: str) -> SlideTopic:
        """Get slide by title"""
        for slide in self.slides:
            if slide.title.lower() == title.lower():
                return slide
        raise ValueError(f"Slide with title '{title}' not found")

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "total_slides": self.total_slides,
            "slides": [
                {
                    "title": slide.title,
                    "key_points": slide.key_points,
                    "slide_type": slide.slide_type,
                    "notes": slide.notes
                }
                for slide in self.slides
            ]
        }
