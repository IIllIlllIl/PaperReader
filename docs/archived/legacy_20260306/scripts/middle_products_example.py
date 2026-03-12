"""
中间产物示例

这个文件展示了PaperReader在处理论文过程中产生的各种中间产物
"""

# ============================================
# 1. PDF验证结果示例
# ============================================

validation_result_example = {
    "is_valid": True,
    "quality": "GOOD",
    "layout_type": "SINGLE_COLUMN",
    "page_count": 12,
    "has_text": True,
    "text_ratio": 0.92,
    "issues": [
        "Multi-column layout detected in pages 8-10"
    ],
    "recommendations": [
        "PDF is suitable for standard processing",
        "Some pages may have text ordering issues"
    ]
}

# ============================================
# 2. 提取的文本示例
# ============================================

extracted_text_example = """
Attention Is All You Need

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit,
Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin

Abstract

The dominant sequence transduction models are based on complex recurrent or
convolutional neural networks that include an encoder and a decoder. The best
performing models also connect the encoder and decoder through an attention
mechanism. We propose a new simple network architecture, the Transformer,
based solely on attention mechanisms, dispensing with recurrence and convolutions
entirely. Experiments on two machine translation tasks show that these models are
superior in quality while being more parallelizable and requiring significantly
less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German
translation task, improving over the existing best results, including ensembles,
by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model
establishes a new single-model state-of-the-art BLEU score of 41.8 after training
for 3.5 days on eight GPUs...

1 Introduction

Recurrent neural networks, long short-term memory and gated recurrent neural
networks in particular, have been firmly established as state of the art approaches
in sequence modeling and transduction problems such as language modeling and
machine translation. Numerous efforts have since continued to push the boundaries
of recurrent language models and encoder-decoder architectures...

[... truncated for brevity ...]
"""

# ============================================
# 3. 提取的元数据示例
# ============================================

metadata_example = {
    "title": "Attention Is All You Need",
    "authors": [
        "Ashish Vaswani",
        "Noam Shazeer",
        "Niki Parmar",
        "Jakob Uszkoreit",
        "Llion Jones",
        "Aidan N. Gomez",
        "Łukasz Kaiser",
        "Illia Polosukhin"
    ],
    "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
    "keywords": [],
    "year": "2017",
    "venue": "NeurIPS",
    "doi": None
}

# ============================================
# 4. AI分析结果示例 (PaperAnalysis)
# ============================================

paper_analysis_example = {
    "title": "Attention Is All You Need",
    "authors": [
        "Ashish Vaswani",
        "Noam Shazeer",
        "Niki Parmar"
    ],
    "problem": "Existing sequence transduction models based on RNNs and CNNs are inherently sequential, preventing parallelization and requiring significant training time. These models struggle with long-range dependencies and are computationally expensive.",
    "motivation": "Sequence-to-sequence tasks like machine translation are crucial for many applications. Current approaches using recurrent or convolutional architectures have fundamental limitations in parallelization and modeling long-range dependencies. A more efficient architecture could dramatically reduce training time and improve model quality.",
    "method": "The Transformer architecture relies entirely on self-attention mechanisms, dispensing with recurrence and convolutions. It uses an encoder-decoder structure where both consist of stacked layers of multi-head self-attention and position-wise feed-forward networks. Key innovations include: (1) Multi-head attention allowing the model to jointly attend to information from different representation subspaces, (2) Positional encodings to inject sequence order information, (3) Scaled dot-product attention for efficient computation, and (4) Residual connections and layer normalization for stable training.",
    "innovations": [
        "Pure attention-based architecture without recurrence or convolutions",
        "Multi-head self-attention mechanism for capturing different types of relationships",
        "Positional encoding for sequence order information",
        "Highly parallelizable design enabling significantly faster training",
        "Scaled dot-product attention mechanism"
    ],
    "experiments": "Evaluated on WMT 2014 English-to-German and English-to-French translation tasks. Used the WMT 2014 English-German dataset with 4.5 million sentence pairs and English-French with 36 million sentences. Compared against state-of-the-art models including GNMT, ConvS2S, and various RNN-based approaches. Training performed on 8 NVIDIA P100 GPUs with Adam optimizer.",
    "results": [
        "Achieved 28.4 BLEU on WMT 2014 English-German, outperforming previous best by 2 BLEU",
        "Established new state-of-the-art 41.8 BLEU on WMT 2014 English-French",
        "Training time reduced to 12 hours (3.5 days for big model) vs weeks for RNN models",
        "Model quality improves with more attention heads and layers",
        "Demonstrated superior generalization on English constituency parsing"
    ],
    "pros": [
        "Significantly faster training due to parallelization",
        "Better handling of long-range dependencies through self-attention",
        "Superior translation quality compared to existing approaches",
        "More interpretable attention weights",
        "Scalable architecture that benefits from more computation",
        "No recurrence enables efficient GPU utilization"
    ],
    "cons": [
        "Quadratic memory complexity O(n²) with sequence length due to self-attention",
        "Limited to fixed maximum sequence length during training",
        "Positional encoding may not generalize well to longer sequences than seen during training",
        "Requires large amounts of training data",
        "High memory requirements for long sequences",
        "Less inductive bias than CNNs for some tasks"
    ],
    "conclusions": "The Transformer demonstrates that attention mechanisms alone are sufficient for high-quality sequence transduction, without relying on recurrent or convolutional architectures. This enables significantly faster training through parallelization while achieving state-of-the-art results on translation tasks. The architecture's simplicity and effectiveness suggest it could be applied to many other sequence modeling problems.",
    "future_work": "Future research directions include: extending Transformer to handle even longer sequences efficiently through sparse attention patterns, applying the architecture to other modalities like images and audio, investigating different attention mechanisms to reduce quadratic complexity, and exploring the use of Transformer for generative tasks beyond translation."
}

