# html2typst

Convert HTML documents to [Typst](https://typst.app/) markup syntax.

## Features

This module provides comprehensive HTML to Typst conversion with support for:

### Text & Structure
- Headings (`<h1>` - `<h6>`) → Typst headings (`=`, `==`, `===`, ...)
- Paragraphs (`<p>`)
- Line breaks (`<br>`)
- Horizontal rules (`<hr>`)
- Containers (`<div>`, `<span>`)

### Text Formatting
- Bold (`<strong>`, `<b>`) → `*bold*`
- Italic (`<em>`, `<i>`) → `_italic_`
- Underline (`<u>`) → `#underline()`
- Strikethrough (`<s>`, `<del>`) → `#strike()`
- Highlight (`<mark>`) → `#highlight()`
- Inline code (`<code>`) → `` `code` ``
- Code blocks (`<pre>`) → ` ```code``` `
- Block quotes (`<blockquote>`)
- Superscript/subscript (`<sup>`, `<sub>`)

### Lists
- Unordered lists (`<ul>`)
- Ordered lists (`<ol>`)
- List items (`<li>`)
- Description lists (`<dl>`, `<dt>`, `<dd>`)

### Links & Media
- Links (`<a href="">`) → `#link()`
- Images (`<img>`) → `#image()`
- Figures (`<figure>`, `<figcaption>`)
- Video/audio placeholders

### Tables
- Tables (`<table>`)
- Table sections (`<thead>`, `<tbody>`)
- Table rows and cells (`<tr>`, `<th>`, `<td>`)

### Semantic HTML5
- `<header>`, `<footer>`, `<main>`
- `<section>`, `<article>`, `<aside>`
- `<nav>`

### Misc Elements
- `<abbr>`, `<cite>`, `<time>`
- `<kbd>`, `<var>`, `<samp>`
- `<details>`, `<summary>`
- And more...

### Inline CSS Styles (Quill.js Support)
- `style="text-align: center|left|right"` → `#align(center|left|right)[...]`
- `style="text-align: justify"` → `#par(justify: true)[...]`
- `style="color: #rrggbb"` → `#text(fill: rgb(...))[...]`
- `style="color: red|blue|green|..."` → `#text(fill: color)[...]` (standard CSS colors)
- `style="background-color: #rrggbb"` → `#highlight(fill: rgb(...))[...]`
- `style="font-size: small|large|huge|px|pt|em"` → `#text(size: ...)[...]`
- Support for multiple styles on a single element
- Proper handling of block-level alignment wrapping entire paragraphs
- CSS keywords (`inherit`, `initial`, `transparent`, `currentColor`, etc.) are properly handled and don't generate invalid Typst code
- CSS system colors (`windowtext`, `buttonface`, etc.) are gracefully ignored while preserving content
- Unknown or invalid style values preserve content as plain text without generating errors

### Content Preservation Policy
**html2typst** follows a strict content preservation policy:
- **Unknown HTML tags**: Content is preserved as plain text
- **Invalid CSS values**: Content is preserved without the invalid style
- **Unsupported styles**: Content is preserved, unsupported styles are ignored
- **No errors on unknown syntax**: The converter never throws errors or cuts content due to unrecognized HTML or CSS

This ensures that even when converting HTML with non-standard elements or styles, your text content is never lost.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### As a Module

```python
from html2typst import html_to_typst

html = """
<h1>Hello World</h1>
<p>This is a <strong>bold</strong> statement.</p>
<ul>
    <li>First item</li>
    <li>Second item</li>
</ul>
"""

typst = html_to_typst(html)
print(typst)
```

### Command Line

Run with example HTML:
```bash
python html2typst.py
```

Convert an HTML file:
```bash
python html2typst.py input.html
```

## Example

**Input HTML:**
```html
<h1>Document Title</h1>
<p>A paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
<ul>
    <li>Item 1</li>
    <li>Item 2</li>
</ul>
```

**Output Typst:**
```typst
= Document Title

A paragraph with *bold* and _italic_ text.

- Item 1
- Item 2
```

### Quill.js Editor HTML

**Input HTML (from Quill.js):**
```html
<p style="text-align: center;"><strong>Centered Title</strong></p>
<p style="color: #333333;">Paragraph with custom text color.</p>
<p><span style="background-color: #ffff00;">Highlighted text</span> in a paragraph.</p>
<p style="text-align: right; font-size: small;">Small right-aligned text</p>
```

**Output Typst:**
```typst
#align(center)[*Centered Title*]

#text(fill: rgb(51, 51, 51))[Paragraph with custom text color.]

#highlight(fill: rgb(255, 255, 0))[Highlighted text] in a paragraph.

#align(right)[#text(size: 0.85em)[Small right-aligned text]]
```

## Architecture

The converter uses:
- **BeautifulSoup** for HTML parsing
- **Recursive DOM traversal** to preserve document structure
- **Extensible tag mapping** - easily add new tag handlers in one place
- **Type hints** and docstrings for maintainability

## Extending

To add support for new HTML tags, simply add an entry to the `tag_handlers` dictionary in the `HTML2Typst` class:

```python
self.tag_handlers['newtag'] = lambda tag: f'#newtag([{self._get_content(tag)}])'
```

## Troubleshooting

### Content not appearing in PDF after conversion

If you're experiencing issues where content doesn't appear in your PDF after converting HTML with `text-align: justify`:

1. **Verify the conversion worked**: Check that the generated `.typ` file contains your content
   ```python
   from html2typst import html_to_typst
   result = html_to_typst(your_html)
   print(result)  # Should show your content wrapped in #par(justify: true)[...]
   ```

2. **Check Typst version**: This library works with Typst 0.10.0 or later. The `#par(justify: true)` syntax has been tested and verified with Typst 0.12.0. Check your version:
   ```bash
   typst --version
   ```

3. **Test compilation**: Try compiling the generated Typst file manually:
   ```bash
   typst compile output.typ
   ```
   If you see errors, please report them as an issue.

4. **Encoding issues**: Always use UTF-8 encoding when reading HTML and writing Typst files:
   ```python
   with open('input.html', 'r', encoding='utf-8') as f:
       html = f.read()
   
   typst = html_to_typst(html)
   
   with open('output.typ', 'w', encoding='utf-8') as f:
       f.write(typst)
   ```

5. **Example script**: See `example_justify_usage.py` for a complete working example with justified text.

### Verified working

The library has been tested with Typst 0.12.0 and handles:
- Multiple paragraphs with `text-align: justify`
- Non-breaking spaces (`&nbsp;`)
- Superscripts and subscripts within justified text
- Nested inline styles (color, bold, etc.) within justified paragraphs
- Empty or whitespace-only justified paragraphs

If you're still experiencing issues, please open an issue with:
- Your HTML input
- The generated Typst code
- Your Typst version
- Any error messages

## License

MIT