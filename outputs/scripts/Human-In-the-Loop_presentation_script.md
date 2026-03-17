# Presentation Script

---

## Research Narrative

**Hook:** Coding agents promise to automate software work, but real enterprise development is less about generating code than producing plans developers trust and pull requests teams will merge.

**Problem:** This paper asks how to make LLM agents useful for enterprise issue resolution beyond benchmarks, with stage-wise human collaboration inside production workflows. That matters because issue automation must fit real JIRA and Bitbucket processes and earn practitioner acceptance.

**Key Idea:** HULA is a human-in-the-loop multi-agent system where a planner localizes files and drafts a fix, a human approves or edits the plan, and a coder generates validated code before opening a pull request.

**Evidence:** Across 663 real production issues, HULA achieved 82% plan approval, a 59% merged PR rate, and 8% end-to-end issue-to-merge. Offline, it reached 86% file recall and 31% test pass on SWE-bench Verified, but only 30% code similarity on Atlassian internal tasks, revealing a remaining code-quality gap.

**Implications:** The results suggest the near-term future of software agents is human-AI co-development, with humans steering planning and AI accelerating execution inside existing engineering tools. They also highlight that better context and documentation will be critical for reliable enterprise automation.


---

## Slide-by-Slide Notes

### Slide 1: Human-In-the-Loop Software Development Agents

**Purpose:** Paper identity and presentation framing

**Key Points:**
- Wannita Takerngsaksiri et al.
- 2025
- HULA framework
- Atlassian JIRA + Bitbucket deployment

### Slide 2: Motivation

**Purpose:** Why enterprise human-AI coding matters

**Key Points:**
- Enterprise software maintenance burden
- Benchmark-to-production mismatch
- Risks of unsupervised code changes
- Need for stage-wise human oversight
- Missing practitioner adoption evidence

### Slide 3: Research Questions

**Purpose:** Main research questions this paper addresses

**Key Points:**
- RQ1: 🔥 JIRA deployment
- RQ2: How does the proposed approach address 🔥 **82%** plan approval...?
- RQ3: How does the method improve over prior work?

### Slide 4: Problem Definition

**Purpose:** Define the paper's target problem precisely

**Key Points:**
- JIRA issue-to-PR automation task
- Human-guided planning and coding stages
- File localization, plan generation, code synthesis
- Enterprise repositories across 10+ languages
- Success criteria from plan approval to PR merge

### Slide 5: Related Work

**Purpose:** Contrast prior agent designs with HULA

**Key Points:**
- SWE-agent-style autonomous coding agents
- Benchmark-centric evaluation on SWE-bench
- Multi-agent coding without human feedback loops
- Limited enterprise deployment and user studies
- HULA advantage: stage-wise collaboration + production validation

### Slide 6: Core Idea

**Purpose:** One-line contribution distilled into core elements

**Key Points:**
- Planner-coder-human triad
- Approve plans before writing code
- Editable code with tool-guided refinement
- JIRA-native workflow to Bitbucket PRs

### Slide 7: Method Overview

**Purpose:** End-to-end workflow at a glance

**Key Points:**
- Issue and repository selection
- Planner file localization
- Draft implementation plan
- Human review, edits, approval
- Code generation, refinement, PR raising

### Slide 8: Method Details

**Purpose:** Technical mechanisms and implementation insights

**Key Points:**
- DPDE coordination
- Shared repository memory
- LLM-based file localization and plan generation
- Code synthesis with compiler/linter-guided self-refinement
- Human feedback insertion points

### Slide 9: Experiment Setup

**Purpose:** Offline, online, and practitioner evaluation design

**Key Points:**
- GPT-4 backbone; Atlassian JIRA + Bitbucket environment
- SWE-bench Verified: 500 Python issues
- Atlassian internal offline set: 369 issues, 94 repos, 10+ languages
- Online deployment + survey: 663 issues; 109/146 responses
- Baselines and metrics: offline HULA, human PRs, SWE-agent; recall, test pass, similarity, PR outcomes

### Slide 10: Results

**Purpose:** Headline numbers with brief interpretation

**Key Points:**
- 82% plan approval: planning alignment
- 59% merged PR rate: practical utility
- 8% issue-to-merge: end-to-end production success
- 86% file recall vs 31% test pass: localization strength, execution gap
- 30% internal code similarity: code-quality gap to human PRs

### Slide 11: Limitations

**Purpose:** Critical analysis beyond positive deployment results

**Key Points:**
- Code-quality inconsistency across generated PRs
- Sparse or ambiguous issue descriptions
- Single-backbone dependence on GPT-4
- Atlassian-specific tooling and workflow bias
- Limited correctness evaluation and missing test generation

### Slide 12: Future Work

**Purpose:** Future research directions and opportunities

**Key Points:**
- Address: Code-quality inconsistency
- Address: Short issue descriptions
- Reduce input effort required
- Explore other domains
- Long-term impact studies

### Slide 13: Takeaways & Discussion

**Purpose:** Key insights and open discussion directions

**Key Points:**
- Humans-in-the-loop as default design pattern
- Planning-stage approval over full autonomy
- Deployment feasibility for simple enterprise tasks
- Documentation quality as a performance lever
- Discussion: context augmentation, richer evaluation, broader transfer