# ============================================
# 5. 演示内容示例 (PresentationContent)
# ============================================

presentation_content_example = {
    "title": "Attention Is All You Need",
    "authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar et al.",
    "venue": "NeurIPS",
    "year": "2017",
    "motivation": [
        "Sequence-to-sequence tasks are crucial for many applications",
        "Current RNN and CNN approaches have parallelization limitations",
        "Long-range dependencies are difficult to model",
        "Training takes significant time and computation"
    ],
    "existing_problems": [
        "Recurrent models prevent parallelization",
        "Sequential nature leads to slow training",
        "Difficulty capturing long-range dependencies"
    ],
    "research_problem": "Can we build a sequence transduction model that is both highly parallelizable and achieves superior quality?",
    "method_overview": "The Transformer relies entirely on self-attention mechanisms, using an encoder-decoder structure with multi-head attention and positional encodings, dispensing with recurrence and convolutions entirely.",
    "technical_details": [
        "Multi-head self-attention for different representation subspaces",
        "Positional encoding to inject sequence order information",
        "Scaled dot-product attention for efficient computation",
        "Stacked encoder-decoder layers with residual connections",
        "Layer normalization for stable training"
    ],
    "innovations": [
        "1. Pure attention-based architecture",
        "2. Multi-head self-attention mechanism",
        "3. Positional encoding scheme",
        "4. Highly parallelizable design",
        "5. Scaled dot-product attention"
    ],
    "experimental_setup": "Evaluated on WMT 2014 translation tasks: English-German (4.5M pairs) and English-French (36M sentences). Baselines: GNMT, ConvS2S, RNN-based models. Training: 8 NVIDIA P100 GPUs.",
    "main_results": [
        "28.4 BLEU on English-German (+2 over previous best)",
        "41.8 BLEU on English-French (new state-of-the-art)",
        "Training time: 12 hours vs weeks for RNNs",
        "Better quality with more attention heads",
        "Strong generalization on parsing tasks"
    ],
    "result_analysis": "The Transformer demonstrates significant improvements in both quality and training efficiency, achieving state-of-the-art results with dramatically reduced training time.",
    "discussion": "The approach shows superior performance and efficiency. The pure attention mechanism effectively captures dependencies. However, quadratic complexity and memory requirements remain challenges for very long sequences.",
    "pros": [
        "✓ Significantly faster training",
        "✓ Better long-range dependency modeling",
        "✓ State-of-the-art translation quality",
        "✓ Highly interpretable",
        "✓ Excellent parallelization"
    ],
    "cons": [
        "✗ Quadratic memory complexity O(n²)",
        "✗ Fixed maximum sequence length",
        "✗ High memory for long sequences",
        "✗ Requires large training data"
    ],
    "future_work": [
        "Extend to longer sequences with sparse attention",
        "Apply to other modalities (images, audio)",
        "Reduce quadratic complexity",
        "Explore generative tasks beyond translation"
    ],
    "conclusions": "The Transformer proves attention alone is sufficient for high-quality sequence transduction, enabling faster training while achieving state-of-the-art results with a simple, effective architecture."
}

