"""Test defined selectors."""
from __future__ import unicode_literals
from .. import util


class TestDefined(util.TestCase):
    """Test defined selectors."""

    def test_defined_html(self):
        """Test defined HTML."""

        markup = """
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
        <div id="0"></div>
        <div-custom id="1"></div-custom>
        <prefix:div id="2"></prefix:div>
        <prefix:div-custom id="3"></prefix:div-custom>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            'body :defined',
            ['0', '2', '3'],
            flags=util.HTML
        )

    def test_defined_xhtml(self):
        """Test defined XHTML."""

        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
            "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
        <head>
        </head>
        <body>
        <div id="0"></div>
        <div-custom id="1"></div-custom>
        <prefix:div id="2"></prefix:div>
        <!--
        lxml or BeautifulSoup seems to strip away the prefix.
        This is most likely because prefix with no namespace is not really valid.
        XML does allow colons in names, but encourages them to be used for namespaces.
        Do we really care that the prefix is wiped out in XHTML if there is no namespace?
        If we do, we should look into this in the future.
        -->
        <prefix:div-custom id="3"></prefix:div-custom>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            'body :defined',
            ['0', '2'],  # We should get 3, but we don't for reasons stated above.
            flags=util.XHTML
        )

    def test_defined_xml(self):
        """Test defined HTML."""

        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <html>
        <head>
        </head>
        <body>
        <div id="0"></div>
        <div-custom id="1"></div-custom>
        <prefix:div id="2"></prefix:div>
        <prefix:div-custom id="3"></prefix:div-custom>
        </body>
        </html>
        """

        # Defined is a browser thing.
        # XML doesn't care about defined and this will match nothing in XML.
        self.assert_selector(
            markup,
            'body :defined',
            [],
            flags=util.XML
        )


class TestDefinedQuirks(TestDefined):
    """Test defined selectors with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True
