#!/bin/bash
#
# Demo script for clean intermediates feature
#
# This script demonstrates the clean intermediates feature
# by showing both default (clean) and debug (--no-clean) modes
#

echo "========================================================================"
echo "Clean Intermediates Feature - Quick Demo"
echo "========================================================================"
echo ""

# Setup: Create some intermediate files
echo "Step 1: Creating sample intermediate files..."
mkdir -p outputs/intermediates/{images,markdown,scripts,plans}
echo "Sample markdown" > outputs/intermediates/markdown/test.md
echo "Sample script" > outputs/intermediates/scripts/test.txt
echo "Sample plan" > outputs/intermediates/plans/test.json

echo "✓ Created test intermediate files"
ls -lh outputs/intermediates/*/test.*
echo ""

# Demo: Dry run cleanup
echo "------------------------------------------------------------------------"
echo "Step 2: Preview cleanup (dry run)"
echo "------------------------------------------------------------------------"
echo ""
python3 scripts/clean_intermediates.py
echo ""

# Demo: Execute cleanup
echo "------------------------------------------------------------------------"
echo "Step 3: Execute cleanup"
echo "------------------------------------------------------------------------"
echo ""
echo "y" | python3 scripts/clean_intermediates.py --execute
echo ""

# Verify cleanup
echo "------------------------------------------------------------------------"
echo "Step 4: Verify files cleaned and structure recreated"
echo "------------------------------------------------------------------------"
echo ""

if [ ! -f "outputs/intermediates/markdown/test.md" ]; then
    echo "✓ Intermediate files successfully deleted"
else
    echo "✗ Files still exist"
    exit 1
fi

if [ -d "outputs/intermediates/images" ] && [ -d "outputs/intermediates/markdown" ]; then
    echo "✓ Directory structure successfully recreated"
    ls -la outputs/intermediates/
else
    echo "✗ Directory structure not recreated"
    exit 1
fi

echo ""
echo "========================================================================"
echo "Demo Complete!"
echo "========================================================================"
echo ""
echo "Summary:"
echo "  • Clean intermediates feature works correctly"
echo "  • Manual cleanup script provides control"
echo "  • Directory structure is maintained"
echo ""
echo "Next steps:"
echo "  • Run pipeline: python cli/main.py pipeline --paper your_paper.pdf"
echo "  • Debug mode: python cli/main.py pipeline --paper your_paper.pdf --no-clean"
echo "  • Manual clean: python scripts/clean_intermediates.py --execute"
echo ""