# ============================================
# 6. 组织的幻灯片内容示例
# ============================================

organized_slides_example = [
    {
        "slide_number": 1,
        "title": "Attention Is All You Need",
        "bullet_points": [
            "Ashish Vaswani, Noam Shazeer, Niki Parmar et al.",
            "NeurIPS | 2017"
        ],
        "notes": "Welcome slide. Introduce the paper and authors."
    },
    {
        "slide_number": 2,
        "title": "背景与动机",
        "bullet_points": [
            "Sequence-to-sequence tasks are crucial for many applications",
            "Current RNN and CNN approaches have parallelization limitations",
            "Long-range dependencies are difficult to model",
            "Training takes significant time and computation"
        ],
        "notes": "Explain the background and motivation for this research."
    },
    {
        "slide_number": 3,
        "title": "现有问题",
        "bullet_points": [
            "Recurrent models prevent parallelization",
            "Sequential nature leads to slow training",
            "Difficulty capturing long-range dependencies"
        ],
        "notes": "Describe the existing problems this paper addresses."
    },
    {
        "slide_number": 4,
        "title": "研究问题",
        "bullet_points": [
            "Can we build a sequence transduction model that is both highly parallelizable and achieves superior quality?"
        ],
        "notes": "State the core research problem clearly."
    },
    {
        "slide_number": 5,
        "title": "方法概述",
        "bullet_points": [
            "The Transformer relies entirely on self-attention mechanisms.",
            "Uses encoder-decoder structure with multi-head attention.",
            "Dispenses with recurrence and convolutions entirely.",
            "Incorporates positional encodings for sequence order."
        ],
        "notes": "Provide an overview of the proposed method."
    },
    {
        "slide_number": 6,
        "title": "技术细节",
        "bullet_points": [
            "Multi-head self-attention for different representation subspaces",
            "Positional encoding to inject sequence order information",
            "Scaled dot-product attention for efficient computation",
            "Stacked encoder-decoder layers with residual connections",
            "Layer normalization for stable training"
        ],
        "notes": "Explain the technical details of the approach."
    },
    {
        "slide_number": 7,
        "title": "创新点",
        "bullet_points": [
            "1. Pure attention-based architecture",
            "2. Multi-head self-attention mechanism",
            "3. Positional encoding scheme",
            "4. Highly parallelizable design",
            "5. Scaled dot-product attention"
        ],
        "notes": "Highlight the key innovations and contributions."
    },
    {
        "slide_number": 8,
        "title": "实验设置",
        "bullet_points": [
            "WMT 2014 translation tasks",
            "English-German: 4.5M sentence pairs",
            "English-French: 36M sentences",
            "Baselines: GNMT, ConvS2S, RNN models",
            "Training: 8 NVIDIA P100 GPUs"
        ],
        "notes": "Describe the experimental setup."
    },
    {
        "slide_number": 9,
        "title": "主要结果",
        "bullet_points": [
            "28.4 BLEU on English-German (+2 over previous best)",
            "41.8 BLEU on English-French (new state-of-the-art)",
            "Training time: 12 hours vs weeks for RNNs",
            "Better quality with more attention heads",
            "Strong generalization on parsing tasks"
        ],
        "notes": "Present the main experimental results."
    },
    {
        "slide_number": 10,
        "title": "结果分析",
        "bullet_points": [
            "The Transformer demonstrates significant improvements in both quality and training efficiency.",
            "Achieving state-of-the-art results with dramatically reduced training time."
        ],
        "notes": "Analyze and interpret the results."
    },
    {
        "slide_number": 11,
        "title": "讨论",
        "bullet_points": [
            "The approach shows superior performance and efficiency.",
            "The pure attention mechanism effectively captures dependencies.",
            "Quadratic complexity remains a challenge for very long sequences."
        ],
        "notes": "Discuss the implications of the results."
    },
    {
        "slide_number": 12,
        "title": "优点",
        "bullet_points": [
            "✓ Significantly faster training",
            "✓ Better long-range dependency modeling",
            "✓ State-of-the-art translation quality",
            "✓ Highly interpretable",
            "✓ Excellent parallelization"
        ],
        "notes": "Highlight the advantages of the approach."
    },
    {
        "slide_number": 13,
        "title": "局限性",
        "bullet_points": [
            "✗ Quadratic memory complexity O(n²)",
            "✗ Fixed maximum sequence length",
            "✗ High memory for long sequences",
            "✗ Requires large training data"
        ],
        "notes": "Discuss the limitations honestly."
    },
    {
        "slide_number": 14,
        "title": "未来工作",
        "bullet_points": [
            "Extend to longer sequences with sparse attention",
            "Apply to other modalities (images, audio)",
            "Reduce quadratic complexity",
            "Explore generative tasks beyond translation"
        ],
        "notes": "Suggest directions for future research."
    },
    {
        "slide_number": 15,
        "title": "结论",
        "bullet_points": [
            "Attention alone is sufficient for high-quality sequence transduction.",
            "Enables faster training while achieving state-of-the-art results.",
            "Simple, effective architecture with broad applicability."
        ],
        "notes": "Summarize the key takeaways."
    },
    {
        "slide_number": 16,
        "title": "Q&A",
        "bullet_points": [
            "谢谢！",
            "Questions & Discussion"
        ],
        "notes": "Open for questions."
    }
]

