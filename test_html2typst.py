"""
Test suite for html2typst module
"""

from html2typst import html_to_typst


def test_headings():
    """Test heading conversion"""
    html = '<h1>H1</h1><h2>H2</h2><h3>H3</h3><h4>H4</h4><h5>H5</h5><h6>H6</h6>'
    result = html_to_typst(html)
    assert '= H1' in result
    assert '== H2' in result
    assert '=== H3' in result
    assert '==== H4' in result
    assert '===== H5' in result
    assert '====== H6' in result
    print("✓ Headings test passed")


def test_text_formatting():
    """Test text formatting tags"""
    html = '<p><strong>bold</strong> <b>also bold</b> <em>italic</em> <i>also italic</i></p>'
    result = html_to_typst(html)
    assert '*bold*' in result
    assert '*also bold*' in result
    assert '_italic_' in result
    assert '_also italic_' in result
    print("✓ Text formatting test passed")


def test_underline_strike():
    """Test underline and strikethrough"""
    html = '<u>underlined</u> <s>struck</s> <del>deleted</del>'
    result = html_to_typst(html)
    assert '#underline([underlined])' in result
    assert '#strike([struck])' in result
    assert '#strike([deleted])' in result
    print("✓ Underline/strike test passed")


def test_code():
    """Test code elements"""
    html = '<code>inline code</code><pre><code>block code</code></pre>'
    result = html_to_typst(html)
    assert '`inline code`' in result
    assert '```' in result
    assert 'block code' in result
    print("✓ Code test passed")


def test_lists():
    """Test list elements"""
    html = '<ul><li>item1</li><li>item2</li></ul><ol><li>num1</li><li>num2</li></ol>'
    result = html_to_typst(html)
    assert '- item1' in result
    assert '- item2' in result
    assert '#enum(' in result
    assert '[num1]' in result
    assert '[num2]' in result
    print("✓ Lists test passed")


def test_links():
    """Test link elements"""
    html = '<a href="https://example.com">link text</a>'
    result = html_to_typst(html)
    assert '#link("https://example.com")[link text]' in result
    print("✓ Links test passed")


def test_images():
    """Test image elements"""
    html = '<img src="test.png" alt="Test image">'
    result = html_to_typst(html)
    assert '#image("test.png"' in result
    assert 'alt: "Test image"' in result
    print("✓ Images test passed")


def test_table():
    """Test table elements"""
    html = '''
    <table>
        <tr><th>Header1</th><th>Header2</th></tr>
        <tr><td>Cell1</td><td>Cell2</td></tr>
    </table>
    '''
    result = html_to_typst(html)
    assert '#table(' in result
    assert 'columns: 2' in result
    assert '*Header1*' in result
    assert '*Header2*' in result
    assert 'Cell1' in result
    assert 'Cell2' in result
    print("✓ Table test passed")


def test_blockquote():
    """Test blockquote elements"""
    html = '<blockquote>quoted text</blockquote>'
    result = html_to_typst(html)
    assert '#quote(block: true)' in result
    assert 'quoted text' in result
    print("✓ Blockquote test passed")


def test_line_break():
    """Test line break"""
    html = '<p>Line 1<br>Line 2</p>'
    result = html_to_typst(html)
    assert 'Line 1' in result
    assert 'Line 2' in result
    print("✓ Line break test passed")


def test_horizontal_rule():
    """Test horizontal rule"""
    html = '<hr>'
    result = html_to_typst(html)
    assert '#line(length: 100%)' in result
    print("✓ Horizontal rule test passed")


def test_superscript_subscript():
    """Test superscript and subscript"""
    html = '<p>E=mc<sup>2</sup> and H<sub>2</sub>O</p>'
    result = html_to_typst(html)
    assert '#super([2])' in result
    assert '#sub([2])' in result
    print("✓ Superscript/subscript test passed")


def test_mark():
    """Test mark/highlight"""
    html = '<mark>highlighted</mark>'
    result = html_to_typst(html)
    assert '#highlight([highlighted])' in result
    print("✓ Mark/highlight test passed")


def test_semantic_html5():
    """Test semantic HTML5 tags"""
    html = '<header>Header</header><footer>Footer</footer><main>Main</main>'
    result = html_to_typst(html)
    assert '// HEADER' in result
    assert '// FOOTER' in result
    assert '// MAIN' in result
    print("✓ Semantic HTML5 test passed")


