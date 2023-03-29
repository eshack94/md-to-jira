#!/usr/bin/env python3

# Author: Elijah Shackelford (eshack94)

# This script converts a markdown file to Jira/Confluence markup syntax.
# It will write to stdout, so you can redirect the output to a file if desired.
#
# The original markdown file will not be modified unless you redirect the output
# to the same file.

# Usage:
# python3 md_to_jira.py <markdown_file>
# python3 md_to_jira.py <markdown_file> > <jira_file>
# python3 md_to_jira.py <markdown_file> | pbcopy

import sys
import re


def convert_line(line):
    # Convert headers
    line = re.sub(r'^#{6}\s*(.+)', r'h6. \1', line)
    line = re.sub(r'^#{5}\s*(.+)', r'h5. \1', line)
    line = re.sub(r'^#{4}\s*(.+)', r'h4. \1', line)
    line = re.sub(r'^#{3}\s*(.+)', r'h3. \1', line)
    line = re.sub(r'^#{2}\s*(.+)', r'h2. \1', line)
    line = re.sub(r'^#\s*(.+)', r'h1. \1', line)

    # Convert bold and italic
    line = re.sub(r'\*\*(.+?)\*\*', r'*\1*', line)
    line = re.sub(r'__(.+?)__', r'*\1*', line)
    line = re.sub(r'\*(.+?)\*', r'_\1_', line)
    line = re.sub(r'_(.+?)_', r'_\1_', line)

    # Convert inline code
    line = re.sub(r'`([^`]+)`', r'{{\1}}', line)

    # Convert strikethrough
    line = re.sub(r'~~(.+?)~~', r'-\1-', line)

    # Convert links
    line = re.sub(r'\[(.*?)\]\((.+?)\)', r'[\1|\2]', line)

    # Convert unordered lists
    line = re.sub(r'^\*\s+', r'- ', line)

    # Convert GFM task lists
    line = re.sub(r'^\s*-\s*\[(x|X| )\]', lambda match: f'[{match.group(1)}]', line)

    # Convert fenced code blocks
    line = re.sub(r'```\s*([\s\S]*?)```', r'{code}\1{code}', line)

    return line


def process_code_block(match):
    lang = match.group(1)
    code = match.group(2)
    if lang:
        return f'{{code:{lang}}}\n{code}{{code}}'
    else:
        return f'{{code}}\n{code}{{code}}'


def markdown_to_jira(file_path):
    with open(file_path, "r") as md_file:
        content = md_file.readlines()

    in_code_block = False
    for line in content:
        # Check if we're entering or exiting a fenced code block
        # Uses toggle logic. When we enter a code block, we set the flag to True.
        # When we exit a code block, we set the flag to False.
        if line.strip().startswith("```"):
            in_code_block = not in_code_block

            # Process the code block line
            jira_line = convert_line(line)
        elif not in_code_block:
            # If not inside a code block, process the line normally
            jira_line = convert_line(line)
        else:
            # If inside a code block, don't process the line and keep it as is
            jira_line = line

        print(jira_line, end='')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n".join(line.strip() for line in """
        Usage:
        python3 md_to_jira.py <markdown_file>
        python3 md_to_jira.py <markdown_file> > <jira_file>
        python3 md_to_jira.py <markdown_file> | pbcopy
        """.split("\n")))

        print("\n".join(line.strip() for line in """
        Examples:
        python3 md_to_jira.py README.md
        python3 md_to_jira.py README.md > README.jira
        python3 md_to_jira.py README.md | pbcopy
        """.split("\n")))
        sys.exit(1)

    markdown_file_path = sys.argv[1]
    markdown_to_jira(markdown_file_path)
