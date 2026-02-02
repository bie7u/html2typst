"""
html2typst: Convert HTML to Typst markup syntax

This module provides functionality to convert HTML documents into Typst markup,
supporting a wide range of HTML tags and preserving document structure.

Typst documentation: https://typst.app/
"""

from typing import Optional, Dict, Callable, Any
from bs4 import BeautifulSoup, NavigableString, Tag
import re


class HTML2Typst:
    """
    Converter class for transforming HTML to Typst markup.
    
    Attributes:
        tag_handlers: Dictionary mapping HTML tag names to conversion functions
    """
    
    def __init__(self):
        """Initialize the HTML to Typst converter with tag handlers."""
        self.tag_handlers: Dict[str, Callable] = {
            # Headings
            'h1': lambda tag: self._heading(tag, 1),
            'h2': lambda tag: self._heading(tag, 2),
            'h3': lambda tag: self._heading(tag, 3),
            'h4': lambda tag: self._heading(tag, 4),
            'h5': lambda tag: self._heading(tag, 5),
            'h6': lambda tag: self._heading(tag, 6),
            
            # Text structure
            'p': self._paragraph,
            'br': lambda tag: '\\\n',
            'hr': lambda tag: '\n#line(length: 100%)\n',
            'div': self._container,
            'span': self._inline,
            
            # Text formatting
            'strong': lambda tag: f'*{self._get_content(tag)}*',
            'b': lambda tag: f'*{self._get_content(tag)}*',
            'em': lambda tag: f'_{self._get_content(tag)}_',
            'i': lambda tag: f'_{self._get_content(tag)}_',
            'u': lambda tag: f'#underline([{self._get_content(tag)}])',
            's': lambda tag: f'#strike([{self._get_content(tag)}])',
            'del': lambda tag: f'#strike([{self._get_content(tag)}])',
            'mark': lambda tag: f'#highlight([{self._get_content(tag)}])',
            'code': lambda tag: f'`{tag.get_text()}`',
            'pre': self._preformatted,
            'blockquote': self._blockquote,
            'sup': lambda tag: f'#super([{self._get_content(tag)}])',
            'sub': lambda tag: f'#sub([{self._get_content(tag)}])',
            
            # Lists
            'ul': self._unordered_list,
            'ol': self._ordered_list,
            'li': self._list_item,
            'dl': self._description_list,
            'dt': lambda tag: f'/ {self._get_content(tag)}',
            'dd': lambda tag: f': {self._get_content(tag)}',
            
            # Links and media
            'a': self._link,
            'img': self._image,
            'figure': self._figure,
            'figcaption': lambda tag: f'  caption: [{self._get_content(tag)}],\n',
            'video': lambda tag: f'// Video: {tag.get("src", "unknown")}\n',
            'audio': lambda tag: f'// Audio: {tag.get("src", "unknown")}\n',
            
            # Tables
            'table': self._table,
            'thead': self._table_section,
            'tbody': self._table_section,
            'tr': self._table_row,
            'th': lambda tag: f'*{self._get_content(tag)}*',
            'td': self._table_cell,
            
            # Semantic HTML5
            'header': self._semantic_section,
            'footer': self._semantic_section,
            'main': self._semantic_section,
            'section': self._semantic_section,
            'article': self._semantic_section,
            'aside': self._semantic_section,
            'nav': self._semantic_section,
            
            # Misc elements
            'abbr': lambda tag: f'#text([{tag.get_text()}])',
            'cite': lambda tag: f'_{self._get_content(tag)}_',
            'time': lambda tag: tag.get_text(),
            'kbd': lambda tag: f'#box(stroke: 0.5pt, inset: 2pt, radius: 2pt)[`{tag.get_text()}`]',
            'var': lambda tag: f'_{self._get_content(tag)}_',
            'samp': lambda tag: f'`{tag.get_text()}`',
            'details': self._details,
            'summary': lambda tag: f'*{self._get_content(tag)}*',
            
            # Additional common tags
            'q': lambda tag: f'"{self._get_content(tag)}"',
            'small': lambda tag: f'#text(size: 0.85em)[{self._get_content(tag)}]',
            'ins': lambda tag: f'#underline([{self._get_content(tag)}])',
        }
    
    def _get_content(self, tag: Tag) -> str:
        """
        Recursively process child elements of a tag.
        
        Args:
            tag: BeautifulSoup Tag object
            
        Returns:
            Processed Typst content as string
        """
        result = []
        for child in tag.children:
            result.append(self._process_node(child))
        return ''.join(result)
    
    def _process_node(self, node: Any) -> str:
        """
        Process a single DOM node (tag or text).
        
        Args:
            node: BeautifulSoup node (Tag or NavigableString)
            
        Returns:
            Typst representation of the node
        """
        if isinstance(node, NavigableString):
            # Handle text nodes
            text = str(node)
            # Preserve whitespace but normalize excessive newlines
            text = re.sub(r'\n\s*\n', '\n\n', text)
            return text
        elif isinstance(node, Tag):
            # Handle element nodes
            tag_name = node.name.lower()
            if tag_name in self.tag_handlers:
                return self.tag_handlers[tag_name](node)
            else:
                # Fallback: process children for unsupported tags
                return self._get_content(node)
        return ''
    
    def _heading(self, tag: Tag, level: int) -> str:
        """Convert heading tags to Typst heading syntax."""
        prefix = '=' * level
        content = self._get_content(tag)
        return f'\n{prefix} {content}\n'
    
    def _paragraph(self, tag: Tag) -> str:
        """Convert paragraph tag to Typst paragraph."""
        content = self._get_content(tag)
        return f'\n{content}\n'
    
    def _container(self, tag: Tag) -> str:
        """Convert div/container tags."""
        content = self._get_content(tag)
        return f'\n{content}\n'
    
    def _inline(self, tag: Tag) -> str:
        """Convert inline span tags."""
        return self._get_content(tag)
    
    def _preformatted(self, tag: Tag) -> str:
        """Convert pre tag to Typst code block."""
        # Check if there's a nested code tag
        code_tag = tag.find('code')
        if code_tag:
            code_content = code_tag.get_text()
            lang = code_tag.get('class', [''])[0].replace('language-', '') if code_tag.get('class') else ''
        else:
            code_content = tag.get_text()
            lang = ''
        
        if lang:
            return f'\n```{lang}\n{code_content}\n```\n'
        else:
            return f'\n```\n{code_content}\n```\n'
    
    def _blockquote(self, tag: Tag) -> str:
        """Convert blockquote to Typst block quote."""
        content = self._get_content(tag).strip()
        # Indent each line with "> " for block quote style
        lines = content.split('\n')
        quoted = '\n'.join(f'  {line}' if line.strip() else '' for line in lines)
        return f'\n#quote(block: true)[\n{quoted}\n]\n'
    
    def _unordered_list(self, tag: Tag) -> str:
        """Convert ul tag to Typst unordered list."""
        content = self._get_content(tag)
        return f'\n{content}\n'
    
    def _ordered_list(self, tag: Tag) -> str:
        """Convert ol tag to Typst ordered list."""
        content = self._get_content(tag)
        return f'\n#enum(\n{content})\n'
    
    def _list_item(self, tag: Tag) -> str:
        """Convert li tag to Typst list item."""
        content = self._get_content(tag).strip()
        # Check if parent is ol or ul
        parent = tag.parent
        if parent and parent.name == 'ol':
            return f'  [{content}],\n'
        else:
            return f'- {content}\n'
    
    def _description_list(self, tag: Tag) -> str:
        """Convert dl tag to Typst description list."""
        content = self._get_content(tag)
        return f'\n{content}\n'
    
    def _link(self, tag: Tag) -> str:
        """Convert anchor tag to Typst link."""
        href = tag.get('href', '')
        text = self._get_content(tag)
        if href:
            return f'#link("{href}")[{text}]'
        else:
            return text
    
    def _image(self, tag: Tag) -> str:
        """Convert img tag to Typst image."""
        src = tag.get('src', '')
        alt = tag.get('alt', '')
        width = tag.get('width', '')
        
        if not src:
            return f'// Image missing src'
        
        params = [f'"{src}"']
        if alt:
            params.append(f'alt: "{alt}"')
        if width:
            # Try to parse width
            if width.endswith('%'):
                params.append(f'width: {width}')
            elif width.isdigit():
                params.append(f'width: {width}pt')
        
        return f'#image({", ".join(params)})'
    
    def _figure(self, tag: Tag) -> str:
        """Convert figure tag to Typst figure."""
        # Extract image and caption
        img_tag = tag.find('img')
        caption_tag = tag.find('figcaption')
        
        content = []
        if img_tag:
            content.append(self._image(img_tag))
        
        result = '#figure(\n'
        if content:
            result += f'  {content[0]},\n'
        
        if caption_tag:
            caption_text = self._get_content(caption_tag)
            result += f'  caption: [{caption_text}],\n'
        
        result += ')\n'
        return result
    
    def _table(self, tag: Tag) -> str:
        """Convert table tag to Typst table."""
        # Count columns
        first_row = tag.find('tr')
        if first_row:
            cols = len(first_row.find_all(['th', 'td']))
        else:
            cols = 1
        
        # Process table content
        rows = []
        for row_tag in tag.find_all('tr'):
            cells = []
            for cell in row_tag.find_all(['th', 'td']):
                cell_content = self._get_content(cell).strip()
                # Handle header cells
                if cell.name == 'th':
                    cells.append(f'*{cell_content}*')
                else:
                    cells.append(cell_content)
            if cells:
                rows.append(cells)
        
        # Build table syntax
        result = f'#table(\n  columns: {cols},\n'
        for row in rows:
            for cell in row:
                result += f'  [{cell}],\n'
        result += ')\n'
        return result
    
    def _table_section(self, tag: Tag) -> str:
        """Process thead/tbody sections."""
        return self._get_content(tag)
    
    def _table_row(self, tag: Tag) -> str:
        """Process table row."""
        return self._get_content(tag)
    
    def _table_cell(self, tag: Tag) -> str:
        """Process table cell."""
        return self._get_content(tag)
    
    def _semantic_section(self, tag: Tag) -> str:
        """Convert semantic HTML5 tags."""
        content = self._get_content(tag)
        # Add comment to indicate section type
        tag_name = tag.name
        return f'\n// {tag_name.upper()}\n{content}\n'
    
    def _details(self, tag: Tag) -> str:
        """Convert details/summary tags."""
        summary = tag.find('summary')
        if summary:
            summary_text = self._get_content(summary)
            # Remove summary from content processing
            summary.extract()
        else:
            summary_text = 'Details'
        
        content = self._get_content(tag).strip()
        return f'\n// {summary_text}\n{content}\n'
    
    def convert(self, html: str) -> str:
        """
        Convert HTML to Typst markup.
        
        Args:
            html: HTML string to convert
            
        Returns:
            Typst markup string
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Process the body if it exists, otherwise process the whole document
        body = soup.find('body')
        if body:
            result = self._get_content(body)
        else:
            result = self._get_content(soup)
        
        # Clean up excessive whitespace
        result = re.sub(r'\n\s*\n\s*\n+', '\n\n', result)
        return result.strip()


def html_to_typst(html: str) -> str:
    """
    Convert HTML string to Typst markup.
    
    This is the main entry point for HTML to Typst conversion.
    
    Args:
        html: HTML content as a string
        
    Returns:
        Typst markup as a string
        
    Example:
        >>> html = '<h1>Hello</h1><p>World</p>'
        >>> typst = html_to_typst(html)
        >>> print(typst)
        = Hello
        
        World
    """
    converter = HTML2Typst()
    return converter.convert(html)


if __name__ == '__main__':
    import sys
    
    # CLI example
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            html_content = f.read()
    else:
        # Example HTML
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sample Document</title>
        </head>
        <body>
            <h1>Main Title</h1>
            <p>This is a <strong>bold</strong> and <em>italic</em> example.</p>
            
            <h2>Lists</h2>
            <ul>
                <li>First item</li>
                <li>Second item</li>
                <li>Third item</li>
            </ul>
            
            <ol>
                <li>Numbered one</li>
                <li>Numbered two</li>
            </ol>
            
            <h2>Code</h2>
            <p>Inline code: <code>print("hello")</code></p>
            
            <pre><code>
def hello():
    print("Hello, world!")
            </code></pre>
            
            <h2>Links and Images</h2>
            <p>Visit <a href="https://typst.app">Typst</a> for more info.</p>
            <img src="image.png" alt="Sample image" />
            
            <h2>Table</h2>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Age</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Alice</td>
                        <td>30</td>
                    </tr>
                    <tr>
                        <td>Bob</td>
                        <td>25</td>
                    </tr>
                </tbody>
            </table>
            
            <blockquote>
                This is a block quote with some wisdom.
            </blockquote>
            
            <hr>
            
            <footer>
                <p>Footer content</p>
            </footer>
        </body>
        </html>
        """
    
    # Convert and print
    typst_output = html_to_typst(html_content)
    print(typst_output)
    print("\n" + "="*50)
    print("Conversion complete!")
