#!/usr/bin/env python3
"""
Enhanced AI Analyzer for PaperReader (V3)

V3 Improvements:
- Slides only (no Chinese text)
- Max 30 words per slide
- Keywords-first approach
- Tables for structured data
- Key breakthroughs marked with emoji
"""

import logging
import json
import re
from typing import Optional, Dict, List
from dataclasses import dataclass, field
import anthropic

logger = logging.getLogger(__name__)


@dataclass
class PaperAnalysis:
    """Detailed analysis of the paper (V3)"""

    # Basic information
    title: str
    authors: str
    year: str
    summary: str

    # V3: Research Background (keywords only)
    research_background_keywords: List[str] = field(default_factory=list)
    research_context_stats: Dict[str, str] = field(default_factory=dict)

    # V3: Research Gap (keywords only)
    research_gap_keywords: List[str] = field(default_factory=list)
    research_problem_statement: str = ""

    # V3: Key Insights (with breakthrough markers)
    key_insights: List[str] = field(default_factory=list)

    # V3: Method Overview (keywords only)
    framework_name: str = ""
    key_components: List[str] = field(default_factory=list)
    workflow_steps: List[str] = field(default_factory=list)

    # V3: Technical Details (keywords + table)
    core_algorithms: List[str] = field(default_factory=list)
    key_techniques: List[str] = field(default_factory=list)
    techniques_comparison_table: Dict[str, List[str]] = field(default_factory=dict)

    # V3: Experimental Setup (TABLE format)
    datasets_table: Dict[str, str] = field(default_factory=dict)
    baselines_table: Dict[str, str] = field(default_factory=dict)
    metrics_table: Dict[str, str] = field(default_factory=dict)
    experimental_setup_table: Dict[str, str] = field(default_factory=dict)

    # V3: Main Results (with bold numbers)
    main_results: List[str] = field(default_factory=list)
    performance_comparison_table: Dict[str, List[str]] = field(default_factory=dict)

    # V3: Analysis (keywords only)
    key_findings: List[str] = field(default_factory=list)
    implications: List[str] = field(default_factory=list)

    # V3: Discussion (keywords only)
    strengths: List[str] = field(default_factory=list)
    limitations_keywords: List[str] = field(default_factory=list)
    future_work_keywords: List[str] = field(default_factory=list)

    # Conclusion (keywords only)
    key_takeaways: List[str] = field(default_factory=list)

    # Citation analysis (Phase 3)
    citation_data: Optional[Dict] = None  # Citation analysis results
    has_citation_data: bool = False  # Whether citation data is available


class AIAnalyzer:
    """Enhanced AI analyzer with V3 prompt engineering"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        self.api_key = api_key
        self.model = model
        self.call_count = 0
        self.total_tokens = 0
        self.total_cost = 0.0

        self.cost_per_1k = {
            "claude-sonnet-4-6": {"input": 0.003, "output": 0.015}
        }

    def analyze_paper_detailed(self, paper_text: str, metadata: Optional[Dict] = None) -> PaperAnalysis:
        """Perform detailed analysis of paper with V3 format"""
        logger.info("Starting V3 detailed paper analysis")

        # Truncate if too long
        max_chars = 150000

        # Build V3 prompt
        prompt = self._generate_v3_prompt(paper_text, metadata, max_chars)

        # Call Claude API
        client = anthropic.Anthropic(api_key=self.api_key)

        response = client.messages.create(
            model=self.model,
            max_tokens=8192,
            temperature=0,  # IMPORTANT: Use temperature=0 for stable JSON output
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
        content = next(
            (block.text for block in response.content if hasattr(block, "text") and block.text),
            None,
        )
        if content is None:
            raise ValueError("Claude API response did not contain a text block")

        # Extract structured data from response
        analysis = self._parse_v3_response(content, metadata)

        logger.info(f"V3 analysis completed: {len(content)} characters")
        return analysis

    def _generate_v3_prompt(self, paper_text: str, metadata: Optional[Dict] = None, max_chars: int = 150000) -> str:
        """Generate V3-compliant prompt"""

        prompt = f"""
You are creating presentation slides from an academic paper.

**CRITICAL V3 REQUIREMENTS:**
1. **English ONLY** - No Chinese characters anywhere
2. **Max 30 words per slide** - Strict limit
3. **Keywords, NOT sentences** - Use concise phrases
4. **Tables for data** - Use Markdown tables for datasets, baselines, metrics
5. **Bold numbers** - Format all numbers as **X%** not "X percent"
6. **Mark breakthroughs** - Use 🔥 emoji for 3-5 key breakthroughs

Paper text:
{paper_text[:max_chars]}

**IMPORTANT: Return STRICT JSON ONLY. Do not include any explanations or markdown formatting outside the JSON.**