# ============================================
# 7. Markdown输出示例 (部分)
# ============================================

markdown_output_example = """---
marp: true
theme: academic
paginate: true
size: 16:9
style: |
  section {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 24px;
    color: #333;
    background: #fff;
  }
  h2 {
    color: #34495e;
    font-size: 36px;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
  }
---

<!-- Slide 1: Attention Is All You Need -->
## Attention Is All You Need

- Ashish Vaswani, Noam Shazeer, Niki Parmar et al.
- NeurIPS | 2017

<!-- Notes: Welcome slide. Introduce the paper and authors. -->

---

<!-- Slide 2: 背景与动机 -->
## 背景与动机

- Sequence-to-sequence tasks are crucial for many applications
- Current RNN and CNN approaches have parallelization limitations
- Long-range dependencies are difficult to model
- Training takes significant time and computation

<!-- Notes: Explain the background and motivation for this research. -->

---

<!-- Slide 3: 现有问题 -->
## 现有问题

- Recurrent models prevent parallelization
- Sequential nature leads to slow training
- Difficulty capturing long-range dependencies

<!-- Notes: Describe the existing problems this paper addresses. -->

---

<!-- ... 更多幻灯片 ... -->

---

<!-- Slide 16: Q&A -->
## Q&A

- 谢谢！
- Questions & Discussion

<!-- Notes: Open for questions. -->
"""

# ============================================
# 8. 缓存文件内容示例
# ============================================

cache_file_example = {
    "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "timestamp": "2026-03-05T14:30:15.123456",
    "analysis": paper_analysis_example,
    "presentation_content": presentation_content_example,
    "metadata": {
        "model": "claude-sonnet-4-6",
        "tokens_used": 87500,
        "cost": 0.0925,
        "processing_time_seconds": 12.5
    }
}

# ============================================
# 使用示例
# ============================================

def print_example(name: str, data):
    """打印示例数据"""
    import json
    print(f"\n{'='*60}")
    print(f"{name}")
    print('='*60)
    if isinstance(data, str):
        print(data[:500] + "..." if len(data) > 500 else data)
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
    print()


if __name__ == "__main__":
    # 展示所有示例
    print_example("1. PDF验证结果", validation_result_example)
    print_example("2. 提取的文本", extracted_text_example)
    print_example("3. 元数据", metadata_example)
    print_example("4. AI分析结果", paper_analysis_example)
    print_example("5. 演示内容", presentation_content_example)
    print_example("6. 组织的幻灯片 (前5个)", organized_slides_example[:5])
    print_example("7. Markdown输出", markdown_output_example)
    print_example("8. 缓存文件", cache_file_example)
