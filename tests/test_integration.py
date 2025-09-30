"""Integration tests for crypto_manager.

These tests make actual API calls and should be run sparingly.
Set CRYPTO_MANAGER_RUN_INTEGRATION_TESTS=1 to enable.
"""
import unittest
import os

from crypto_manager import bitcoin, ethereum, ltc, doge, transactions


INTEGRATION_TESTS_ENABLED = os.getenv("CRYPTO_MANAGER_RUN_INTEGRATION_TESTS") == "1"


@unittest.skipUnless(INTEGRATION_TESTS_ENABLED, "Integration tests disabled")
class TestBitcoinIntegration(unittest.TestCase):
    """Integration tests for Bitcoin module."""
    
    def test_get_bitcoin_account_info(self):
        """Test fetching real Bitcoin account info."""
        # Using a public address with known balance
        address = "bc1qwrvfsrn2mt0srfkc7petwxfer70y533sac6y2e"
        
        result = bitcoin.get_account_info(address, skip_linked_addresses=True)
        
        self.assertEqual(result["currency"], "BTC")
        self.assertIn("balance", result)
        self.assertIn("transactions", result)
        self.assertIsInstance(result["balance"], float)


@unittest.skipUnless(INTEGRATION_TESTS_ENABLED, "Integration tests disabled")
class TestTransactionsIntegration(unittest.TestCase):
    """Integration tests for transactions module."""
    
    def test_get_btc_exchange_rate(self):
        """Test fetching real BTC exchange rate."""
        result = transactions.get_exchange_rate("BTC")
        
        self.assertIn("method_to_usd", result)
        self.assertGreater(result["method_to_usd"], 0)
        self.assertLess(result["method_to_usd"], 1000000)  # Sanity check
    
    def test_get_eth_exchange_rate(self):
        """Test fetching real ETH exchange rate."""
        result = transactions.get_exchange_rate("ETH")
        
        self.assertIn("method_to_usd", result)
        self.assertGreater(result["method_to_usd"], 0)
        self.assertLess(result["method_to_usd"], 100000)  # Sanity check


class TestModuleImports(unittest.TestCase):
    """Test that all modules can be imported."""
    
    def test_import_bitcoin(self):
        """Test importing bitcoin module."""
        from crypto_manager import bitcoin
        self.assertTrue(hasattr(bitcoin, "get_account_info"))
        self.assertTrue(hasattr(bitcoin, "ONE_BTC"))
    
    def test_import_ethereum(self):
        """Test importing ethereum module."""
        from crypto_manager import ethereum
        self.assertTrue(hasattr(ethereum, "get_account_info_eth"))
        self.assertTrue(hasattr(ethereum, "ONE_ETHER"))
    
    def test_import_ltc(self):
        """Test importing ltc module."""
        from crypto_manager import ltc
        self.assertTrue(hasattr(ltc, "get_account_info"))
        self.assertTrue(hasattr(ltc, "ONE_LTC"))
    
    def test_import_doge(self):
        """Test importing doge module."""
        from crypto_manager import doge
        self.assertTrue(hasattr(doge, "get_account_info"))
        self.assertTrue(hasattr(doge, "ONE_DOGE"))
    
    def test_import_transactions(self):
        """Test importing transactions module."""
        from crypto_manager import transactions
        self.assertTrue(hasattr(transactions, "get_exchange_rate"))
    
    def test_import_config(self):
        """Test importing config module."""
        from crypto_manager import config
        self.assertTrue(hasattr(config, "ETHERSCAN_API_KEY"))


if __name__ == "__main__":
    unittest.main()

