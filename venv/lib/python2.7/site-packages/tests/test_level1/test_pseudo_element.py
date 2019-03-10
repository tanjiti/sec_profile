"""Test general pseudo-element cases."""
from __future__ import unicode_literals
from .. import util


class TestPseudoElement(util.TestCase):
    """Test pseudo-elements."""

    def test_pseudo_element(self):
        """Test that pseudo elements always fail because they are not supported."""

        self.assert_raises('::first-line', NotImplementedError)


class TestPseudoElementQuirks(TestPseudoElement):
    """Test pseudo-elements with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True
