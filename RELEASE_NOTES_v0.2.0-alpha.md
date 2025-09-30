# Crypto Manager v0.2.0-alpha

Second alpha release with full Litecoin and Dogecoin support, plus comprehensive test suite! 🚀

## 🌟 What's New

### 💰 Full Litecoin (LTC) Support
- Complete wallet tracking via Blockchair API
- Balance queries and transaction history
- Standardized response format matching other chains
- Example usage in README

```python
from crypto_manager.ltc import get_account_info

ltc_wallet = get_account_info("LTC_address_here")
print(f"LTC Balance: {ltc_wallet['balance']} LTC")
```

### 🐕 Full Dogecoin (DOGE) Support  
- Complete wallet tracking via Blockchair API
- Balance queries and transaction history
- Much wow! To the moon! 🚀
- Example usage in README

```python
from crypto_manager.doge import get_account_info

doge_wallet = get_account_info("DOGE_address_here")
print(f"DOGE Balance: {doge_wallet['balance']} DOGE")
```

### 🧪 Comprehensive Test Suite
We've added **49+ unit and integration tests** for stability:

- **Bitcoin tests** (10 tests) - Constants, proxy config, transactions
- **Ethereum tests** (12 tests) - ETH and ERC-20 token functionality
- **LTC/DOGE tests** (7 tests) - New implementations
- **Transaction tests** (8 tests) - Exchange rate fetching
- **Integration tests** (6 tests) - Real API calls (opt-in)
- **Configuration tests** (2 tests) - Config validation

Run tests:
```bash
# All tests
python3 -m pytest tests/ -v

# Specific module
python3 -m pytest tests/test_ltc_doge.py -v

# With coverage
python3 -m pytest tests/ --cov=crypto_manager
```

## 📚 Documentation Improvements

- ✅ Complete testing guide in `tests/README.md`
- ✅ Updated README with LTC/DOGE examples
- ✅ Enhanced project structure documentation
- ✅ GitHub issue templates (bug report, feature request)
- ✅ Release checklist for maintainers
- ✅ Updated CHANGELOG with all changes

## 🔧 Technical Improvements

- Enhanced error handling in LTC and DOGE modules
- Comprehensive docstrings for all new functions
- Mock API testing framework (no external API calls in unit tests)
- Organized tests by module for better maintainability
- Support for both `unittest` and `pytest` test runners

## 📊 Statistics

- **7 supported cryptocurrencies**: BTC, ETH, USDT (ERC-20), USDC (ERC-20), BUSD (ERC-20), LTC, DOGE
- **49+ test cases** ensuring stability
- **~1,428 lines** of code added
- **12 files** modified or created

## 🚀 Quick Start

```bash
# Clone repository
git clone git@github.com:brendadeeznuts1111/crypto-manager.git
cd crypto-manager

# Install dependencies
pip install loguru requests

# Try Litecoin
python3 -m crypto_manager.ltc

# Try Dogecoin
python3 -m crypto_manager.doge

# Run tests
python3 -m pytest tests/ -v
```

## 📖 Documentation

- [README](https://github.com/brendadeeznuts1111/crypto-manager#readme)
- [Onboarding Guide](https://github.com/brendadeeznuts1111/crypto-manager/blob/main/docs/ONBOARDING.md)
- [Setup Guide](https://github.com/brendadeeznuts1111/crypto-manager/blob/main/docs/SETUP.md)
- [Testing Guide](https://github.com/brendadeeznuts1111/crypto-manager/blob/main/tests/README.md)
- [Contributing](https://github.com/brendadeeznuts1111/crypto-manager/blob/main/CONTRIBUTING.md)
- [Changelog](https://github.com/brendadeeznuts1111/crypto-manager/blob/main/CHANGELOG.md)

## 🐛 Known Issues

- Blockchair API rate limits may apply to LTC/DOGE queries
- Etherscan API key still required for Ethereum queries (5 calls/sec on free tier)
- Solana and Polkadot modules are still placeholders (coming soon!)

## 🗺️ What's Next

- Solana wallet integration
- Polkadot wallet integration
- Caching layer for exchange rates
- CI/CD pipeline with GitHub Actions
- WebSocket support for real-time updates
- Publish to PyPI

## 💬 Feedback

This is an alpha release - we'd love your feedback!

- 🐛 [Report bugs](https://github.com/brendadeeznuts1111/crypto-manager/issues/new?template=bug_report.md)
- 💡 [Request features](https://github.com/brendadeeznuts1111/crypto-manager/issues/new?template=feature_request.md)
- 💬 [Start a discussion](https://github.com/brendadeeznuts1111/crypto-manager/discussions)

---

**Full Changelog**: https://github.com/brendadeeznuts1111/crypto-manager/compare/v0.1.0-alpha...v0.2.0-alpha

**Thanks for using Crypto Manager!** 🎉