def test_figure():
    """Test figure with caption"""
    html = '<figure><img src="fig.png"><figcaption>Figure caption</figcaption></figure>'
    result = html_to_typst(html)
    assert '#figure(' in result
    assert '#image("fig.png")' in result
    assert 'caption: [Figure caption]' in result
    print("✓ Figure test passed")


def test_misc_tags():
    """Test miscellaneous tags"""
    html = '<kbd>Ctrl</kbd> <var>x</var> <samp>output</samp> <cite>citation</cite>'
    result = html_to_typst(html)
    assert '`Ctrl`' in result
    assert 'output' in result
    print("✓ Misc tags test passed")


def test_nested_formatting():
    """Test nested formatting"""
    html = '<p>Text with <strong>bold <em>and italic</em></strong> nested.</p>'
    result = html_to_typst(html)
    assert '*bold _and italic_*' in result
    print("✓ Nested formatting test passed")


def test_complex_document():
    """Test a complex document"""
    html = '''
    <article>
        <h1>Article Title</h1>
        <p>Introduction with <strong>important</strong> information.</p>
        <section>
            <h2>Section 1</h2>
            <ul>
                <li>Point 1</li>
                <li>Point 2</li>
            </ul>
        </section>
        <section>
            <h2>Section 2</h2>
            <p>See <a href="https://example.com">this link</a> for more.</p>
        </section>
    </article>
    '''
    result = html_to_typst(html)
    assert '= Article Title' in result
    assert '*important*' in result
    assert '- Point 1' in result
    assert '#link("https://example.com")' in result
    print("✓ Complex document test passed")


def test_code_language_extraction():
    """Test code block with language class"""
    html = '<pre><code class="language-python">print("Hello")</code></pre>'
    result = html_to_typst(html)
    assert '```python' in result
    print("✓ Code language extraction test passed")


def test_code_language_with_multiple_classes():
    """Test code block with multiple classes"""
    html = '<pre><code class="hljs language-javascript other-class">console.log("test")</code></pre>'
    result = html_to_typst(html)
    assert '```javascript' in result
    print("✓ Code language with multiple classes test passed")


def test_image_width_units():
    """Test image with various width units"""
    # Test percentage
    html1 = '<img src="test.png" width="50%">'
    result1 = html_to_typst(html1)
    assert 'width: 50%' in result1
    
    # Test pixels
    html2 = '<img src="test.png" width="200px">'
    result2 = html_to_typst(html2)
    assert 'width: 200pt' in result2
    
    # Test decimal values
    html3 = '<img src="test.png" width="150.5">'
    result3 = html_to_typst(html3)
    assert 'width: 150.5pt' in result3
    
    print("✓ Image width units test passed")


def test_quill_text_align_center():
    """Test Quill.js style text-align: center"""
    html = '<p style="text-align: center;"><strong>Hi</strong></p>'
    result = html_to_typst(html)
    assert '#align(center)[*Hi*]' in result
    print("✓ Quill text-align center test passed")


def test_quill_text_align_variations():
    """Test all text-align variations"""
    # Left
    html_left = '<p style="text-align: left;">Left aligned</p>'
    result_left = html_to_typst(html_left)
    assert '#align(left)[Left aligned]' in result_left
    
    # Right
    html_right = '<p style="text-align: right;">Right aligned</p>'
    result_right = html_to_typst(html_right)
    assert '#align(right)[Right aligned]' in result_right
    
    # Justify
    html_justify = '<p style="text-align: justify;">Justified text</p>'
    result_justify = html_to_typst(html_justify)
    assert '#align(justify)[Justified text]' in result_justify
    
    print("✓ Quill text-align variations test passed")


def test_quill_color_hex():
    """Test Quill.js style color with hex values"""
    html = '<span style="color: #ff0000;">Red text</span>'
    result = html_to_typst(html)
    assert '#text(fill: rgb(255, 0, 0))[Red text]' in result
    print("✓ Quill color hex test passed")


def test_quill_color_hex_shorthand():
    """Test Quill.js style color with hex shorthand"""
    html = '<span style="color: #f00;">Red</span>'
    result = html_to_typst(html)
    assert '#text(fill: rgb(255, 0, 0))[Red]' in result
    print("✓ Quill color hex shorthand test passed")


def test_quill_background_color():
    """Test Quill.js style background-color"""
    html = '<span style="background-color: #ffff00;">Highlighted</span>'
    result = html_to_typst(html)
    assert '#highlight(fill: rgb(255, 255, 0))[Highlighted]' in result
    print("✓ Quill background-color test passed")


