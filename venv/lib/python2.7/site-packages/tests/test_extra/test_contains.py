"""Test contains selectors."""
from __future__ import unicode_literals
from .. import util


class TestContains(util.TestCase):
    """Test contains selectors."""

    MARKUP = """
    <body>
    <div id="1">
    Testing
    <span id="2"> that </span>
    contains works.
    </div>
    </body>
    """

    def test_contains(self):
        """Test contains."""

        self.assert_selector(
            self.MARKUP,
            'body span:contains(that)',
            ['2'],
            flags=util.HTML
        )

    def test_contains_quoted_with_space(self):
        """Test contains quoted with spaces."""

        self.assert_selector(
            self.MARKUP,
            'body span:contains(" that ")',
            ['2'],
            flags=util.HTML
        )

    def test_contains_quoted_without_space(self):
        """Test contains quoted with spaces."""

        self.assert_selector(
            self.MARKUP,
            'body :contains( "Testing" )',
            ['1'],
            flags=util.HTML
        )

    def test_contains_quoted_with_escaped_newline(self):
        """Test contains quoted with escaped newline."""

        self.assert_selector(
            self.MARKUP,
            'body :contains("Test\\\ning")',
            ['1'],
            flags=util.HTML
        )

    def test_contains_quoted_with_escaped_newline_with_carriage_return(self):
        """Test contains quoted with escaped newline with carriage return."""

        self.assert_selector(
            self.MARKUP,
            'body :contains("Test\\\r\ning")',
            ['1'],
            flags=util.HTML
        )

    def test_contains_with_descendants(self):
        """Test that contains returns descendants as well as the top level that contain."""

        self.assert_selector(
            self.MARKUP,
            'body :contains(" that ")',
            ['1', '2'],
            flags=util.HTML
        )

    def test_contains_bad(self):
        """Test contains when it finds no text."""

        self.assert_selector(
            self.MARKUP,
            'body :contains(bad)',
            [],
            flags=util.HTML
        )

    def test_contains_escapes(self):
        """Test contains with escape characters."""

        markup = """
        <body>
        <div id="1">Testing<span id="2">
        that</span>contains works.</div>
        </body>
        """

        self.assert_selector(
            markup,
            r'body span:contains("\0a that")',
            ['2'],
            flags=util.HTML
        )

    def test_contains_cdata_html(self):
        """Test contains CDATA in HTML5."""

        markup = """
        <body><div id="1">Testing that <span id="2"><![CDATA[that]]></span>contains works.</div></body>
        """

        self.assert_selector(
            markup,
            'body *:contains("that")',
            ['1'],
            flags=util.HTML
        )

    def test_contains_cdata_xhtml(self):
        """Test contains CDATA in XHTML."""

        markup = """
        <div id="1">Testing that <span id="2"><![CDATA[that]]></span>contains works.</div>
        """

        self.assert_selector(
            self.wrap_xhtml(markup),
            'body *:contains("that")',
            ['1', '2'],
            flags=util.XHTML
        )

    def test_contains_cdata_xml(self):
        """Test contains CDATA in XML."""

        markup = """
        <div id="1">Testing that <span id="2"><![CDATA[that]]></span>contains works.</div>
        """

        self.assert_selector(
            markup,
            '*:contains("that")',
            ['1', '2'],
            flags=util.XML
        )


class TestContainsQuirks(TestContains):
    """Test contains selectors with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True
