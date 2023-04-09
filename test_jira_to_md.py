#!/usr/bin/env python3

import re
from textwrap import dedent
import unittest
from io import StringIO
from unittest.mock import patch

from jira_to_md import (convert_line, convert_multiline_elements,
                        jira_to_markdown, process_code_block)


class TestJiraToMd(unittest.TestCase):
    def test_convert_line(self):
        self.assertEqual(convert_line('h1. Header'), '# Header')
        self.assertEqual(convert_line('h2. Header'), '## Header')
        self.assertEqual(convert_line('h3. Header'), '### Header')
        self.assertEqual(convert_line('h4. Header'), '#### Header')
        self.assertEqual(convert_line('h5. Header'), '##### Header')
        self.assertEqual(convert_line('h6. Header'), '###### Header')
        self.assertEqual(convert_line('*bold*'), '**bold**')
        self.assertEqual(convert_line('_italic_'), '*italic*')
        self.assertEqual(convert_line('{{code}}'), '`code`')
        self.assertEqual(convert_line('-strikethrough-'), '~~strikethrough~~')
        self.assertEqual(convert_line('[link|http://example.com]'), '[link](http://example.com)')
        self.assertEqual(convert_line('- item'), '* item')
        self.assertEqual(convert_line(' [x] task'), '- [x] task')
        self.assertEqual(convert_line(' [ ] task'), '- [ ] task')
        self.assertEqual(convert_line(' [X] task'), '- [X] task')

    def test_convert_multiline_elements(self):
        self.assertEqual(convert_multiline_elements('{code:python}\nprint("Hello World!")\n{code}'), '```python\nprint("Hello World!")\n```')

    def test_process_code_block(self):
        code_block_pattern = r'{code(?:\:([a-zA-Z]+))?}\n(.*?){code}'
        code_block_string = "{code}\nprint('Hello, World!')\n{code}"
        match = re.search(code_block_pattern, code_block_string, flags=re.MULTILINE | re.DOTALL)
        self.assertEqual(process_code_block(match), "```\nprint('Hello, World!')\n```")

    def test_jira_to_markdown(self):
        test_jira_content = dedent('''\
            h1. Test Jira Syntax Formatting

            h2. Header

            - item

            [x] task

            {code:python}
            print('Hello, World!')
            {code}
            ''')

        expected_output = "# Test Jira Syntax Formatting\n\n## Header\n\n* item\n\n- [x] task\n\n```python\nprint('Hello, World!')\n```\n"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.open', return_value=StringIO(test_jira_content)):
                jira_to_markdown("test.jira")
                self.assertEqual(fake_out.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
