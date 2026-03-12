---
marp: true
theme: academic
paginate: true
size: 16:9
style: |
  section {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 28px;
    color: #333;
    background: #fff;
    line-height: 1.6;
  }
  h1 {
    color: #2c3e50;
    font-size: 48px;
    font-weight: bold;
  }
  h2 {
    color: #34495e;
    font-size: 40px;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
  }
  ul, ol {
    margin-left: 2em;
  }
  li {
    margin-bottom: 0.8em;
    font-size: 26px;
    line-height: 1.5;
  }
  strong {
    color: #e74c3c;
    font-weight: bold;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 22px;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  th {
    background-color: #3498db;
    color: white;
    font-weight: bold;
  }
---

<!-- Slide 1: Human-In-the-Loop Software Development Agents -->
## Human-In-the-Loop Software Development Agents

- 2024

<!-- Notes: Welcome slide -->

---

<!-- Slide 2: Outline -->
## Outline

- Background & Problem
- Key Insights
- Method & Technical Details
- Experiments & Results
- Analysis & Discussion
- Conclusion & Future Work

<!-- Notes: Presentation outline -->

---

<!-- Slide 3: Research Background -->
## Research Background

- Large Language Models (LLMs) have recently
- Existing frameworks such as SWE-agent and
- g
- , engineers, testers) to interact with
- However, the state of the field

<!-- Notes: Research background -->

---

<!-- Slide 4: Research Problem -->
## Research Problem

- The core problem is the limitations
- Specifically, existing work: (1) relies on
- The paper addresses the challenge of

<!-- Notes: Research problem -->

---

<!-- Slide 5: Key Insights -->
## Key Insights

- 💡 Agile-driven organizations often use brief issue descriptions (user stories) rather than the detailed documentation found in open-source projects, necessitating agents that can handle sparse context or prompt users for detail.
- 💡 Human feedback is not just for verification but for context enrichment; allowing engineers to edit plans significantly improves the alignment of generated code with intent.
- 💡 A 'Decentralized Planning Decentralized Execution' (DPDE) paradigm is more efficient than centralized control, reducing computational overhead while allowing agents to adapt to human feedback.
- 💡 User perception of success is tied more to 'reduction of initial development effort' and 'ease of modification' than to the agent generating a perfect, hands-off solution.

<!-- Notes: Key insights and breakthroughs -->

---

<!-- Slide 6: Method Overview -->
## Method Overview

