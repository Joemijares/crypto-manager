# 🎓 Crypto Manager - Onboarding Guide

Welcome to Crypto Manager! This guide will help you get started with tracking cryptocurrency wallets and transactions across multiple blockchain networks.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Getting API Keys](#getting-api-keys)
4. [Your First Query](#your-first-query)
5. [Understanding the Data](#understanding-the-data)
6. [Common Use Cases](#common-use-cases)
7. [Next Steps](#next-steps)

## Prerequisites

Before you begin, make sure you have:

- ✅ Python 3.10 or higher installed
- ✅ Basic understanding of Python programming
- ✅ A cryptocurrency wallet address you want to track
- ✅ Internet connection for API queries

### Check Your Python Version

```bash
python --version
# Should output: Python 3.10.x or higher
```

If you need to install Python:
- **macOS**: `brew install python@3.10`
- **Ubuntu/Debian**: `sudo apt install python3.10`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

## Installation

### Step 1: Clone or Download the Repository

```bash
# Using Git
git clone git@github.com:brendadeeznuts1111/crypto-manager.git
cd crypto-manager
```

Or download the ZIP file from GitHub and extract it.

### Step 2: Install Dependencies

We recommend using `uv` for faster package management:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

**Alternative: Using pip**
```bash
pip install loguru requests
```

### Step 3: Verify Installation

```bash
python -c "import crypto_manager; print('✅ Installation successful!')"
```

## Getting API Keys

### Etherscan API Key (Required for Ethereum)

Etherscan provides free API access for querying Ethereum blockchain data.

**Step-by-step:**

1. **Create an Account**
   - Visit [etherscan.io/register](https://etherscan.io/register)
   - Fill in your details and verify your email

2. **Generate API Key**
   - Log in to your account
   - Navigate to: **Account** → **API Keys**
   - Click **"+ Add"** to create a new API key
   - Give it a name (e.g., "Crypto Manager")
   - Copy the generated API key

3. **Configure in Code**
   ```python
   import crypto_manager
   
   # Initialize with your API key
   crypto_manager.init(etherscan_api_key="YOUR_API_KEY_HERE")
   ```

**Alternative: Using config_local.py**

Create a file at `crypto_manager/config_local.py`:
```python
ETHERSCAN_API_KEY = "YOUR_API_KEY_HERE"
```

This keeps your API key separate from your code! 🔒

### Other Blockchains

Good news! Most other blockchains don't require API keys:
- ✅ **Bitcoin** - Uses public Blockstream API
- ✅ **Tron** - Uses public TronGrid API
- ❌ **Ethereum/ERC-20** - Requires Etherscan API key

## Your First Query

Let's track a Bitcoin wallet!

### Example 1: Check Bitcoin Balance

Create a file `my_first_query.py`:

```python
from crypto_manager.bitcoin import get_account_info

# This is a public Bitcoin address (feel free to use any address)
address = "bc1qwrvfsrn2mt0srfkc7petwxfer70y533sac6y2e"

print("📊 Fetching Bitcoin wallet data...")
wallet = get_account_info(address)

print(f"\n💰 Balance: {wallet['balance']} BTC")
print(f"📥 Total Received: {wallet['total_received']} BTC")
print(f"📤 Total Sent: {wallet['total_sent']} BTC")
print(f"📝 Number of Transactions: {len(wallet['transactions'])}")

# Show latest 5 transactions
print("\n🔄 Latest Transactions:")
for tx in wallet['transactions'][:5]:
    emoji = "📥" if tx['type'] == 'received' else "📤"
    print(f"{emoji} {tx['dt'].strftime('%Y-%m-%d %H:%M')} - {tx['value']:.8f} BTC")
```

Run it:
```bash
python my_first_query.py
```

### Example 2: Track Ethereum Wallet

```python
import crypto_manager
from crypto_manager.ethereum import get_account_info_eth

# Initialize with your Etherscan API key
crypto_manager.init(etherscan_api_key="YOUR_API_KEY")

address = "0x8672f9c41325Fc9605c36C5542dF4f56c0490805"

print("📊 Fetching Ethereum wallet data...")
wallet = get_account_info_eth(address)

print(f"\n💰 Balance: {wallet['balance']} ETH")
print(f"📝 Transaction Count: {len(wallet['transactions'])}")
```

### Example 3: Check Multiple Currencies

```python
import crypto_manager
from crypto_manager.bitcoin import get_account_info as get_btc_info
from crypto_manager.ethereum import get_account_info_eth, get_account_info_usdt
from crypto_manager.transactions import get_exchange_rate

# Initialize
crypto_manager.init(etherscan_api_key="YOUR_API_KEY")

# Your addresses
btc_address = "bc1q..."
eth_address = "0x..."

# Get balances
btc = get_btc_info(btc_address)
eth = get_account_info_eth(eth_address)
usdt = get_account_info_usdt(eth_address)

# Get exchange rates
btc_rate = get_exchange_rate("BTC")
eth_rate = get_exchange_rate("ETH")

# Calculate USD values
btc_usd = btc['balance'] * btc_rate['method_to_usd']
eth_usd = eth['balance'] * eth_rate['method_to_usd']
usdt_usd = usdt['balance']  # USDT is already in USD

total_usd = btc_usd + eth_usd + usdt_usd

print(f"\n💼 Portfolio Summary:")
print(f"Bitcoin:  {btc['balance']:.8f} BTC = ${btc_usd:,.2f}")
print(f"Ethereum: {eth['balance']:.8f} ETH = ${eth_usd:,.2f}")
print(f"USDT:     {usdt['balance']:.2f} USDT = ${usdt_usd:,.2f}")
print(f"{'='*50}")
print(f"Total:    ${total_usd:,.2f} USD")
```

## Understanding the Data

### Transaction Types

Every transaction has a `type` field:
- **`"received"`** - You received cryptocurrency
- **`"sent"`** - You sent cryptocurrency

### Values Explained

Each transaction includes multiple value fields:

```python
{
    "value": 0.5,           # Amount transferred (excluding fees)
    "value_raw": "50000000", # Raw blockchain value (in satoshis, wei, etc.)
    "fee": 0.0001,          # Transaction fee
    "fee_raw": "10000",     # Raw fee value
    "total": 0.5001,        # Total = value + fee (for sent transactions)
    "total_raw": "50010000" # Raw total value
}
```

**Why both formats?**
- **Decimal values** (0.5 BTC) are human-readable
- **Raw values** ("50000000") are exact and prevent rounding errors

### Timestamps

Each transaction includes:
```python
{
    "dt": datetime(2024, 1, 1, 12, 0, 0),  # Python datetime object
    "ts": 1704110400.0                      # Unix timestamp (float)
}
```

Use `dt` for formatting, `ts` for calculations!

## Common Use Cases

### 1. Portfolio Tracker
Track total balance across multiple wallets and currencies.

### 2. Transaction Monitor
Get alerts when new transactions occur (check periodically).

### 3. Tax Reporting
Export transaction history for tax calculations.

### 4. Balance Notifications
Send alerts when balance drops below threshold.

### 5. Multi-Wallet Analytics
Compare activity across multiple wallet addresses.

## Next Steps

Now that you're up and running, explore:

1. **[Setup Guide](SETUP.md)** - Advanced configuration options
2. **[API Reference](../README.md#response-format)** - Detailed API documentation
3. **[Contributing](../CONTRIBUTING.md)** - Help improve the project

### Practice Exercises

1. ✏️ Track your own wallet address
2. ✏️ Calculate your portfolio value in USD
3. ✏️ Find your largest transaction
4. ✏️ Calculate total fees paid
5. ✏️ Export transactions to a CSV file

### Example: Calculate Total Fees

```python
from crypto_manager.bitcoin import get_account_info

wallet = get_account_info("bc1q...")

total_fees = sum(tx['fee'] for tx in wallet['transactions'])
print(f"Total fees paid: {total_fees:.8f} BTC")
```

## Getting Help

- 📖 Read the [main README](../README.md)
- 🐛 Found a bug? [Open an issue](https://github.com/brendadeeznuts1111/crypto-manager/issues)
- 💬 Have questions? [Start a discussion](https://github.com/brendadeeznuts1111/crypto-manager/discussions)

## Tips for Success

1. **Start Simple** - Begin with a single wallet query before building complex apps
2. **Use Test Addresses** - Practice with public addresses before using your own
3. **Handle Errors** - Wrap API calls in try/except blocks
4. **Cache Results** - Store exchange rates to avoid repeated API calls
5. **Rate Limits** - Be mindful of API rate limits (especially Etherscan)

---

**🎉 Congratulations!** You're now ready to build powerful crypto tracking applications!

