"""Test matches selectors."""
from __future__ import unicode_literals
from .. import util


class TestMatches(util.TestCase):
    """Test matches selectors."""


class TestMatchesQuirks(TestMatches):
    """Test matches selectors with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True
