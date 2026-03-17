"""
Slide Planning Prompt

This prompt asks the LLM to create a high-level slide plan
from a PaperAnalysis object.
"""

SLIDE_PLANNING_PROMPT = """You are an expert research presentation designer.

Your task is to create a **high-level slide plan** for a PhD research group meeting presentation.

You will receive a detailed analysis of a research paper, and you must design a logical presentation flow.

**IMPORTANT**: You are creating a PLAN, not the full presentation. Output topics and key points, not full sentences.

**REQUIRED SLIDE STRUCTURE** (11 slides total):

1. **Title** - Paper title, authors, year
2. **Motivation** - WHY this problem matters (real-world impact, research gap)
3. **Problem Definition** - The specific problem this paper solves
4. **Related Work** - Previous approaches, their limitations, and this paper's advantages
5. **Core Idea** - Main contribution in ONE clear sentence
6. **Method Overview** - High-level approach and key components
7. **Method Details** - Technical details and implementation insights
8. **Experiment Setup** - Datasets, baselines, metrics, environment
9. **Results** - Key findings with brief interpretations
10. **Limitations** - Honest weaknesses and critical analysis
11. **Takeaways & Discussion** - Key insights and discussion questions

**INPUT**: PaperAnalysis (detailed analysis of the paper)

**OUTPUT**: SlidePlan (JSON with slide titles and 3-5 key topics per slide)

**RULES**:
1. Each slide MUST have 3-5 key points (no more, no less)
2. Key points should be TOPICS, not full sentences
3. Focus on WHAT should be covered, not HOW to say it
4. Each slide should have a clear purpose
5. Ensure logical flow from motivation to conclusions
6. Be specific - avoid generic topics like "introduction" or "conclusion"

**EXAMPLE OUTPUT FORMAT**:

```json
{
  "slides": [
    {
      "title": "Motivation",
      "key_points": [
        "Limitations of existing autonomous coding agents",
        "Mismatch between SWE-bench and enterprise complexity",
        "Need for human oversight in critical decisions",
        "Gap between benchmark performance and real-world deployment"
      ],
      "slide_type": "content",
      "notes": "Explain WHY this problem is important for real-world software development"
    },
    {
      "title": "Related Work",
      "key_points": [
        "SWE-agent: fully autonomous - lacks human feedback loop",
        "AutoCodeRover: strong performance - limited to historical benchmarks",
        "Multi-agent systems: collaborative - no industrial deployment validation",
        "This work: human-in-the-loop + real-world evaluation"
      ],
      "slide_type": "content",
      "notes": "Compare approaches and highlight limitations of previous work"
    }
  ]
}
```

**PaperAnalysis Input**:

{{PAPER_ANALYSIS_PLACEHOLDER}}

Now create the SlidePlan in JSON format. Return ONLY valid JSON, no markdown, no explanations.

Remember:
- 11 slides total
- 3-5 key topics per slide
- Topics should be specific and actionable
- Ensure logical flow
- No empty slides
"""
