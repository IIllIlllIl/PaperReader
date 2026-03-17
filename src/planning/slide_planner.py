"""
Slide Planner

Converts PaperAnalysis into a structured SlidePlan using LLM.
"""

import json
import logging
import anthropic
from typing import Optional, Dict
from dataclasses import asdict

from src.planning.models import SlidePlan, SlideTopic
from src.prompts.slide_planning_prompt import SLIDE_PLANNING_PROMPT

logger = logging.getLogger(__name__)


class SlidePlanner:
    """
    Plans slide structure from PaperAnalysis

    This is the PLANNING layer - it decides WHAT should be covered,
    not the full content.
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

    def plan_slides(self, paper_analysis) -> SlidePlan:
        """
        Generate slide plan from PaperAnalysis

        Args:
            paper_analysis: PaperAnalysis or ResearchMeetingAnalysis object

        Returns:
            SlidePlan with 13 slides (including Research Questions and Future Work)
        """
        logger.info("Planning slides from paper analysis")

        # Convert analysis to dict for prompt
        analysis_dict = self._analysis_to_dict(paper_analysis)


        # Call LLM to generate slide plan
        client = anthropic.Anthropic(api_key=self.api_key)

        response = client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=0,  # Deterministic planning
            messages=[
                {
                    "role": "user",
                    "content": SLIDE_PLANNING_PROMPT.replace(
                        "{{PAPER_ANALYSIS_PLACEHOLDER}}",
                        json.dumps(analysis_dict, indent=2)
                    )
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
        slide_plan = self._parse_slide_plan(content)

        # TASK 3: Auto-inject Research Questions if not present
        slide_plan = self._ensure_research_questions(slide_plan, paper_analysis)

        # TASK 3: Auto-inject Future Work if not present
        slide_plan = self._ensure_future_work(slide_plan, paper_analysis)

        logger.info(f"Generated slide plan with {slide_plan.total_slides} slides")

        return slide_plan

    def _ensure_research_questions(self, slide_plan: SlidePlan, analysis) -> SlidePlan:
        """
        Ensure Research Questions slide is present (TASK 3)

        Auto-generates research questions based on problem statement if not present in the plan.

        """
        # Check if Research Questions slide exists
        has_rq = any('research question' in slide.title.lower() for slide in slide_plan.slides)

        if not has_rq:
            # Generate research questions based on analysis
            rq_slide = self._generate_research_questions(analysis)

            # Insert after Motivation slide
            insert_index = 0
            for i, slide in enumerate(slide_plan.slides):
                if 'motivation' in slide.title.lower():
                    insert_index = i + 1
                    break

            slide_plan.slides.insert(insert_index, rq_slide)
            slide_plan.total_slides = len(slide_plan.slides)

            logger.info("Auto-generated Research Questions slide")

        return slide_plan

    def _generate_research_questions(self, analysis) -> SlideTopic:
        """
        Generate Research Questions slide based on paper analysis (TASK 3)

        Args:
            analysis: Paper analysis object

        Returns:
            SlideTopic with research questions
        """
        # Extract problem-related information
        problem_context = []

        if hasattr(analysis, 'research_problem_keywords'):
            problem_context = analysis.research_problem_keywords[:3]
        elif hasattr(analysis, 'problem'):
            problem_context = [analysis.problem]

        elif hasattr(analysis, 'key_insights'):
            # Derive from key insights
            problem_context = analysis.key_insights[:3]

        # Generate standard research questions
        key_points = [
            "RQ1: What problem does this work attempt to solve?",
            "RQ2: What hypothesis does the method test?",
            "RQ3: How does the method improve over prior work?"
        ]

        # Customize based on problem context if available
        if problem_context:
            key_points[0] = f"RQ1: {problem_context[0] if len(problem_context[0]) < 60 else key_points[0]}"

            if len(problem_context) > 1:
                key_points[1] = f"RQ2: How does the proposed approach address {problem_context[1][:50]}...?"

        return SlideTopic(
            title="Research Questions",
            key_points=key_points,
            slide_type="content",
            notes="Main research questions this paper addresses"
        )

    def _ensure_future_work(self, slide_plan: SlidePlan, analysis) -> SlidePlan:
        """
        Ensure Future Work slide is present (TASK 3)

        Auto-generates future work directions if not present in the plan.
        """
        # Check if Future Work slide exists
        has_future = any('future' in slide.title.lower() for slide in slide_plan.slides)

        if not has_future:
            # Generate future work based on analysis
            future_slide = self._generate_future_work(analysis)

            # Insert before Discussion/Q&A slide
            insert_index = len(slide_plan.slides) - 1
            for i, slide in enumerate(slide_plan.slides):
                if 'discussion' in slide.title.lower() or 'q&a' in slide.title.lower():
                    insert_index = i
                    break

            slide_plan.slides.insert(insert_index, future_slide)
            slide_plan.total_slides = len(slide_plan.slides)

            logger.info("Auto-generated Future Work slide")

        return slide_plan

    def _generate_future_work(self, analysis) -> SlideTopic:
        """
        Generate Future Work slide based on paper analysis (TASK 3)

        Args:
            analysis: Paper analysis object

        Returns:
            SlideTopic with future work directions
        """
        key_points = [
            "Extend to more complex tasks",
            "Improve code generation quality",
            "Reduce input effort required",
            "Explore other domains",
            "Long-term impact studies"
        ]

        # Customize based on limitations if available
        if hasattr(analysis, 'limitations_keywords'):
            limitations = analysis.limitations_keywords[:2]
            if limitations:
                # Derive future work from limitations
                key_points[0] = f"Address: {limitations[0]}"
                if len(limitations) > 1:
                    key_points[1] = f"Address: {limitations[1]}"

        return SlideTopic(
            title="Future Work",
            key_points=key_points,
            slide_type="content",
            notes="Future research directions and opportunities"
        )

    def _analysis_to_dict(self, analysis) -> dict:
        """Convert PaperAnalysis to dictionary for prompt"""

        # Handle both dataclass and dict
        if hasattr(analysis, '__dataclass_fields__'):
            # It's a dataclass
            return asdict(analysis)
        elif isinstance(analysis, dict):
            return analysis
        else:
            # Try to convert to dict
            return {
                key: getattr(analysis, key)
                for key in dir(analysis)
                if not key.startswith('_')
            }

    def _parse_slide_plan(self, content: str) -> SlidePlan:
        """
        Parse LLM response into SlidePlan

        Handles:
        1. Strict JSON
        2. JSON in code blocks
        3. Fallback to default structure
        """
        logger.info("Parsing slide plan from LLM response")

        # Try strict JSON parse
        try:
            data = json.loads(content)
            logger.info("✓ Parsed as strict JSON")
            return self._build_slide_plan(data)
        except json.JSONDecodeError as e:
            logger.warning(f"Strict JSON parse failed: {e}")

        # Try extracting JSON from markdown code blocks
        try:
            import re
            json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                data = json.loads(json_str)
                logger.info("✓ Extracted JSON from code block")
                return self._build_slide_plan(data)
        except Exception as e:
            logger.warning(f"JSON extraction failed: {e}")

        # Fallback: create default plan
        logger.warning("Using default slide plan")
        return self._create_default_plan()

    def _build_slide_plan(self, data: dict) -> SlidePlan:
        """Build SlidePlan from parsed JSON"""

        slides = []
        slides_data = data.get("slides", [])

        for slide_data in slides_data:
            slide = SlideTopic(
                title=slide_data.get("title", "Untitled"),
                key_points=slide_data.get("key_points", []),
                slide_type=slide_data.get("slide_type", "content"),
                notes=slide_data.get("notes", "")
            )
            slides.append(slide)

        return SlidePlan(slides=slides)

    def _create_default_plan(self) -> SlidePlan:
        """
        Create default research meeting slide plan (TASK 3)

        Enhanced plan includes:
        - Research Questions (new)
        - Future Work (new)
        - Better academic structure

        Returns:
            SlidePlan with 13 slides for PhD research meeting
        """

        default_slides = [
            SlideTopic(
                title="Title",
                key_points=["Paper title", "Authors", "Year", "Research context"],
                slide_type="title",
                notes="Establish paper identity and research context"
            ),
            SlideTopic(
                title="Motivation",
                key_points=["Why this problem matters", "Real-world impact", "Research gap", "Practical motivation"],
                slide_type="content",
                notes="Explain WHY this research is important"
            ),
            SlideTopic(
                title="Research Questions",
                key_points=[
                    "RQ1: What problem does this work attempt to solve?",
                    "RQ2: What hypothesis does the method test?",
                    "RQ3: How does the method improve over prior work?"
                ],
                slide_type="content",
                notes="Main research questions this paper addresses"
            ),
            SlideTopic(
                title="Problem Definition",
                key_points=["Specific problem", "Challenges", "Scope", "Constraints"],
                slide_type="content",
                notes="Define the specific problem this paper addresses"
            ),
            SlideTopic(
                title="Related Work",
                key_points=["Previous approaches", "Limitations", "Our improvement", "Gap analysis"],
                slide_type="content",
                notes="Compare approaches and highlight limitations of previous work"
            ),
            SlideTopic(
                title="Core Idea",
                key_points=["Main contribution in one sentence", "Key innovation", "Novel approach"],
                slide_type="content",
                notes="Main contribution in one clear concept"
            ),
            SlideTopic(
                title="Method Overview",
                key_points=["High-level approach", "Key components", "Novel techniques", "Architecture"],
                slide_type="diagram",
                notes="High-level architecture and component overview"
            ),
            SlideTopic(
                title="Method Details",
                key_points=["Technical details", "Implementation", "Algorithms", "Design decisions"],
                slide_type="content",
                notes="Technical implementation and design choices"
            ),
            SlideTopic(
                title="Experiment Setup",
                key_points=["Datasets", "Baselines", "Metrics", "Environment", "Evaluation protocol"],
                slide_type="table",
                notes="Evaluation methodology and experimental configuration"
            ),
            SlideTopic(
                title="Results",
                key_points=["Key findings", "Interpretations", "Comparisons", "Statistical significance"],
                slide_type="table",
                notes="Main experimental results with baseline comparison"
            ),
            SlideTopic(
                title="Limitations",
                key_points=["Weaknesses", "Constraints", "Gaps", "Threats to validity"],
                slide_type="content",
                notes="Honest assessment of weaknesses and challenges"
            ),
            SlideTopic(
                title="Future Work",
                key_points=[
                    "Immediate next steps",
                    "Long-term research directions",
                    "Open problems",
                    "Potential extensions"
                ],
                slide_type="content",
                notes="Future research directions and opportunities"
            ),
            SlideTopic(
                title="Discussion & Takeaways",
                key_points=["Key insights", "Broader impact", "Lessons learned", "Questions for discussion"],
                slide_type="discussion",
                notes="Key insights and questions for group discussion"
            )
        ]

        return SlidePlan(slides=default_slides)

    def get_stats(self) -> dict:
        """Get usage statistics"""
        return {
            'call_count': self.call_count,
            'total_tokens': self.total_tokens,
            'total_cost': self.total_cost
        }
