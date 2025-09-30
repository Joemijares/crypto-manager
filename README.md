# 🪙 Crypto Manager

A comprehensive Python library for managing and tracking cryptocurrency wallets across multiple blockchain networks. Monitor balances, transaction history, and exchange rates for Bitcoin, Ethereum, and various altcoins.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🌟 Features

### Supported Cryptocurrencies
- **Bitcoin (BTC)** ✅ Full transaction tracking with linked address discovery
- **Ethereum (ETH)** ✅ Native ETH + ERC-20 token support
  - USDT (ERC-20) ✅
  - USDC (ERC-20) ✅
  - BUSD (ERC-20) ✅
- **Tron (TRX)** ✅ TRC-20 USDT support
- **Litecoin (LTC)** ✅ Full wallet tracking (NEW!)
- **Dogecoin (DOGE)** ✅ Full wallet tracking (NEW!)
- **Solana (SOL)** 🚧 Coming soon
- **Polkadot (DOT)** 🚧 Coming soon

### Core Capabilities
✅ **Account Balance Tracking** - Real-time balance queries across all supported chains  
✅ **Transaction History** - Complete transaction logs with sent/received classification  
✅ **Linked Address Discovery** - Automatically detect related wallet addresses (BTC)  
✅ **Exchange Rate Fetching** - Real-time USD conversion rates  
✅ **Multi-Network Support** - Query multiple blockchains from a single interface  
✅ **Proxy Support** - SOCKS5 and HTTP proxy configuration for Bitcoin queries  
✅ **Raw & Formatted Values** - Access both human-readable and raw blockchain values  
✅ **Comprehensive Testing** - 49+ unit and integration tests for stability  
✅ **Well Documented** - Detailed guides for onboarding, setup, and contributing  

## 📦 Installation

### Using uv (Recommended)
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

### Using pip
```bash
pip install -r requirements.txt
```

### Dependencies
- `loguru>=0.7.3` - Structured logging
- `requests>=2.32.5` - HTTP client for API requests

## 🚀 Quick Start

### 1. Initialize with API Keys
```python
import crypto_manager

# Set your Etherscan API key for Ethereum queries
crypto_manager.init(etherscan_api_key="YOUR_ETHERSCAN_API_KEY")
```

### 2. Query Bitcoin Wallet
```python
from crypto_manager.bitcoin import get_account_info

# Get account info for a BTC address
btc_info = get_account_info("bc1qwrvfsrn2mt0srfkc7petwxfer70y533sac6y2e")

print(f"Balance: {btc_info['balance']} BTC")
print(f"Total Received: {btc_info['total_received']} BTC")
print(f"Total Sent: {btc_info['total_sent']} BTC")

# Access transactions
for tx in btc_info['transactions']:
    print(f"{tx['dt']} - {tx['type']}: {tx['value']} BTC ({tx['hash']})")
```

### 3. Query Ethereum Wallet
```python
from crypto_manager.ethereum import get_account_info_eth, get_account_info_usdt

# Get ETH balance and transactions
eth_info = get_account_info_eth("0x8672f9c41325Fc9605c36C5542dF4f56c0490805")
print(f"ETH Balance: {eth_info['balance']} ETH")

# Get USDT (ERC-20) balance and transactions
usdt_info = get_account_info_usdt("0x8672f9c41325Fc9605c36C5542dF4f56c0490805")
print(f"USDT Balance: {usdt_info['balance']} USDT")
```

### 4. Get Exchange Rates
```python
from crypto_manager.transactions import get_exchange_rate

# Get current exchange rate
btc_rate = get_exchange_rate("BTC")
print(f"1 BTC = ${btc_rate['method_to_usd']:.2f} USD")

eth_rate = get_exchange_rate("ETH")
print(f"1 ETH = ${eth_rate['method_to_usd']:.2f} USD")
```

### 5. Query Tron (TRC-20 USDT)
```python
from crypto_manager.tron import get_account_info_usdt

# Get USDT balance on Tron network
tron_usdt = get_account_info_usdt("TADCt9L4JjrSrCLM2ZtVcs4yuhWoFTxYbT")
print(f"USDT (TRC-20) Balance: {tron_usdt['balance']} USDT")
```

