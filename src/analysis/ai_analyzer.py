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
from typing import Optional, Dict, List
from dataclasses import dataclass, field
import anthropic

logger = logging.getLogger(__name__)


@dataclass
class PaperAnalysis:
    """Detailed analysis of the paper"""
    
    # Basic information
    title: str
    authors: str
    year: str
    summary: str
    
    # V3: Research Background (keywords only)
    research_background_keywords: List[str]
    research_context_stats: Dict[str, str]  # {"metric": "value"}
    
    # V3: Research Gap (keywords only)
    research_gap_keywords: List[str]
    research_problem_statement: str  # Max 30 words
    
    # V3: Key Insights (with breakthrough markers)
    key_insights: List[str]  # Include 🔥 emoji for breakthroughs
    
    # V3: Method Overview (keywords only)
    framework_name: str
    key_components: List[str]  # Max 6 keywords
    workflow_steps: List[str]  # Max 6 keywords
    
    # V3: Technical Details (keywords + table)
    core_algorithms: List[str]  # Max 6 keywords
    key_techniques: List[str]  # Max 6 keywords
    techniques_comparison_table: Dict[str, List[str]]  # {"Technique": ["Pro", "Con"]}
    
    # V3: Experimental Setup (TABLE format)
    datasets_table: Dict[str, str]  # {"Name": "Description"}
    baselines_table: Dict[str, str]  # {"Name": "Description"}
    metrics_table: Dict[str, str]  # {"Name": "Description"}
    experimental_setup_table: Dict[str, str]  # {"Config": "Value"}
    
    # V3: Main Results (with bold numbers)
    main_results: List[str]  # Bold all numbers, mark breakthroughs with 🔥
    performance_comparison_table: Dict[str, List[str]]  # {"Metric": ["Method1", "Method2"]}
    
    # V3: Analysis (keywords only)
    key_findings: List[str]  # Max 6 findings
    implications: List[str]  # Max 3 keywords
    
    # V3: Discussion (keywords only)
    strengths: List[str]  # Max 4 keywords
    limitations_keywords: List[str]  # Max 4 keywords
    future_work_keywords: List[str]  # Max 3 keywords
    
    # Conclusion (keywords only)
    key_takeaways: List[str]  # Max 4 keywords


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
        prompt = self._generate_v3_prompt(paper_text, metadata)
        
        # Call Claude API
        client = anthropic.Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=8192,
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
        content = response.content[0].text
        
        # Extract structured data from response
        analysis = self._parse_v3_response(content, metadata)
        
        logger.info(f"V3 analysis completed: {len(content)} characters")
        return analysis
    
    def _generate_v3_prompt(self, paper_text: str, metadata: Optional[Dict] = None) -> str:
        """Generate V3-compliant prompt"""
        
        prompt = f"""
Analyze this academic paper for a presentation. Generate **30 slides** in pure **English**.

**CRITICAL V3 Requirements:**
1. **Slides Only** - NO Chinese text (English only)
2. **Max 30 Words** - Maximum 30 words per slide (strict limit)
3. **Keywords First** - Use keywords, NOT full sentences
4. **Tables for Data** - Use Markdown tables for structured data
5. **Key Breakthroughs** - Mark 3-5 breakthroughs with 🔥 emoji
6. **Bold Numbers** - Bold all key quantitative results (**27%**)

**Slide Structure (30 slides total):**

1. **Title Slide** (1 slide)
   - Paper title
   - Authors | Year

2. **Outline** (1 slide)
   - 6-8 main sections

3. **Research Background** (2-3 slides)
   - Context (1 sentence max)
   - 3-5 keywords per slide
   - Bold key statistics

4. **Research Gap** (1-2 slides)
   - Problem statement (1 sentence max)
   - 3-4 keywords

5. **Key Insights** (1-2 slides)
   - 3-5 key insights
   - Mark breakthroughs with 🔥

6. **Method Overview** (4-5 slides)
   - Framework name
   - Key components (3-4 keywords each)
   - Workflow steps (keywords)

7. **Technical Details** (3-4 slides)
   - Core algorithms (2-3 keywords each)
   - Key techniques (2-3 keywords each)
   - Use table for comparison

8. **Experimental Setup** (1-2 slides)
   - **USE TABLE** format:
     * Datasets (name, size)
     * Baselines (name, type)
     * Metrics (name, description)

9. **Main Results** (3-4 slides)
   - 3-5 key results per slide
   - Bold all numbers (**27%**)
   - Mark breakthroughs with 🔥

10. **Analysis** (2-3 slides)
   - Key findings (2-3 per slide)
   - Performance comparison (use table)

11. **Discussion** (2-3 slides)
   - Strengths (3-4 keywords)
   - Limitations (3-4 keywords)
   - Future work (2-3 keywords)

12. **Conclusion** (1-2 slides)
   - Key takeaways (3-4 bullets)
   - Future work (2-3 bullets)

13. **Q&A** (1 slide)
   - Thank you | Questions

**TABLE FORMAT Example:**

```markdown
## Experimental Setup

| Component | Details |
|----------|---------|
| **Dataset** | SWE-bench (500 issues) |
| **Baselines** | SWE-agent, AutoCodeRover |
| **Metrics** | Resolution Rate, Time Cost |
| **Environment** | Linux shell, Docker |
```

**KEYWORD FORMAT Example:**

```markdown
## Method Overview

- Framework: HULA (3 agents)
- Approach: Human-in-the-Loop
- Style: Collaborative AI
- Focus: Enterprise development
```

**BREAKTHROUGH FORMAT Example:**

```markdown
## Key Results

- 🔥 **59% PR Merge Rate** - Industry-first
- **82% Plan Approval** - Human-AI alignment
- **8% End-to-End Success** - Complete automation
- **30% Code Similarity** - Quality match
```

Now analyze the paper:

**CRITICAL Rules:**
- Maximum 30 words per slide
- English only (no Chinese)
- Use keywords, not sentences
- Bold all numbers: **27%** not "27 percent"
- Use tables for: datasets, baselines, experimental setup, results comparison
- Mark 3-5 breakthroughs with 🔥 emoji
- Keep it concise and scannable

Paper text to analyze:
{paper_text[:max_chars]}
"""

        return prompt
    
    def _parse_v3_response(self, content: str, metadata: Optional[Dict] = None) -> PaperAnalysis:
        """Parse V3 response into structured data"""
        
        # Extract data from response
        lines = content.strip().split('\n')
        
        # Parse sections from response
        # This is a simplified parser - you may need to enhance it
        analysis = PaperAnalysis(
            title=metadata.get('title', 'Unknown') if metadata else 'Unknown',
            authors=metadata.get('authors', 'Unknown') if metadata else 'Unknown',
            year=metadata.get('year', '2024') if metadata else '2024',
            summary='',
            research_background_keywords=[],
            research_context_stats={},
            research_gap_keywords=[],
            research_problem_statement='',
            key_insights=[],
            framework_name='',
            key_components=[],
            workflow_steps=[],
            core_algorithms=[],
            key_techniques=[],
            techniques_comparison_table={},
            datasets_table={},
            baselines_table={},
            metrics_table={},
            experimental_setup_table={},
            main_results=[],
            performance_comparison_table={},
            key_findings=[],
            implications=[],
            strengths=[],
            limitations_keywords=[],
            future_work_keywords=[],
            key_takeaways=[]
        )
        
        # TODO: Implement proper parsing logic to extract data from response
        # For now, return basic structure
        logger.warning("V3 response parsing not fully implemented - returning basic structure")
        
        return analysis
    
    def get_stats(self) -> Dict:
        """Get usage statistics"""
        return {
            'call_count': self.call_count,
            'total_tokens': self.total_tokens,
            'total_cost': self.total_cost
        }
