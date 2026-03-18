# Presentation Script

---

## Research Narrative

**Hook:** While autonomous coding agents excel in benchmarks, they struggle to deliver reliable results in complex, real-world software development environments.

**Problem:** Existing LLM-based agents lack human feedback mechanisms and have not been validated in industry deployments, limiting their ability to handle the nuance of enterprise software tasks.

**Key Idea:** HULA introduces the first industry-deployed Human-in-the-Loop framework that integrates iterative developer feedback directly into the planning and coding lifecycle of LLM agents.

**Evidence:** Deployed at scale with 2,600 Atlassian practitioners, HULA achieved an 82% plan approval rate and a 59% merged pull request rate, demonstrating effective human-AI synergy.

**Implications:** This successful enterprise deployment proves that human-AI collaboration is viable for software engineering, significantly reducing development effort while highlighting the need for improved code quality in future iterations.


---

## Slide-by-Slide Notes

### Slide 1: Human-In-the-Loop Software Development Agents

**Purpose:** Set the stage for the presentation - emphasize this is pioneering industry work

**Key Points:**
- Paper title and research focus
- Authors: Wannita Takerngsaksiri et al.
- Year: 2025
- First industry deployment of human-in-the-loop software agents

### Slide 2: Motivation

**Purpose:** Explain WHY this problem is important for real-world software development

**Key Points:**
- Growing adoption of LLM-based multi-agent paradigms in software development
- Demand for automated software development tasks in enterprise settings
- Gap between benchmark performance and real-world deployment needs
- Potential of human-AI synergy to overcome autonomous agent limitations

### Slide 3: Research Questions

**Purpose:** Main research questions this paper addresses

**Key Points:**
- RQ1: 💡 Human-in-the-loop enhances AI planning
- RQ2: How does the proposed approach address 🔥 **59%** merged PR rate with human feedback...?
- RQ3: How does the method improve over prior work?

### Slide 4: Problem Definition

**Purpose:** Define the specific gap this paper addresses

**Key Points:**
- Existing agents lack human feedback integration mechanisms
- Current systems rely solely on historical benchmark datasets
- Limited industry deployment and validation of software agents
- Need for practical human-in-the-loop solutions in enterprise environments

### Slide 5: Related Work

**Purpose:** Compare approaches and highlight limitations of previous work

**Key Points:**
- SWE-agent Claude: 6th ranked on SWE-bench - fully autonomous approach
- Existing multi-agent systems: lack human feedback loop
- Benchmark-focused approaches: no industrial deployment validation
- HULA advantage: human-in-the-loop + real-world enterprise evaluation

### Slide 6: Core Idea

**Purpose:** Main contribution in clear, focused points

**Key Points:**
- Human-in-the-loop integration enhances AI planning and execution
- Multi-stage workflow with iterative human feedback checkpoints
- Cooperative coordination between AI agents and human practitioners
- Enterprise-scale deployment validation in production environment

### Slide 7: Method Overview: HULA Framework

**Purpose:** High-level architecture and key components

**Key Points:**
- AI Planner Agent: File localization and task planning
- AI Coding Agent: Code generation and refinement
- Human Agent: Feedback provision and approval decisions
- Shared memory: JIRA integration and repository context

### Slide 8: Method Details

**Purpose:** Technical details and implementation insights

**Key Points:**
- DPDE: Decentralized planning and execution algorithm
- LLM-as-a-Judge: Code similarity scoring mechanism
- Self-refinement: Compiler and linter feedback integration
- Multi-stage task dissection and context augmentation techniques

### Slide 9: Experiment Setup

**Purpose:** Comprehensive experimental configuration

**Key Points:**
- Datasets: SWE-bench Verified (500 issues) + Internal Atlassian (369 issues)
- Baseline: SWE-agent Claude (6th ranked on SWE-bench)
- Metrics: Plan approval rate, merged PR rate, file recall
- Deployment: GPT-4 backbone, 2,600 practitioners, 75% survey response

### Slide 10: Results

**Purpose:** Key findings with brief interpretations

**Key Points:**
- 59% merged PR rate demonstrating industry success
- 82% plan approval rate showing human-AI alignment
- 8% full end-to-end automation success rate
- 86% file recall on SWE-bench, 61% code readability rating

### Slide 11: Limitations

**Purpose:** Honest weaknesses and critical analysis

**Key Points:**
- Code functionality issues in generated solutions
- Incomplete code changes for complex tasks
- High input effort required from human practitioners
- Performance degradation on complex multi-file tasks

### Slide 12: Future Work

**Purpose:** Future research directions and opportunities

**Key Points:**
- Address: Code functionality issues
- Address: Incomplete code changes
- Reduce input effort required
- Explore other domains
- Long-term impact studies

### Slide 13: Takeaways & Discussion

**Purpose:** Key insights and discussion questions for the group

**Key Points:**
- Human-in-the-loop proven effective for enterprise deployment
- Input quality and documentation practices are critical success factors
- Code quality enhancement remains key area for future work
- Discussion: How to balance automation vs. human oversight?
