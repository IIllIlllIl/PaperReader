#!/usr/bin/env python3
"""
Research Group Meeting AI Analyzer for PaperReader

Optimized for academic research group presentations (组会专用)

Key improvements:
- Motivation slide (why this problem matters)
- Related work context (comparison with previous work)
- Core idea (main contribution in one sentence)
- Discussion questions (for audience engagement)
- Critical analysis (honest limitations)
"""

import logging
import json
import re
from typing import Optional, Dict, List
from dataclasses import dataclass, field
import anthropic

logger = logging.getLogger(__name__)


@dataclass
class ResearchMeetingAnalysis:
    """Analysis optimized for research group meeting presentation"""

    # Basic information
    title: str
    authors: str
    year: str

    # Motivation (WHY this problem matters)
    motivation: List[str] = field(default_factory=list)

    # Problem Definition
    problem_definition: List[str] = field(default_factory=list)

    # Related Work (comparison + limitations)
    related_work: List[str] = field(default_factory=list)

    # Core Idea (main contribution in ONE sentence)
    core_idea: str = ""

    # Method Overview
    method_overview: List[str] = field(default_factory=list)

    # Method Details
    method_details: List[str] = field(default_factory=list)

    # Experiment Setup
    experiment_setup: Dict[str, str] = field(default_factory=dict)

    # Main Results (with bold numbers and 🔥 markers)
    main_results: List[str] = field(default_factory=list)

    # Limitations (critical and honest)
    limitations: List[str] = field(default_factory=list)

    # Key Takeaways
    key_takeaways: List[str] = field(default_factory=list)

    # Discussion Questions (for audience)
    discussion_questions: List[str] = field(default_factory=list)


