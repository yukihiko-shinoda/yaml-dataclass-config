"""Tests for unittest scenario"""
from yourproduct import CONFIG
from yourproduct.unittest_context import ConfigurableTestCase


class TestConfigHandlerUnittest(ConfigurableTestCase):
    """Tests for unittest scenario"""
    def test_config_handler_unittest(self):
        """Config file for test should be loaded."""
        self.assertEqual(CONFIG.some_property, 'test value')
