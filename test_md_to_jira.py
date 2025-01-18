#!/usr/bin/env python3

import re
from textwrap import dedent
import unittest
from io import StringIO
from unittest.mock import patch

from md_to_jira import convert_line, convert_multiline_elements, markdown_to_jira


class TestMdToJira(unittest.TestCase):
    def test_convert_line(self):
        self.assertEqual(convert_line('# Header'), 'h1. Header')
        self.assertEqual(convert_line('## Header'), 'h2. Header')
        self.assertEqual(convert_line('### Header'), 'h3. Header')
        self.assertEqual(convert_line('#### Header'), 'h4. Header')
        self.assertEqual(convert_line('##### Header'), 'h5. Header')
        self.assertEqual(convert_line('###### Header'), 'h6. Header')
        self.assertEqual(convert_line('**bold**'), '*bold*')
        self.assertEqual(convert_line('__bold__'), '*bold*')
        self.assertEqual(convert_line('*italic*'), '_italic_')
        self.assertEqual(convert_line('_italic_'), '_italic_')
        self.assertEqual(convert_line('`code`'), '{{code}}')
        self.assertEqual(convert_line('~~strikethrough~~'), '-strikethrough-')
        self.assertEqual(convert_line('[link](http://example.com)'), '[link|http://example.com]')
        self.assertEqual(convert_line('* item'), '- item')
        self.assertEqual(convert_line('- [x] task'), '[x] task')
        self.assertEqual(convert_line('- [ ] task'), '[ ] task')
        self.assertEqual(convert_line('- [X] task'), '[X] task')

    def test_convert_multiline_elements(self):
        self.assertEqual(convert_multiline_elements('```python\nprint("Hello World!")\n```'), '{code:python}\nprint("Hello World!")\n{code}')

    def test_markdown_to_jira(self):
        test_md_content = dedent('''\
            # Test Markdown Syntax Formatting

            ## Header

            * item

            - [x] task

            ```python
            print('Hello, World!')
            ```
            ''')

        expected_output = "h1. Test Markdown Syntax Formatting\n\nh2. Header\n\n- item\n\n[x] task\n\n{code:python}\nprint('Hello, World!')\n{code}\n"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.open', return_value=StringIO(test_md_content)):
                markdown_to_jira("test.md")
                self.assertEqual(fake_out.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