### 6. Query Litecoin (NEW!)
```python
from crypto_manager.ltc import get_account_info

# Get Litecoin wallet info
ltc_wallet = get_account_info("LTC_address_here")
print(f"LTC Balance: {ltc_wallet['balance']} LTC")
print(f"Transactions: {len(ltc_wallet['transactions'])}")
```

### 7. Query Dogecoin (NEW!)
```python
from crypto_manager.doge import get_account_info

# Get Dogecoin wallet info  
doge_wallet = get_account_info("DOGE_address_here")
print(f"DOGE Balance: {doge_wallet['balance']} DOGE")
print("Much wow! To the moon! 🚀🐕")
```

## 📖 Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed configuration and API key setup
- **[Onboarding](docs/ONBOARDING.md)** - Step-by-step guide for new users
- **[Contributing](CONTRIBUTING.md)** - How to contribute to the project

## 🛠️ Advanced Usage

### Using Proxies (Bitcoin)
```python
from crypto_manager.bitcoin import get_account_info

proxy_config = {
    "type": "socks5",  # or "http"
    "host": "proxy.example.com",
    "port": 1080,
    "username": "user",  # optional
    "password": "pass"   # optional
}

btc_info = get_account_info(
    "bc1qwrvfsrn2mt0srfkc7petwxfer70y533sac6y2e",
    proxy_info=proxy_config
)
```

### Incremental Sync (Bitcoin)
```python
# First sync
btc_info = get_account_info("bc1q...")
latest_blocks = btc_info['latest_block_per_address']

# Later syncs - only fetch new transactions
btc_info = get_account_info(
    "bc1q...",
    latest_block_per_address=latest_blocks
)
```

### Skip Linked Address Discovery (Bitcoin)
```python
# Faster queries when you don't need linked addresses
btc_info = get_account_info(
    "bc1q...",
    skip_linked_addresses=True
)
```

## 📊 Response Format

All account info methods return a standardized dictionary:

```python
{
    "currency": "BTC",
    "unit": 100000000,  # Satoshis per BTC
    "address": "bc1q...",
    "balance": 0.12345678,
    "balance_raw": "12345678",
    "total_received": 1.5,
    "total_received_raw": "150000000",
    "total_sent": 1.37654322,
    "total_sent_raw": "137654322",
    "transactions": [
        {
            "hash": "abc123...",
            "type": "received",  # or "sent"
            "value": 0.5,
            "value_raw": "50000000",
            "fee": 0.0001,
            "fee_raw": "10000",
            "total": 0.5001,
            "total_raw": "50010000",
            "dt": datetime(2024, 1, 1, 12, 0, 0),
            "ts": 1704110400.0,
            "confirmed": true,
            "from": [...],
            "to": [...]
        }
    ],
    "latest_block_per_address": {
        "bc1q...": 850000
    }
}
```

## 🔑 API Keys & Configuration

