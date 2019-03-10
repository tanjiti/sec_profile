"""Test root selectors."""
from __future__ import unicode_literals
from .. import util


class TestRoot(util.TestCase):
    """Test root selectors."""

    MARKUP = """
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

    def test_root(self):
        """Test root."""

        # Root in HTML is `<html>`
        self.assert_selector(
            self.MARKUP,
            ":root",
            ["root"],
            flags=util.HTML
        )

    def test_root_complex(self):
        """Test root within a complex selector."""

        self.assert_selector(
            self.MARKUP,
            ":root > body > div",
            ["div"],
            flags=util.HTML
        )


class TestRootQuirks(TestRoot):
    """Test root selectors with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True
