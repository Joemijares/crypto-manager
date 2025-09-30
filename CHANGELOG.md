# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Full Litecoin support
- Full Dogecoin support
- Solana wallet integration
- Polkadot wallet integration
- Caching layer for exchange rates
- WebSocket support for real-time updates
- CSV/JSON export functionality
- Docker container
- GraphQL API wrapper

## [0.1.0-alpha] - 2024-09-30

### Added
- Initial alpha release 🎉
- Bitcoin wallet tracking with transaction history
- Bitcoin linked address discovery
- Bitcoin proxy support (SOCKS5 and HTTP)
- Ethereum wallet tracking
- ERC-20 token support (USDT, USDC, BUSD)
- Tron TRC-20 USDT support
- Exchange rate fetching for BTC, ETH, DOT, LTC, SOL, DOGE
- Exchange rate history support (with yfinance)
- Standardized response format across all chains
- Comprehensive documentation
  - README with quick start guide
  - ONBOARDING guide for new users
  - SETUP guide with advanced configuration
  - CONTRIBUTING guide for developers
- MIT License
- Python 3.10+ support
- Proxy configuration for Bitcoin queries
- Incremental sync capability
- Raw and formatted value formats
- Timestamp support (datetime and unix)

### Supported Cryptocurrencies
- ✅ Bitcoin (BTC) - Full support
- ✅ Ethereum (ETH) - Full support
- ✅ USDT (ERC-20) - Full support
- ✅ USDC (ERC-20) - Full support
- ✅ BUSD (ERC-20) - Full support
- ✅ USDT (TRC-20) - Full support
- 🚧 Litecoin (LTC) - Constants only
- 🚧 Dogecoin (DOGE) - Constants only
- 🚧 Solana (SOL) - Constants only
- 🚧 Polkadot (DOT) - Constants only

### Dependencies
- loguru >= 0.7.3
- requests >= 2.32.5
- yfinance (optional, for exchange rate history)

### Known Limitations
- Etherscan API rate limits apply (5 calls/sec on free tier)
- Bitcoin linked address discovery can be slow for high-activity wallets
- LTC, DOGE, SOL, DOT modules are placeholders (constants only)
- Exchange rate history requires optional yfinance dependency

### Security
- API keys managed via config system
- Support for config_local.py to keep secrets separate
- All API calls over HTTPS
- No sensitive data logged

[Unreleased]: https://github.com/brendadeeznuts1111/crypto-manager/compare/v0.1.0-alpha...HEAD
[0.1.0-alpha]: https://github.com/brendadeeznuts1111/crypto-manager/releases/tag/v0.1.0-alpha

