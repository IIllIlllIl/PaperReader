# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PaperReader** is an AI-powered academic paper reading and presentation generation tool. It automatically analyzes PDF papers and generates professional academic-style presentation slides.

**Core Workflow**: PDF Input → Text Extraction → AI Analysis → Content Organization → Slide Generation → Output (Markdown/HTML/PDF)

## Technology Stack

- **Language**: Python 3.8+
- **PDF Processing**: PyMuPDF (fitz), PyPDF2
- **AI Integration**: Anthropic Claude API (claude-sonnet-4-6, claude-haiku-4-5-20251001)
- **Presentation**: Marp CLI (Markdown to slides)
- **CLI**: Click
- **Progress UI**: Rich
- **Configuration**: PyYAML

## Architecture

### Module Structure

```
src/
├── pdf_parser.py       # PDF text extraction, section identification, metadata extraction
├── pdf_validator.py    # PDF quality validation, layout detection
├── ai_analyzer.py      # Claude API integration, paper analysis, content generation
├── content_extractor.py # Slide content organization, structure planning
├── ppt_generator.py    # Markdown generation, Marp conversion
├── cache_manager.py    # Analysis result caching (hash-based)
├── resilience.py       # Retry logic, exponential backoff, fallback strategies
├── progress_reporter.py # Rich progress bars and status updates
└── utils.py            # Configuration loading, logging, file utilities
```

### Data Flow

1. **Input**: PDF file in `papers/` directory
2. **Validation**: Check PDF quality and layout type
3. **Extraction**: Parse text, sections, metadata
4. **Caching**: Check for cached analysis (by file hash)
5. **AI Analysis**: Send to Claude API with structured prompts
6. **Content Organization**: Extract slide content from analysis
7. **Generation**: Create Markdown slides
8. **Conversion**: Convert to HTML/PDF using Marp
9. **Output**: Save to `output/` directory

### Key Classes

- `PDFParser`: Extracts text, metadata, sections from PDF
- `PDFValidator`: Validates PDF quality, detects layout type
- `AIAnalyzer`: Interfaces with Claude API for paper analysis
- `ContentExtractor`: Organizes analysis into slide structure
- `PPTGenerator`: Generates Markdown and converts to final format
- `CacheManager`: Manages cached analysis results
- `ResilientAIAnalyzer`: Wraps AIAnalyzer with retry logic

## Common Commands

### Running the Application

```bash
# Process single paper
python main.py process --paper papers/example.pdf

# Process all papers
python main.py process --all

# With options
python main.py process -p papers/example.pdf -f html --verbose

# Cache management
python main.py stats
python main.py clear-cache
python main.py cleanup
```

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Run tests
pytest tests/

# Run with verbose logging
python main.py process -p papers/example.pdf -v
```

## Configuration

Configuration is in `config.yaml`:

- **AI settings**: Model selection, retry behavior, token limits
- **Cache settings**: Enable/disable, TTL, cache directory
- **Presentation settings**: Output format, theme, conversion tool
- **Logging**: Log level, log file location

## Key Design Decisions

### 1. Two-Stage Analysis Strategy
- **Quick Analysis** (Haiku): Analyze abstract + conclusions for rapid overview (~$0.01)
- **Full Analysis** (Sonnet): Deep analysis of entire paper (~$0.05-0.10)
- Reduces cost while maintaining quality

### 2. Hash-Based Caching
- Uses MD5 hash of PDF file to cache analysis results
- Avoids redundant API calls (50-70% cost savings)
- 7-day TTL by default

### 3. Resilience Pattern
- Exponential backoff retry (max 3 attempts)
- Fallback to cheaper model on failure
- Comprehensive error handling

### 4. PDF Quality Validation
- Detects layout type (single-column, multi-column, scanned)
- Assesses text extraction quality
- Provides recommendations before processing

### 5. Modular Architecture
- Clear separation of concerns
- Each module has single responsibility
- Easy to test and maintain

## AI Prompt Engineering

### Full Analysis Prompt Structure

The `FULL_ANALYSIS_PROMPT` in `ai_analyzer.py` extracts:
- Problem statement and motivation
- Method description and innovations
- Experimental setup and results
- Pros and cons (balanced evaluation)
- Conclusions and future work

**Key principles**:
- Structured JSON output for reliable parsing
- Specific constraints (sentence counts, bullet limits)
- Request for concrete details and numbers
- Balanced critical analysis

## Output Formats

### Markdown Structure

Generated Markdown uses Marp format:
```markdown
---
marp: true
theme: academic
paginate: true
size: 16:9
---

## Slide Title

- Bullet point 1
- Bullet point 2
```

### Slide Types

- Title slides (centered, large text)
- Content slides (bulleted lists)
- Two-column layouts (rare)
- Q&A slides

## Testing Strategy

### Unit Tests
- Test PDF parsing accuracy
- Test AI response parsing
- Test Markdown generation
- Test cache operations

### Integration Tests
- End-to-end: PDF → Slides
- Test with real papers from different domains

### Test Data
- Include sample PDFs in `tests/fixtures/`
- Mock API responses for consistent testing

## Performance Considerations

### Cost Optimization
- Use Haiku for quick analysis when possible
- Enable caching by default
- Track costs with `analyzer.get_stats()`

### Speed Optimization
- Cache file I/O operations
- Parallel processing for multiple papers (future)
- Asynchronous API calls (future)

### Memory Management
- Truncate long papers (>150K chars)
- Close PDF files properly
- Clean up temporary resources

## Known Limitations

1. **Scanned PDFs**: Not supported (requires OCR integration)
2. **Multi-column layouts**: Text may be out of order
3. **Formula extraction**: Limited support for mathematical notation
4. **Image extraction**: Basic support, not fully integrated into slides
5. **Marp dependency**: Requires Node.js for HTML/PDF conversion

## Future Enhancements

- OCR support for scanned PDFs
- Image and table extraction
- Multi-template support
- Web UI
- Batch processing optimizations
- Multi-language support

## Error Handling

### Common Errors

1. **API Key Missing**: Check `.env` file or environment variable
2. **PDF Parsing Failed**: Validate PDF quality first
3. **API Rate Limit**: Automatic retry with backoff
4. **Marp Not Found**: Fallback to standalone HTML

### Logging

- Logs saved to `logs/paperreader.log`
- Verbose mode shows progress bars
- Error messages include actionable guidance

## Development Workflow

1. **Add new feature**: Create module in `src/`
2. **Update main.py**: Integrate into processing pipeline
3. **Add tests**: Create `tests/test_*.py`
4. **Update config**: Add configuration options if needed
5. **Update docs**: Update README.md and this file

## Code Conventions

- Follow PEP 8 style
- Use dataclasses for structured data
- Type hints for function signatures
- Docstrings for public methods
- Logging instead of print statements
- Exceptions for error conditions

## Dependencies Management

Core dependencies in `requirements.txt`:
- Keep versions pinned for reproducibility
- Separate dev dependencies (testing, linting)
- Document Node.js dependencies (Marp) separately