def test_quill_font_size_named():
    """Test Quill.js style font-size with named values"""
    # Small
    html_small = '<span style="font-size: small;">Small text</span>'
    result_small = html_to_typst(html_small)
    assert '#text(size: 0.85em)[Small text]' in result_small
    
    # Large
    html_large = '<span style="font-size: large;">Large text</span>'
    result_large = html_to_typst(html_large)
    assert '#text(size: 1.2em)[Large text]' in result_large
    
    # Huge
    html_huge = '<span style="font-size: huge;">Huge text</span>'
    result_huge = html_to_typst(html_huge)
    assert '#text(size: 1.5em)[Huge text]' in result_huge
    
    print("✓ Quill font-size named test passed")


def test_quill_font_size_px():
    """Test Quill.js style font-size with px values"""
    html = '<span style="font-size: 18px;">Text</span>'
    result = html_to_typst(html)
    assert '#text(size: 18pt)[Text]' in result or '#text(size: 18.0pt)[Text]' in result
    print("✓ Quill font-size px test passed")


def test_quill_multiple_inline_styles():
    """Test multiple inline styles on span"""
    html = '<span style="color: #0000ff; font-size: large;">Blue large</span>'
    result = html_to_typst(html)
    # Both color and size should be applied
    assert 'rgb(0, 0, 255)' in result
    assert '1.2em' in result
    print("✓ Quill multiple inline styles test passed")


def test_quill_paragraph_with_color_and_alignment():
    """Test paragraph with both color and alignment"""
    html = '<p style="text-align: center; color: #ff0000;">Centered red</p>'
    result = html_to_typst(html)
    assert '#align(center)' in result
    assert 'rgb(255, 0, 0)' in result
    print("✓ Quill paragraph with color and alignment test passed")


def test_quill_nested_formatting_with_styles():
    """Test nested formatting inside styled paragraph"""
    html = '<p style="text-align: center;"><strong>Bold</strong> and <em>italic</em></p>'
    result = html_to_typst(html)
    assert '#align(center)[*Bold* and _italic_]' in result
    print("✓ Quill nested formatting with styles test passed")


def test_quill_complex_example():
    """Test complex Quill.js-like document"""
    html = '''
    <p style="text-align: center;"><strong>Title</strong></p>
    <p style="color: #333333;">Normal paragraph with color</p>
    <p><span style="background-color: #ffff00;">Highlighted text</span> in paragraph</p>
    <p style="text-align: right; font-size: small;">Small right-aligned footer</p>
    '''
    result = html_to_typst(html)
    assert '#align(center)[*Title*]' in result
    assert 'rgb(51, 51, 51)' in result
    assert '#highlight(fill: rgb(255, 255, 0))[Highlighted text]' in result
    assert '#align(right)' in result
    assert '0.85em' in result
    print("✓ Quill complex example test passed")


def test_parse_inline_css_helper():
    """Test the parse_inline_css helper function"""
    from html2typst import parse_inline_css
    
    # Basic parsing
    result = parse_inline_css("color: red; font-size: 12px")
    assert result['color'] == 'red'
    assert result['font-size'] == '12px'
    
    # Empty string
    result_empty = parse_inline_css("")
    assert result_empty == {}
    
    # Single property
    result_single = parse_inline_css("text-align: center")
    assert result_single['text-align'] == 'center'
    
    # With spaces
    result_spaces = parse_inline_css(" color : blue ; ")
    assert result_spaces['color'] == 'blue'
    
    print("✓ Parse inline CSS helper test passed")


def run_all_tests():
    """Run all tests"""
    print("Running html2typst tests...\n")
    
    test_headings()
    test_text_formatting()
    test_underline_strike()
    test_code()
    test_lists()
    test_links()
    test_images()
    test_table()
    test_blockquote()
    test_line_break()
    test_horizontal_rule()
    test_superscript_subscript()
    test_mark()
    test_semantic_html5()
    test_figure()
    test_misc_tags()
    test_nested_formatting()
    test_complex_document()
    test_code_language_extraction()
    test_code_language_with_multiple_classes()
    test_image_width_units()
    
    # Quill.js tests
    test_parse_inline_css_helper()
    test_quill_text_align_center()
    test_quill_text_align_variations()
    test_quill_color_hex()
    test_quill_color_hex_shorthand()
    test_quill_background_color()
    test_quill_font_size_named()
    test_quill_font_size_px()
    test_quill_multiple_inline_styles()
    test_quill_paragraph_with_color_and_alignment()
    test_quill_nested_formatting_with_styles()
    test_quill_complex_example()
    
    print("\n" + "="*50)
    print("All tests passed! ✓")


if __name__ == '__main__':
    run_all_tests()
