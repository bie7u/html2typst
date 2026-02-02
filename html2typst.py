#!/usr/bin/env python3
"""
html2typst - Convert HTML to Typst markup

This module provides functions to convert HTML content to Typst format,
making it easy to integrate HTML content into Typst documents.
"""

from html.parser import HTMLParser
import sys
import argparse


class HTML2TypstConverter(HTMLParser):
    """Convert HTML to Typst markup"""
    
    def __init__(self):
        super().__init__()
        self.output = []
        self.list_depth = 0
        self.in_pre = False
        self.in_code = False
        self.last_was_text = False
        
    def handle_starttag(self, tag, attrs):
        """Handle opening HTML tags"""
        tag_lower = tag.lower()
        
        if tag_lower == 'h1':
            self.output.append('\n= ')
            self.last_was_text = False
        elif tag_lower == 'h2':
            self.output.append('\n== ')
            self.last_was_text = False
        elif tag_lower == 'h3':
            self.output.append('\n=== ')
            self.last_was_text = False
        elif tag_lower == 'h4':
            self.output.append('\n==== ')
            self.last_was_text = False
        elif tag_lower == 'h5':
            self.output.append('\n===== ')
            self.last_was_text = False
        elif tag_lower == 'h6':
            self.output.append('\n====== ')
            self.last_was_text = False
        elif tag_lower == 'p':
            self.output.append('\n\n')
            self.last_was_text = False
        elif tag_lower == 'br':
            self.output.append('\\\n')
            self.last_was_text = False
        elif tag_lower == 'strong' or tag_lower == 'b':
            if self.last_was_text and self.output and not self.output[-1].endswith(' '):
                self.output.append(' ')
            self.output.append('*')
            self.last_was_text = False
        elif tag_lower == 'em' or tag_lower == 'i':
            if self.last_was_text and self.output and not self.output[-1].endswith(' '):
                self.output.append(' ')
            self.output.append('_')
            self.last_was_text = False
        elif tag_lower == 'code':
            self.in_code = True
            if self.last_was_text and self.output and not self.output[-1].endswith(' '):
                self.output.append(' ')
            self.output.append('`')
            self.last_was_text = False
        elif tag_lower == 'pre':
            self.in_pre = True
            self.output.append('\n```\n')
            self.last_was_text = False
        elif tag_lower == 'ul' or tag_lower == 'ol':
            self.list_depth += 1
            self.output.append('\n')
            self.last_was_text = False
        elif tag_lower == 'li':
            indent = '  ' * (self.list_depth - 1)
            self.output.append(f'{indent}- ')
            self.last_was_text = False
        elif tag_lower == 'a':
            # Extract href attribute
            href = dict(attrs).get('href', '')
            if href:
                if self.last_was_text and self.output and not self.output[-1].endswith(' '):
                    self.output.append(' ')
                self.output.append('#link("' + href + '")[')
            self.last_was_text = False
        elif tag_lower == 'blockquote':
            self.output.append('\n#quote[')
            self.last_was_text = False
        elif tag_lower == 'hr':
            self.output.append('\n#line(length: 100%)\n')
            self.last_was_text = False
    
    def handle_endtag(self, tag):
        """Handle closing HTML tags"""
        tag_lower = tag.lower()
        
        if tag_lower in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.output.append('\n')
            self.last_was_text = False
        elif tag_lower == 'strong' or tag_lower == 'b':
            self.output.append('*')
            self.last_was_text = True
        elif tag_lower == 'em' or tag_lower == 'i':
            self.output.append('_')
            self.last_was_text = True
        elif tag_lower == 'code':
            self.in_code = False
            self.output.append('`')
            self.last_was_text = True
        elif tag_lower == 'pre':
            self.in_pre = False
            self.output.append('\n```\n')
            self.last_was_text = False
        elif tag_lower == 'ul' or tag_lower == 'ol':
            self.list_depth -= 1
            self.output.append('\n')
            self.last_was_text = False
        elif tag_lower == 'li':
            self.output.append('\n')
            self.last_was_text = False
        elif tag_lower == 'a':
            self.output.append(']')
            self.last_was_text = True
        elif tag_lower == 'blockquote':
            self.output.append(']\n')
            self.last_was_text = False
    
    def handle_data(self, data):
        """Handle text content"""
        if self.in_pre or self.in_code:
            self.output.append(data)
        else:
            # Clean up whitespace but preserve intentional spacing
            cleaned = ' '.join(data.split())
            if cleaned:
                # Add space before text if previous was a closing formatting tag
                # but not if the text starts with punctuation
                if self.last_was_text and self.output and not self.output[-1].endswith(' '):
                    if not cleaned[0] in '.,;:!?)]}':
                        self.output.append(' ')
                self.output.append(cleaned)
                self.last_was_text = True
    
    def get_typst(self):
        """Get the converted Typst output"""
        result = ''.join(self.output)
        # Clean up extra newlines
        while '\n\n\n' in result:
            result = result.replace('\n\n\n', '\n\n')
        # Clean up spaces before newlines
        result = result.replace(' \n', '\n')
        # Clean up multiple spaces
        while '  ' in result:
            result = result.replace('  ', ' ')
        return result.strip()


def html_to_typst(html_content):
    """
    Convert HTML content to Typst markup.
    
    Args:
        html_content (str): HTML content to convert
        
    Returns:
        str: Typst markup
        
    Example:
        >>> html = '<h1>Title</h1><p>Hello <strong>world</strong>!</p>'
        >>> typst = html_to_typst(html)
        >>> print(typst)
        = Title
        
        Hello *world*!
    """
    converter = HTML2TypstConverter()
    converter.feed(html_content)
    return converter.get_typst()


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Convert HTML to Typst markup',
        epilog='Example: html2typst input.html -o output.typ'
    )
    parser.add_argument(
        'input',
        nargs='?',
        help='Input HTML file (or read from stdin if not provided)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file (or write to stdout if not provided)'
    )
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            html_content = f.read()
    else:
        html_content = sys.stdin.read()
    
    # Convert
    typst_content = html_to_typst(html_content)
    
    # Write output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(typst_content)
        print(f'Converted HTML to Typst: {args.output}', file=sys.stderr)
    else:
        print(typst_content)


if __name__ == '__main__':
    main()
