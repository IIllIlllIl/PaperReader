---
marp: true
theme: academic
paginate: true
size: 16:9
style: |
  section {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 22px;
    color: #333;
    background: #fff;
  }
  h1 {
    color: #2c3e50;
    font-size: 44px;
    font-weight: bold;
  }
  h2 {
    color: #34495e;
    font-size: 32px;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
  }
  ul, ol {
    margin-left: 1.5em;
  }
  li {
    margin-bottom: 0.4em;
    font-size: 20px;
    line-height: 1.4;
  }
  strong {
    color: #e74c3c;
  }
---

<!-- Slide 1: Human-In-the-Loop Software Development Agents -->
## Human-In-the-Loop Software Development Agents

- 作者:
- 年份: 2025
- Research Paper Presentation

<!-- Notes: Welcome slide. Introduce the paper title and authors. -->

---

<!-- Slide 2: 报告大纲 -->
## 报告大纲

- 📚 研究背景与动机
- ❓ 核心问题与挑战
- 💡 关键洞察与假设
- 🔧 方法与技术细节
- 🔬 实验设置与结果
- 📊 分析与讨论
- 🎯 结论与未来工作

<!-- Notes: Outline of the presentation. Give audience an overview of what to expect. -->

---

<!-- Slide 3: 研究背景 (Research Background) -->
## 研究背景 (Research Background)

- Large Language Models (LLMs) and multi-agent paradigms have recently demonstrated remarkable capabilities in software engineering (SE) tasks.
- In this context, an LLM-based multi-agent functions as an autonomous entity receiving inputs from environments like compilers or linters to perform actions such as writing code or fixing bugs to achieve specific objectives.
- Various frameworks like SWE-agent, AutoCodeRover, and Magis have been proposed to address complex software development tasks using these agents.
- However, the integration of these systems into real-world enterprise workflows remains limited, as most existing research focuses on open-source benchmarks.
- The potential for these agents to act as collaborative assistants rather than autonomous replacements is a growing area of interest, particularly in industrial settings where human oversight is critical.

<!-- Notes: Explain the broader research context and why this topic is important. -->

---

<!-- Slide 4: 相关工作 (Related Work) -->
## 相关工作 (Related Work)

- SWE-agent (Yang et al.): An LLM-based agent built on a Linux shell to search, navigate, and edit code. Limitation: Evaluated primarily on open-source benchmarks without deployment in industry.
- AutoCodeRover (Zhang et al.): Utilizes code search on Abstract Syntax Trees (AST) and spectrum-based fault localization. Limitation: Lacks human-in-the-loop mechanisms for iterative refinement.
- Magis (Tao et al.): A multi-agent framework with roles like manager and developer. Limitation: Focuses on autonomous resolution without integrating continuous human feedback.
- RepoUnderstander (Ma et al.): Uses Monte Carlo tree search on repository knowledge graphs. Limitation: Not tested in practical, closed-loop enterprise environments.
- Masai (Arora et al.): A modular framework dividing problems into sub-problems. Limitation: Does not address the 'Human-AI synergy' required for enterprise adoption.

<!-- Notes: Overview of related work and their limitations. -->

---

<!-- Slide 5: 研究动机 (Motivation) -->
## 研究动机 (Motivation)

- The motivation for this work stems from three critical gaps in existing LLM-based software development agents: (1) they are evaluated on historical benchmark datasets, limiting understanding of their effectiveness in enterprise contexts; (2) they rarely consider human feedback at each stage of the development process; and (3) they have not been deployed in practice.
- This paper addresses the need for a system that integrates into existing industrial workflows (specifically Atlassian JIRA) to understand how practitioners interact with, refine, and perceive these agents.
- The authors argue that for LLMs to be effective in software engineering, they must function as assistants in a Human-AI synergy, leveraging human intelligence and authority.

<!-- Notes: Explain what motivated this specific research. -->

---

<!-- Slide 6: 核心问题 (Core Problem) -->
## 核心问题 (Core Problem)

- The core problem is the lack of an LLM-based software development framework that is both effective in an enterprise setting and capable of incorporating human feedback throughout the entire workflow.
- Existing systems operate autonomously without the necessary checks and balances required for complex, high-stakes enterprise codebases.
- The challenge is to design a system that can resolve JIRA issues (from planning to Pull Request) while allowing software engineers to review, edit, and guide the agent at every step (file localization, planning, coding), thereby minimizing development effort while ensuring code quality and alignment with task requirements.

