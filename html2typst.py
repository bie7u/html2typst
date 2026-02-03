"""
html2typst: Convert HTML to Typst markup syntax

This module provides functionality to convert HTML documents into Typst markup,
supporting a wide range of HTML tags and preserving document structure.

Typst documentation: https://typst.app/
"""

from typing import Optional, Dict, Callable, Any, Tuple
from bs4 import BeautifulSoup, NavigableString, Tag
import re


def parse_inline_css(style: str) -> Dict[str, str]:
    """
    Parse inline CSS style attribute into a dictionary.
    
    Args:
        style: CSS style string (e.g., "color: red; font-size: 12px")
        
    Returns:
        Dictionary mapping CSS properties to values
        
    Example:
        >>> parse_inline_css("color: red; font-size: 12px")
        {'color': 'red', 'font-size': '12px'}
    """
    if not style:
        return {}
    
    styles = {}
    # Split by semicolon and parse each property
    for declaration in style.split(';'):
        declaration = declaration.strip()
        if not declaration or ':' not in declaration:
            continue
        
        # Split by first colon only
        prop, value = declaration.split(':', 1)
        prop = prop.strip().lower()
        value = value.strip()
        
        if prop and value:
            styles[prop] = value
    
    return styles


class HTML2Typst:
    """
    Converter class for transforming HTML to Typst markup.
    
    Attributes:
        tag_handlers: Dictionary mapping HTML tag names to conversion functions
    """
    
    # Style constants
    KBD_STROKE = '0.5pt'
    KBD_INSET = '2pt'
    KBD_RADIUS = '2pt'
    
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
            'kbd': lambda tag: f'#box(stroke: {self.KBD_STROKE}, inset: {self.KBD_INSET}, radius: {self.KBD_RADIUS})[`{tag.get_text()}`]',
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
        
        # Join and fix Typst syntax issues
        content = ''.join(result)
        
        # Fix syntax errors when parentheses immediately follow Typst function outputs
        # This prevents Typst from interpreting the parentheses as additional function arguments
        
        # Pattern 1: #function(...)[...](  -> #function(...)[...] (
        # This occurs when styled content (like #text(fill: ...)[...]) is followed by text starting with (
        # We need to be specific to avoid breaking valid Typst syntax like [text](url)
        # Only fix when preceded by ] that follows a Typst function call pattern
        content = re.sub(r'(\#\w+\([^)]*\)\[[^\]]*\])\(', r'\1 (', content)
        
        # Pattern 2: #function([...])( -> #function([...]) (
        # This occurs when functions like #underline([...]) are followed by text starting with (
        content = re.sub(r'(\#\w+\(\[[^\]]*\]\))\(', r'\1 (', content)
        
        return content
    
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
    
    def _should_skip_css_value(self, value: str) -> bool:
        """
        Check if a CSS value should be skipped (not converted to Typst).
        
        Args:
            value: CSS value string
            
        Returns:
            True if the value should be skipped, False otherwise
        """
        # CSS keywords that should not be converted to Typst
        skip_keywords = frozenset({
            'inherit',
            'initial',
            'unset',
            'revert',
            'transparent',
            'currentcolor',
            'auto',
        })
        
        # CSS system colors that are not valid in Typst
        # These are deprecated in modern CSS but still appear in legacy HTML
        css_system_colors = frozenset({
            'activeborder', 'activecaption', 'appworkspace', 'background',
            'buttonface', 'buttonhighlight', 'buttonshadow', 'buttontext',
            'captiontext', 'graytext', 'highlight', 'highlighttext',
            'inactiveborder', 'inactivecaption', 'inactivecaptiontext',
            'infobackground', 'infotext', 'menu', 'menutext', 'scrollbar',
            'threeddarkshadow', 'threedface', 'threedhighlight', 'threedlightshadow',
            'threeddkshadow', 'window', 'windowframe', 'windowtext',
        })
        
        # Check if value is empty or whitespace-only after stripping
        if not value or not value.strip():
            return True
        
        value_lower = value.strip().lower()
        return value_lower in skip_keywords or value_lower in css_system_colors
    
    def _css_color_to_typst(self, color: str) -> str:
        """
        Convert CSS color to Typst rgb() format.
        
        Args:
            color: CSS color string (e.g., "#ff0000", "#f00", "rgb(255,0,0)")
            
        Returns:
            Typst rgb() expression or original color if not a hex/rgb format,
            or None if the color should be skipped
        """
        color = color.strip()
        
        # Skip CSS keywords that don't have Typst equivalents
        if self._should_skip_css_value(color):
            return None
        
        # Handle hex colors #rrggbb or #rgb
        if color.startswith('#'):
            hex_color = color[1:]
            
            # Expand shorthand #rgb to #rrggbb
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            
            if len(hex_color) == 6:
                try:
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    return f'rgb({r}, {g}, {b})'
                except ValueError:
                    # Invalid hex color, return None to skip applying color style
                    return None
        
        # Handle rgb(r, g, b) format
        rgb_match = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', color)
        if rgb_match:
            r, g, b = rgb_match.groups()
            return f'rgb({r}, {g}, {b})'
        
        # CSS named colors to RGB mapping
        # Typst requires colors in rgb() format, so we convert CSS named colors
        css_named_colors_to_rgb = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'lime': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'aqua': (0, 255, 255),
            'fuchsia': (255, 0, 255),
            'silver': (192, 192, 192),
            'gray': (128, 128, 128),
            'maroon': (128, 0, 0),
            'olive': (128, 128, 0),
            'green': (0, 128, 0),
            'purple': (128, 0, 128),
            'teal': (0, 128, 128),
            'navy': (0, 0, 128),
            'orange': (255, 165, 0),
        }
        
        color_lower = color.lower()
        if color_lower in css_named_colors_to_rgb:
            r, g, b = css_named_colors_to_rgb[color_lower]
            return f'rgb({r}, {g}, {b})'
        
        # Unknown color value - skip it to preserve content
        return None
    
    def _css_font_size_to_typst(self, size: str) -> str:
        """
        Convert CSS font-size to Typst size expression.
        
        Args:
            size: CSS font-size value (e.g., "12px", "small", "large", "1.5em")
            
        Returns:
            Typst size value, or None if the size should be skipped
        """
        size = size.strip().lower()
        
        # Skip CSS keywords that don't have Typst equivalents
        if self._should_skip_css_value(size):
            return None
        
        # Named sizes
        size_map = {
            'small': '0.85em',
            'large': '1.2em',
            'huge': '1.5em',
            'x-small': '0.7em',
            'x-large': '1.4em',
            'xx-small': '0.6em',
            'xx-large': '1.6em',
        }
        
        if size in size_map:
            return size_map[size]
        
        # Handle px values (convert to pt)
        if size.endswith('px'):
            try:
                value = float(size[:-2])
                return f'{value}pt'
            except ValueError:
                pass
        
        # Handle pt, em, rem values (pass through)
        if size.endswith(('pt', 'em', 'rem')):
            return size
        
        # Handle numeric values (assume pt)
        try:
            value = float(size)
            return f'{value}pt'
        except ValueError:
            pass
        
        return size
    
    def _apply_inline_styles(self, content: str, styles: Dict[str, str]) -> str:
        """
        Apply inline CSS styles to content by wrapping with Typst functions.
        
        Args:
            content: The text content to style
            styles: Dictionary of CSS properties
            
        Returns:
            Content wrapped with appropriate Typst styling functions
        """
        result = content
        
        # Apply text color
        if 'color' in styles:
            color_typst = self._css_color_to_typst(styles['color'])
            if color_typst is not None:
                result = f'#text(fill: {color_typst})[{result}]'
        
        # Apply background color (highlight)
        if 'background-color' in styles:
            bg_color = self._css_color_to_typst(styles['background-color'])
            if bg_color is not None:
                result = f'#highlight(fill: {bg_color})[{result}]'
        
        # Apply font size
        if 'font-size' in styles:
            size = self._css_font_size_to_typst(styles['font-size'])
            if size is not None:
                result = f'#text(size: {size})[{result}]'
        
        return result
    
    def _apply_block_styles(self, content: str, styles: Dict[str, str]) -> str:
        """
        Apply block-level CSS styles to content.
        
        Args:
            content: The text content to style
            styles: Dictionary of CSS properties
            
        Returns:
            Content wrapped with appropriate Typst block-level functions
        """
        result = content
        
        # Apply text alignment
        if 'text-align' in styles:
            alignment = styles['text-align'].lower()
            if alignment == 'justify':
                # In Typst, text justification uses #par(justify: true) not #align()
                result = f'#par(justify: true)[{result}]'
            elif alignment in ('left', 'center', 'right'):
                result = f'#align({alignment})[{result}]'
        
        return result
    
    def _paragraph(self, tag: Tag) -> str:
        """Convert paragraph tag to Typst paragraph."""
        # Get inline styles
        style_attr = tag.get('style', '')
        styles = parse_inline_css(style_attr)
        
        # Get content
        content = self._get_content(tag)
        
        # Apply inline styles (color, background, font-size)
        inline_style_keys = {'color', 'background-color', 'font-size'}
        inline_styles = {k: v for k, v in styles.items() if k in inline_style_keys}
        if inline_styles:
            content = self._apply_inline_styles(content, inline_styles)
        
        # Apply block styles (alignment)
        block_style_keys = {'text-align'}
        block_styles = {k: v for k, v in styles.items() if k in block_style_keys}
        if block_styles:
            content = self._apply_block_styles(content, block_styles)
        
        return f'\n{content}\n'
    
    def _inline(self, tag: Tag) -> str:
        """Convert inline span tags."""
        # Get inline styles
        style_attr = tag.get('style', '')
        styles = parse_inline_css(style_attr)
        
        # Get content
        content = self._get_content(tag)
        
        # Apply inline styles
        if styles:
            content = self._apply_inline_styles(content, styles)
        
        return content
    
    def _container(self, tag: Tag) -> str:
        """Convert div/container tags."""
        content = self._get_content(tag)
        return f'\n{content}\n'
    
    def _preformatted(self, tag: Tag) -> str:
        """Convert pre tag to Typst code block."""
        # Check if there's a nested code tag
        code_tag = tag.find('code')
        if code_tag:
            code_content = code_tag.get_text()
            # Extract language from class attribute
            lang = ''
            classes = code_tag.get('class', [])
            for cls in classes:
                if cls.startswith('language-'):
                    lang = cls.replace('language-', '')
                    break
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
            # Parse width with better unit handling
            width_str = str(width).strip()
            # Extract numeric value
            match = re.match(r'([0-9.]+)\s*(%|px|pt|em|rem)?', width_str)
            if match:
                value, unit = match.groups()
                if unit == '%':
                    params.append(f'width: {value}%')
                elif unit in ('px', 'pt', None):
                    # Default to pt for numeric values
                    params.append(f'width: {value}pt')
                elif unit in ('em', 'rem'):
                    params.append(f'width: {value}em')
        
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
