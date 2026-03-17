#!/usr/bin/env python3
"""
Narrative Planner

Extracts a compelling research narrative from paper analysis.
"""

import logging
import json
import re
from typing import Any, Dict
import anthropic

from src.planning.models import PresentationNarrative

logger = logging.getLogger(__name__)


class NarrativePlanner:
    """
    Extracts research narrative from paper analysis

    The narrative follows a storytelling structure:
    Hook → Problem → Limitations → Key Idea → Method → Evidence → Implications
    """

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        self.api_key = api_key
        self.model = model
        self.call_count = 0
        self.total_tokens = 0
        self.total_cost = 0.0

        self.cost_per_1k = {
            "claude-sonnet-4-6": {"input": 0.003, "output": 0.015}
        }

    def extract_narrative(self, paper_analysis: Any) -> PresentationNarrative:
        """
        Extract research narrative from paper analysis

        Args:
            paper_analysis: PaperAnalysis or ResearchMeetingAnalysis object

        Returns:
            PresentationNarrative object with hook, problem, key idea, etc.
        """
        logger.info("Extracting research narrative from paper analysis")

        # Convert analysis to dict
        analysis_dict = self._analysis_to_dict(paper_analysis)

        # Generate prompt
        prompt = self._generate_narrative_prompt(analysis_dict)

        # Call LLM
        narrative = self._call_llm(prompt)

        logger.info(f"Narrative extraction completed: {narrative.key_idea[:50]}...")
        return narrative

    def _analysis_to_dict(self, analysis: Any) -> Dict:
        """Convert PaperAnalysis to dictionary"""
        if hasattr(analysis, 'to_dict'):
            return analysis.to_dict()
        elif hasattr(analysis, '__dict__'):
            # Convert dataclass to dict
            result = {}
            for key, value in analysis.__dict__.items():
                if isinstance(value, list):
                    result[key] = value
                elif isinstance(value, dict):
                    result[key] = value
                else:
                    result[key] = str(value) if value else ""
            return result
        else:
            # Fallback to string representation
            return {"raw_text": str(analysis)}

    def _generate_narrative_prompt(self, analysis_dict: Dict) -> str:
        """Generate narrative planning prompt"""
        from src.prompts.narrative_planning_prompt import NARRATIVE_PLANNING_PROMPT

        # Replace placeholder with analysis
        prompt = NARRATIVE_PLANNING_PROMPT.replace(
            "{{PAPER_ANALYSIS_PLACEHOLDER}}",
            json.dumps(analysis_dict, indent=2, ensure_ascii=False)
        )

        return prompt

    def _call_llm(self, prompt: str) -> PresentationNarrative:
        """Call LLM to extract narrative"""
        logger.info("Calling LLM for narrative extraction")

        client = anthropic.Anthropic(api_key=self.api_key)

        response = client.messages.create(
            model=self.model,
            max_tokens=1024,  # Narrative is short
            temperature=0,  # Deterministic
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
        self.total_cost += (
            usage.input_tokens / 1000 * self.cost_per_1k[self.model]["input"] +
            usage.output_tokens / 1000 * self.cost_per_1k[self.model]["output"]
        )

        # Parse response
        # Find first block with text attribute
        content = None
        for block in response.content:
            if hasattr(block, 'text') and block.text:
                content = block.text
                break
        if content is None:
            raise ValueError("No text block found in response")
        narrative = self._parse_response(content)

        logger.info(f"✓ Narrative extracted (cost: ${self.total_cost:.4f})")
        return narrative

    def _parse_response(self, content: str) -> PresentationNarrative:
        """
        Parse LLM response into PresentationNarrative

        Strategy:
        1. Try strict JSON parsing
        2. Try JSON extraction from markdown
        3. Fallback to default
        """
        logger.info("Parsing narrative response")

        # ------------------------------------------------
        # 1. Try strict JSON parsing
        # ------------------------------------------------
        try:
            data = json.loads(content)
            logger.info("✓ Parsed as strict JSON")
            return self._build_narrative_from_json(data)
        except json.JSONDecodeError as e:
            logger.warning(f"Strict JSON parse failed: {e}")

        # ------------------------------------------------
        # 2. Try extracting JSON from markdown
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
                logger.info("✓ Extracted JSON from response")
                return self._build_narrative_from_json(data)

        except Exception as e:
            logger.warning(f"JSON extraction failed: {e}")

        # ------------------------------------------------
        # 3. Safe fallback
        # ------------------------------------------------
        logger.error("Failed to parse narrative, returning default")
        return PresentationNarrative()

    def _build_narrative_from_json(self, data: Dict) -> PresentationNarrative:
        """Build PresentationNarrative from JSON data"""
        return PresentationNarrative(
            hook=data.get("hook", ""),
            problem=data.get("problem", ""),
            limitations_of_prior_work=data.get("limitations_of_prior_work", ""),
            key_idea=data.get("key_idea", ""),
            method=data.get("method", ""),
            evidence=data.get("evidence", ""),
            implications=data.get("implications", "")
        )

    def get_stats(self) -> Dict:
        """Get usage statistics"""
        return {
            'call_count': self.call_count,
            'total_tokens': self.total_tokens,
            'total_cost': self.total_cost
        }


if __name__ == "__main__":
    # Test
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    from src.utils import load_config, get_api_key
    from src.parser.pdf_parser import PDFParser
    from src.analysis.ai_analyzer_research_meeting import ResearchMeetingAnalyzer

    # Load config
    config = load_config()
    api_key = get_api_key(config)

    # Parse PDF
    pdf_path = "papers/Human-In-the-Loop.pdf"
    parser = PDFParser(pdf_path)
    text = parser.extract_text()

    # Analyze
    analyzer = ResearchMeetingAnalyzer(api_key=api_key, model=config['ai']['model'])
    analysis = analyzer.analyze_paper_for_meeting(text)

    # Extract narrative
    planner = NarrativePlanner(api_key=api_key, model=config['ai']['model'])
    narrative = planner.extract_narrative(analysis)

    # Display
    print("\n" + "=" * 70)
    print("EXTRACTED NARRATIVE")
    print("=" * 70)
    print(f"\nHook:\n  {narrative.hook}")
    print(f"\nProblem:\n  {narrative.problem}")
    print(f"\nLimitations of Prior Work:\n  {narrative.limitations_of_prior_work}")
    print(f"\nKey Idea:\n  {narrative.key_idea}")
    print(f"\nMethod:\n  {narrative.method}")
    print(f"\nEvidence:\n  {narrative.evidence}")
    print(f"\nImplications:\n  {narrative.implications}")
    print("\n" + "=" * 70)