<!-- Notes: State the core research problem clearly and specifically. -->

---

<!-- Slide 7: 主要挑战 (Key Challenges) -->
## 主要挑战 (Key Challenges)

- ⚡ Generalization to Enterprise Context: Models performing well on open-source Python benchmarks (SWE-bench) often struggle with the diversity of languages (10+), file types, and complex dependencies found in large organizations like Atlassian.
- ⚡ Context Scarcity: Enterprise JIRA issues (Agile-driven) often contain brief descriptions (median 75 tokens) compared to detailed open-source issue reports (median 295 tokens), making file localization and planning harder.
- ⚡ Integration of Human Feedback: Designing a workflow that seamlessly integrates human intervention without causing excessive context switching or cognitive load.
- ⚡ Code Quality and Functional Correctness: Generating code that passes linters/compilers is insufficient; the code must be maintainable, defect-free, and pass unit tests, which current agents struggle with autonomously.
- ⚡ Deployment Scalability: Deploying LLM-based agents to thousands of users (2,600+ practitioners) without disrupting existing workflows or overwhelming computational resources.

<!-- Notes: Highlight the key technical or practical challenges. -->

---

<!-- Slide 8: 研究空白 (Research Gap) -->
## 研究空白 (Research Gap)

- The specific gap addressed is the absence of a 'Human-in-the-Loop' evaluation and deployment of LLM-based agents in a real-world industrial software development environment.
- While previous works have automated SE tasks, none have comprehensively studied the interaction dynamics where humans refine AI-generated plans and code within a live production environment (JIRA/Bitbucket), specifically measuring approval rates and merged PR rates based on human-AI collaboration.

<!-- Notes: Explain the specific gap in existing research. -->

---

<!-- Slide 9: 关键洞察 (Key Insights) -->
## 关键洞察 (Key Insights)

- 💡 Human-AI Synergy is Superior: Rather than aiming for full automation, treating LLMs as cooperative agents under human authority leads to better alignment with complex task requirements.
- 💡 Input Detail Dictates Performance: The performance of agents correlates strongly with the detail level of the issue description; brief Agile user stories result in significantly lower file localization accuracy than detailed open-source bug reports.
- 💡 Iterative Refinement is Critical: A multi-stage workflow (Plan -> Review -> Code -> Refine) with mandatory human checkpoints significantly increases the likelihood of generating acceptable code compared to one-shot generation.
- 💡 Evaluation beyond Accuracy: Success in enterprise is defined not just by code similarity or passing tests, but by 'Plan Approval Rate' and 'PR Merge Rate', reflecting actual utility to developers.
- 💡 LLM-as-a-Judge: For large codebases where BERT-based models fail (512 token limit), GPT-4 can serve as an effective judge for code similarity against ground truth.

<!-- Notes: Present the key insights that motivated the approach. -->

---

<!-- Slide 10: 研究假设 (Hypotheses) -->
## 研究假设 (Hypotheses)

- 🤔 Incorporating human feedback at intermediate stages (planning and coding) will significantly increase the acceptance and merge rate of generated code compared to fully autonomous agents.
- 🤔 An LLM-based agent can effectively reduce the 'initial development time' and cognitive load for straightforward tasks, even if it requires human refinement for complex tasks.
- 🤔 Providing a decentralized planning and execution (DPDE) framework where agents share memory but act independently allows for better adaptability in dynamic enterprise environments.
- 🤔 The framework will reveal that while LLMs are good at 'initiating' code, they still face significant challenges in ensuring complete functional correctness and adherence to non-functional requirements without human oversight.

<!-- Notes: State the research hypotheses or assumptions. -->

---

<!-- Slide 11: 方法概述 (Method Overview) -->
## 方法概述 (Method Overview)

