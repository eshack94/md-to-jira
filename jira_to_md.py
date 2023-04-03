#!/usr/bin/env python3

# Description:
#
# This script converts a JIRA/Confluence markup syntax file to a markdown file.
# It will write to stdout, so you can redirect the output to a file if desired.
#
# The original JIRA file will not be modified unless you redirect the output
# to the same file.

# Usage:
# python3 jira_to_md.py <jira_file>
# python3 jira_to_md.py <jira_file> > <markdown_file>
# python3 jira_to_md.py <jira_file> | pbcopy

import sys
import re


def convert_line(line):
    # Convert headers
    line = re.sub(r'^h1\.\s*(.+)', r'# \1', line)
    line = re.sub(r'^h2\.\s*(.+)', r'## \1', line)
    line = re.sub(r'^h3\.\s*(.+)', r'### \1', line)
    line = re.sub(r'^h4\.\s*(.+)', r'#### \1', line)
    line = re.sub(r'^h5\.\s*(.+)', r'##### \1', line)
    line = re.sub(r'^h6\.\s*(.+)', r'###### \1', line)

    # Convert bold and italic
    line = re.sub(r'\*(.+?)\*', r'**\1**', line)
    line = re.sub(r'_([^_]+)_', r'*\1*', line)

    # Convert inline code
    line = re.sub(r'{{([^}]+)}}', r'`\1`', line)

    # Convert strikethrough
    line = re.sub(r'-(.+?)-', r'~~\1~~', line)

    # Convert links
    line = re.sub(r'\[(.*?)\|(.+?)\]', r'[\1](\2)', line)

    # Convert unordered lists
    line = re.sub(r'^-\s+', r'* ', line)

    # Convert GFM task lists
    line = re.sub(r'^\s*\[(x|X| )\]', lambda match: f'- [{match.group(1)}]', line)

    return line


def convert_multiline_elements(content):
    # Convert multiline code blocks
    content = re.sub(r'{code(?:\:([a-zA-Z]+))?}\n(.*?){code}', process_code_block, content, flags=re.MULTILINE | re.DOTALL)

    return content


def process_code_block(match):
    lang = match.group(1)
    code = match.group(2)
    if lang:
        return f'```{lang}\n{code}```'
    else:
        return f'```\n{code}```'


def jira_to_markdown(file_path):
    with open(file_path, "r") as jira_file:
        content = jira_file.read()

    # Convert multiline elements
    content = convert_multiline_elements(content)

    # Process the lines
    # add toggle flag to keep track of whether we're in a code block or not
    # so we don't convert # characters in code blocks
    # toggles on when we enter a code block and toggles off when we exit
    # toggle state determines whether we convert the line or not
    in_code_block = False
    md_lines = []
    for line in content.splitlines():
        if line.startswith("```") or line.startswith("{code"):
            in_code_block = not in_code_block

        if not in_code_block:
            line = convert_line(line)
        md_lines.append(line)

    # Print the converted lines
    for md_line in md_lines:
        print(md_line)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n".join(line.strip() for line in """
        Usage:
        python3 jira_to_md.py <jira_file>
        python3 jira_to_md.py <jira_file> > <markdown_file>
        python3 jira_to_md.py <jira_file> | pbcopy
        """.split("\n")))

        print("\n".join(line.strip() for line in """
        Examples:
        python3 jira_to_md.py README.jira
        python3 jira_to_md.py README.jira > README.md
        python3 jira_to_md.py README.jira | pbcopy
        """.split("\n")))
        sys.exit(1)

    jira_file_path = sys.argv[1]
    jira_to_markdown(jira_file_path)
