"""Unit tests for Ethereum module."""
import unittest
from unittest.mock import patch, MagicMock

from crypto_manager import ethereum


class TestEthereumConstants(unittest.TestCase):
    """Test Ethereum constants."""
    
    def test_one_ether_value(self):
        """Test that ONE_ETHER has correct value."""
        self.assertEqual(ethereum.ONE_ETHER, 1000000000000000000)
        self.assertEqual(ethereum.ONE_ETHER, 10**18)
    
    def test_one_usdt_value(self):
        """Test that ONE_USDT has correct value."""
        self.assertEqual(ethereum.ONE_USDT, 1000000)
        self.assertEqual(ethereum.ONE_USDT, 10**6)
    
    def test_one_usdc_value(self):
        """Test that ONE_USDC has correct value."""
        self.assertEqual(ethereum.ONE_USDC, 1000000)
        self.assertEqual(ethereum.ONE_USDC, 10**6)
    
    def test_one_busd_value(self):
        """Test that ONE_BUSD has correct value."""
        self.assertEqual(ethereum.ONE_BUSD, 1000000000000000000)
        self.assertEqual(ethereum.ONE_BUSD, 10**18)
    
    def test_contract_addresses(self):
        """Test contract addresses are valid."""
        self.assertTrue(ethereum.CONTRACT_ADDRESS_USDT.startswith("0x"))
        self.assertTrue(ethereum.CONTRACT_ADDRESS_USDC.startswith("0x"))
        self.assertTrue(ethereum.CONTRACT_ADDRESS_BUSD.startswith("0x"))
        self.assertEqual(len(ethereum.CONTRACT_ADDRESS_USDT), 42)


class TestParseTransaction(unittest.TestCase):
    """Test transaction parsing."""
    
    def test_parse_eth_transaction_received(self):
        """Test parsing received ETH transaction."""
        address = "0xtest"
        transaction = {
            "hash": "0xabc123",
            "blockNumber": "12345",
            "from": "0xother",
            "to": address,
            "value": "1000000000000000000",  # 1 ETH
            "gasUsed": "21000",
            "gasPrice": "50000000000",  # 50 Gwei
            "timeStamp": "1234567890",
            "confirmations": "10"
        }
        
        result = ethereum.parse_transaction(address, transaction, 18, ethereum.ONE_ETHER)
        
        self.assertEqual(result["type"], "received")
        self.assertEqual(result["value"], 1.0)
        self.assertEqual(result["hash"], "0xabc123")
        self.assertTrue(result["confirmed"])
    
    def test_parse_eth_transaction_sent(self):
        """Test parsing sent ETH transaction."""
        address = "0xtest"
        transaction = {
            "hash": "0xabc123",
            "blockNumber": "12345",
            "from": address,
            "to": "0xother",
            "value": "1000000000000000000",  # 1 ETH
            "gasUsed": "21000",
            "gasPrice": "50000000000",  # 50 Gwei
            "timeStamp": "1234567890",
            "confirmations": "10"
        }
        
        result = ethereum.parse_transaction(address, transaction, 18, ethereum.ONE_ETHER)
        
        self.assertEqual(result["type"], "sent")
        self.assertEqual(result["value"], 1.0)
        self.assertGreater(result["fee"], 0)
    
    def test_parse_token_transaction(self):
        """Test parsing ERC-20 token transaction."""
        address = "0xtest"
        transaction = {
            "hash": "0xabc123",
            "blockNumber": "12345",
            "from": "0xother",
            "to": address,
            "value": "1000000",  # 1 USDT
            "gasUsed": "0",
            "gasPrice": "0",
            "timeStamp": "1234567890",
            "confirmations": "10"
        }
        
        result = ethereum.parse_token_transaction(address, transaction, 6, ethereum.ONE_USDT)
        
        self.assertEqual(result["type"], "received")
        self.assertEqual(result["value"], 1.0)
        self.assertEqual(result["fee"], 0)  # Tokens don't have fees in this context


class TestEtherscanRequest(unittest.TestCase):
    """Test Etherscan API request function."""
    
    @patch('crypto_manager.ethereum.requests.get')
    def test_successful_request(self, mock_get):
        """Test successful API request."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "1",
            "result": {"balance": "1000000000000000000"}
        }
        mock_get.return_value = mock_response
        
        result = ethereum.etherscan_request({"module": "account", "action": "balance"})
        self.assertEqual(result, {"balance": "1000000000000000000"})
    
    @patch('crypto_manager.ethereum.requests.get')
    def test_failed_request(self, mock_get):
        """Test failed API request."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "0",
            "result": "Error"
        }
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError):
            ethereum.etherscan_request({"module": "account", "action": "balance"})


class TestAccountInfoStructure(unittest.TestCase):
    """Test account info structure."""
    
    @patch('crypto_manager.ethereum.etherscan_request')
    def test_eth_account_structure(self, mock_request):
        """Test ETH account info structure."""
        # Mock balance request
        mock_request.side_effect = [
            "1000000000000000000",  # balance
            []  # no transactions
        ]
        
        result = ethereum.get_account_info_eth("0xtest")
        
        # Check structure
        self.assertEqual(result["currency"], "ETH")
        self.assertEqual(result["unit"], ethereum.ONE_ETHER)
        self.assertEqual(result["address"], "0xtest")
        self.assertIn("balance", result)
        self.assertIn("transactions", result)
        self.assertIsInstance(result["transactions"], list)


if __name__ == "__main__":
    unittest.main()

