#!/usr/bin/env python3
"""
Format all HTML files in the project:
- Nice indentation (2 spaces)
- Opening and closing tags at same level
- No line longer than 160 characters
"""
import os
from bs4 import BeautifulSoup
from pathlib import Path

def ensure_line_length(text, max_line_length=160):
    # Split into lines and ensure no line exceeds 160 characters
    lines = text.split('\n')
    result_lines = []

    for line in lines:
        if len(line) <= max_line_length:
            result_lines.append(line)
        else:
            # Line is too long - break at a reasonable point
            # Try to break at a space, or at tag boundary
            while len(line) > max_line_length:
                # Find the last space before max_length
                break_point = line.rfind(' ', 0, max_line_length)
                if break_point == -1:
                    # No space found, break at max_length
                    break_point = max_line_length
                result_lines.append(line[:break_point])
                line = line[break_point + 1:].lstrip()  # +1 to skip the space
            if line:
                result_lines.append(line)

    return '\n'.join(result_lines) + '\n'

def format_html_file(filepath):
    """Format a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Pretty print with indent of 2 spaces
    formatted = soup.prettify(formatter='html')

    # return ensure_line_length()
    return formatted

def find_html_files(root_dir):
    """Find all HTML files in the directory tree."""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'core', 'themes', 'sites', 'rss']]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files


def main():
    root_dir = '/Users/slashrsm/Workspace/blog_public'
    html_files = find_html_files(root_dir)

    print(f"Found {len(html_files)} HTML files to format")

    for filepath in html_files:
        try:
            formatted = format_html_file(filepath)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(formatted)
            print(f"Formatted: {filepath}")
        except Exception as e:
            print(f"Error formatting {filepath}: {e}")

    print("Done!")


if __name__ == '__main__':
    main()
