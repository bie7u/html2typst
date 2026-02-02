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
- `style="background-color: #rrggbb"` → `#highlight(fill: rgb(...))[...]`
- `style="font-size: small|large|huge|px|pt|em"` → `#text(size: ...)[...]`
- Support for multiple styles on a single element
- Proper handling of block-level alignment wrapping entire paragraphs

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

## License

MIT