- The proposed method, HULA (Human-in-the-Loop LLM-based Agents), is a framework integrated into Atlassian JIRA consisting of three cooperative agents: AI Planner Agent, AI Coding Agent, and Human Agent.
- The framework operates in four stages: (1) Task Setup, selecting a JIRA issue; (2) Planning, where the AI Planner identifies relevant files and generates a coding plan for human review; (3) Coding, where the AI Coding Agent generates code changes based on the approved plan, followed by an iterative self-refinement loop using linters/compilers and human feedback; and (4) Raising a PR.
- The architecture follows a Decentralized Planning Decentralized Execution (DPDE) paradigm to minimize communication overhead while utilizing shared memory (JIRA context and repository).

<!-- Notes: Provide high-level overview of the proposed method. -->

---

<!-- Slide 12: 方法细节 - Part 1 (Method Details) -->
## 方法细节 - Part 1 (Method Details)

- Stage 1 - Task Setup: The workflow initiates when a software engineer selects a JIRA issue (software development task) and links it to the relevant source code repository.
- Stage 2.1 - File Localization: The AI Planner Agent analyzes the JIRA issue summary and description to identify relevant source files requiring modification.
- Stage 2.2 - Plan Generation: The AI Planner Agent generates a specific coding plan (e.g., 'Add tests for method X') based on the localized files.
- Human Review (Planning): The Human Agent reviews the file list and coding plan. They can edit files, modify the plan, or request regeneration before approval.
- Stage 3.1 - Code Generation: The AI Coding Agent receives the approved plan and generates specific code changes for the identified files.
- Stage 3.2 - Self-Refinement: The AI Coding Agent automatically validates generated code using compilers and linters, iteratively refining the code until it passes validation or reaches a retry limit.
- Human Review (Coding): The Human Agent reviews the refined code. If unsatisfied, they can provide natural language feedback to trigger regeneration or manually edit the code.
- Stage 4 - PR Creation: Once the human approves the code, the system facilitates raising a Pull Request to BitBucket or creating a new branch for further manual work.

<!-- Notes: Detailed explanation of the method steps (first part). -->

---

<!-- Slide 13: 方法细节 - Part 2 (Method Details) -->
## 方法细节 - Part 2 (Method Details)

- UI Integration: The interface is embedded directly into the JIRA issue view, providing a seamless experience with expandable sections for viewing relevant files, plans, and code diffs.

<!-- Notes: Detailed explanation of the method steps (second part). -->

---

<!-- Slide 14: 技术创新 (Technical Innovations) -->
## 技术创新 (Technical Innovations)

- 🚀 Human-in-the-Loop DPDE Architecture: A cooperative multi-agent system that enforces human checkpoints between planning and execution stages, diverging from fully autonomous agent models.
- 🚀 Multi-Stage Evaluation Framework: A comprehensive evaluation methodology combining offline benchmarking (SWE-bench), online deployment metrics (PR rates), and qualitative user surveys.
- 🚀 LLM-as-a-Judge for Similarity: Utilizing GPT-4 to evaluate code similarity between generated code and ground truth for large codebases (exceeding 512 tokens), overcoming BERT limitations.
- 🚀 Iterative Self-Refinement with Tool Feedback: Integrating compiler and linter feedback directly into the agent's generation loop to ensure syntactic correctness before human review.
- 🚀 Context-Aware File Localization: Using LLMs to bridge the gap between informal JIRA descriptions and complex repository structures to identify necessary changes.

<!-- Notes: Highlight the key technical innovations. -->

---

<!-- Slide 15: 系统架构 (System Architecture) -->
## 系统架构 (System Architecture)

- HULA utilizes a Decentralized Planning Decentralized Execution (DPDE) architecture consisting of three core agents: the AI Planner Agent (P), the AI Coding Agent (C), and the Human Agent (H).
- These agents interact via a shared memory containing the JIRA issue context and source code repository.
- The system is implemented as a seamless plugin within the Atlassian JIRA interface.
- The flow is sequential: P generates a plan -> H reviews/modifies -> C generates code -> Tools validate -> H reviews/modifies -> PR raised.
- This design minimizes the computational overhead of a central controller while maximizing human control over the development trajectory.

<!-- Notes: Describe the overall system architecture. -->

---

<!-- Slide 16: 关键组件 (Key Components) -->
## 关键组件 (Key Components)

