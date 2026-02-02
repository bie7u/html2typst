# Quick Start Guide for html2typst

This guide helps you quickly get started with html2typst to add HTML content to your Typst templates.

## Problem: How Do I Use HTML in My Typst Template?

If you have HTML content that you want to include in your Typst document, here are the easiest ways to do it:

### Method 1: Command Line (Quickest)

If you have an HTML file and want to convert it:

```bash
# Download or have html2typst.py available
python3 html2typst.py your-content.html -o content.typ
```

Then in your Typst template:

```typst
// your-template.typ
#set document(title: "My Document")

= My Document

#include "content.typ"

= Conclusion
```

### Method 2: Python Script (Most Flexible)

If you want to programmatically combine HTML with your template:

```python
#!/usr/bin/env python3
from html2typst import html_to_typst

# Your HTML content
html = """
<h2>My Section</h2>
<p>This is my content.</p>
"""

# Convert to Typst
typst_content = html_to_typst(html)

# Create your final document
document = f"""
#set document(title: "My Document")

= My Document

{typst_content}

= Conclusion
"""

# Save it
with open('final.typ', 'w') as f:
    f.write(document)
```

### Method 3: Stdin/Stdout (For Pipelines)

If you want to use it in a script or pipeline:

```bash
# Convert and append to a template
cat template-header.typ > final.typ
python3 html2typst.py content.html >> final.typ
cat template-footer.typ >> final.typ

# Or pipe HTML directly
curl https://example.com/content.html | python3 html2typst.py > content.typ
```

## Common Use Cases

### Use Case 1: Converting Existing HTML Files

You have existing HTML files and want to convert them to Typst:

```bash
# Single file
python3 html2typst.py article.html -o article.typ

# Multiple files
for file in *.html; do
    python3 html2typst.py "$file" -o "${file%.html}.typ"
done
```

### Use Case 2: Dynamic Content Generation

You're generating HTML programmatically and want to create Typst documents:

```python
from html2typst import html_to_typst

# Generate HTML from your data
html = f"<h1>{title}</h1><p>{description}</p>"

# Convert to Typst
typst = html_to_typst(html)

# Use it in your template
template = f"""
#import "style.typ": *

{typst}
"""

with open('output.typ', 'w') as f:
    f.write(template)
```

### Use Case 3: API/Database Content

You're fetching content from an API or database:

```python
import requests
from html2typst import html_to_typst

# Fetch HTML content
response = requests.get('https://api.example.com/article/123')
html_content = response.json()['content']

# Convert to Typst
typst_content = html_to_typst(html_content)

# Create document
document = f"""
#set document(
    title: "Article",
    author: "Author Name"
)

{typst_content}
"""

with open('article.typ', 'w') as f:
    f.write(document)
```

## Tips

1. **Keep HTML Simple**: The converter works best with semantic HTML (headings, paragraphs, lists, etc.)

2. **Test Your Output**: Always review the generated Typst to ensure it looks correct

3. **Customize if Needed**: You can edit the generated `.typ` files to fine-tune the output

4. **Handle Complex Layouts Manually**: For complex layouts, convert sections separately and arrange them manually

5. **Extend the Converter**: If you need additional HTML elements, edit `html2typst.py` to add them

## Troubleshooting

**Q: The spacing looks weird**
A: The converter does its best with whitespace. You may need to manually adjust the generated `.typ` file.

**Q: Some HTML elements are missing**
A: Only common elements are supported. Unsupported elements are ignored but their text content is preserved.

**Q: Can I convert entire web pages?**
A: Yes, but the results will be best with content-focused HTML. Complex layouts may not convert well.

**Q: How do I add custom styles?**
A: Convert the HTML first, then add Typst styling directives in your template.

## Next Steps

- Read the full README.md for detailed documentation
- Check the `examples/` directory for more examples
- Modify `html2typst.py` to add custom element mappings

## Support

For issues, questions, or contributions:
- GitHub: https://github.com/bie7u/html2typst
- Issues: https://github.com/bie7u/html2typst/issues