Provide analysis in this EXACT JSON format:
{{
    "title": "Paper title (English only)",
    "authors": "Author names",
    "year": "Publication year",
    "summary": "3-5 sentence summary for presentation",

    "research_background_keywords": [
        "Keyword 1 about background",
        "Keyword 2 about context",
        "Max 5 keywords, total ≤30 words"
    ],

    "research_gap_keywords": [
        "Keyword 1 about problem",
        "Keyword 2 about challenge",
        "Max 4 keywords, total ≤30 words"
    ],

    "research_problem_statement": "One sentence, max 30 words",

    "key_insights": [
        "💡 Insight 1: breakthrough description",
        "🔥 Insight 2: breakthrough with emoji",
        "Max 5 insights, total ≤30 words"
    ],

    "framework_name": "Method/framework name",
    "key_components": [
        "Component 1: brief description",
        "Component 2: brief description",
        "Max 6 components, total ≤30 words"
    ],
    "workflow_steps": [
        "Step 1: brief description",
        "Step 2: brief description",
        "Max 6 steps, total ≤30 words"
    ],

    "core_algorithms": [
        "Algorithm 1: brief description",
        "Algorithm 2: brief description",
        "Max 6 algorithms, total ≤30 words"
    ],
    "key_techniques": [
        "Technique 1: brief description",
        "Technique 2: brief description",
        "Max 6 techniques, total ≤30 words"
    ],

    "datasets_table": {{
        "Dataset 1": "Description",
        "Dataset 2": "Description"
    }},
    "baselines_table": {{
        "Baseline 1": "Description",
        "Baseline 2": "Description"
    }},
    "metrics_table": {{
        "Metric 1": "Description",
        "Metric 2": "Description"
    }},
    "experimental_setup_table": {{
        "Config": "Value",
        "Environment": "Description"
    }},

    "main_results": [
        "🔥 **59%** PR merge rate - Industry-first",
        "**82%** plan approval - Human-AI aligned",
        "**8%** end-to-end success - Full automation",
        "**31%** test pass rate - Benchmark result",
        "Max 6 results, bold ALL numbers, mark breakthroughs with 🔥"
    ],

    "key_findings": [
        "Finding 1: 2-3 keywords",
        "Finding 2: 2-3 keywords",
        "Max 6 findings, total ≤30 words"
    ],
    "implications": [
        "Implication 1: brief keyword",
        "Implication 2: brief keyword",
        "Max 3 implications, total ≤30 words"
    ],

    "strengths": [
        "Strength 1: brief keyword",
        "Strength 2: brief keyword",
        "Max 4 strengths, total ≤30 words"
    ],
    "limitations_keywords": [
        "Limitation 1: brief keyword",
        "Limitation 2: brief keyword",
        "Max 4 limitations, total ≤30 words"
    ],
    "future_work_keywords": [
        "Future work 1: brief keyword",
        "Future work 2: brief keyword",
        "Max 3 keywords, total ≤30 words"
    ],

    "key_takeaways": [
        "Takeaway 1: brief keyword",
        "Takeaway 2: brief keyword",
        "Max 4 takeaways, total ≤30 words"
    ]
}}

