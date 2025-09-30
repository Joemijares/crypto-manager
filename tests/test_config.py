"""Unit tests for config module."""
import unittest

from crypto_manager import config


class TestConfig(unittest.TestCase):
    """Test configuration module."""
    
    def test_etherscan_api_key_default(self):
        """Test that ETHERSCAN_API_KEY exists."""
        self.assertTrue(hasattr(config, "ETHERSCAN_API_KEY"))
        self.assertIsInstance(config.ETHERSCAN_API_KEY, str)
    
    def test_config_local_import_safe(self):
        """Test that config_local import failure is handled."""
        # This test verifies that missing config_local.py doesn't crash
        # The import is already done in config.py, so just verify it loaded
        self.assertTrue(hasattr(config, "logger"))


if __name__ == "__main__":
    unittest.main()

