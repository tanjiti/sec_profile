"""Test child combinators."""
from __future__ import unicode_literals
from .. import util
import soupsieve as sv
from soupsieve import SelectorSyntaxError


class TestChild(util.TestCase):
    """Test child combinators."""

    MARKUP = """
    <div>
    <p id="0">Some text <span id="1"> in a paragraph</span>.</p>
    <a id="2" href="http://google.com">Link</a>
    <span id="3">Direct child</span>
    <pre>
    <span id="4">Child 1</span>
    <span id="5">Child 2</span>
    <span id="6">Child 3</span>
    </pre>
    </div>
    """

    def test_direct_child(self):
        """Test direct child."""

        # Spaces
        self.assert_selector(
            self.MARKUP,
            "div > span",
            ["3"],
            flags=util.HTML
        )

    def test_direct_child_no_spaces(self):
        """Test direct child with no spaces."""

        # No spaces
        self.assert_selector(
            self.MARKUP,
            "div>span",
            ["3"],
            flags=util.HTML
        )

    def test_invalid_double_combinator(self):
        """Test that selectors cannot have double combinators."""

        self.assert_raises('div >> p', SelectorSyntaxError)
        self.assert_raises('>> div > p', SelectorSyntaxError)

    def test_invalid_trailing_combinator(self):
        """Test that selectors cannot have a trailing combinator."""

        self.assert_raises('div >', SelectorSyntaxError)
        self.assert_raises('div >, div', SelectorSyntaxError)

    @util.skip_quirks
    def test_invalid_non_quirk_combination(self):
        """Non quirk mode should not allow selectors in selector lists to start with combinators."""

        self.assert_raises('> p', SelectorSyntaxError)
        self.assert_raises('div, > a', SelectorSyntaxError)


class TestChildQuirks(TestChild):
    """Test child combinators with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True

    @util.requires_html5lib
    def test_leading_combinator_quirks(self):
        """Test scope with quirks."""

        markup = """
        <html id="root">
        <head>
        </head>
        <body>
        <div id="div">
        <p id="0" class="somewordshere">Some text <span id="1"> in a paragraph</span>.</p>
        <a id="2" href="http://google.com">Link</a>
        <span id="3" class="herewords">Direct child</span>
        <pre id="pre" class="wordshere">
        <span id="4">Child 1</span>
        <span id="5">Child 2</span>
        <span id="6">Child 3</span>
        </pre>
        </div>
        </body>
        </html>
        """

        soup = self.soup(markup, 'html5lib')
        el = soup.div
        ids = []
        for el in sv.select('> span, > #pre', el, flags=sv.DEBUG | sv._QUIRKS):
            ids.append(el.attrs['id'])
        self.assertEqual(sorted(ids), sorted(['3', 'pre']))
