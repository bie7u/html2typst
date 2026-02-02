# html2typst

Convert HTML content to [Typst](https://typst.app/) markup format. This tool makes it easy to integrate HTML content into your Typst documents.

## 🚀 Quick Answer: How to Add HTML to Your Typst Template

**The simplest way:**

1. Convert your HTML to Typst format:
   ```bash
   python3 html2typst.py your-content.html -o content.typ
   ```

2. Include it in your Typst template:
   ```typst
   // my-template.typ
   #set document(title: "My Document")
   
   = My Document
   
   #include "content.typ"  // Your converted HTML content
   
   = Conclusion
   ```

3. Compile with Typst:
   ```bash
   typst compile my-template.typ
   ```

**See [USAGE.md](USAGE.md) for more detailed examples and use cases.**

## Installation

### Option 1: Direct Usage (No Installation)

Simply download the `html2typst.py` file and use it directly:

```bash
python3 html2typst.py input.html -o output.typ
```

### Option 2: Make it Executable

```bash
chmod +x html2typst.py
./html2typst.py input.html -o output.typ
```

### Option 3: Install as a Module

```bash
# Clone the repository
git clone https://github.com/bie7u/html2typst.git
cd html2typst

# Use it in your Python code
python3 -c "from html2typst import html_to_typst; print(html_to_typst('<h1>Hello</h1>'))"
```

## Usage

### Command Line Interface (CLI)

#### Convert an HTML file to Typst:

```bash
python3 html2typst.py input.html -o output.typ
```

#### Read from stdin and write to stdout:

```bash
echo '<h1>Hello World</h1>' | python3 html2typst.py
```

#### Read from stdin, write to file:

```bash
cat mypage.html | python3 html2typst.py -o output.typ
```

### Programmatic Usage (Python API)

Use the `html_to_typst()` function in your Python code:

```python
from html2typst import html_to_typst

# Simple conversion
html = '<h1>My Title</h1><p>Hello <strong>world</strong>!</p>'
typst = html_to_typst(html)
print(typst)
# Output:
# = My Title
# 
# Hello *world*!

# Read HTML from a file and convert
with open('input.html', 'r') as f:
    html_content = f.read()

typst_content = html_to_typst(html_content)

# Write to a Typst file
with open('output.typ', 'w') as f:
    f.write(typst_content)
```

### Integrating HTML into Typst Templates

Here's how to add HTML content to your Typst templates:

#### Method 1: Convert and Include

```bash
# First, convert your HTML to Typst
python3 html2typst.py content.html -o content.typ
```

Then in your Typst template:

```typst
// my-template.typ
#set document(title: "My Document")
#set page(numbering: "1")

= Introduction

// Include the converted HTML content
#include "content.typ"

= Conclusion

This is the end of the document.
```

#### Method 2: Direct String Embedding (Python Script)

Create a Python script to combine HTML conversion with template generation:

```python
from html2typst import html_to_typst

# Your HTML content
html_content = """
<h2>Section from HTML</h2>
<p>This content came from HTML and was converted to Typst.</p>
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
"""

# Convert to Typst
typst_content = html_to_typst(html_content)

# Create your Typst document with the converted content
template = f"""
#set document(title: "My Document")
#set page(numbering: "1")

= Main Title

{typst_content}

= Conclusion

This is the end.
"""

# Write the final document
with open('final-document.typ', 'w') as f:
    f.write(template)

print("Generated: final-document.typ")
```

#### Method 3: Pipeline Approach

```bash
# Convert HTML and pipe directly into a template
cat header.typ > document.typ
python3 html2typst.py content.html >> document.typ
cat footer.typ >> document.typ

# Compile with Typst
typst compile document.typ
```

## Supported HTML Elements

The converter supports common HTML elements:

- **Headings**: `<h1>` to `<h6>` → `=` to `======`
- **Paragraphs**: `<p>` → Double newline
- **Line breaks**: `<br>` → `\`
- **Bold**: `<strong>`, `<b>` → `*text*`
- **Italic**: `<em>`, `<i>` → `_text_`
- **Code**: `<code>` → `` `code` ``
- **Code blocks**: `<pre>` → ` ```code``` `
- **Lists**: `<ul>`, `<ol>`, `<li>` → `- item`
- **Links**: `<a href="...">` → `#link("url")[text]`
- **Quotes**: `<blockquote>` → `#quote[text]`
- **Horizontal rule**: `<hr>` → `#line(length: 100%)`

## Examples

See the `examples/` directory for sample HTML files and their Typst conversions.

### Basic Example

**Input HTML** (`examples/basic.html`):
```html
<h1>Welcome to html2typst</h1>
<p>This tool converts <strong>HTML</strong> to <em>Typst</em> format.</p>
<ul>
  <li>Easy to use</li>
  <li>Supports common elements</li>
  <li>Works with templates</li>
</ul>
```

**Output Typst** (`examples/basic.typ`):
```typst
= Welcome to html2typst

This tool converts *HTML* to _Typst_ format.

- Easy to use
- Supports common elements
- Works with templates
```

### Template Integration Example

**HTML Content** (`examples/content.html`):
```html
<h2>Project Overview</h2>
<p>This is a detailed description of my project.</p>
<h3>Features</h3>
<ul>
  <li>Feature 1</li>
  <li>Feature 2</li>
</ul>
```

**Typst Template** (`examples/template.typ`):
```typst
#set document(title: "Project Report")
#set page(
  paper: "a4",
  numbering: "1 / 1",
)

= Project Report

// Include the converted content
#include "content.typ"

= Conclusion

End of report.
```

**Conversion and Compilation**:
```bash
# Convert HTML to Typst
python3 html2typst.py examples/content.html -o examples/content.typ

# Compile the template with Typst
typst compile examples/template.typ examples/output.pdf
```

## How It Works

The tool uses Python's built-in HTML parser to:
1. Parse HTML tags and content
2. Map HTML elements to corresponding Typst syntax
3. Generate clean, readable Typst markup

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Add support for more HTML elements

## License

MIT License - feel free to use this in your projects!

## Related

- [Typst](https://typst.app/) - The markup-based typesetting system
- [Typst Documentation](https://typst.app/docs/) - Official Typst docs

## FAQ

### Q: Can I use this in my automated workflow?
Yes! The tool is designed to work in scripts and pipelines. Use it with stdin/stdout for maximum flexibility.

### Q: What if my HTML has unsupported elements?
Unsupported elements will be ignored, but their text content will be preserved. You can extend the converter by modifying the `HTML2TypstConverter` class.

### Q: Can I customize the conversion?
Yes! The code is straightforward and easy to modify. Edit `html2typst.py` to add custom mappings or modify existing ones.

### Q: How do I handle complex layouts?
For complex layouts, consider converting sections separately and manually arranging them in your Typst template for best results.