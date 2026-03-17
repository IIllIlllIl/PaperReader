#!/usr/bin/env python3
"""
Narrative Planning Prompt

Instructs the LLM to extract a compelling research narrative from paper analysis.
"""

NARRATIVE_PLANNING_PROMPT = """You are an expert at extracting compelling research narratives from academic papers.

Your task: Extract a clear, engaging research narrative from the following paper analysis.

---

## PAPER ANALYSIS:

{{PAPER_ANALYSIS_PLACEHOLDER}}

---

## YOUR TASK:

Extract a research narrative following this structure:

1. **Hook** (1-2 sentences)
   - Captures audience attention
   - States the big promise or challenge
   - Example: "Coding agents promise full automation but fail in real-world development."

2. **Problem** (1-2 sentences)
   - What specific problem does this research address?
   - Why is it important?
   - Example: "Current benchmarks don't capture enterprise software complexity."

3. **Limitations of Prior Work** (1-2 sentences)
   - What's wrong with previous approaches?
   - What gap exists?
   - Example: "Existing agents operate autonomously, leading to errors on complex tasks."

4. **Key Idea** (1 sentence - CRITICAL!)
   - The main contribution in ONE clear sentence
   - Should be memorable and specific
   - Example: "We introduce a Human-in-the-Loop agent framework for iterative refinement."

5. **Method** (2-3 sentences)
   - Brief overview of the approach
   - Key technical innovation
   - Example: "Our framework allows developers to review and approve agent plans before execution. This enables iterative refinement based on human feedback."

6. **Evidence** (2-3 sentences)
   - Key results that support the idea
   - Specific numbers and metrics
   - Example: "In a real-world JIRA deployment, we achieved 82% plan approval rate and 59% PR merge rate, significantly outperforming autonomous baselines."

7. **Implications** (1-2 sentences)
   - What does this mean for the future?
   - Broader impact
   - Example: "Human-AI collaboration may be the future of software engineering, combining AI efficiency with human judgment."

---

## OUTPUT FORMAT:

Output ONLY a JSON object with this EXACT structure:

```json
{
  "hook": "...",
  "problem": "...",
  "limitations_of_prior_work": "...",
  "key_idea": "...",
  "method": "...",
  "evidence": "...",
  "implications": "..."
}
```

---

## REQUIREMENTS:

1. **Be Concise**: Each field should be 1-3 sentences maximum
2. **Be Specific**: Include concrete numbers and facts from the paper
3. **Be Compelling**: Make it engaging and memorable
4. **Be Accurate**: Only use information from the paper analysis
5. **Tell a Story**: The narrative should flow logically from hook to implications

---

## EXAMPLE OUTPUT:

```json
{
  "hook": "Coding agents promise full automation but fail in real-world development.",
  "problem": "Current benchmarks don't capture enterprise software complexity.",
  "limitations_of_prior_work": "Existing agents operate autonomously, leading to errors on complex tasks.",
  "key_idea": "We introduce a Human-in-the-Loop agent framework for iterative refinement.",
  "method": "Our framework allows developers to review and approve agent plans before execution, enabling iterative refinement based on human feedback.",
  "evidence": "In a real-world JIRA deployment, we achieved 82% plan approval rate and 59% PR merge rate, significantly outperforming autonomous baselines.",
  "implications": "Human-AI collaboration may be the future of software engineering, combining AI efficiency with human judgment."
}
```

---

## CRITICAL:

- Output ONLY the JSON object, no other text
- Use information ONLY from the provided paper analysis
- Keep each field concise (1-3 sentences)
- Make it engaging and memorable
- Ensure the narrative flows logically

Now extract the narrative from the paper analysis above.
"""

if __name__ == "__main__":
    print(NARRATIVE_PLANNING_PROMPT)
