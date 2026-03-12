"""
AI Analyzer for PaperReader

Analyzes papers using Claude AI to extract key information
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import anthropic

logger = logging.getLogger(__name__)


@dataclass
class PaperAnalysis:
    """Structured analysis of a paper"""
    title: str
    authors: List[str]
    problem: str
    motivation: str
    method: str
    innovations: List[str]
    experiments: str
    results: List[str]
    pros: List[str]
    cons: List[str]
    conclusions: str
    future_work: str


@dataclass
class PresentationContent:
    """Content for presentation slides"""
    title: str
    authors: str
    venue: str
    year: str
    motivation: List[str]
    existing_problems: List[str]
    research_problem: str
    method_overview: str
    technical_details: List[str]
    innovations: List[str]
    experimental_setup: str
    main_results: List[str]
    result_analysis: str
    discussion: str
    pros: List[str]
    cons: List[str]
    future_work: List[str]
    conclusions: str


class AIAnalyzer:
    """Analyzes academic papers using Claude AI"""

    # Prompt for quick analysis (abstract + conclusions only)
    QUICK_ANALYSIS_PROMPT = """You are an academic paper analysis expert. Analyze the following paper excerpt (abstract and conclusions) and provide a brief overview.

Paper text:
{paper_text}

Provide a brief analysis in JSON format:
{{
    "title": "Paper title if identifiable",
    "main_topic": "Main topic in 1-2 sentences",
    "key_contribution": "Primary contribution in 1-2 sentences",
    "relevance": "Why this paper is relevant/important"
}}

Keep responses concise and focused."""

    # Prompt for full analysis
    FULL_ANALYSIS_PROMPT = """You are an academic paper analysis expert. Analyze the following research paper and extract key information.

Paper text:
{paper_text}

Provide a structured analysis in JSON format:
{{
    "problem": "What is the main research problem or question? (2-3 sentences)",
    "motivation": "Why is this problem important? What gap does it address? (2-3 sentences)",
    "method": "Describe the proposed method/approach in detail (4-6 sentences covering the main approach, key techniques, and how it works)",
    "innovations": ["List 3-5 key innovations/contributions as bullet points"],
    "experiments": "Summarize the experimental setup and evaluation (2-3 sentences covering datasets, baselines, metrics)",
    "results": ["List 3-5 main results as bullet points with specific numbers if available"],
    "pros": ["List 3-5 advantages/strengths as bullet points"],
    "cons": ["List 3-5 limitations/weaknesses as bullet points"],
    "conclusions": "What are the main conclusions and implications? (2-3 sentences)",
    "future_work": "What future work is suggested or would be valuable? (2-3 sentences)"
}}

