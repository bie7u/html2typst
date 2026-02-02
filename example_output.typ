// HEADER

= Complete HTML to Typst Demonstration

This document showcases the conversion of various HTML elements to Typst markup.

// MAIN

// SECTION

== Text Formatting

This paragraph demonstrates *bold text*, _italic text_, 
            #underline([underlined text]), #strike([strikethrough text]), and #highlight([highlighted text]).

You can also use #super([superscript]) and #sub([subscript]) for scientific notation 
            like E=mc#super([2]) or chemical formulas like H#sub([2])O.

// SECTION

== Code Examples

Inline code can be written like this: `print("Hello, World!")`

Code blocks are formatted as follows:

```
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

// SECTION

== Lists

=== Unordered List

- First item

- Second item with *bold* text

- Third item with a #link("https://example.com")[link]

=== Ordered List

#enum(

  [Step one],

  [Step two],

  [Step three],

)

=== Description List

/ HTML
: HyperText Markup Language
/ Typst
: A modern markup-based typesetting system

// SECTION

== Links and Media

Visit #link("https://typst.app")[Typst's official website] to learn more.

#figure(
  #image("diagram.png", alt: "Sample diagram", width: 300pt),
  caption: [Figure 1: A sample diagram showing the conversion process],
)

// SECTION

== Tables

#table(
  columns: 3,
  [*Feature*],
  [*HTML*],
  [*Typst*],
  [Bold],
  [<strong>],
  [*text*],
  [Italic],
  [<em>],
  [_text_],
  [Code],
  [<code>],
  [`code`],
)

// SECTION

== Quotes

#quote(block: true)[
  The best way to predict the future is to invent it.
]

- Alan Kay

#line(length: 100%)

// SECTION

== Miscellaneous Elements

Keyboard shortcuts: Press #box(stroke: 0.5pt, inset: 2pt, radius: 2pt)[`Ctrl`]+#box(stroke: 0.5pt, inset: 2pt, radius: 2pt)[`C`] to copy.

Variables: The value of _x_ is unknown.

Sample output: `Error: File not found`

Citation: _The Art of Computer Programming_ by Donald Knuth.

Time: The meeting is at 14:00.

Abbreviation: #text([HTML]) is widely used.

// SECTION

== Nested Structures

// ARTICLE

=== Article Example

This is an article with *bold _and italic_ text* nested together.

// ASIDE

_Note: This is an aside with additional information._

// SECTION

== Interactive Elements

// Click to expand
This content is hidden by default but can be revealed.

// FOOTER

// NAV

Navigation: #link("#top")[Back to top]

Copyright © 2024. All rights reserved.

==================================================
Conversion complete!
