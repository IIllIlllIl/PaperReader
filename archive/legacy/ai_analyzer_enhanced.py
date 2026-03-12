"""
Enhanced AI Analyzer for PaperReader

Analyzes papers using Claude AI to extract detailed information for richer presentations
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import anthropic

logger = logging.getLogger(__name__)


@dataclass
class DetailedPaperAnalysis:
    """Detailed structured analysis of a paper"""
    title: str
    authors: List[str]
    
    # Background & Context
    research_background: str  # 研究背景
    related_work: List[str]   # 相关工作
    motivation: str           # 研究动机
    
    # Problem & Challenges
    core_problem: str         # 核心问题
    challenges: List[str]     # 主要挑战
    research_gap: str         # 研究空白
    
    # Insights & Hypotheses
    key_insights: List[str]   # 关键洞察
    hypotheses: List[str]     # 研究假设
    
    # Method
    method_overview: str      # 方法概述
    method_details: List[str] # 方法细节
    technical_innovations: List[str]  # 技术创新
    
    # Implementation
    architecture: str         # 系统架构
    key_components: List[str] # 关键组件
    algorithms: List[str]     # 核心算法
    
    # Experiments
    datasets: List[str]       # 数据集
    baselines: List[str]      # 基线方法
    metrics: List[str]        # 评估指标
    experimental_setup: str   # 实验设置
    
    # Results
    main_results: List[str]   # 主要结果
    performance_analysis: str # 性能分析
    ablation_studies: List[str]  # 消融实验
    case_studies: List[str]   # 案例研究
    
    # Analysis
    advantages: List[str]     # 优势
    limitations: List[str]    # 局限性
    discussion: str           # 讨论
    
    # Conclusions
    conclusions: str          # 结论
    implications: List[str]   # 研究启示
    future_work: List[str]    # 未来工作


class EnhancedAIAnalyzer:
    """Enhanced analyzer with more detailed content extraction"""

    ENHANCED_ANALYSIS_PROMPT = """You are an academic paper analysis expert. Analyze the following research paper and extract DETAILED, COMPREHENSIVE information for creating an in-depth presentation.

Paper text:
{paper_text}

Provide a detailed structured analysis in JSON format. Be THOROUGH and SPECIFIC:

{{
    "research_background": "Detailed research background (4-6 sentences): What is the broader context? What is the state of the field? Why is this topic important?",
    
    "related_work": [
        "List 4-6 key related works or approaches",
        "For each: brief description and limitation"
    ],
    
    "motivation": "Research motivation (3-4 sentences): What specific gap or problem motivated this work? Why is it important now?",
    
    "core_problem": "Core research problem (3-4 sentences): What is the main problem being addressed? Be specific about the challenge.",
    
    "challenges": [
        "List 4-6 technical or practical challenges",
        "Be specific and concrete"
    ],
    
    "research_gap": "Research gap (2-3 sentences): What specific gap in existing work does this paper address?",
    
    "key_insights": [
        "List 3-5 key insights or observations that motivated the approach",
        "What did the authors realize that others missed?"
    ],
    
    "hypotheses": [
        "List 2-4 research hypotheses or assumptions",
        "What assumptions does the method make?"
    ],
    
    "method_overview": "Method overview (4-6 sentences): High-level description of the proposed approach. What is the main idea?",
    
    "method_details": [
        "List 6-10 detailed steps or components of the method",
        "Include technical specifics, not just general descriptions"
    ],
    
    "technical_innovations": [
        "List 4-6 specific technical innovations",
        "What is new or different from existing approaches?"
    ],
    
    "architecture": "System architecture (3-5 sentences): Describe the overall system design. How do components interact?",
    
    "key_components": [
        "List 4-6 key system components or modules",
        "What are the main building blocks?"
    ],
    
    "algorithms": [
        "List 3-5 core algorithms or techniques used",
        "Include specifics, not just names"
    ],
    
    "datasets": [
        "List datasets used with details (name, size, characteristics)"
    ],
    
    "baselines": [
        "List baseline methods with brief descriptions"
    ],
    
    "metrics": [
        "List evaluation metrics with explanations"
    ],
    
    "experimental_setup": "Experimental setup (4-6 sentences): Detailed description of how experiments were conducted. Include hardware, training details, hyperparameters.",
    
    "main_results": [
        "List 6-10 main results with SPECIFIC NUMBERS and statistics",
        "Include comparisons to baselines with improvement percentages"
    ],
    
    "performance_analysis": "Performance analysis (3-5 sentences): How does the method perform? What are the key findings?",
    
    "ablation_studies": [
        "List 3-5 findings from ablation studies",
        "What components are most important?"
    ],
    
    "case_studies": [
        "List 2-4 interesting case study examples",
        "Specific examples that illustrate the method's effectiveness"
    ],
    
    "advantages": [
        "List 4-6 advantages or strengths",
        "Be specific and concrete"
    ],
    
    "limitations": [
        "List 3-5 limitations or weaknesses",
        "What doesn't work well? What are the constraints?"
    ],
    
    "discussion": "Discussion (4-6 sentences): Broader implications of the results. How do the results relate to the initial hypotheses?",
    
    "conclusions": "Conclusions (4-6 sentences): Main takeaways. What did we learn? What is the impact?",
    
    "implications": [
        "List 3-5 implications for researchers or practitioners",
        "What does this mean for the field?"
    ],
    
    "future_work": [
        "List 4-6 specific future research directions",
        "What questions remain unanswered?"
    ]
}}

