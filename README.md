# PaperReader

🤖 **AI-Powered Academic Paper Reading and Presentation Generation Tool**

PaperReader automatically analyzes academic papers and generates professional presentation slides using AI.

## 📂 Project Structure

PaperReader uses a clear, layered structure:

| Directory | Purpose |
|-----------|---------|
| `src/` | Core source code - stable API |
| `cli/` | Command-line interface |
| `tools/` | Utility scripts and tools |
| `docs/` | Detailed documentation |
| `tests/` | Test suite |
| `tools/manual_tests/` | Manual test scripts |

**Quick Links**:
- 📚 [Documentation Center](docs/README.md) - All detailed docs
- 🎯 [Quick Start](#quick-start) - Get started in 5 minutes
- 🛠️ [Developer Guide](CLAUDE.md) - Architecture and development

## Features

- 📄 **PDF Parsing**: Extracts text, sections, and metadata from PDF papers
- 🤖 **AI Analysis**: Uses Claude AI to understand and analyze paper content
- 📊 **Presentation Generation**: Creates academic-style slides in Markdown, HTML, or PDF
- 💾 **Smart Caching**: Caches analysis results to avoid redundant API calls
- 🔄 **Resilient**: Automatic retry and error handling for reliable processing
- 📈 **Progress Tracking**: Real-time progress updates with rich UI

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js (optional, for Marp CLI)
- Anthropic API key

### Setup

1. **Clone the repository**
```bash
cd PaperReader
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Marp CLI (optional, for HTML/PDF output)**
```bash
npm install -g @marp-team/marp-cli
```

4. **Configure API key**

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your-api-key-here
```

Or set it as an environment variable:
```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

## Quick Start

### Method 1: Using Full Pipeline (Recommended) ⭐

Generate complete presentation with all outputs:

```bash
python cli/main.py pipeline --paper papers/example.pdf
```

**Benefits**:
- ✅ Complete 8-stage pipeline
- ✅ Generates PPTX, Markdown, Script, and Plan
- ✅ Includes research narrative
- ✅ Best for academic presentations

### Method 2: Using Basic Process

For quick analysis without full pipeline:

```bash
python cli/main.py process --paper papers/example.pdf
```

### Process All Papers

```bash
# Place your PDF papers in the papers/ directory
python cli/main.py process --all
```

### Specify Output Format

```bash
# Generate HTML slides
python cli/main.py process --paper papers/example.pdf --format html

# Generate PDF slides
python cli/main.py process --paper papers/example.pdf --format pdf

# Generate Markdown only
python cli/main.py process --paper papers/example.pdf --format markdown
```

### Verbose Mode

```bash
python cli/main.py process --paper papers/example.pdf --verbose
```

## Usage

### Basic Commands

```bash
# Process single paper
python cli/main.py process -p papers/paper.pdf

# Process all papers in papers/ directory
python cli/main.py process --all

# Specify output format
python cli/main.py process -p papers/paper.pdf -f html

# Verbose output
python cli/main.py process -p papers/paper.pdf -v

# Disable cache
python cli/main.py process -p papers/paper.pdf --no-cache

# Use custom config
python cli/main.py process -p papers/paper.pdf --config my_config.yaml
```

### Cache Management

```bash
# View cache statistics
python cli/main.py stats

# Clear all cache
python cli/main.py clear-cache

# Clean up expired cache files
python cli/main.py cleanup
```

## Output Structure

```
outputs/
├── markdown/
│   └── paper_name.md                    # Generated Markdown slides
├── slides/
│   └── paper_name.pptx                  # PowerPoint presentation
├── scripts/
│   └── paper_name_presentation_script.md # Presentation script
└── plans/
    └── paper_name_plan.json             # Slide plan (JSON)
```

## Generated Presentation Structure

The tool generates a 12-15 slide presentation (depending on paper content) with the following structure:

1. **Title Slide** - Paper title, authors, venue, year
2. **Background & Motivation** - Research context and motivation
3. **Existing Problems** - Current challenges
4. **Research Problem** - Core research question
5. **Method Overview** - Proposed approach
6. **Technical Details** - Implementation details
7. **Innovations** - Key contributions
8. **Experimental Setup** - Datasets, baselines, metrics
9. **Main Results** - Experimental results
10. **Result Analysis** - Interpretation of results
11. **Discussion** - Implications and insights
12. **Pros** - Advantages and strengths
13. **Cons** - Limitations and weaknesses
14. **Future Work** - Future research directions
15. **Conclusion** - Summary and takeaways
16. **Q&A** - Questions and discussion

## Configuration

Edit `config.yaml` to customize behavior:

```yaml
ai:
  model: "claude-sonnet-4-6"          # Primary model
  haiku_model: "claude-haiku-4-5-20251001"  # Cheaper model for quick analysis
  max_tokens: 4096
  temperature: 0.7
  max_retries: 3

cache:
  enabled: true
  cache_dir: "./runtime/cache"
  ttl: 604800  # 7 days

presentation:
  theme: "academic"
  slide_conversion_tool: "marp"

marp:
  theme: "academic"
  paginate: true
  size: "16:9"
```

## Cost Estimation

### API Costs (approximate)

- **Quick analysis** (abstract + conclusions): ~$0.01 per paper
- **Full analysis**: ~$0.05-0.10 per paper (depending on length)
- **With caching**: 50-70% cost reduction on repeated processing

### Tips to Reduce Costs

1. **Enable caching** (enabled by default)
2. **Use verbose mode** to track costs: `--verbose`
3. **Process papers once** and reuse cached results
4. **Clear cache periodically**: `python cli/main.py cleanup`

## Architecture

```
PaperReader/
├── papers/              # Input PDF papers
├── src/
│   ├── parser/
│   ├── analysis/
│   ├── generation/
│   ├── core/
│   ├── planning/
│   ├── prompts/
│   └── utils.py
├── templates/
│   └── ppt_template.md  # Slide template
├── runtime/
│   ├── cache/           # Cached analysis results
│   └── logs/            # Log files
├── outputs/             # Generated presentations and artifacts
├── config.yaml          # Configuration
└── requirements.txt     # Dependencies
```

## Troubleshooting

### PDF Parsing Issues

**Problem**: "No extractable text found"

**Solution**: The PDF may be scanned. Currently, scanned PDFs are not supported. Use OCR tools to convert to text.

### API Errors

**Problem**: "API key not found"

**Solution**: Set the `ANTHROPIC_API_KEY` environment variable or create a `.env` file.

**Problem**: "Rate limit exceeded"

**Solution**: The tool will automatically retry with exponential backoff. Wait a moment and try again.

### Marp Conversion Issues

**Problem**: "Marp CLI not found"

**Solution**:
- Install Marp CLI: `npm install -g @marp-team/marp-cli`
- Or use `--format markdown` to generate Markdown only
- The tool will fallback to standalone HTML generation

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License

## Acknowledgments

- Powered by [Anthropic Claude](https://www.anthropic.com/)
- Presentation generation with [Marp](https://marp.app/)
- PDF parsing with [PyMuPDF](https://pymupdf.readthedocs.io/)

## Understanding the Data Flow

To better understand how PaperReader processes your papers:

- **[Documentation Center](docs/README.md)** - Complete documentation hub
- **[Data Flow Guide](docs/architecture/DATA_FLOW.md)** - Detailed data flow explanation
- **[Quick Reference](docs/architecture/DATA_FLOW_QUICK_REFERENCE.md)** - Quick reference card
- **[Project Improvements](docs/project/IMPROVEMENTS_SUMMARY.md)** - Recent pipeline improvements

### Debugging Tool

Track the data flow of a specific paper:

```bash
# Using example data (no API key needed)
python tools/debug_data_flow.py papers/example.pdf --skip-ai

# Real processing (requires API key)
python tools/debug_data_flow.py papers/example.pdf
```

This will show you:
- PDF validation results
- Extracted text and metadata
- AI analysis results
- Generated presentation content
- All intermediate products

## Support

For issues and questions, please [open an issue](https://github.com/yourusername/paperreader/issues).
