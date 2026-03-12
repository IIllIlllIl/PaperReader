"""
Enhanced Content Extractor for PaperReader

Extracts and organizes DETAILED content for presentation slides
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import logging

from .ai_analyzer_enhanced import DetailedPaperAnalysis

logger = logging.getLogger(__name__)


@dataclass
class EnhancedSlideContent:
    """Content for a single slide"""
    title: str
    bullet_points: List[str]
    notes: str = ""
    slide_type: str = "content"  # content, title, section


@dataclass
class EnhancedOrganizedPresentation:
    """Organized presentation with all slides"""
    slides: List[EnhancedSlideContent]
    total_slides: int


class EnhancedContentExtractor:
    """Extracts and organizes detailed content for presentation"""

    def __init__(self):
        """Initialize content extractor"""
        pass

    def extract_detailed_slides(self, analysis: DetailedPaperAnalysis) -> EnhancedOrganizedPresentation:
        """
        Extract detailed content for all slides
        
        Args:
            analysis: Detailed paper analysis
            
        Returns:
            EnhancedOrganizedPresentation with all slide content
        """
        logger.info("Extracting detailed slide content")
        
        slides = []
        
        # ============ INTRODUCTION SECTION ============
        
        # Slide 1: Title Slide
        slides.append(EnhancedSlideContent(
            title=analysis.title,
            bullet_points=[
                f"作者: {', '.join(analysis.authors[:3])}" + (" et al." if len(analysis.authors) > 3 else ""),
                f"年份: 2025",
                "Research Paper Presentation"
            ],
            notes="Welcome slide. Introduce the paper title and authors.",
            slide_type="title"
        ))
        
        # Slide 2: Outline
        slides.append(EnhancedSlideContent(
            title="报告大纲",
            bullet_points=[
                "📚 研究背景与动机",
                "❓ 核心问题与挑战",
                "💡 关键洞察与假设",
                "🔧 方法与技术细节",
                "🔬 实验设置与结果",
                "📊 分析与讨论",
                "🎯 结论与未来工作"
            ],
            notes="Outline of the presentation. Give audience an overview of what to expect.",
            slide_type="section"
        ))
        
        # ============ BACKGROUND SECTION ============
        
        # Slide 3: Research Background
        if analysis.research_background:
            slides.append(EnhancedSlideContent(
                title="研究背景 (Research Background)",
                bullet_points=self._split_into_points(analysis.research_background, max_points=8),
                notes="Explain the broader research context and why this topic is important.",
                slide_type="content"
            ))
        
        # Slide 4: Related Work
        if analysis.related_work:
            slides.append(EnhancedSlideContent(
                title="相关工作 (Related Work)",
                bullet_points=analysis.related_work[:8],
                notes="Overview of related work and their limitations.",
                slide_type="content"
            ))
        
        # Slide 5: Research Motivation
        if analysis.motivation:
            slides.append(EnhancedSlideContent(
                title="研究动机 (Motivation)",
                bullet_points=self._split_into_points(analysis.motivation, max_points=6),
                notes="Explain what motivated this specific research.",
                slide_type="content"
            ))
        
        # ============ PROBLEM SECTION ============
        
        # Slide 6: Core Problem
        if analysis.core_problem:
            slides.append(EnhancedSlideContent(
                title="核心问题 (Core Problem)",
                bullet_points=self._split_into_points(analysis.core_problem, max_points=6),
                notes="State the core research problem clearly and specifically.",
                slide_type="content"
            ))
        
        # Slide 7: Research Challenges
        if analysis.challenges:
            slides.append(EnhancedSlideContent(
                title="主要挑战 (Key Challenges)",
                bullet_points=[f"⚡ {c}" for c in analysis.challenges[:8]],
                notes="Highlight the key technical or practical challenges.",
                slide_type="content"
            ))
        
        # Slide 8: Research Gap
        if analysis.research_gap:
            slides.append(EnhancedSlideContent(
                title="研究空白 (Research Gap)",
                bullet_points=self._split_into_points(analysis.research_gap, max_points=5),
                notes="Explain the specific gap in existing research.",
                slide_type="content"
            ))
        
        # ============ INSIGHTS SECTION ============
        
        # Slide 9: Key Insights
        if analysis.key_insights:
            slides.append(EnhancedSlideContent(
                title="关键洞察 (Key Insights)",
                bullet_points=[f"💡 {i}" for i in analysis.key_insights[:6]],
                notes="Present the key insights that motivated the approach.",
                slide_type="content"
            ))
        
        # Slide 10: Research Hypotheses
        if analysis.hypotheses:
            slides.append(EnhancedSlideContent(
                title="研究假设 (Hypotheses)",
                bullet_points=[f"🤔 {h}" for h in analysis.hypotheses[:5]],
                notes="State the research hypotheses or assumptions.",
                slide_type="content"
            ))
        
        # ============ METHOD SECTION ============
        
        # Slide 11: Method Overview
        if analysis.method_overview:
            slides.append(EnhancedSlideContent(
                title="方法概述 (Method Overview)",
                bullet_points=self._split_into_points(analysis.method_overview, max_points=8),
                notes="Provide high-level overview of the proposed method.",
                slide_type="content"
            ))
        
        # Slide 12: Method Details (Part 1)
        if analysis.method_details:
            slides.append(EnhancedSlideContent(
                title="方法细节 - Part 1 (Method Details)",
                bullet_points=analysis.method_details[:8],
                notes="Detailed explanation of the method steps (first part).",
                slide_type="content"
            ))
        
        # Slide 13: Method Details (Part 2) - if there are more details
        if len(analysis.method_details) > 8:
            slides.append(EnhancedSlideContent(
                title="方法细节 - Part 2 (Method Details)",
                bullet_points=analysis.method_details[8:16],
                notes="Detailed explanation of the method steps (second part).",
                slide_type="content"
            ))
        
        # Slide 14: Technical Innovations
        if analysis.technical_innovations:
            slides.append(EnhancedSlideContent(
                title="技术创新 (Technical Innovations)",
                bullet_points=[f"🚀 {i}" for i in analysis.technical_innovations[:6]],
                notes="Highlight the key technical innovations.",
                slide_type="content"
            ))
        
        # Slide 15: System Architecture
        if analysis.architecture:
            slides.append(EnhancedSlideContent(
                title="系统架构 (System Architecture)",
                bullet_points=self._split_into_points(analysis.architecture, max_points=7),
                notes="Describe the overall system architecture.",
                slide_type="content"
            ))
        
        # Slide 16: Key Components
        if analysis.key_components:
            slides.append(EnhancedSlideContent(
                title="关键组件 (Key Components)",
                bullet_points=[f"🔧 {c}" for c in analysis.key_components[:6]],
                notes="Explain the key system components or modules.",
                slide_type="content"
            ))
        
        # Slide 17: Algorithms
        if analysis.algorithms:
            slides.append(EnhancedSlideContent(
                title="核心算法 (Core Algorithms)",
                bullet_points=[f"⚙️ {a}" for a in analysis.algorithms[:5]],
                notes="Describe the core algorithms or techniques.",
                slide_type="content"
            ))
        
        # ============ EXPERIMENTS SECTION ============
        
        # Slide 18: Datasets
        if analysis.datasets:
            slides.append(EnhancedSlideContent(
                title="数据集 (Datasets)",
                bullet_points=[f"📊 {d}" for d in analysis.datasets[:6]],
                notes="Describe the datasets used in experiments.",
                slide_type="content"
            ))
        
        # Slide 19: Baselines & Metrics
        slides.append(EnhancedSlideContent(
            title="基线方法与评估指标 (Baselines & Metrics)",
            bullet_points=[
                "基线方法 (Baselines):",
                *analysis.baselines[:4],
                "",
                "评估指标 (Metrics):",
                *analysis.metrics[:4]
            ],
            notes="List baseline methods and evaluation metrics.",
            slide_type="content"
        ))
        
        # Slide 20: Experimental Setup
        if analysis.experimental_setup:
            slides.append(EnhancedSlideContent(
                title="实验设置 (Experimental Setup)",
                bullet_points=self._split_into_points(analysis.experimental_setup, max_points=8),
                notes="Detailed description of the experimental setup.",
                slide_type="content"
            ))
        
        # ============ RESULTS SECTION ============
        
        # Slide 21: Main Results (Part 1)
        if analysis.main_results:
            slides.append(EnhancedSlideContent(
                title="主要结果 - Part 1 (Main Results)",
                bullet_points=[f"✅ {r}" for r in analysis.main_results[:6]],
                notes="Present the main experimental results (first part).",
                slide_type="content"
            ))
        
        # Slide 22: Main Results (Part 2)
        if len(analysis.main_results) > 6:
            slides.append(EnhancedSlideContent(
                title="主要结果 - Part 2 (Main Results)",
                bullet_points=[f"✅ {r}" for r in analysis.main_results[6:12]],
                notes="Present the main experimental results (second part).",
                slide_type="content"
            ))
        
        # Slide 23: Performance Analysis
        if analysis.performance_analysis:
            slides.append(EnhancedSlideContent(
                title="性能分析 (Performance Analysis)",
                bullet_points=self._split_into_points(analysis.performance_analysis, max_points=6),
                notes="Analyze the performance of the method.",
                slide_type="content"
            ))
        
        # Slide 24: Ablation Studies
        if analysis.ablation_studies:
            slides.append(EnhancedSlideContent(
                title="消融实验 (Ablation Studies)",
                bullet_points=[f"🔬 {a}" for a in analysis.ablation_studies[:6]],
                notes="Present findings from ablation studies.",
                slide_type="content"
            ))
        
        # Slide 25: Case Studies
        if analysis.case_studies:
            slides.append(EnhancedSlideContent(
                title="案例研究 (Case Studies)",
                bullet_points=[f"📋 {c}" for c in analysis.case_studies[:4]],
                notes="Show interesting case study examples.",
                slide_type="content"
            ))
        
        # ============ ANALYSIS SECTION ============
        
        # Slide 26: Advantages
        if analysis.advantages:
            slides.append(EnhancedSlideContent(
                title="优势 (Advantages)",
                bullet_points=[f"✓ {a}" for a in analysis.advantages[:6]],
                notes="Highlight the advantages of the approach.",
                slide_type="content"
            ))
        
        # Slide 27: Limitations
        if analysis.limitations:
            slides.append(EnhancedSlideContent(
                title="局限性 (Limitations)",
                bullet_points=[f"✗ {l}" for l in analysis.limitations[:5]],
                notes="Discuss the limitations honestly.",
                slide_type="content"
            ))
        
        # Slide 28: Discussion
        if analysis.discussion:
            slides.append(EnhancedSlideContent(
                title="讨论 (Discussion)",
                bullet_points=self._split_into_points(analysis.discussion, max_points=7),
                notes="Discuss the broader implications of the results.",
                slide_type="content"
            ))
        
        # ============ CONCLUSION SECTION ============
        
        # Slide 29: Conclusions
        if analysis.conclusions:
            slides.append(EnhancedSlideContent(
                title="结论 (Conclusions)",
                bullet_points=self._split_into_points(analysis.conclusions, max_points=7),
                notes="Summarize the main conclusions.",
                slide_type="content"
            ))
        
        # Slide 30: Research Implications
        if analysis.implications:
            slides.append(EnhancedSlideContent(
                title="研究启示 (Research Implications)",
                bullet_points=[f"🎯 {i}" for i in analysis.implications[:5]],
                notes="Discuss implications for researchers and practitioners.",
                slide_type="content"
            ))
        
        # Slide 31: Future Work
        if analysis.future_work:
            slides.append(EnhancedSlideContent(
                title="未来工作 (Future Work)",
                bullet_points=[f"🔮 {f}" for f in analysis.future_work[:6]],
                notes="Suggest directions for future research.",
                slide_type="content"
            ))
        
        # Slide 32: Thank You & Q&A
        slides.append(EnhancedSlideContent(
            title="谢谢！Questions & Discussion",
            bullet_points=[
                "感谢您的聆听！",
                "欢迎提问与讨论",
                "",
                f"论文标题: {analysis.title}",
                f"作者: {', '.join(analysis.authors[:3])}"
            ],
            notes="Thank the audience and open for questions.",
            slide_type="title"
        ))
        
        organized = EnhancedOrganizedPresentation(
            slides=slides,
            total_slides=len(slides)
        )
        
        logger.info(f"Extracted content for {organized.total_slides} detailed slides")
        return organized
    
    def _split_into_points(self, text: str, max_points: int = 6) -> List[str]:
        """Split text into bullet points"""
        if not text:
            return []
        
        # Split by sentences
        sentences = text.split('. ')
        points = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                if not sentence.endswith('.'):
                    sentence += '.'
                points.append(sentence)
        
        return points[:max_points]
