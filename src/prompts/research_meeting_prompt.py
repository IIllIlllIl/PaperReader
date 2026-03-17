"""
Research Group Meeting Prompt for PaperReader

Optimized for academic research group presentations (组会专用)

Key differences from V3:
- Motivation slide (Why this problem matters)
- Related Work context (How it differs from previous work)
- Core Idea slide (Main contribution in one sentence)
- Discussion Questions (For audience engagement)
- Critical analysis (Limitations + Weaknesses)
"""

RESEARCH_MEETING_PROMPT = """You are creating presentation slides for a research group meeting (学术组会).

**CRITICAL REQUIREMENTS FOR RESEARCH PRESENTATION:**
1. **English ONLY** - No Chinese characters
2. **Max 5 bullet points per slide** - Strict limit for clarity
3. **Group meeting focus** - Emphasize WHY and HOW, not just WHAT
4. **Bold key numbers** - Format as **X%** not "X percent"
5. **Critical thinking** - Include limitations and questions
6. **Discussion-ready** - Generate questions for audience engagement

Paper text:
{paper_text}

Provide analysis in this EXACT JSON format:
{{
    "title": "Paper title",
    "authors": "Author names",
    "year": "Publication year",

    "motivation": [
        "Why this problem is important (real-world impact)",
        "What is missing in current approaches",
        "Why we need this research NOW",
        "Max 4 points, each ≤20 words"
    ],

    "problem_definition": [
        "The specific problem this paper solves",
        "Key challenges addressed",
        "Scope of the solution",
        "Max 3 points, each ≤20 words"
    ],

    "related_work": [
        "Previous approach 1: brief description + limitation",
        "Previous approach 2: brief description + limitation",
        "How this paper is DIFFERENT",
        "Max 4 points, each ≤25 words"
    ],

    "core_idea": "One clear sentence (≤30 words) describing the MAIN contribution/innovation",

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
        "🔥 **X%** improvement - what this means",
        "🔥 **Y%** success rate - why this matters",
        "**Z%** performance - comparison context",
        "Max 5 results, bold ALL numbers, mark top 2-3 with 🔥"
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
        "Question 1 for audience (open-ended, thought-provoking)",
        "Question 2 about implications/future",
        "Question 3 about methodology/applicability",
        "Max 3 questions"
    ]
}}

**IMPORTANT:**
- motivation: Focus on REAL-WORLD IMPACT
- related_work: Include LIMITATIONS of previous work
- core_idea: ONE clear sentence, like "We propose X, which achieves Y by Z"
- main_results: Bold ALL numbers (**X%**), mark breakthroughs with 🔥
- limitations: Be HONEST and CRITICAL
- discussion_questions: Open-ended questions that spark discussion

Return STRICT JSON only. No markdown. No explanations.
"""
