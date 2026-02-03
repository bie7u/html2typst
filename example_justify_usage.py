#!/usr/bin/env python3
"""
Example script demonstrating correct usage of html2typst with justified text.

This addresses the issue where users report not seeing content in PDFs when
using text-align: justify styling.
"""

from html2typst import html_to_typst

# Example HTML with text-align: justify (from user's issue)
html_content = """<p style="text-align: justify;">
    1.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;fsadf się sdfas
    zaliczki na poczet sdfas mediów do indywidualnych lokali w fdsaf wysokościach :</p>
<p style="text-align: justify;">- centralne fsdafas i ciepła woda użytkowa (fsadf stała) – 1,333 zł/m<sup>2</sup></p>
<p style="text-align: justify;">- fdsafds fdsafd (opłata zmienna ) -&nbsp;105,74 zł/GJ</p>
<p style="text-align: justify;">- zimna woda i odprowadzenie ścieków – 13,61 zł/m<sup>3</sup></p>
<p style="text-align: justify;">- podgrzanie&nbsp;wody – 23,48 zł/m<sup>3. </sup></p>
<p style="text-align: justify;">
    2.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sdfsaf za fdsafas odpadów
    komunalnych będą naliczane zgodnie z przepisami aktualnie fdasfsaf na sdfasf Miasta Kraków oraz Regulaminem
    fdsafs mediów.</p>
<p style="text-align: justify;">
    3.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;fsdafsafsafdsafsaf. </p>
<p style="text-align: justify;"><strong style="color: black;">&nbsp;</strong></p>"""

# Convert HTML to Typst
typst_output = html_to_typst(html_content)

# Save to file with UTF-8 encoding
with open('output.typ', 'w', encoding='utf-8') as f:
    f.write(typst_output)

print("✓ Conversion complete!")
print(f"✓ Generated {len(typst_output)} characters of Typst code")
print("✓ Saved to 'output.typ'")
print("\nTo compile to PDF, run:")
print("  typst compile output.typ")
print("\nGenerated Typst code:")
print("=" * 60)
print(typst_output)
print("=" * 60)
