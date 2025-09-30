"""Unit tests for Litecoin and Dogecoin modules."""
import unittest
from unittest.mock import patch, MagicMock

from crypto_manager import ltc, doge


class TestLitecoinConstants(unittest.TestCase):
    """Test Litecoin constants."""
    
    def test_one_ltc_value(self):
        """Test that ONE_LTC has correct value."""
        self.assertEqual(ltc.ONE_LTC, 100000000)
        self.assertEqual(ltc.ONE_LTC, 10**8)


class TestDogecoinConstants(unittest.TestCase):
    """Test Dogecoin constants."""
    
    def test_one_doge_value(self):
        """Test that ONE_DOGE has correct value."""
        self.assertEqual(doge.ONE_DOGE, 100000000)
        self.assertEqual(doge.ONE_DOGE, 10**8)


class TestLitecoinGetAccountInfo(unittest.TestCase):
    """Test Litecoin get_account_info function."""
    
    @patch('crypto_manager.ltc.requests.get')
    def test_account_info_structure(self, mock_get):
        """Test that LTC account info returns correct structure."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "LTC_address": {
                    "address": {
                        "balance": 100000000
                    },
                    "transactions": []
                }
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        result = ltc.get_account_info("LTC_address")
        
        # Check structure
        self.assertEqual(result["currency"], "LTC")
        self.assertEqual(result["unit"], ltc.ONE_LTC)
        self.assertIn("balance", result)
        self.assertIn("transactions", result)
        self.assertIsInstance(result["transactions"], list)
    
    @patch('crypto_manager.ltc.requests.get')
    def test_api_error_handling(self, mock_get):
        """Test LTC API error handling."""
        mock_get.side_effect = Exception("API Error")
        
        with self.assertRaises(ValueError):
            ltc.get_account_info("invalid_address")


class TestDogecoinGetAccountInfo(unittest.TestCase):
    """Test Dogecoin get_account_info function."""
    
    @patch('crypto_manager.doge.requests.get')
    def test_account_info_structure(self, mock_get):
        """Test that DOGE account info returns correct structure."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "DOGE_address": {
                    "address": {
                        "balance": 100000000
                    },
                    "transactions": []
                }
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        result = doge.get_account_info("DOGE_address")
        
        # Check structure
        self.assertEqual(result["currency"], "DOGE")
        self.assertEqual(result["unit"], doge.ONE_DOGE)
        self.assertIn("balance", result)
        self.assertIn("transactions", result)
        self.assertIsInstance(result["transactions"], list)
    
    @patch('crypto_manager.doge.requests.get')
    def test_api_error_handling(self, mock_get):
        """Test DOGE API error handling."""
        mock_get.side_effect = Exception("API Error")
        
        with self.assertRaises(ValueError):
            doge.get_account_info("invalid_address")


class TestFixSendTxAmount(unittest.TestCase):
    """Test transaction amount calculation for LTC."""
    
    def test_ltc_fix_send_tx_amount(self):
        """Test LTC transaction amount calculation."""
        our_addresses = ["LTC_address"]
        transaction = {
            "vin": [
                {
                    "prevout": {
                        "scriptpubkey_address": "other_address",
                        "value": 100000000
                    }
                }
            ],
            "vout": [
                {
                    "scriptpubkey_address": "LTC_address",
                    "value": 100000000
                }
            ]
        }
        
        result = ltc.fix_send_tx_amount(transaction, our_addresses)
        self.assertIn("balance_diff", result)
        self.assertEqual(result["balance_diff"], 100000000)


if __name__ == "__main__":
    unittest.main()

