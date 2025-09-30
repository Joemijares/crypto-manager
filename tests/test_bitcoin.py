"""Unit tests for Bitcoin module."""
import unittest
from unittest.mock import patch, MagicMock
import datetime

from crypto_manager import bitcoin


class TestBitcoinConstants(unittest.TestCase):
    """Test Bitcoin constants."""
    
    def test_one_btc_value(self):
        """Test that ONE_BTC has correct value."""
        self.assertEqual(bitcoin.ONE_BTC, 100000000)
        self.assertEqual(bitcoin.ONE_BTC, 10**8)


class TestProxyUrlFor(unittest.TestCase):
    """Test proxy URL generation."""
    
    def test_socks5_proxy_basic(self):
        """Test basic SOCKS5 proxy URL."""
        proxy = {
            "type": "socks5",
            "host": "proxy.example.com",
            "port": 1080
        }
        result = bitcoin.proxy_url_for(proxy)
        self.assertEqual(result, "socks5://proxy.example.com:1080")
    
    def test_http_proxy_basic(self):
        """Test basic HTTP proxy URL."""
        proxy = {
            "type": "http",
            "host": "proxy.example.com",
            "port": 8080
        }
        result = bitcoin.proxy_url_for(proxy)
        self.assertEqual(result, "http://proxy.example.com:8080")
    
    def test_proxy_with_auth(self):
        """Test proxy with username and password."""
        proxy = {
            "type": "socks5",
            "host": "proxy.example.com",
            "port": 1080,
            "username": "user",
            "password": "pass"
        }
        result = bitcoin.proxy_url_for(proxy)
        self.assertEqual(result, "socks5://user:pass@proxy.example.com:1080")
    
    def test_proxy_with_username_only(self):
        """Test proxy with username but no password."""
        proxy = {
            "type": "socks5",
            "host": "proxy.example.com",
            "port": 1080,
            "username": "user"
        }
        result = bitcoin.proxy_url_for(proxy)
        self.assertEqual(result, "socks5://user@proxy.example.com:1080")
    
    def test_proxy_without_port(self):
        """Test proxy without port."""
        proxy = {
            "type": "http",
            "host": "proxy.example.com"
        }
        result = bitcoin.proxy_url_for(proxy)
        self.assertEqual(result, "http://proxy.example.com")
    
    def test_invalid_proxy_type(self):
        """Test invalid proxy type raises error."""
        proxy = {
            "type": "invalid",
            "host": "proxy.example.com"
        }
        with self.assertRaises(ValueError):
            bitcoin.proxy_url_for(proxy)


class TestFixSendTxAmount(unittest.TestCase):
    """Test transaction amount calculation."""
    
    def test_received_transaction(self):
        """Test received transaction calculation."""
        our_addresses = ["bc1qtest"]
        transaction = {
            "vin": [
                {
                    "prevout": {
                        "scriptpubkey_address": "bc1qother",
                        "value": 50000000
                    }
                }
            ],
            "vout": [
                {
                    "scriptpubkey_address": "bc1qtest",
                    "value": 50000000
                }
            ]
        }
        
        result = bitcoin.fix_send_tx_amount(transaction, our_addresses)
        self.assertEqual(result["balance_diff"], 50000000)
    
    def test_sent_transaction(self):
        """Test sent transaction calculation."""
        our_addresses = ["bc1qtest"]
        transaction = {
            "vin": [
                {
                    "prevout": {
                        "scriptpubkey_address": "bc1qtest",
                        "value": 50000000
                    }
                }
            ],
            "vout": [
                {
                    "scriptpubkey_address": "bc1qother",
                    "value": 49990000
                }
            ]
        }
        
        result = bitcoin.fix_send_tx_amount(transaction, our_addresses)
        self.assertEqual(result["balance_diff"], -50000000)


class TestGetAccountInfo(unittest.TestCase):
    """Test get_account_info function."""
    
    @patch('crypto_manager.bitcoin.requests.get')
    def test_account_info_structure(self, mock_get):
        """Test that account info returns correct structure."""
        # Mock API responses
        mock_wallet_response = MagicMock()
        mock_wallet_response.json.return_value = {
            "chain_stats": {
                "tx_count": 0,
                "funded_txo_sum": 100000000,
                "spent_txo_sum": 0
            },
            "mempool_stats": {
                "tx_count": 0
            }
        }
        
        mock_tx_response = MagicMock()
        mock_tx_response.json.return_value = []
        
        mock_get.side_effect = [mock_wallet_response, mock_tx_response]
        
        result = bitcoin.get_account_info("bc1qtest", skip_linked_addresses=True)
        
        # Check structure
        self.assertIn("currency", result)
        self.assertIn("unit", result)
        self.assertIn("address", result)
        self.assertIn("balance", result)
        self.assertIn("balance_raw", result)
        self.assertIn("total_sent", result)
        self.assertIn("total_sent_raw", result)
        self.assertIn("total_received", result)
        self.assertIn("total_received_raw", result)
        self.assertIn("transactions", result)
        self.assertIn("latest_block_per_address", result)
        
        # Check values
        self.assertEqual(result["currency"], "BTC")
        self.assertEqual(result["unit"], bitcoin.ONE_BTC)
        self.assertEqual(result["address"], "bc1qtest")


if __name__ == "__main__":
    unittest.main()

