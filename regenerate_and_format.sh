#!/bin/bash
#
# Script to regenerate the frontpage and format all HTML files
#
# This script:
# 1. Activates the Python virtual environment
# 2. Runs regenerate_frontpage.py to regenerate index.html
# 3. Runs format_html.py to format all HTML files
# 4. Deactivates the virtual environment
#

set -e  # Exit on any error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "Regenerating frontpage and formatting"
echo "========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if beautifulsoup4 is installed, install if not
if ! python -c "import bs4" 2>/dev/null; then
    echo "Installing beautifulsoup4..."
    pip install beautifulsoup4
fi

# Run regenerate_frontpage.py
echo ""
echo "Running regenerate_frontpage.py..."
python regenerate_frontpage.py

# Run format_html.py
echo ""
echo "Running format_html.py..."
python format_html.py

# Deactivate virtual environment
echo ""
echo "Deactivating virtual environment..."
deactivate

echo ""
echo "========================================="
echo "Done!"
echo "========================================="
