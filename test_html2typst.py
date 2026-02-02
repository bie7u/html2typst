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
    
    print("\n" + "="*50)
    print("All tests passed! ✓")


if __name__ == '__main__':
    run_all_tests()