- 🔧 AI Planner Agent: An LLM responsible for file localization and generating high-level coding strategies based on issue context.
- 🔧 AI Coding Agent: An LLM responsible for translating the approved plan into concrete code changes and performing self-refinement based on tool outputs.
- 🔧 Human Agent: The software engineer who provides authoritative feedback, reviews artifacts, and makes final decisions on merging code.
- 🔧 Shared Memory: A centralized context store containing the JIRA issue description and the source code repository state, accessible to all agents.
- 🔧 Validation Tools: External tools (compilers, linters) integrated into the loop to provide automated feedback to the AI Coding Agent.
- 🔧 JIRA-Bitbucket Interface: The user-facing component that visualizes the workflow steps (files, plan, code diff) and captures user actions.

<!-- Notes: Explain the key system components or modules. -->

---

<!-- Slide 17: 核心算法 (Core Algorithms) -->
## 核心算法 (Core Algorithms)

- ⚙️ File Localization Algorithm: An LLM-driven search that maps natural language issue descriptions to specific file paths in the repository.
- ⚙️ Iterative Self-Refinement Loop: A process where generated code is fed into linters/compilers; errors are returned to the LLM for correction until syntax checks pass.
- ⚙️ LLM-as-a-Judge (GPT-4): A prompt-based evaluation technique where GPT-4 compares generated code against ground truth to output a similarity score (1-4).
- ⚙️ Code Generation with Context Injection: Injecting the specific file content and the human-approved plan into the LLM prompt to guide code synthesis.

<!-- Notes: Describe the core algorithms or techniques. -->

---

<!-- Slide 18: 数据集 (Datasets) -->
## 数据集 (Datasets)

- 📊 SWE-bench Verified: 500 high-quality development tasks (GitHub issues) from 12 Python repositories, verified for appropriate unit tests and descriptions. Median issue length: 295 tokens.
- 📊 Atlassian Internal Dataset (Offline): 369 completed JIRA issues from 94 software repositories covering 10+ languages (Java, TypeScript, Kotlin, etc.). Median issue length: 75 tokens.
- 📊 Atlassian Online Deployment Data: Real-world usage data from 663 JIRA issues attempted by 2,600 practitioners over 2 months.
- 📊 Survey Responses: Qualitative and quantitative feedback from 109 Atlassian practitioners (75% response rate).

<!-- Notes: Describe the datasets used in experiments. -->

---

<!-- Slide 19: 基线方法与评估指标 (Baselines & Metrics) -->
## 基线方法与评估指标 (Baselines & Metrics)

- 基线方法 (Baselines):
- SWE-agent (Leaderboard comparison): HULA's offline performance (31% pass@1) is compared against the SWE-agent Claude (ranked 6th on SWE-bench).
- Internal Human Performance (Proxy): Implicit baseline comparing the AI-generated code similarity (30-45%) against the ground truth of human-written code.
- Standard LLM Generation: The offline evaluation serves as a baseline for the online evaluation, highlighting the impact of adding human feedback (e.g., increase in acceptance rates).

- 评估指标 (Metrics):
- Recall of File Localization: Percentage of correct files identified by the AI Planner Agent relative to the actual files changed.
- Success Generation Rate (%): Percentage of issues where the agent successfully completes the entire workflow without crashing or failing to generate.
- Plan Approval Rate (%): Percentage of generated plans that were approved by human practitioners in the online evaluation.
- Raised PR Rate (%): Percentage of code generations that resulted in a practitioner raising a Pull Request.

<!-- Notes: List baseline methods and evaluation metrics. -->

---

<!-- Slide 20: 实验设置 (Experimental Setup) -->
## 实验设置 (Experimental Setup)

- The evaluation consisted of three stages: (1) Offline Evaluation using SWE-bench Verified and an internal Atlassian dataset (369 issues) to measure baseline capability without human feedback.
- (2) Online Deployment where HULA was integrated into JIRA and rolled out to 2,600 practitioners between July and Sept 2024.
- (3) User Survey involving 109 participants to assess perception.
- The backbone LLM used was GPT-4.
- For the offline code similarity assessment, a prompt engineering approach was used with GPT-4 as a judge, validated against human scores (correlation 0.7).

<!-- Notes: Detailed description of the experimental setup. -->

---

<!-- Slide 21: 主要结果 - Part 1 (Main Results) -->
## 主要结果 - Part 1 (Main Results)

