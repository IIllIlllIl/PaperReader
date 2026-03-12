# AI Prompt Engineering V3 Guidelines

**Version**: 3.0  
**Date**: 2026-03-06  
**Status**: Production Ready

---

## Core Principles

### 1. Keyword-First Approach
- Use keywords instead of full sentences
- Maximum 1-2 sentences per bullet point
- Focus on key information only

### 2. Table-Based Structured Data
- Use Markdown tables for:
  - Experimental setup
  - Dataset descriptions
  - Baseline comparisons
  - Metric results

### 3. Highlight Key Breakthroughs
- Identify 3-5 key breakthroughs per paper
- Use emoji (🔥) to mark breakthroughs
- Bold key numbers and findings
- Separate breakthrough section

### 4. Reduce Text Density
- Target: 50% less text vs V2
- Maximum 5-6 bullet points per slide
- Maximum 60 characters per point
- Use visual hierarchy (tables, lists)

---

## Prompt Structure V3

### Output Requirements

```json
{
  "key_breakthroughs": [
    "Breakthrough 1: Brief description with specific number (e.g., 27% improvement)",
    "Breakthrough 2: Brief description with specific number"
  ],
  
  "experimental_setup": {
    "datasets": "Name (size)",
    "baselines": ["Method1", "Method2"],
    "metrics": ["Metric1", "Metric2"],
    "environment": "Setup details",
    "tasks": "Number and type"
  },
  
  "method_overview": {
    "framework_name": "HULA",
    "key_components": [
      "Component1: Brief description",
      "Component2: Brief description"
    ],
    "workflow": ["Step1", "Step2", "Step3"],
    "key_features": [
      "Feature1: Brief description",
      "Feature2: Brief description"
    ]
  },
  
  "main_results": [
    "Result 1: 27% improvement over baseline",
    "Result 2: 89% user acceptance",
    "Result 3: 52% error reduction"
  ]
}
```

---

## Content Extraction Rules

### Rule 1: Tables Over Lists
```markdown
## Experimental Setup

| Item | Content | Note |
|------|---------|------|
| **Datasets** | SWE-bench | 2,294 issues |
| **Baselines** | SWE-agent<br>AutoCodeRover | Autonomous agents |
| **Metrics** | Resolution Rate<br>Time Cost | Success rate, time |
| **Environment** | Atlassian JIRA | Real enterprise |
| **Tasks** | 64 tasks | Real dev tasks |
```

### Rule 2: Keywords Over Sentences
```markdown
## Method Overview

**HULA Framework**

**Key Components**:
- 🤖 Planner Agent: File localization, plan generation
- 💻 Coding Agent: Code generation
- 👤 Human Agent: Feedback & review

**Workflow**:
1. Task Setup → 2. Planning → 3. Coding → 4. PR

**Features**:
- ✅ DPDE architecture
- ✅ Iterative refinement
- ✅ Tool integration
```

### Rule 3: Highlight Breakthroughs
```markdown
## 🔥 Key Breakthroughs

**Breakthrough 1**: Human-AI Collaboration
- First enterprise deployment of Human-in-the-Loop
- **27%** improvement vs autonomous

**Breakthrough 2**: Empirical Validation
- Real-world testing: **64** tasks
- User acceptance: **89%**

**Breakthrough 3**: Practical Insights
- Human feedback reduces **52%** errors
- Average time saved: **4.3** min/task
```

---

## Slide Structure V3

### Breakthrough Slides
- **Slide 8**: Key Breakthroughs (🔥 emoji)
- **Slide 13**: Technical Innovations
- **Slide 23**: Key Findings (🔥 emoji)

### Table Slides
- **Slide 18**: Experimental Setup (table)
- **Slide 19-20**: Results Comparison (table)
- **Slide 21**: Performance Metrics (table)

### Keyword Slides
- All other slides use keywords
- Maximum 5-6 bullet points
- Maximum 60 characters per point

---

## Quality Metrics

| Metric | V2 (Current) | V3 (Target) | Improvement |
|--------|--------------|-------------|-------------|
| **Text per slide** | 120+ words | **60 words** | -50% ✨ |
| **Format** | Text lists | **Tables** | Clearer ✨ |
| **Keywords** | None | **All content** | Focused ✨ |
| **Breakthroughs** | Scattered | **Highlighted** | Prominent ✨ |
| **Visual hierarchy** | Low | **High** | Better ✨ |

---

## Implementation

### Modified Files

1. **src/ai_analyzer_enhanced.py**
   - Update prompt to require keywords
   - Add breakthrough extraction
   - Request table-friendly structure

2. **src/content_extractor_enhanced.py**
   - Add `_generate_table_content()` method
   - Add `_generate_keyword_list()` method
   - Add `_highlight_breakthroughs()` method

3. **src/ppt_generator_enhanced.py**
   - Increase font sizes (28px content, 40px title)
   - Add table support in Markdown
   - Add emoji support for breakthroughs

---

## Testing Checklist

- [ ] Tables render correctly in PPTX
- [ ] Keywords are concise (<60 chars)
- [ ] Breakthroughs use 🔥 emoji
- [ ] Key numbers are **bolded**
- [ ] Text density reduced 50%
- [ ] All slides use visual hierarchy

---

## Examples

### Before (V2 - Too Verbose)
```markdown
## Experimental Setup

- We evaluated our system on SWE-bench, a benchmark dataset 
  containing 2,294 GitHub issues from popular open-source 
  repositories...
- The baselines included SWE-agent, which operates on a Linux 
  shell to search and edit code...
(150+ words, hard to scan)
```

### After (V3 - Concise)
```markdown
## Experimental Setup

| Item | Content |
|------|---------|
| **Datasets** | SWE-bench (2,294 issues) |
| **Baselines** | SWE-agent, AutoCodeRover |
| **Metrics** | Resolution Rate, Time Cost |
| **Tasks** | 64 real tasks |

(50 words, easy to scan)
```

---

## Prompt Template V3

```
You are an academic paper analysis expert. Analyze the following research paper and extract KEY INFORMATION.

REQUIREMENTS:
1. Use KEYWORDS, not full sentences
2. Include SPECIFIC NUMBERS for all results
3. Identify 3-5 KEY BREAKTHROUGHS
4. Structure data for TABLES
5. Be CONCISE: max 1-2 sentences per point

Paper text:
{paper_text}

Provide analysis in JSON format:

{
  "key_breakthroughs": [
    "Breakthrough 1: [Description with number]",
    ...
  ],
  
  "experimental_setup": {
    "datasets": "[Name] ([size])",
    "baselines": ["[Method1]", "[Method2]"],
    "metrics": ["[Metric1]", "[Metric2]"],
    "environment": "[Setup]",
    "tasks": "[Number] [type]"
  },
  
  "main_results": [
    "[Result]: [Number]% improvement",
    ...
  ]
}

CRITICAL: 
- Extract 6 items maximum per field
- Use numbers for all quantitative results
- Bold key findings with **text**
- Keep descriptions under 60 characters
```

---

**Last Updated**: 2026-03-06  
**Status**: ✅ Ready for Implementation
