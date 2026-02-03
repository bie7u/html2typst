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
    assert '#par(justify: true)[Justified text]' in result_justify
    
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


def test_css_inherit_keyword():
    """Test CSS inherit keyword handling"""
    # Test color: inherit
    html_color = '<span style="color: inherit;">test</span>'
    result_color = html_to_typst(html_color)
    # Should not have #text(fill: inherit) - should just be 'test'
    assert 'inherit' not in result_color.lower()
    assert result_color.strip() == 'test'
    
    # Test background-color: inherit
    html_bg = '<span style="background-color: inherit;">test</span>'
    result_bg = html_to_typst(html_bg)
    assert 'inherit' not in result_bg.lower()
    assert result_bg.strip() == 'test'
    
    # Test mixed scenario: text-align with inherit color (text-align should still work)
    html_mixed = '<p style="text-align: center; color: inherit;">centered text</p>'
    result_mixed = html_to_typst(html_mixed)
    assert '#align(center)' in result_mixed
    assert 'inherit' not in result_mixed.lower()
    assert 'centered text' in result_mixed
    
    print("✓ CSS inherit keyword test passed")


def test_css_initial_keyword():
    """Test CSS initial keyword handling"""
    # Test color: initial
    html = '<span style="color: initial;">test</span>'
    result = html_to_typst(html)
    assert 'initial' not in result.lower()
    assert result.strip() == 'test'
    
    print("✓ CSS initial keyword test passed")


def test_css_transparent_keyword():
    """Test CSS transparent keyword handling"""
    # For transparent, we might skip or use a transparent color
    html = '<span style="background-color: transparent;">test</span>'
    result = html_to_typst(html)
    # Should either skip the style or handle transparent appropriately
    # For now, we'll skip it
    assert result.strip() == 'test'
    
    print("✓ CSS transparent keyword test passed")


def test_css_currentcolor_keyword():
    """Test CSS currentColor keyword handling"""
    html = '<span style="color: currentColor;">test</span>'
    result = html_to_typst(html)
    # currentColor should be skipped (it means use current text color)
    assert 'currentcolor' not in result.lower()
    assert result.strip() == 'test'
    
    print("✓ CSS currentColor keyword test passed")


def test_css_unset_revert_auto_keywords():
    """Test CSS unset, revert, and auto keywords"""
    # Test unset
    html_unset = '<span style="color: unset;">test</span>'
    result_unset = html_to_typst(html_unset)
    assert 'unset' not in result_unset.lower()
    assert result_unset.strip() == 'test'
    
    # Test revert
    html_revert = '<span style="font-size: revert;">test</span>'
    result_revert = html_to_typst(html_revert)
    assert 'revert' not in result_revert.lower()
    assert result_revert.strip() == 'test'
    
    # Test auto (for font-size)
    html_auto = '<span style="font-size: auto;">test</span>'
    result_auto = html_to_typst(html_auto)
    assert 'auto' not in result_auto.lower()
    assert result_auto.strip() == 'test'
    
    print("✓ CSS unset/revert/auto keywords test passed")


def test_css_named_colors():
    """Test CSS named colors"""
    # Test basic named color
    html = '<span style="color: red;">Red text</span>'
    result = html_to_typst(html)
    # Named colors should be passed through or converted to rgb
    # For now we accept the named color as-is
    assert 'Red text' in result
    assert '#text(fill: red)[Red text]' in result
    
    print("✓ CSS named colors test passed")


def test_font_size_inherit_keyword():
    """Test font-size with inherit keyword"""
    html = '<span style="font-size: inherit;">test</span>'
    result = html_to_typst(html)
    assert 'inherit' not in result.lower()
    assert result.strip() == 'test'
    
    print("✓ Font-size inherit keyword test passed")


def test_parentheses_after_styled_text():
    """Test that parentheses after styled text don't cause Typst syntax errors"""
    # This is a regression test for the issue where ]( would cause "expected comma" error
    html = '<p style="text-align: justify;"><span style="color: black;">Text before </span>(text in parentheses) <span style="color: black;">Text after</span></p>'
    result = html_to_typst(html)
    
    # Should have space between ] and ( to prevent Typst syntax error
    assert '] (' in result
    # Should not have ]( without space
    assert '](' not in result
    
    print("✓ Parentheses after styled text test passed")


def test_parentheses_after_function_wrappers():
    """Test that parentheses after function wrappers like #underline don't cause errors"""
    # Test case where )( could be misinterpreted as additional function arguments
    html = '<p><u>Underlined text</u>(note in parentheses)</p>'
    result = html_to_typst(html)
    
    # Should have space between ) and ( to prevent Typst syntax error
    assert ') (' in result
    # Should not have )( without space
    assert ')(' not in result
    
    print("✓ Parentheses after function wrappers test passed")


def test_css_system_color_windowtext():
    """Test CSS system color 'windowtext' is properly skipped"""
    html = '<span style="color: windowtext;">Styled text content</span>'
    result = html_to_typst(html)
    # Should preserve text without color styling
    assert result.strip() == 'Styled text content'
    # Should not contain Typst fill directive with windowtext
    assert 'fill:' not in result.lower()
    
    print("✓ CSS system color windowtext test passed")