CRITICAL REQUIREMENTS:
1. BE SPECIFIC: Include concrete details, numbers, examples - not just general descriptions
2. BE THOROUGH: Extract as much relevant detail as possible from the paper
3. BE ACCURATE: Ensure all information is faithful to the paper content
4. USE TECHNICAL LANGUAGE: Don't oversimplify - use appropriate technical terminology
5. INCLUDE NUMBERS: Always include specific statistics, percentages, measurements when available
6. BE COMPREHENSIVE: Aim for 10+ slides worth of detailed content

DO NOT:
- Make vague statements without specifics
- Skip technical details
- Omit numbers or statistics
- Oversimplify complex concepts
"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        """Initialize enhanced analyzer"""
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.call_count = 0
        self.total_tokens = 0
        self.total_cost = 0.0
        
        self.cost_per_1k = {
            "claude-sonnet-4-6": {"input": 0.003, "output": 0.015},
        }
    
    def analyze_paper_detailed(self, paper_text: str, metadata: Optional[Dict] = None) -> DetailedPaperAnalysis:
        """Perform detailed analysis of paper"""
        logger.info("Starting detailed paper analysis")
        
        # Truncate if too long
        max_chars = 150000
        if len(paper_text) > max_chars:
            logger.warning(f"Paper text too long ({len(paper_text)} chars), truncating")
            paper_text = paper_text[:max_chars] + "\n\n[Text truncated]"
        
        # Call API
        response = self._call_claude(
            prompt=self.ENHANCED_ANALYSIS_PROMPT.format(paper_text=paper_text),
            model=self.model
        )
        
        # Parse response
        analysis_dict = self._parse_json_response(response)
        
        # Create analysis object
        analysis = DetailedPaperAnalysis(
            title=metadata.get('title', 'Unknown Title') if metadata else 'Unknown Title',
            authors=metadata.get('authors', []) if metadata else [],
            research_background=analysis_dict.get('research_background', ''),
            related_work=analysis_dict.get('related_work', []),
            motivation=analysis_dict.get('motivation', ''),
            core_problem=analysis_dict.get('core_problem', ''),
            challenges=analysis_dict.get('challenges', []),
            research_gap=analysis_dict.get('research_gap', ''),
            key_insights=analysis_dict.get('key_insights', []),
            hypotheses=analysis_dict.get('hypotheses', []),
            method_overview=analysis_dict.get('method_overview', ''),
            method_details=analysis_dict.get('method_details', []),
            technical_innovations=analysis_dict.get('technical_innovations', []),
            architecture=analysis_dict.get('architecture', ''),
            key_components=analysis_dict.get('key_components', []),
            algorithms=analysis_dict.get('algorithms', []),
            datasets=analysis_dict.get('datasets', []),
            baselines=analysis_dict.get('baselines', []),
            metrics=analysis_dict.get('metrics', []),
            experimental_setup=analysis_dict.get('experimental_setup', ''),
            main_results=analysis_dict.get('main_results', []),
            performance_analysis=analysis_dict.get('performance_analysis', ''),
            ablation_studies=analysis_dict.get('ablation_studies', []),
            case_studies=analysis_dict.get('case_studies', []),
            advantages=analysis_dict.get('advantages', []),
            limitations=analysis_dict.get('limitations', []),
            discussion=analysis_dict.get('discussion', ''),
            conclusions=analysis_dict.get('conclusions', ''),
            implications=analysis_dict.get('implications', []),
            future_work=analysis_dict.get('future_work', [])
        )
        
        logger.info("Detailed analysis completed")
        return analysis
    
    def _call_claude(self, prompt: str, model: str) -> str:
        """Call Claude API"""
        try:
            message = self.client.messages.create(
                model=model,
                max_tokens=8192,  # Increased for more detailed output
                messages=[{"role": "user", "content": prompt}]
            )
            
            self.call_count += 1
            input_tokens = message.usage.input_tokens
            output_tokens = message.usage.output_tokens
            self.total_tokens += input_tokens + output_tokens
            
            cost_data = self.cost_per_1k.get(model, self.cost_per_1k["claude-sonnet-4-6"])
            cost = (input_tokens / 1000 * cost_data["input"] +
                   output_tokens / 1000 * cost_data["output"])
            self.total_cost += cost
            
            logger.info(f"API call: {input_tokens} + {output_tokens} tokens, ${cost:.4f}")
            
            return message.content[0].text
            
        except anthropic.APIError as e:
            logger.error(f"Claude API error: {e}")
            raise
    
    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON from response"""
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                logger.error("No JSON found in response")
                return {}
            
            json_str = response[json_start:json_end]
            return json.loads(json_str)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            return {}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get analyzer statistics"""
        return {
            'call_count': self.call_count,
            'total_tokens': self.total_tokens,
            'total_cost': self.total_cost,
        }
