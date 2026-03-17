"""
V3 Prompt for Enhanced AI Analyzer

Requirements:
- English ONLY (no Chinese)
- Max 30 words per slide
- Keywords, not sentences
- Tables for data
- Bold numbers
- Mark breakthroughs with emoji
"""

V3_ANALYSIS_PROMPT = """You are creating presentation slides from an academic paper.

**CRITICAL V3 REQUIREMENTS:**
1. **English ONLY** - No Chinese characters anywhere
2. **Max 30 words per slide** - Strict limit
3. **Keywords, NOT sentences** - Use concise phrases
4. **Tables for data** - Use Markdown tables for datasets, baselines, metrics
5. **Bold numbers** - Format all numbers as **X%** not "X percent"
6. **Mark breakthroughs** - Use 🔥 emoji for 3-5 key breakthroughs

Paper text:
{paper_text}

Provide analysis in this EXACT JSON format:
{{
    "title": "Paper title (English only)",
    "authors": "Author names",
    "year": "Publication year",

    "research_background_keywords": [
        "Keyword 1 about background",
        "Keyword 2 about context",
        "Max 5 keywords, total ≤30 words"
    ],

    "research_problem_keywords": [
        "Keyword 1 about problem",
        "Keyword 2 about challenge",
        "Max 4 keywords, total ≤30 words"
    ],

    "key_insights": [
        "💡 Insight 1: Keywords only",
        "🔥 Breakthrough 2: Major finding with emoji",
        "🔥 Breakthrough 3: Another major result",
        "3-5 insights, mark breakthroughs with 🔥"
    ],

    "method_keywords": [
        "Framework: Name and type",
        "Component 1: Brief description",
        "Component 2: Brief description",
        "Workflow: Step1 → Step2 → Step3",
        "Max 6 keywords, total ≤30 words"
    ],

    "technical_details_keywords": [
        "Algorithm 1: 2-3 keyword description",
        "Technique 2: 2-3 keyword description",
        "Max 6 items, total ≤30 words"
    ],

    "datasets_table": "| Dataset | Size | Type | Purpose |
|---------|------|------|---------|
| Name1   | 500  | Python | Offline |
| Name2   | 369  | Multi  | Internal |",

    "baselines_table": "| Method | Type | Description |
|--------|------|-------------|
| Name1  | Shell-based | Brief desc |
| Name2  | AST-based | Brief desc |",

    "metrics_table": "| Metric | Description |
|--------|-------------|
| Name1  | Brief desc |
| Name2  | Brief desc |",

    "experimental_setup_keywords": [
        "Environment: Linux, Docker",
        "Duration: 2 months",
        "Participants: 2,600 users",
        "Max 4 keywords, total ≤30 words"
    ],

    "main_results_keywords": [
        "🔥 **59%** PR merge rate - Industry-first",
        "**82%** plan approval - Human-AI aligned",
        "**8%** end-to-end success - Full automation",
        "**31%** test pass rate - Benchmark result",
        "Max 6 results, bold ALL numbers, mark breakthroughs with 🔥"
    ],

    "key_findings_keywords": [
        "Finding 1: 2-3 keywords",
        "Finding 2: 2-3 keywords",
        "Max 4 findings, total ≤30 words"
    ],

    "advantages_keywords": [
        "Advantage 1: 2-3 keywords",
        "Advantage 2: 2-3 keywords",
        "Max 4 advantages, total ≤30 words"
    ],

    "limitations_keywords": [
        "Limitation 1: 2-3 keywords",
        "Limitation 2: 2-3 keywords",
        "Max 3 limitations, total ≤30 words"
    ],

    "future_work_keywords": [
        "Direction 1: 2-3 keywords",
        "Direction 2: 2-3 keywords",
        "Max 3 items, total ≤30 words"
    ]
}}

**STRICT RULES:**
- Each field MUST be keywords/phrases, NOT sentences
- Each slide MUST have ≤30 words total
- ALL numbers MUST be bolded: **27%** not "27 percent"
- Use 🔥 emoji for 3-5 BIGGEST breakthroughs
- Use Markdown tables for: datasets, baselines, metrics, experimental setup
- NO Chinese characters anywhere
- Use these emojis: 💡 (insights), 🔥 (breakthroughs), ⚡ (challenges)

**TABLE FORMAT:**
Use Markdown table syntax:
| Column1 | Column2 | Column3 |
|---------|---------|---------|
| Value1  | Value2  | Value3  |

Provide analysis in JSON format now. Follow ALL requirements strictly.
"""