### Etherscan API Key (Required for Ethereum)
1. Sign up at [etherscan.io](https://etherscan.io/register)
2. Navigate to API Keys section
3. Create a new API key
4. Initialize the library with your key:
   ```python
   import crypto_manager
   crypto_manager.init(etherscan_api_key="YOUR_KEY_HERE")
   ```

### Local Configuration (Optional)
Create `crypto_manager/config_local.py` to override default values:
```python
ETHERSCAN_API_KEY = "your_api_key_here"
```

## 🧪 Testing

### Run Unit Tests

Comprehensive test suite with 49+ tests covering all modules:

```bash
# Run all tests
python3 -m pytest tests/ -v

# Or using unittest
python3 -m unittest discover tests

# Run specific module tests
python3 -m pytest tests/test_bitcoin.py -v
python3 -m pytest tests/test_ethereum.py -v
python3 -m pytest tests/test_ltc_doge.py -v

# Run with coverage
pip install pytest-cov
python3 -m pytest tests/ --cov=crypto_manager --cov-report=html
```

### Test Coverage

- **Bitcoin**: 10 tests covering constants, proxy config, transactions
- **Ethereum**: 12 tests covering ETH and ERC-20 tokens
- **LTC/DOGE**: 7 tests covering new implementations
- **Transactions**: 8 tests covering exchange rates
- **Integration**: 6 tests for real API calls (opt-in)

See [tests/README.md](tests/README.md) for detailed testing documentation.

### Run Example Scripts

Test functionality with example scripts:

```bash
# Test Bitcoin
python3 -m crypto_manager.bitcoin

# Test Ethereum
python3 -m crypto_manager.ethereum

# Test Litecoin
python3 -m crypto_manager.ltc

# Test Dogecoin
python3 -m crypto_manager.doge

# Test Tron USDT
python3 -m crypto_manager.tron

# Test Exchange Rates
python3 -m crypto_manager.transactions
```

## 🏗️ Project Structure

```
crypto-manager/
├── crypto_manager/
│   ├── __init__.py          # Initialization & config
│   ├── bitcoin.py           # Bitcoin implementation
│   ├── ethereum.py          # Ethereum + ERC-20 tokens
│   ├── tron.py              # Tron TRC-20 support
│   ├── ltc.py               # Litecoin implementation ✨
│   ├── doge.py              # Dogecoin implementation ✨
│   ├── transactions.py      # Exchange rates & utils
│   ├── sol.py               # Solana constants
│   ├── dot.py               # Polkadot constants
│   └── config.py            # Configuration management
├── tests/                   # Test suite ✨
│   ├── test_bitcoin.py      # Bitcoin tests
│   ├── test_ethereum.py     # Ethereum tests
│   ├── test_ltc_doge.py     # LTC/DOGE tests
│   ├── test_transactions.py # Exchange rate tests
│   ├── test_integration.py  # Integration tests
│   └── README.md            # Testing guide
├── docs/                    # Documentation
│   ├── ONBOARDING.md        # New user guide
│   ├── SETUP.md             # Configuration guide
│   └── RELEASE.md           # Release process
├── scripts/                 # Automation scripts
│   ├── setup-github-repo.sh # Repository configuration
│   └── create-release.sh    # Release automation
├── .github/                 # GitHub templates
│   └── ISSUE_TEMPLATE/      # Issue templates
├── pyproject.toml           # Project metadata
├── CHANGELOG.md             # Version history
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # MIT License
└── README.md                # This file
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
# Clone the repository
git clone git@github.com:brendadeeznuts1111/crypto-manager.git
cd crypto-manager

# Install dependencies
uv sync

# Make your changes and test
python -m crypto_manager.bitcoin
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛡️ Security

- Never commit API keys to the repository
- Use environment variables or `config_local.py` for sensitive data
- Review transaction data carefully before processing
- Always verify addresses before sending transactions

## 🐛 Known Issues & Limitations

- Litecoin, Dogecoin, Solana, and Polkadot modules are currently placeholders
- Ethereum queries are limited by Etherscan API rate limits
- Bitcoin linked address discovery can be slow for wallets with many transactions
- Exchange rate history requires `yfinance` package (optional dependency)

## 📮 Support

- **Issues**: [GitHub Issues](https://github.com/brendadeeznuts1111/crypto-manager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/brendadeeznuts1111/crypto-manager/discussions)

## 🗺️ Roadmap

- [x] Implement full Litecoin support ✅ (v0.2.0-alpha)
- [x] Implement full Dogecoin support ✅ (v0.2.0-alpha)
- [x] Comprehensive test suite ✅ (v0.2.0-alpha)
- [ ] Implement Solana support
- [ ] Implement Polkadot support
- [ ] Add caching layer for exchange rates
- [ ] WebSocket support for real-time updates
- [ ] Export transaction history to CSV/JSON
- [ ] Docker container for easy deployment
- [ ] GraphQL API wrapper
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Publish to PyPI

---

**Made with ❤️ by the Crypto Manager Team**

