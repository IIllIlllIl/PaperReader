# Presentation Script

Total Slides: 11
Suggested Duration: 10-15 minutes

---

## Slide 1: Human-In-the-Loop Software Development Agents

**Type**: title
**Word Count**: 18 words

**Speaker Notes:**
Welcome slide - introduce paper

**Talking Points:**
- Authors: Wannita Takerngsaksiri, Jirat Pasuksmit, Patanamon Thongtanunam, Chakkrit Tantithamthavorn, et al.
- Year: 2025

---

## Slide 2: Motivation

**Type**: content
**Word Count**: 31 words

**Speaker Notes:**
Why this problem is important - real-world impact and research gap

**Talking Points:**
- Existing agents lack human feedback and real-world deployment validation
- Benchmarks like SWE-bench do not reflect complex enterprise contexts
- Need to balance automation with human oversight in critical SE tasks

---

## Slide 3: Problem Definition

**Type**: content
**Word Count**: 26 words

**Speaker Notes:**
The specific problem this paper solves

**Talking Points:**
- Integrating human feedback into multi-stage automated software development
- Bridging the gap between benchmark performance and industrial deployment
- Evaluating LLM agents in real-world enterprise environments

---

## Slide 4: Related Work & Our Advantage

**Type**: content
**Word Count**: 46 words

**Speaker Notes:**
How this paper differs from previous work - focus on limitations and improvements

**Talking Points:**
- SWE-agent / AutoCodeRover: autonomous agents - lack human-in-the-loop capabilities
- Magis / Masai: multi-agent systems - evaluated only on historical open-source data
- HULA IMPROVEMENT: integrates human feedback at planning and coding stages
- HULA IMPROVEMENT: deploys and evaluates in a large-scale industrial setting

---

## Slide 5: Core Idea

**Type**: content
**Word Count**: 23 words

**Speaker Notes:**
Main contribution in one clear sentence - the key insight

**Talking Points:**
- A Human-in-the-Loop LLM-based Agent framework (HULA) that integrates human feedback for planning and coding within real-world JIRA workflows.

---

## Slide 6: Method Overview

**Type**: content
**Word Count**: 26 words
**Has Figure**: Yes - fig. 1. an overview of our human-in-the-loop llm-b...

**Speaker Notes:**
High-level approach and key components

**Talking Points:**
- Multi-agent system: AI Planner, AI Coding Agent, and Human Agent
- Cooperative Decentralized Planning Decentralized Execution (DPDE) paradigm
- Iterative refinement loop with linters/compilers for code validation

---

## Slide 7: Method Details

**Type**: content
**Word Count**: 46 words

**Speaker Notes:**
Technical details and implementation insights

**Talking Points:**
- AI Planner Agent: identifies relevant files and generates coding plan
- AI Coding Agent: implements code changes based on approved plan
- Human Agent: reviews, edits, and approves plans and code at each stage
- LLM-as-a-Judge (GPT-4) used for evaluating code similarity in offline tests

---

## Slide 8: Experiment Setup

**Type**: table
**Word Count**: 34 words

**Speaker Notes:**
Experimental configuration - datasets, baselines, metrics

**Talking Points:**
- | Component | Details |
|-----------|---------|
| **datasets** | SWE-bench Verified (500 issues), Atlassian Internal (369 issues) |
| **baselines** | SWE-bench leaderboard (comparable to 6th ranked agent) |
| **metrics** | Recall, Plan Approval Rate, PR Merge Rate, Code Similarity |
| **environment** | Atlassian JIRA production environment (2,600+ practitioners) |

---

## Slide 9: Results & Interpretations

**Type**: content
**Word Count**: 57 words

**Speaker Notes:**
Main experimental results with interpretations - what they mean

**Talking Points:**
- ****82%**** plan approval rate - indicates high trust in AI-generated planning
- ****59%**** merged PR rate - demonstrates strong real-world applicability
- ****86%**** file localization recall (SWE-bench) - competitive with top agents
- ****30%**** file localization recall (Internal) - reveals domain gap between OSS and enterprise
- ****61%**** agreed code is easy to modify - highlights value as an assistant rather than replacement

---

## Slide 10: Limitations & Critical Analysis

**Type**: content
**Word Count**: 41 words

**Speaker Notes:**
Honest weaknesses, scope constraints, evaluation gaps

**Talking Points:**
- Performance drops significantly on internal data vs. open-source benchmarks
- Generated code often functionally incorrect or incomplete without human edits
- Requires detailed issue descriptions, which are often scarce in Agile teams
- Evaluation relies heavily on GPT-4 as the backbone LLM

---

## Slide 11: Takeaways & Discussion

**Type**: discussion
**Word Count**: 86 words

**Speaker Notes:**
Summary of key insights and open questions for audience discussion

**Talking Points:**
- **Key Takeaways:**
- ✓ Human-in-the-loop is critical for quality assurance in enterprise coding
- ✓ Enterprise context complexity far exceeds current benchmark capabilities
- ✓ AI agents excel at initiation/planning but struggle with complete implementation
- **Discussion Questions:**
- ❓ How can we design benchmarks that better simulate the ambiguity of real-world enterprise tickets?
- ❓ Does the requirement for detailed prompts for HULA negate the productivity gains it aims to provide?
- ❓ How might the 'Human-in-the-Loop' paradigm evolve as LLMs approach higher reasoning capabilities?

---