- The paper introduces HULA (Human-in-the-Loop LLM-based
- Unlike fully autonomous systems, HULA exploits
- The process involves four stages: Setting
- The framework is designed to prioritize

<!-- Notes: Method overview -->

---

<!-- Slide 7: Technical Details -->
## Technical Details

- Human-in-the-Loop Integration: A specific workflow design that mandates human review and modification capabilities at both the planning and coding stages, differing from 'correction-only' approaches.
- Multi-Stage Evaluation Framework: A comprehensive methodology combining offline benchmarking (SWE-bench), online deployment (2,600+ users), and user surveys to capture both technical efficacy and human perception.
- LLM-as-a-Judge for Similarity: Addressing the limitations of BERTScore (512 token limit), the authors use GPT-4 to evaluate code similarity between generated code and ground truth for large enterprise files (median 1,275 tokens).
- DPDE Agent Coordination: Utilizing Decentralized Planning Decentralized Execution to minimize communication overhead and central LLM computational load while maximizing adaptability to human input.
- Industrial Deployment: The actual implementation and scaling of the framework within Atlassian's internal production environment (JIRA + BitBucket).

<!-- Notes: Technical details -->

---

<!-- Slide 8: Experimental Setup -->
## Experimental Setup

- The evaluation was conducted in three
- (1) Offline Evaluation: HULA ran on
- (2) Online Deployment: HULA was deployed
- Usage data was tracked for 2

<!-- Notes: Experimental setup -->

---

<!-- Slide 9: Main Results -->
## Main Results

- 🔥 **RQ1 (Offline - SWE-bench): HULA achieved 97% Success Generation Rate, 86% Recall for File Localization, 84% Perfect File Localization, 31% Pass@1 (Passing Test Cases), and 45% High Code Similarity.**
- 🔥 **RQ1 (Offline - Internal Dataset): Performance dropped significantly: 100% Success Generation, but only 30% Recall for File Localization and 30% High Code Similarity. This highlights the difficulty of enterprise tasks with brief descriptions.**
- 🔥 **RQ2 (Online - Adoption): 82% Plan Approval Rate (433/527 issues). Engineers approved the AI's plan in the vast majority of cases.**
- 🔥 **RQ2 (Online - Code): 25% Raised PR Rate (95/376 issues). Engineers felt confident enough to raise a PR for a quarter of the generated code.**
- 🔥 **RQ2 (Online - Impact): 59% Merged PR Rate (56/95 PRs). More than half of the raised PRs were merged into the codebase.**
- 🔥 **RQ3 (Survey - File Localization): 71% agreed identified files were relevant; 62% agreed they aligned with their own approach.**

<!-- Notes: Main results -->

---

<!-- Slide 10: Key Findings -->
## Key Findings

- HULA demonstrates that LLM-based agents are
- However, the online evaluation reveals that
- High approval rates for plans (82%)
- The 59% merge rate for raised

<!-- Notes: Key findings -->

---

<!-- Slide 11: Advantages -->
## Advantages

- Human-AI Synergy: By allowing intervention at planning and coding stages, HULA avoids the 'black box' problem of autonomous agents, ensuring the output matches engineer intent.
- Production Integration: Seamlessly integrated into JIRA and BitBucket, fitting naturally into the existing workflow of 2,600+ Atlassian engineers.
- High Plan Accuracy: Achieved 82% plan approval rate, indicating strong capability in understanding requirements and identifying relevant files.
- Code Readability: 61% of engineers found the code easy to modify, reducing the 'blank page' friction of starting new tasks.

<!-- Notes: Advantages -->

---

<!-- Slide 12: Limitations -->
## Limitations

- Input Dependency: The framework's effectiveness is heavily dependent on the quality and detail of the input JIRA issue description; brief 'Agile-style' stories degrade performance.
- Code Completeness: The agent struggles with non-functional requirements and complex logic; 67% of engineers felt the code did not completely solve the task without human edits.
- Context Awareness: Limited awareness of external dependencies or broader architectural context often led to incomplete code changes.

<!-- Notes: Limitations -->

---

<!-- Slide 13: Future Work -->
## Future Work

- Context Augmentation: Investigate methods to automatically enrich input context (e.g., using type definitions, design patterns, or historical solutions) to reduce the burden on engineers to write detailed prompts.
- Advanced Evaluation Metrics: Develop evaluation frameworks that go beyond 'passing tests' to measure technical debt, maintainability, and the effort required to fix generated code.
- Workflow Flexibility: Improve the UI/UX to allow non-linear workflows, enabling engineers to revisit the planning stage during coding if requirements change.

<!-- Notes: Future work -->

---

<!-- Slide 14: Figure 1 -->
## Figure 1

- ![Figure 1](output/images/Human-In-the-Loop_figure_1.png)

<!-- Notes: Figure from page 4 -->

---

<!-- Slide 15: Figure 2 -->
## Figure 2

- ![Figure 2](output/images/Human-In-the-Loop_figure_2.png)

<!-- Notes: Figure from page 4 -->

---

<!-- Slide 16: Figure 3 -->
## Figure 3

- ![Figure 3](output/images/Human-In-the-Loop_figure_3.png)

<!-- Notes: Figure from page 4 -->

---

<!-- Slide 17: Q&A -->
## Q&A

- Thank you
- Questions?

<!-- Notes: Open for questions -->