Return ONLY the JSON object, nothing else.
"""
        return prompt

    def _parse_v3_response(self, content: str, metadata: Optional[Dict] = None) -> PaperAnalysis:
        """
        Parse AI response into structured PaperAnalysis.

        Strategy:
        1. Try strict JSON parsing
        2. Try JSON extraction from text
        3. Fallback to Markdown parsing
        4. Return safe default structure
        """

        logger.info("Parsing AI response (V3)")

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
        # 3. Markdown fallback (not recommended for V3)
        # ------------------------------------------------

        logger.warning("Falling back to Markdown parsing (not recommended for V3)")

        try:
            analysis = self._parse_markdown_fallback(content, metadata)
            logger.info("✓ Markdown parsing succeeded")
            return analysis

        except Exception as e:
            logger.error(f"Markdown parsing failed: {e}")

        # ------------------------------------------------
        # 4. Safe fallback - minimal structure
        # ------------------------------------------------

        logger.error("Failed to parse AI response, returning minimal structure")

        return PaperAnalysis(
            title=metadata.get('title', 'Unknown Paper') if metadata else 'Unknown Paper',
            authors=metadata.get('authors', 'Unknown Authors') if metadata else 'Unknown Authors',
            year=metadata.get('year', '2024') if metadata else '2024',
            summary="AI response parsing failed - please check logs"
        )

    def _build_analysis_from_json(self, data: Dict, metadata: Optional[Dict] = None) -> PaperAnalysis:
        """Build PaperAnalysis from JSON data"""

        logger.info("Building PaperAnalysis from JSON")

        # Extract basic info from JSON or fallback to metadata
        title = data.get("title", "")
        if not title and metadata:
            title = metadata.get("title", "Unknown Title")

        authors = data.get("authors", "")
        if not authors and metadata:
            authors = metadata.get("authors", "Unknown Authors")

        year = data.get("year", "")
        if not year and metadata:
            year = metadata.get("year", "2024")

        summary = data.get("summary", "")

        # Build analysis
        analysis = PaperAnalysis(
            title=title,
            authors=authors,
            year=year,
            summary=summary,

            # Research background
            research_background_keywords=data.get("research_background_keywords", []),
            research_context_stats=data.get("research_context_stats", {}),

            # Research gap
            research_gap_keywords=data.get("research_gap_keywords", []),
            research_problem_statement=data.get("research_problem_statement", ""),

            # Key insights
            key_insights=data.get("key_insights", []),

            # Method
            framework_name=data.get("framework_name", ""),
            key_components=data.get("key_components", []),
            workflow_steps=data.get("workflow_steps", []),

            # Technical details
            core_algorithms=data.get("core_algorithms", []),
            key_techniques=data.get("key_techniques", []),
            techniques_comparison_table=data.get("techniques_comparison_table", {}),

            # Experimental setup
            datasets_table=data.get("datasets_table", {}),
            baselines_table=data.get("baselines_table", {}),
            metrics_table=data.get("metrics_table", {}),
            experimental_setup_table=data.get("experimental_setup_table", {}),

            # Results
            main_results=data.get("main_results", []),
            performance_comparison_table=data.get("performance_comparison_table", {}),

            # Analysis
            key_findings=data.get("key_findings", []),
            implications=data.get("implications", []),

            # Discussion
            strengths=data.get("strengths", []),
            limitations_keywords=data.get("limitations_keywords", []),
            future_work_keywords=data.get("future_work_keywords", []),

            # Conclusion
            key_takeaways=data.get("key_takeaways", [])
        )

        logger.info(f"✓ Built analysis: {len(analysis.key_insights)} insights, "
                   f"{len(analysis.main_results)} results, "
                   f"{len(analysis.key_findings)} findings")

        return analysis

    def _parse_markdown_fallback(self, content: str, metadata: Optional[Dict] = None) -> PaperAnalysis:
        """Fallback parser for Markdown format (not recommended for V3)"""

        logger.warning("Using Markdown fallback parser")

        def extract_section(text: str, *keywords) -> str:
            """Extract section by keyword"""
            for keyword in keywords:
                pattern = rf"(?:^|\n)[#]*\s*{keyword}.*?\n(.*?)(?=\n[#]|\Z)"
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    return match.group(1).strip()
            return ""

        def extract_bullets(text: str, *keywords) -> List[str]:
            """Extract bullet points"""
            for keyword in keywords:
                section = extract_section(text, keyword)
                if section:
                    bullets = re.findall(r"[-*]\s+(.*)", section)
                    if bullets:
                        return [b.strip() for b in bullets][:6]
            return []

        # Extract basic info
        title = extract_section(content, "title")
        authors = extract_section(content, "author")
        year = extract_section(content, "year")
        summary = extract_section(content, "summary")

        # Extract keywords
        research_background_keywords = extract_bullets(content, "background", "context")
        research_gap_keywords = extract_bullets(content, "problem", "gap")
        key_insights = extract_bullets(content, "insight", "contribution")
        key_components = extract_bullets(content, "component", "method")
        main_results = extract_bullets(content, "result", "performance")
        key_findings = extract_bullets(content, "finding")
        strengths = extract_bullets(content, "strength", "advantage")
        limitations_keywords = extract_bullets(content, "limitation")
        future_work_keywords = extract_bullets(content, "future")
        key_takeaways = extract_bullets(content, "takeaway", "conclusion")

        return PaperAnalysis(
            title=title or metadata.get('title', 'Unknown') if metadata else 'Unknown',
            authors=authors or metadata.get('authors', 'Unknown') if metadata else 'Unknown',
            year=year or metadata.get('year', '2024') if metadata else '2024',
            summary=summary,

            research_background_keywords=research_background_keywords,
            research_gap_keywords=research_gap_keywords,
            key_insights=key_insights,
            key_components=key_components,
            main_results=main_results,
            key_findings=key_findings,
            strengths=strengths,
            limitations_keywords=limitations_keywords,
            future_work_keywords=future_work_keywords,
            key_takeaways=key_takeaways
        )

    # Backward compatibility aliases
    def analyze_paper(self, paper_text: str, metadata: Optional[Dict] = None) -> PaperAnalysis:
        """Alias for analyze_paper_detailed for backward compatibility"""
        return self.analyze_paper_detailed(paper_text, metadata)

    def quick_analysis(self, paper_text: str, metadata: Optional[Dict] = None) -> PaperAnalysis:
        """Quick analysis - same as detailed for now"""
        return self.analyze_paper_detailed(paper_text, metadata)

    def get_stats(self) -> Dict:
        """Get usage statistics"""
        return {
            'call_count': self.call_count,
            'total_tokens': self.total_tokens,
            'total_cost': self.total_cost
        }
