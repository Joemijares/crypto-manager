"""Unit tests for transactions module."""
import unittest
from unittest.mock import patch, MagicMock

from crypto_manager import transactions


class TestExchangeRates(unittest.TestCase):
    """Test exchange rate functions."""
    
    @patch('crypto_manager.transactions.requests.get')
    def test_btc_exchange_rate(self, mock_get):
        """Test BTC exchange rate fetching."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "rates": {"BTC": 0.000025},
            "timestamp": 1234567890
        }
        mock_get.return_value = mock_response
        
        result = transactions.get_exchange_rate("BTC")
        
        self.assertIn("method_to_usd", result)
        self.assertIn("usd_to_method", result)
        self.assertIn("unit", result)
        self.assertIn("exchange_rate_ts", result)
        self.assertGreater(result["method_to_usd"], 0)
    
    @patch('crypto_manager.transactions.requests.get')
    def test_eth_exchange_rate(self, mock_get):
        """Test ETH exchange rate fetching."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Data": {
                "Data": [
                    {"open": 2000.0, "time": 1234567890}
                ]
            }
        }
        mock_get.return_value = mock_response
        
        result = transactions.get_exchange_rate("ETH")
        
        self.assertIn("method_to_usd", result)
        self.assertEqual(result["method_to_usd"], 2000.0)
    
    def test_usdt_exchange_rate(self):
        """Test USDT exchange rate (should be 1:1 with USD)."""
        result = transactions.get_exchange_rate("USDT")
        
        self.assertEqual(result["method_to_usd"], 1)
        self.assertEqual(result["usd_to_method"], 1)
    
    def test_usdc_exchange_rate(self):
        """Test USDC exchange rate (should be 1:1 with USD)."""
        result = transactions.get_exchange_rate("USDC")
        
        self.assertEqual(result["method_to_usd"], 1)
        self.assertEqual(result["usd_to_method"], 1)
    
    def test_unsupported_method(self):
        """Test unsupported cryptocurrency raises error."""
        with self.assertRaises(RuntimeError):
            transactions.get_exchange_rate("INVALID_COIN")
    
    @patch('crypto_manager.transactions.requests.get')
    def test_exchange_rate_retry_mechanism(self, mock_get):
        """Test that exchange rate fetching retries on failure."""
        # First two calls fail, third succeeds
        mock_get.side_effect = [
            Exception("Network error"),
            Exception("Network error"),
            MagicMock(json=lambda: {
                "rates": {"BTC": 0.000025},
                "timestamp": 1234567890
            })
        ]
        
        result = transactions.get_exchange_rate("BTC")
        self.assertIsNotNone(result)
        self.assertEqual(mock_get.call_count, 3)


if __name__ == "__main__":
    unittest.main()