class ResearchMeetingAnalyzer:
    """AI analyzer optimized for research group meeting presentations"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        self.api_key = api_key
        self.model = model
        self.call_count = 0
        self.total_tokens = 0
        self.total_cost = 0.0

        self.cost_per_1k = {
            "claude-sonnet-4-6": {"input": 0.003, "output": 0.015}
        }

    def analyze_paper_for_meeting(self, paper_text: str, metadata: Optional[Dict] = None) -> ResearchMeetingAnalysis:
        """Analyze paper for research group meeting presentation"""
        logger.info("Starting research meeting paper analysis")

        # Truncate if too long
        max_chars = 150000

        # Build prompt
        prompt = self._generate_research_meeting_prompt(paper_text, max_chars)

        # Call Claude API
        client = anthropic.Anthropic(api_key=self.api_key)

        response = client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=0,  # Stable JSON output
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Track usage
        usage = response.usage
        self.call_count += 1
        self.total_tokens += usage.input_tokens + usage.output_tokens
        self.total_cost += (usage.input_tokens / 1000 * self.cost_per_1k[self.model]["input"] +
                             usage.output_tokens / 1000 * self.cost_per_1k[self.model]["output"])

        # Parse response
        # Find first block with text attribute
        content = None
        for block in response.content:
            if hasattr(block, 'text') and block.text:
                content = block.text
                break
        if content is None:
            raise ValueError("No text block found in response")
        analysis = self._parse_research_meeting_response(content, metadata)

        logger.info(f"Research meeting analysis completed: {len(content)} characters")
        return analysis

    def _generate_research_meeting_prompt(self, paper_text: str, max_chars: int) -> str:
        """Generate research meeting optimized prompt"""

        from src.prompts.research_meeting_prompt import RESEARCH_MEETING_PROMPT

        return RESEARCH_MEETING_PROMPT.format(paper_text=paper_text[:max_chars])

    def _parse_research_meeting_response(self, content: str, metadata: Optional[Dict] = None) -> ResearchMeetingAnalysis:
        """
        Parse AI response into ResearchMeetingAnalysis.

        Strategy:
        1. Try strict JSON parsing
        2. Try JSON extraction from text
        3. Fallback to Markdown parsing
        4. Return safe default structure
        """
        logger.info("Parsing research meeting AI response")

        # ------------------------------------------------
        # 1. Try strict JSON parsing
        # ------------------------------------------------
        try:
            data = json.loads(content)
            logger.info("✓ AI response parsed as strict JSON")
            return self._build_analysis_from_json(data, metadata)
        except json.JSONDecodeError as e:
            logger.warning(f"Strict JSON parse failed: {e}")

        # ------------------------------------------------
        # 2. Try extracting JSON block from markdown
        # ------------------------------------------------
        try:
            # Try to find JSON in code blocks
            json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', content, re.DOTALL)
            if not json_match:
                # Try to find raw JSON object
                json_match = re.search(r'\{.*\}', content, re.DOTALL)

            if json_match:
                json_str = json_match.group(1) if '```' in content else json_match.group(0)
                data = json.loads(json_str)
                logger.info("✓ Extracted JSON block from response")
                return self._build_analysis_from_json(data, metadata)

        except Exception as e:
            logger.warning(f"JSON extraction failed: {e}")

        # ------------------------------------------------
        # 3. Markdown fallback
        # ------------------------------------------------
        logger.warning("Falling back to Markdown parsing")
        try:
            analysis = self._parse_markdown_fallback(content, metadata)
            logger.info("✓ Markdown parsing succeeded")
            return analysis
        except Exception as e:
            logger.error(f"Markdown parsing failed: {e}")

        # ------------------------------------------------
        # 4. Safe fallback
        # ------------------------------------------------
        logger.error("Failed to parse AI response, returning minimal structure")
        return self._create_default_analysis(metadata)

    def _build_analysis_from_json(self, data: Dict, metadata: Optional[Dict] = None) -> ResearchMeetingAnalysis:
        """Build ResearchMeetingAnalysis from JSON data"""
        logger.info("Building ResearchMeetingAnalysis from JSON")

        # Ensure all numbers are bolded in main_results
        main_results = data.get("main_results", [])
        main_results = [self._ensure_bold_numbers(r) for r in main_results]

        return ResearchMeetingAnalysis(
            title=data.get("title", metadata.get("title", "Unknown") if metadata else "Unknown"),
            authors=data.get("authors", metadata.get("authors", "Unknown") if metadata else "Unknown"),
            year=data.get("year", metadata.get("year", "2024") if metadata else "2024"),

            motivation=data.get("motivation", [])[:4],  # Max 4 points
            problem_definition=data.get("problem_definition", [])[:3],  # Max 3 points
            related_work=data.get("related_work", [])[:4],  # Max 4 points
            core_idea=data.get("core_idea", ""),

            method_overview=data.get("method_overview", [])[:4],  # Max 4 points
            method_details=data.get("method_details", [])[:4],  # Max 4 points

            experiment_setup=data.get("experiment_setup", {}),

            main_results=main_results[:5],  # Max 5 results
            limitations=data.get("limitations", [])[:4],  # Max 4 limitations
            key_takeaways=data.get("key_takeaways", [])[:3],  # Max 3 takeaways
            discussion_questions=data.get("discussion_questions", [])[:3]  # Max 3 questions
        )

    def _parse_markdown_fallback(self, content: str, metadata: Optional[Dict] = None) -> ResearchMeetingAnalysis:
        """Fallback parser for Markdown format"""
        logger.warning("Using Markdown fallback parser")

        def extract_section(text: str, *keywords) -> List[str]:
            """Extract section by multiple possible keywords"""
            for keyword in keywords:
                pattern = rf"(?:^|\n)[#]*\s*{keyword}.*?\n(.*?)(?=\n[#]|\Z)"
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    section_text = match.group(1).strip()
                    bullets = re.findall(r"[-*]\s+(.*)", section_text)
                    if bullets:
                        return [b.strip() for b in bullets]
            return []

        def extract_bullets(text: str, *keywords) -> List[str]:
            """Extract bullet points from section"""
            for keyword in keywords:
                section = extract_section(text, keyword)
                if section:
                    return section
            return []

        # Extract core idea (usually in abstract or introduction)
        core_idea = ""
        abstract_match = re.search(r"(?:abstract|summary).*?\n(.{50,300})", content, re.IGNORECASE | re.DOTALL)
        if abstract_match:
            core_idea = abstract_match.group(1).strip()

        return ResearchMeetingAnalysis(
            title=metadata.get("title", "Unknown") if metadata else "Unknown",
            authors=metadata.get("authors", "Unknown") if metadata else "Unknown",
            year=metadata.get("year", "2024") if metadata else "2024",

            motivation=extract_bullets(content, "motivation", "why", "background"),
            problem_definition=extract_bullets(content, "problem", "challenge"),
            related_work=extract_bullets(content, "related", "previous", "baseline"),
            core_idea=core_idea,

            method_overview=extract_bullets(content, "method", "approach", "framework"),
            method_details=extract_bullets(content, "technical", "implementation", "detail"),

            experiment_setup={},

            main_results=[self._ensure_bold_numbers(r) for r in extract_bullets(content, "result", "performance", "evaluation")],
            limitations=extract_bullets(content, "limitation", "weakness", "future"),
            key_takeaways=extract_bullets(content, "conclusion", "takeaway", "summary"),
            discussion_questions=[]
        )

    def _ensure_bold_numbers(self, text: str) -> str:
        """Ensure all numbers are bolded"""
        # Bold percentages
        text = re.sub(r'\b(\d+(?:\.\d+)?)\s*%', r'**\1%**', text)
        # Bold standalone numbers (but not in brackets or already bolded)
        text = re.sub(r'(?<!\*)\b(\d+(?:\.\d+)?)\b(?!.*\*)', r'**\1**', text)
        return text

    def _create_default_analysis(self, metadata: Optional[Dict] = None) -> ResearchMeetingAnalysis:
        """Create default analysis structure"""
        return ResearchMeetingAnalysis(
            title=metadata.get("title", "Unknown") if metadata else "Unknown",
            authors=metadata.get("authors", "Unknown") if metadata else "Unknown",
            year=metadata.get("year", "2024") if metadata else "2024",

            motivation=[],
            problem_definition=[],
            related_work=[],
            core_idea="",

            method_overview=[],
            method_details=[],
            experiment_setup={},

            main_results=[],
            limitations=[],
            key_takeaways=[],
            discussion_questions=[]
        )

    # Backward compatibility
    def analyze_paper(self, paper_text: str, metadata: Optional[Dict] = None) -> ResearchMeetingAnalysis:
        """Alias for analyze_paper_for_meeting"""
        return self.analyze_paper_for_meeting(paper_text, metadata)

    def quick_analysis(self, paper_text: str, metadata: Optional[Dict] = None) -> ResearchMeetingAnalysis:
        """Quick analysis - same as detailed for now"""
        return self.analyze_paper_for_meeting(paper_text, metadata)

    def get_stats(self) -> Dict:
        """Get usage statistics"""
        return {
            'call_count': self.call_count,
            'total_tokens': self.total_tokens,
            'total_cost': self.total_cost
        }