def test_css_system_colors_comprehensive():
    """Test various CSS system colors are properly handled"""
    system_colors = [
        'windowtext', 'buttonface', 'threeddarkshadow', 'infotext', 'menutext',
        'window', 'windowframe', 'activeborder', 'inactivecaption', 'graytext'
    ]
    
    for color in system_colors:
        html = f'<span style="color: {color};">Text content</span>'
        result = html_to_typst(html)
        # Each system color should be skipped, leaving only the text
        assert result.strip() == 'Text content', f"System color {color} was not properly skipped: {result}"
        # System color should not appear in a fill directive
        assert 'fill:' not in result.lower(), f"System color {color} appeared in fill directive: {result}"
    
    print("✓ CSS system colors comprehensive test passed")


def test_css_valid_named_colors_preserved():
    """Test that valid CSS named colors are preserved"""
    valid_colors = ['red', 'blue', 'green', 'black', 'white', 'yellow', 'orange', 'purple']
    
    for color in valid_colors:
        html = f'<span style="color: {color};">Colored text</span>'
        result = html_to_typst(html)
        # Valid named colors should be applied
        assert f'#text(fill: {color})' in result, f"Valid color {color} was not applied: {result}"
        assert 'Colored text' in result
    
    print("✓ CSS valid named colors test passed")


def test_css_invalid_color_preserves_content():
    """Test that invalid/unknown color values preserve content"""
    invalid_colors = ['notacolor', 'invalidcolor123', 'foo', 'unknowncolor']
    
    for color in invalid_colors:
        html = f'<span style="color: {color};">Text content</span>'
        result = html_to_typst(html)
        # Content should be preserved even with invalid color
        assert result.strip() == 'Text content', f"Content not preserved with invalid color {color}: {result}"
    
    print("✓ CSS invalid color preserves content test passed")


def test_text_align_justify_with_content():
    """Test that text-align justify preserves text content"""
    html = '<p style="text-align: justify;">This is justified text that must remain visible</p>'
    result = html_to_typst(html)
    
    # Content must be visible
    assert 'This is justified text that must remain visible' in result
    # Should use par(justify: true) syntax
    assert '#par(justify: true)' in result
    
    print("✓ Text-align justify with content test passed")


def test_text_align_justify_with_nested_styles():
    """Test text-align justify with nested inline styles"""
    html = '<p style="text-align: justify;"><span style="color: red;">Red text</span> and normal text</p>'
    result = html_to_typst(html)
    
    # All content should be visible
    assert 'Red text' in result
    assert 'and normal text' in result
    # Should preserve both justify and color
    assert '#par(justify: true)' in result
    assert 'rgb' in result or 'red' in result
    
    print("✓ Text-align justify with nested styles test passed")


def test_mixed_valid_and_invalid_colors():
    """Test paragraph with both valid and invalid color styles"""
    html = '<p><span style="color: red;">Valid</span> <span style="color: windowtext;">Invalid</span> text</p>'
    result = html_to_typst(html)
    
    # Valid color should be applied
    assert '#text(fill: red)[Valid]' in result
    # Invalid color should be skipped but content preserved
    assert 'Invalid' in result
    # System color should not appear in fill directive
    assert 'fill: windowtext' not in result.lower()
    # Other text should be present
    assert 'text' in result
    
    print("✓ Mixed valid and invalid colors test passed")


def test_unknown_html_tag_preserves_content():
    """Test that unknown HTML tags preserve their text content"""
    html = '<unknowntag>This text should be visible</unknowntag>'
    result = html_to_typst(html)
    
    # Content must be preserved
    assert 'This text should be visible' in result
    
    print("✓ Unknown HTML tag preserves content test passed")


def test_unknown_html_tag_with_styles():
    """Test that unknown HTML tags with styles preserve content"""
    html = '<unknowntag style="color: red;">Styled text in unknown tag</unknowntag>'
    result = html_to_typst(html)
    
    # Content must be preserved
    assert 'Styled text in unknown tag' in result
    
    print("✓ Unknown HTML tag with styles preserves content test passed")


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
    
    # CSS keyword tests
    test_css_inherit_keyword()
    test_css_initial_keyword()
    test_css_transparent_keyword()
    test_css_currentcolor_keyword()
    test_css_unset_revert_auto_keywords()
    test_css_named_colors()
    test_font_size_inherit_keyword()
    
    # Syntax fix tests
    test_parentheses_after_styled_text()
    test_parentheses_after_function_wrappers()
    
    # New tests for CSS system colors and content preservation
    test_css_system_color_windowtext()
    test_css_system_colors_comprehensive()
    test_css_valid_named_colors_preserved()
    test_css_invalid_color_preserves_content()
    test_text_align_justify_with_content()
    test_text_align_justify_with_nested_styles()
    test_mixed_valid_and_invalid_colors()
    test_unknown_html_tag_preserves_content()
    test_unknown_html_tag_with_styles()
    
    print("\n" + "="*50)
    print("All tests passed! ✓")


if __name__ == '__main__':
    run_all_tests()