- ✅ Offline Performance (SWE-bench): HULA achieved 84% perfect file localization and 31% perfect passing of test cases. Code similarity to human code was 45%.
- ✅ Offline Performance (Internal): On the diverse internal dataset, performance dropped to 15% perfect file localization and 30% high code similarity.
- ✅ Online Plan Approval: Of the 527 issues where plans were generated, practitioners approved 433, resulting in a high **Plan Approval Rate of 82%**.
- ✅ Online PR Success: Code was generated for 376 issues. Practitioners raised PRs for 95 issues (**Raised PR Rate of 25%**).
- ✅ Final Merge Rate: Of the 95 raised PRs, **56 were merged**, leading to a **Merged PR Rate of 59%**.
- ✅ User Perception (Time/Effort): **61%** of survey participants agreed the generated code was easy to read and modify, reducing initial development time.

<!-- Notes: Present the main experimental results (first part). -->

---

<!-- Slide 22: 主要结果 - Part 2 (Main Results) -->
## 主要结果 - Part 2 (Main Results)

- ✅ User Perception (Quality): Only **33%** agreed the code solved the task without human modification, and **67%** disagreed that the code was free of defects/non-functional issues.
- ✅ Impact of Context: Analysis showed that the brevity of internal JIRA issues (median 75 tokens) correlated with lower file localization accuracy (30% recall) compared to detailed SWE-bench issues (86% recall).

<!-- Notes: Present the main experimental results (second part). -->

---

<!-- Slide 23: 性能分析 (Performance Analysis) -->
## 性能分析 (Performance Analysis)

- HULA demonstrates that while LLMs can autonomously pass benchmarks, their true value in industry lies in reducing 'cold start' effort.
- The high plan approval rate (82%) suggests the AI Planner Agent is effective at understanding context and locating files, especially when humans provide the necessary context.
- However, the drop from 82% plan approval to 25% PR creation indicates a significant 'last mile' problem: generated code often requires substantial debugging or integration effort.
- The 59% merge rate for those who persisted shows that the code is valuable as a draft.
- Performance is significantly better on Python/open-source data than diverse enterprise data, highlighting a generalization challenge.

<!-- Notes: Analyze the performance of the method. -->

---

<!-- Slide 24: 消融实验 (Ablation Studies) -->
## 消融实验 (Ablation Studies)

- 🔬 Impact of Human Feedback (Implicit): Comparing offline (no human feedback) to online results suggests human intervention is critical for moving from 'potential' solutions to 'merged' solutions.
- 🔬 Impact of Input Detail: The study implicitly ablates the 'quality of input' by comparing performance on SWE-bench (detailed) vs. Internal (brief). Detailed descriptions improved file localization recall from 30% to 86%.
- 🔬 LLM-as-a-Judge Validation: Validation of the GPT-4 similarity metric against human evaluators showed a correlation coefficient of 0.7, justifying its use over BERT-based metrics.

<!-- Notes: Present findings from ablation studies. -->

---

<!-- Slide 25: 案例研究 (Case Studies) -->
## 案例研究 (Case Studies)

- 📋 Straightforward Tasks: Participants noted HULA excels at 'boilerplate' or straightforward tasks, where the barrier to entry is context switching rather than algorithmic complexity.
- 📋 Documentation Enforcement: The tool inadvertently improved team practices; users reported writing more detailed JIRA descriptions to get better results from the agent.
- 📋 The 'Last Mile' Gap: A qualitative observation where the AI generates 90% correct code but fails on a specific dependency or non-functional requirement, requiring the human to 'finish' the PR.

<!-- Notes: Show interesting case study examples. -->

---

<!-- Slide 26: 优势 (Advantages) -->
## 优势 (Advantages)

- ✓ Reduces Initial Cognitive Load: Significantly lowers the effort to start a task by handling file localization and initial draft generation.
- ✓ High Plan Accuracy: Achieves an 82% approval rate for coding plans, indicating strong understanding of requirements.
- ✓ Seamless Integration: Integrated directly into JIRA, avoiding context switching between IDEs and project management tools.
- ✓ Promotes Documentation: Incentivizes developers to write clearer, more detailed issue descriptions to improve agent performance.
- ✓ Collaborative over Autonomous: Prioritizes human authority, making it safer and more applicable to enterprise quality standards than fully autonomous agents.

<!-- Notes: Highlight the advantages of the approach. -->

