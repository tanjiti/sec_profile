"""Test class selectors."""
from __future__ import unicode_literals
from .. import util
from soupsieve import SelectorSyntaxError


class TestClass(util.TestCase):
    """Test class selectors."""

    MARKUP = """
    <div>
    <p>Some text <span id="1" class="foo"> in a paragraph</span>.
    <a id="2" class="bar" href="http://google.com">Link</a>
    </p>
    </div>
    """

    def test_class(self):
        """Test class."""

        self.assert_selector(
            self.MARKUP,
            ".foo",
            ["1"],
            flags=util.HTML
        )

    def test_type_and_class(self):
        """Test type and class."""

        self.assert_selector(
            self.MARKUP,
            "a.bar",
            ["2"],
            flags=util.HTML
        )

    def test_malformed_class(self):
        """Test malformed class."""

        # Malformed class
        self.assert_raises('td.+#some-id', SelectorSyntaxError)

    def test_class_xhtml(self):
        """Test tag and class with XHTML since internally classes are stored different for XML."""

        self.assert_selector(
            self.wrap_xhtml(self.MARKUP),
            ".foo",
            ["1"],
            flags=util.XHTML
        )

    def test_multiple_classes(self):
        """Test multiple classes."""

        markup = """
        <div>
        <p>Some text <span id="1" class="foo"> in a paragraph</span>.
        <a id="2" class="bar" href="http://google.com">Link</a>
        <a id="3" class="foo" href="http://google.com">Link</a>
        <a id="4" class="foo bar" href="http://google.com">Link</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            "a.foo.bar",
            ["4"],
            flags=util.HTML
        )

    def test_malformed_pseudo_class(self):
        """Test malformed class."""

        # Malformed pseudo-class
        self.assert_raises('td:#id', SelectorSyntaxError)


class TestClassQuirks(TestClass):
    """Test class selectors with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True
