"""
PhD Research Meeting Prompt V2 (Enhanced with Figure Support)

Key improvements:
- Figure extraction instructions
- Result interpretations
- Related work comparison format
- Discussion depth
"""

PHD_MEETING_PROMPT_V2 = """You are creating presentation slides for a PhD research group meeting.

**CRITICAL REQUIREMENTS FOR PHD-LEVEL PRESENTATION:**
1. **English ONLY** - No Chinese characters
2. **Max 5 bullet points per slide** - Strict limit for clarity
3. **PhD-level depth** - Critical analysis, not just description
4. **Bold key numbers** - Format as **X%** not "X percent"
5. **Result interpretations** - Explain WHY results matter
6. **Comparison focus** - How this differs from previous work
7. **Discussion depth** - Thought-provoking questions

Paper text:
{paper_text}

**FIGURE EXTRACTION REQUEST:**
If the paper contains architecture diagrams, pipeline figures, or method visualizations, identify them.
Format: "FIGURE: [description of what the figure shows]"

Provide analysis in this EXACT JSON format:
{{
    "title": "Paper title",
    "authors": "Author names",
    "year": "Publication year",

    "motivation": [
        "WHY this problem matters (real-world impact)",
        "What is MISSING in current approaches",
        "Why we need this research NOW",
        "Max 3 points, each ≤20 words"
    ],

    "problem_definition": [
        "The specific problem this paper solves",
        "Key challenges addressed",
        "Scope of the solution",
        "Max 3 points, each ≤20 words"
    ],

    "related_work": [
        "Previous method 1: brief description + its LIMITATION",
        "Previous method 2: brief description + its LIMITATION",
        "Our IMPROVEMENT: what we do differently",
        "Max 4 points, focus on LIMITATIONS and IMPROVEMENTS"
    ],

    "core_idea": "One clear sentence (≤30 words) describing the MAIN contribution/innovation",

    "has_architecture_figure": true/false,
    "figure_description": "Description of the main architecture/pipeline figure if exists",

    "method_overview": [
        "High-level approach (1 sentence)",
        "Key components (2-3 items)",
        "Novel techniques used (2-3 items)",
        "Max 4 points, each ≤20 words"
    ],

    "method_details": [
        "Technical detail 1 (specific algorithm/technique)",
        "Technical detail 2",
        "Implementation insight",
        "Max 4 points, each ≤25 words"
    ],

    "experiment_setup": {{
        "datasets": "Dataset names + sizes",
        "baselines": "Baseline methods compared",
        "metrics": "Evaluation metrics used",
        "environment": "Experimental environment"
    }},

    "main_results": [
        "🔥 **X%** improvement - INTERPRETATION of what this means",
        "🔥 **Y%** success rate - INTERPRETATION of significance",
        "**Z%** performance - COMPARISON context",
        "Max 5 results, each MUST have interpretation after dash (-)"
    ],

    "limitations": [
        "Limitation 1: honest weakness",
        "Limitation 2: scope constraint",
        "Limitation 3: evaluation gap",
        "Max 4 points, be CRITICAL and HONEST"
    ],

    "key_takeaways": [
        "Main insight 1: what we learned",
        "Main insight 2: broader implication",
        "Main insight 3: practical impact",
        "Max 3 points, each ≤20 words"
    ],

    "discussion_questions": [
        "Question 1: about methodology/applicability (open-ended)",
        "Question 2: about implications/future work",
        "Question 3: critical thinking about limitations",
        "Max 3 questions, thought-provoking"
    ]
}}

**CRITICAL REQUIREMENTS:**
- main_results: Each result MUST have interpretation after dash (-)
- related_work: Focus on LIMITATIONS of previous work and YOUR improvements
- has_architecture_figure: Set to true if paper contains method diagrams
- figure_description: Describe what the main figure shows
- discussion_questions: Must be thought-provoking, not simple yes/no questions

**INTERPRETATION EXAMPLE:**
❌ Bad: "**59%** merged PR rate"
✅ Good: "**59%** merged PR rate - demonstrates strong real-world applicability"

**RELATED WORK EXAMPLE:**
❌ Bad: "SWE-agent: autonomous coding agent"
✅ Good: "SWE-agent: autonomous agent - lacks human oversight in critical decisions"

Return STRICT JSON only. No markdown. No explanations.
"""