---

<!-- Slide 27: 局限性 (Limitations) -->
## 局限性 (Limitations)

- ✗ Code Quality Issues: Generated code frequently contains defects or fails non-functional requirements (67% disagreement on quality).
- ✗ Context Dependency: Performance heavily relies on the quality of the JIRA description; brief Agile stories lead to poor localization.
- ✗ Complex Task Handling: Struggles with large, complex tasks or those requiring deep knowledge of external dependencies.
- ✗ Evaluation Constraints: Offline evaluation relied on GPT-4 as a judge (imperfect proxy) and lacked unit test execution for the internal dataset.
- ✗ Generalization: Performance was significantly lower on the diverse, multi-language internal dataset compared to the Python-specific SWE-bench.

<!-- Notes: Discuss the limitations honestly. -->

---

<!-- Slide 28: 讨论 (Discussion) -->
## 讨论 (Discussion)

- The results underscore a fundamental shift in how we evaluate SE agents: accuracy on benchmarks is less important than the 'merging likelihood' in practice.
- The study highlights that the 'Human-in-the-Loop' aspect is not just a safety feature but a functional necessity for handling the ambiguity of real-world enterprise software.
- The disparity between SWE-bench and internal performance reveals that current benchmarks may not adequately represent the messy, under-documented reality of industry codebases.
- The authors argue that future agents should focus on 'context enhancement' (automatically augmenting issue descriptions) rather than just code generation.

<!-- Notes: Discuss the broader implications of the results. -->

---

<!-- Slide 29: 结论 (Conclusions) -->
## 结论 (Conclusions)

- HULA represents a successful deployment of LLM-based agents in a large-scale industrial setting.
- The paper concludes that while LLMs are not yet capable of fully automating software development, they are highly effective as collaborative partners that can minimize the initial development effort.
- The key to success is the 'Human-in-the-Loop' design, which allows practitioners to guide the agent and rectify errors.
- The study validates that a multi-stage approach (Plan-Review-Code-Review) yields high acceptance rates (82% for plans, 59% for code PRs).
- The primary remaining challenge is ensuring functional correctness and code quality without excessive human refinement.

<!-- Notes: Summarize the main conclusions. -->

---

<!-- Slide 30: 研究启示 (Research Implications) -->
## 研究启示 (Research Implications)

- 🎯 Tool Design: Future AI coding tools should prioritize 'iterative refinement' workflows over 'one-shot' generation.
- 🎯 Benchmarking: There is a need for new benchmarks that reflect enterprise characteristics: multi-language repositories, brief issue descriptions, and complex dependencies.
- 🎯 Workflow Integration: Integrating AI directly into project management tools (JIRA) is a viable path to adoption, reducing the friction of context switching.
- 🎯 Developer Training: Developers may need to adapt their documentation skills to become better 'prompt engineers' for these agents.
- 🎯 Evaluation Metrics: Research should focus on 'human effort saved' or 'time-to-merge' rather than just 'pass@1' on synthetic tests.

<!-- Notes: Discuss implications for researchers and practitioners. -->

---

<!-- Slide 31: 未来工作 (Future Work) -->
## 未来工作 (Future Work)

- 🔮 Context Augmentation: Investigating methods to automatically enhance input context (e.g., retrieving type definitions, historical solutions) to compensate for brief issue descriptions.
- 🔮 Advanced Code Validation: Moving beyond linters to incorporate automated test generation and execution within the agent loop to verify functionality.
- 🔮 Workflow Flexibility: Improving the UI/UX to allow developers to move non-linearly between stages (e.g., updating the plan after seeing partial code).
- 🔮 Alternative Functional Correctness Metrics: Exploring evaluation methods that do not solely rely on passing unit tests, which are often unavailable or incomplete in industry.
- 🔮 Multi-Modal Input: Allowing agents to process diagrams, meeting transcripts, or chats to better understand requirements.

<!-- Notes: Suggest directions for future research. -->

---

<!-- Slide 32: 谢谢！Questions & Discussion -->
## 谢谢！Questions & Discussion

- 感谢您的聆听！
- 欢迎提问与讨论

- 论文标题: Human-In-the-Loop Software Development Agents
- 作者:

<!-- Notes: Thank the audience and open for questions. -->