Ensure your analysis is:
1. Accurate and faithful to the paper content
2. Concise but comprehensive
3. Structured for presentation purposes
4. Critical and balanced (both pros and cons)
5. Specific with concrete details and numbers where available"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6",
                 haiku_model: str = "claude-haiku-4-5-20251001"):
        """
        Initialize AI analyzer

        Args:
            api_key: Anthropic API key
            model: Primary model for deep analysis
            haiku_model: Cheaper model for quick analysis
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.haiku_model = haiku_model
        self.call_count = 0
        self.total_tokens = 0
        self.total_cost = 0.0

        # Cost per 1K tokens (as of 2024)
        self.cost_per_1k = {
            "claude-sonnet-4-6": {"input": 0.003, "output": 0.015},
            "claude-haiku-4-5-20251001": {"input": 0.0008, "output": 0.004},
        }

    def analyze_paper(self, paper_text: str, metadata: Optional[Dict] = None) -> PaperAnalysis:
        """
        Perform full analysis of paper

        Args:
            paper_text: Full text of the paper
            metadata: Optional paper metadata

        Returns:
            PaperAnalysis object
        """
        logger.info("Starting full paper analysis")

        # Truncate text if too long (Claude has 200K context limit)
        max_chars = 150000  # Conservative limit
        if len(paper_text) > max_chars:
            logger.warning(f"Paper text too long ({len(paper_text)} chars), truncating to {max_chars}")
            paper_text = paper_text[:max_chars] + "\n\n[Text truncated due to length]"

        # Call Claude API
        response = self._call_claude(
            prompt=self.FULL_ANALYSIS_PROMPT.format(paper_text=paper_text),
            model=self.model
        )

        # Parse response
        analysis_dict = self._parse_json_response(response)

        # Create PaperAnalysis object
        analysis = PaperAnalysis(
            title=metadata.get('title', 'Unknown Title') if metadata else 'Unknown Title',
            authors=metadata.get('authors', []) if metadata else [],
            problem=analysis_dict.get('problem', ''),
            motivation=analysis_dict.get('motivation', ''),
            method=analysis_dict.get('method', ''),
            innovations=analysis_dict.get('innovations', []),
            experiments=analysis_dict.get('experiments', ''),
            results=analysis_dict.get('results', []),
            pros=analysis_dict.get('pros', []),
            cons=analysis_dict.get('cons', []),
            conclusions=analysis_dict.get('conclusions', ''),
            future_work=analysis_dict.get('future_work', '')
        )

        logger.info("Full analysis completed")
        return analysis

    def quick_analysis(self, paper_text: str) -> Dict[str, str]:
        """
        Perform quick analysis using abstract and conclusions only

        Args:
            paper_text: Paper text (preferably abstract + conclusions)

        Returns:
            Dictionary with quick analysis results
        """
        logger.info("Starting quick paper analysis")

        # Use Haiku for cheaper quick analysis
        response = self._call_claude(
            prompt=self.QUICK_ANALYSIS_PROMPT.format(paper_text=paper_text),
            model=self.haiku_model
        )

        analysis = self._parse_json_response(response)

        logger.info("Quick analysis completed")
        return analysis

    def generate_presentation_content(self, analysis: PaperAnalysis,
                                     metadata: Optional[Dict] = None) -> PresentationContent:
        """
        Generate presentation content from analysis

        Args:
            analysis: Paper analysis
            metadata: Paper metadata

        Returns:
            PresentationContent object
        """
        logger.info("Generating presentation content")

        # Convert analysis to presentation-friendly format
        content = PresentationContent(
            title=analysis.title,
            authors=", ".join(analysis.authors[:3]) + (" et al." if len(analysis.authors) > 3 else ""),
            venue=metadata.get('venue', 'Unknown Venue') if metadata else 'Unknown Venue',
            year=metadata.get('year', '2024') if metadata else '2024',
            motivation=self._split_bullet_points(analysis.motivation),
            existing_problems=self._extract_problems(analysis.problem),
            research_problem=analysis.problem,
            method_overview=analysis.method,
            technical_details=self._extract_technical_details(analysis.method),
            innovations=analysis.innovations,
            experimental_setup=analysis.experiments,
            main_results=analysis.results,
            result_analysis=self._analyze_results(analysis.results),
            discussion=self._generate_discussion(analysis),
            pros=analysis.pros,
            cons=analysis.cons,
            future_work=self._split_bullet_points(analysis.future_work),
            conclusions=analysis.conclusions
        )

        logger.info("Presentation content generated")
        return content

    def _call_claude(self, prompt: str, model: Optional[str] = None) -> str:
        """
        Make API call to Claude

        Args:
            prompt: Prompt to send
            model: Model to use (defaults to self.model)

        Returns:
            Response text
        """
        model = model or self.model

        try:
            message = self.client.messages.create(
                model=model,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Track usage
            self.call_count += 1
            input_tokens = message.usage.input_tokens
            output_tokens = message.usage.output_tokens
            self.total_tokens += input_tokens + output_tokens

            # Calculate cost
            cost_data = self.cost_per_1k.get(model, self.cost_per_1k["claude-sonnet-4-6"])
            cost = (input_tokens / 1000 * cost_data["input"] +
                   output_tokens / 1000 * cost_data["output"])
            self.total_cost += cost

            logger.info(f"API call #{self.call_count}: {input_tokens} input + {output_tokens} output tokens, cost: ${cost:.4f}")

            return message.content[0].text

        except anthropic.APIError as e:
            logger.error(f"Claude API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error calling Claude: {e}")
            raise

    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON from Claude response"""
        try:
            # Try to find JSON in the response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                logger.error("No JSON found in response")
                logger.debug(f"Response: {response}")
                return {}

            json_str = response[json_start:json_end]
            return json.loads(json_str)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            logger.debug(f"Response: {response}")
            return {}

    def _split_bullet_points(self, text: str) -> List[str]:
        """Split text into bullet points"""
        # If already contains newlines, split by them
        if '\n' in text:
            points = [p.strip() for p in text.split('\n') if p.strip()]
            return points[:5]  # Limit to 5 points

        # Otherwise, try to split by sentences
        sentences = text.split('. ')
        return [s.strip() + '.' for s in sentences[:5] if s.strip()]

    def _extract_problems(self, problem_text: str) -> List[str]:
        """Extract problem statements"""
        points = self._split_bullet_points(problem_text)
        return points[:3] if points else [problem_text]

    def _extract_technical_details(self, method_text: str) -> List[str]:
        """Extract technical details from method description"""
        points = self._split_bullet_points(method_text)
        return points[:6] if points else [method_text]

    def _analyze_results(self, results: List[str]) -> str:
        """Generate analysis of results"""
        if not results:
            return "Results demonstrate the effectiveness of the proposed approach."

        # Summarize results
        return f"The proposed method achieves {len(results)} key improvements over baselines."

    def _generate_discussion(self, analysis: PaperAnalysis) -> str:
        """Generate discussion section"""
        discussion_parts = []

        if analysis.pros:
            discussion_parts.append(f"The approach shows {len(analysis.pros)} main advantages.")

        if analysis.cons:
            discussion_parts.append(f"However, {len(analysis.cons)} limitations should be considered.")

        if analysis.future_work:
            discussion_parts.append(analysis.future_work)

        return " ".join(discussion_parts) if discussion_parts else "The results warrant further investigation."

    def get_stats(self) -> Dict[str, Any]:
        """Get analyzer statistics"""
        return {
            'call_count': self.call_count,
            'total_tokens': self.total_tokens,
            'total_cost': self.total_cost,
            'avg_tokens_per_call': self.total_tokens / self.call_count if self.call_count > 0 else 0,
            'avg_cost_per_call': self.total_cost / self.call_count if self.call_count > 0 else 0,
        }
