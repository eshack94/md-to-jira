# Markdown to JIRA and Confluence Markup Syntax Converter

Simple Python utilities for converting from Github-flavored Markdown syntax to Atlassian's custom markup syntax, and vice-versa. Useful for code maintainers and doc writers who use GitHub, JIRA, and Confluence.

## Introduction

This is a simple Python utility to convert Markdown to JIRA and Confluence
markup syntax. It is written in Python, and is designed to be used as a command line tool.

It has been purposely designed to be fully self-contained, requiring no external libraries or dependencies.

It is also designed to be easily extensible, so that it can be easily modified to support additional Markdown syntax.

## Requirements

* Requires Python 3.6 or later.
* Tested on MacOS, Linux, and Windows.

## Installation

Clone this repository. There are no external dependencies, so no pip installation is required, and no virtual environment is needed.

It's recommended to add this script to your `PATH` environment variable, so that it can be run from anywhere. 

You could alternatively add it to a `~/scripts/` directory and create a `md_to_jira` alias for it by adding the following line to your `~/.bashrc`, `~/.zshrc`, or `~/.profile` file:

```bash
alias md_to_jira="python3 ~/scripts/md_to_jira.py"
```

It can also be run directly from the cloned repository directory, but this is not recommended.

> **NOTE:** I'll update these instructions when `jira_to_md.py` is added.

## Usage

Below are usage instructions with some simple examples. For each item, the usage syntax is first, followed by an example for illustration purposes.

### Usage Syntax and Examples

```bash
# Convert a markdown file to Jira/Confluence markup and print to stdout
python3 md_to_jira.py <markdown_file>
python3 md_to_jira.py README.md
```

```bash
# Convert a markdown file to Jira/Confluence markup and save to a file
python3 md_to_jira.py <markdown_file> > <jira_file>
python3 md_to_jira.py README.md > README.jira
```

```bash
# Convert a markdown file to Jira/Confluence markup and copy to clipboard (MacOS)
python3 md_to_jira.py <markdown_file> | pbcopy
python3 md_to_jira.py README.md | pbcopy
```

```bash
# Convert a markdown file to Jira/Confluence markup and copy to clipboard (Linux)
python3 md_to_jira.py <markdown_file | xclip -selection clipboard
python3 md_to_jira.py README.md | xclip -selection clipboard
```

```bash
# Convert a markdown file to Jira/Confluence markup and copy to clipboard (Windows)
python3 md_to_jira.py <markdown_file | clip
python3 md_to_jira.py README.md | clip
```

## Features (implemented and planned)

### Current Features (implemented)
- [x] Add support for headers 1-6
- [x] Add support for fenced code blocks
    - [x] Do not convert headers in fenced code blocks
- [x] Add support for indented code blocks
    - [x] Do not convert headers in indented code blocks
- [x] Add support for inline code (backticks) - should be converted to JIRA's monospace syntax
- [x] Add support for bold text
- [x] Add support for italic text
- [x] Add support for strikethrough text
- [x] Add support for unordered lists
- [x] Add support for in-line style links
- [x] Add support for task lists
    * **Note**: Added, but this is not supported by JIRA native markup.

### Feature Roadmap (planned) and other TODOs
- [ ] Add support for tables
- [ ] Add support for horizontal rules
- [ ] Add support for ordered lists
- [ ] Add support for blockquotes
- [ ] Add support for images
- [ ] Add support for emojis
- [ ] Add support for in-line style links with titles (if possible)
- [ ] Add support for reference style links
- [ ] Add support for inline HTML
- [ ] Add `jira_to_md.py` to convert JIRA/Confluence markup to GitHub-flavored Markdown (GFM)
- [ ] Add unit tests
- [ ] Refactor and clean up code once all basic features are implemented
- [ ] Add GitHub Actions config to run unit tests, and do flake8 linting and code style checks
- [ ] **Other features TBD**

### Why did I start this mini-project?

This project was created as a way to avoid having to use Atlassian's custom markup syntax.

I wanted to be able to write Confluence documentation and JIRA updates using Github-flavored Markdown, and then have a simple way to convert it without having to use an online converter, browser extension, or any third-party libraries or dependencies.

## Additional Resources
* [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
* [GitHub Flavored Markdown Spec](https://github.github.com/gfm/)
* [Atlassian Text Formatting Notation Help](https://jira.atlassian.com/secure/WikiRendererHelpAction.jspa?section=all)
* [Confluence Wiki Markup](https://confluence.atlassian.com/doc/confluence-wiki-markup-251003035.html)
