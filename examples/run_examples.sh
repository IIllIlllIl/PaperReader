#!/bin/bash

# PaperReader - Example Usage Scripts
# This script demonstrates best practices for generating high-quality academic presentations

set -e  # Exit on error

echo "=========================================="
echo "PaperReader - Example Usage"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Please create .env file with your ANTHROPIC_API_KEY"
    echo ""
    echo "Example:"
    echo "  cp .env.example .env"
    echo "  # Edit .env and add your API key"
    exit 1
fi

echo -e "${GREEN}✓ Environment configured${NC}"
echo ""

# Example 1: Basic pipeline (10 slides, default settings)
echo -e "${BLUE}Example 1: Basic Pipeline (Recommended)${NC}"
echo "Command: python cli/main.py pipeline --paper papers/example.pdf"
echo ""
echo "This generates:"
echo "  - 10-slide structured presentation"
echo "  - Intelligent figure matching (100% accuracy)"
echo "  - All key numbers automatically bolded"
echo "  - Balanced Pros/Cons discussion"
echo ""
read -p "Run Example 1? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python cli/main.py pipeline --paper papers/example.pdf
    echo ""
    echo -e "${GREEN}✓ Example 1 completed${NC}"
    echo "Check outputs:"
    echo "  - outputs/slides/example.pptx"
    echo "  - outputs/markdown/example.md"
    echo ""
fi

# Example 2: Process specific paper with verbose output
echo ""
echo -e "${BLUE}Example 2: Verbose Mode with Cost Tracking${NC}"
echo "Command: python cli/main.py pipeline --paper papers/example.pdf --verbose"
echo ""
echo "Benefits:"
echo "  - See detailed processing steps"
echo "  - Track API costs in real-time"
echo "  - Monitor token usage"
echo ""
read -p "Run Example 2? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python cli/main.py pipeline --paper papers/example.pdf --verbose
    echo ""
    echo -e "${GREEN}✓ Example 2 completed${NC}"
    echo ""
fi

# Example 3: Batch processing
echo ""
echo -e "${BLUE}Example 3: Process All Papers${NC}"
echo "Command: python cli/main.py process --all"
echo ""
echo "This will:"
echo "  - Process all PDF papers in papers/ directory"
echo "  - Use caching to avoid redundant API calls"
echo "  - Generate presentations for each paper"
echo ""
read -p "Run Example 3? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python cli/main.py process --all
    echo ""
    echo -e "${GREEN}✓ Example 3 completed${NC}"
    echo "Check outputs/ directory for all generated presentations"
    echo ""
fi

# Example 4: Check cache statistics
echo ""
echo -e "${BLUE}Example 4: Cache Management${NC}"
echo "Command: python cli/main.py stats"
echo ""
echo "Shows:"
echo "  - Total cached papers"
echo "  - Cache size"
echo "  - Potential cost savings"
echo ""
read -p "Run Example 4? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python cli/main.py stats
    echo ""
    echo -e "${GREEN}✓ Example 4 completed${NC}"
    echo ""
fi

# Example 5: Clear cache (optional)
echo ""
echo -e "${BLUE}Example 5: Clear Cache (Optional)${NC}"
echo "Command: python cli/main.py clear-cache"
echo ""
echo "⚠️  Warning: This will delete all cached analysis results"
echo "Use this to force re-processing of all papers"
echo ""
read -p "Run Example 5? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python cli/main.py clear-cache
    echo ""
    echo -e "${GREEN}✓ Cache cleared${NC}"
    echo ""
fi

echo ""
echo "=========================================="
echo "Examples Complete!"
echo "=========================================="
echo ""
echo "📚 Next Steps:"
echo ""
echo "1. Place your PDF papers in papers/ directory"
echo "2. Run: python cli/main.py pipeline --paper papers/your-paper.pdf"
echo "3. Check outputs/ for generated presentation"
echo ""
echo "📖 Documentation:"
echo "  - README.md - Complete usage guide"
echo "  - CLAUDE.md - Developer documentation"
echo "  - docs/ - Detailed architecture docs"
echo ""
echo "💡 Tips:"
echo "  - Use --verbose to track costs and progress"
echo "  - Enable caching (default) to save API costs"
echo "  - Check outputs/markdown/ for editable source"
echo ""
