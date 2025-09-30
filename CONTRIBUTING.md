# 🤝 Contributing to Crypto Manager

Thank you for your interest in contributing to Crypto Manager! We welcome contributions from the community.

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Adding New Cryptocurrencies](#adding-new-cryptocurrencies)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Expected Behavior

- ✅ Be respectful and considerate
- ✅ Welcome newcomers and help them get started
- ✅ Focus on constructive criticism
- ✅ Accept feedback gracefully
- ✅ Show empathy towards others

### Unacceptable Behavior

- ❌ Harassment or discriminatory language
- ❌ Personal attacks or trolling
- ❌ Publishing others' private information
- ❌ Spam or self-promotion

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating a bug report:
1. Check if the issue already exists
2. Update to the latest version
3. Verify it's not a configuration issue

**Good bug reports include:**
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Error messages and logs
- Code samples (if applicable)

**Example:**
```markdown
**Description:** Bitcoin query fails with proxy timeout

**Steps to Reproduce:**
1. Configure SOCKS5 proxy
2. Call `get_account_info("bc1q...")`
3. Wait for timeout

**Expected:** Should return wallet data
**Actual:** Timeout after 60 seconds

**Environment:**
- Python 3.10.5
- macOS 13.0
- crypto-manager commit abc123

**Error:**
```
requests.exceptions.Timeout: ...
```
```

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**Good enhancement suggestions include:**
- Clear use case
- Benefits and motivation
- Potential implementation approach
- Examples from similar projects

### 📝 Improving Documentation

Documentation improvements are always welcome!

- Fix typos or unclear wording
- Add examples
- Improve code comments
- Translate documentation
- Create tutorials or guides

### 💻 Contributing Code

See [Development Setup](#development-setup) and [Pull Request Process](#pull-request-process).

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone git@github.com:YOUR_USERNAME/crypto-manager.git
cd crypto-manager

# Add upstream remote
git remote add upstream git@github.com:brendadeeznuts1111/crypto-manager.git
```

### 2. Create Virtual Environment

```bash
# Using uv (recommended)
uv sync

# Or using venv
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install loguru requests
```

### 3. Create a Branch

```bash
git checkout -b feature/my-new-feature
# or
git checkout -b fix/bug-description
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions/changes

### 4. Make Your Changes

Follow the [Coding Standards](#coding-standards) below.

### 5. Test Your Changes

```bash
# Test Bitcoin module
python -m crypto_manager.bitcoin

# Test Ethereum module
python -m crypto_manager.ethereum

# Test your specific changes
python your_test_script.py
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 88 characters (Black default)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings
- **Imports**: Organized and alphabetized

### Code Formatting

We use [Black](https://github.com/psf/black) for consistent formatting:

```bash
# Install Black
pip install black

# Format your code
black crypto_manager/

# Check formatting
black --check crypto_manager/
```

### Import Organization

```python
# Standard library imports
import datetime
import time

# Third-party imports
import requests
from loguru import logger

# Local imports
from crypto_manager import config
from crypto_manager.bitcoin import ONE_BTC
```

### Naming Conventions

```python
# Constants
ONE_BTC = 100000000
API_BASE = "https://api.example.com"

# Functions
def get_account_info(address):
    pass

# Classes
class WalletManager:
    pass

# Variables
user_address = "bc1q..."
transaction_list = []
```

### Documentation

#### Docstrings

Use Google-style docstrings:

```python
def get_account_info(address, latest_block=0, proxy_info=None):
    """Fetch Bitcoin account information and transaction history.
    
    Args:
        address (str): Bitcoin address to query
        latest_block (int, optional): Only fetch transactions after this block. Defaults to 0.
        proxy_info (dict, optional): Proxy configuration. Defaults to None.
    
    Returns:
        dict: Account information including balance, transactions, and metadata
        
    Raises:
        ValueError: If address format is invalid
        requests.exceptions.Timeout: If API request times out
        
    Example:
        >>> wallet = get_account_info("bc1qwrvfsrn2mt0srfkc7petwxfer70y533sac6y2e")
        >>> print(wallet['balance'])
        0.12345678
    """
    pass
```

#### Comments

```python
# Good: Explain WHY, not WHAT
# Use exponential backoff to handle rate limiting
time.sleep(2 ** attempt)

# Bad: Obvious comment
# Add 1 to counter
counter += 1
```

### Error Handling

Always handle expected errors:

```python
# Good
try:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.json()
except requests.exceptions.Timeout:
    logger.error(f"Timeout fetching {url}")
    raise
except requests.exceptions.HTTPError as e:
    logger.error(f"HTTP error: {e}")
    raise
except ValueError as e:
    logger.error(f"Invalid JSON response: {e}")
    raise

# Bad
response = requests.get(url)
return response.json()  # What if this fails?
```

## Testing Guidelines

### Manual Testing

Test your changes with real-world scenarios:

```python
# Test with various address formats
addresses = [
    "bc1q...",  # Bech32
    "1A1zP1...", # Legacy
    "3J98t1..."  # P2SH
]

for addr in addresses:
    try:
        wallet = get_account_info(addr)
        assert 'balance' in wallet
        print(f"✅ {addr}")
    except Exception as e:
        print(f"❌ {addr}: {e}")
```

### Test Coverage

Ensure your changes work for:
- ✅ Valid inputs
- ✅ Invalid inputs
- ✅ Edge cases (empty addresses, zero balances)
- ✅ Error conditions (API failures, timeouts)

### Performance Testing

For performance-critical changes:

```python
import time

start = time.time()
result = get_account_info("bc1q...")
duration = time.time() - start

print(f"Query took {duration:.2f} seconds")
```

## Pull Request Process

### 1. Update Your Fork

```bash
# Fetch latest changes
git fetch upstream

# Update your main branch
git checkout main
git merge upstream/main
git push origin main

# Rebase your feature branch
git checkout feature/my-feature
git rebase main
```

### 2. Commit Your Changes

Write clear, descriptive commit messages:

```bash
# Good commit messages
git commit -m "Add support for Litecoin transaction queries"
git commit -m "Fix Bitcoin proxy timeout handling"
git commit -m "Update README with Docker deployment guide"

# Bad commit messages
git commit -m "fix bug"
git commit -m "changes"
git commit -m "update"
```

### 3. Push to Your Fork

```bash
git push origin feature/my-feature
```

### 4. Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template

**Good PR descriptions include:**
- What changed and why
- Related issue numbers (#123)
- Testing performed
- Screenshots (if UI changes)
- Breaking changes (if any)

**Example:**
```markdown
## Description
Adds support for querying Litecoin wallet balances and transaction history.

## Related Issues
Closes #45

## Changes
- Added `ltc.py` with Litecoin API integration
- Updated `transactions.py` to include LTC exchange rates
- Added tests for LTC functionality

## Testing
- ✅ Tested with 5 different LTC addresses
- ✅ Verified exchange rate fetching
- ✅ Confirmed transaction parsing

## Breaking Changes
None
```

### 5. Code Review

- Respond to feedback promptly
- Make requested changes
- Push updates to your branch
- Request re-review when ready

### 6. Merge

Once approved, a maintainer will merge your PR. 🎉

## Adding New Cryptocurrencies

Want to add support for a new cryptocurrency? Follow these steps:

### 1. Research the API

Find a reliable, public API:
- Block explorers (Etherscan-style)
- Official blockchain APIs
- Third-party services

Requirements:
- ✅ Free tier available
- ✅ No mandatory API key (preferred)
- ✅ Reasonable rate limits
- ✅ Documented endpoints

### 2. Create Module File

Create `crypto_manager/your_coin.py`:

```python
import datetime
import requests

# Define the base unit (smallest denomination)
ONE_YOURCOIN = 10**8  # Adjust based on coin's decimals

def get_account_info(address, latest_block=0):
    """Fetch account information for YourCoin.
    
    Args:
        address (str): YourCoin address
        latest_block (int, optional): Fetch transactions after this block
        
    Returns:
        dict: Standardized account information
    """
    # Fetch data from API
    response = requests.get(
        f"https://api.yourcoin.com/address/{address}",
        timeout=60
    ).json()
    
    # Return standardized format
    return {
        "currency": "YOURCOIN",
        "unit": ONE_YOURCOIN,
        "address": address,
        "balance": response['balance'] / ONE_YOURCOIN,
        "balance_raw": str(response['balance']),
        "total_sent": response['total_sent'] / ONE_YOURCOIN,
        "total_sent_raw": str(response['total_sent']),
        "total_received": response['total_received'] / ONE_YOURCOIN,
        "total_received_raw": str(response['total_received']),
        "transactions": [
            # Parse transactions here
        ]
    }
```

### 3. Update transactions.py

Add exchange rate support:

```python
def get_exchange_rate_yourcoin():
    res = requests.get(YOURCOIN_EXCHANGE_URL, timeout=60).json()
    yourcoin_to_usd_rate = res["price"]
    
    return {
        "method_to_usd": yourcoin_to_usd_rate,
        "usd_to_method": 1 / yourcoin_to_usd_rate,
        "unit": yourcoin.ONE_YOURCOIN,
        "exchange_rate_ts": res["timestamp"],
    }

# Add to fn_map
fn_map = {
    "BTC": get_exchange_rate_btc,
    "ETH": get_exchange_rate_eth,
    "YOURCOIN": get_exchange_rate_yourcoin,  # Add this
}
```

### 4. Add Tests

Add example usage in `if __name__ == "__main__":` block:

```python
if __name__ == "__main__":
    wallet = get_account_info("yourcoin_address_here")
    print(f"Balance: {wallet['balance']} YOURCOIN")
    print(f"Transactions: {len(wallet['transactions'])}")
```

### 5. Update Documentation

Update README.md:
- Add to supported cryptocurrencies list
- Add usage example
- Update feature table

### 6. Submit PR

Follow the [Pull Request Process](#pull-request-process) above.

## Questions?

- 💬 [GitHub Discussions](https://github.com/brendadeeznuts1111/crypto-manager/discussions)
- 🐛 [GitHub Issues](https://github.com/brendadeeznuts1111/crypto-manager/issues)

---

**Thank you for contributing! 🎉**

