# ⚙️ Crypto Manager - Setup Guide

Detailed configuration and setup instructions for Crypto Manager.

## 📋 Table of Contents

1. [Environment Setup](#environment-setup)
2. [API Configuration](#api-configuration)
3. [Proxy Configuration](#proxy-configuration)
4. [Performance Optimization](#performance-optimization)
5. [Error Handling](#error-handling)
6. [Production Deployment](#production-deployment)

## Environment Setup

### Python Version Requirements

Crypto Manager requires Python 3.10 or higher.

```bash
# Check your Python version
python --version

# If you need multiple Python versions, use pyenv
pyenv install 3.10.0
pyenv local 3.10.0
```

### Package Manager Options

#### Option 1: uv (Recommended)

`uv` is a fast Python package installer written in Rust.

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync

# Activate virtual environment (if created)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

#### Option 2: pip + venv

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install loguru requests

# Optional: for exchange rate history
pip install yfinance
```

#### Option 3: Poetry

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Run scripts
poetry run python my_script.py
```

### Verify Installation

```bash
python -c "import crypto_manager, loguru, requests; print('✅ All dependencies installed')"
```

## API Configuration

### Etherscan API Key

Required for all Ethereum-based queries (ETH, USDT, USDC, BUSD).

#### Method 1: Initialize in Code

```python
import crypto_manager

crypto_manager.init(etherscan_api_key="YOUR_API_KEY_HERE")
```

#### Method 2: config_local.py (Recommended)

Create `crypto_manager/config_local.py`:

```python
from loguru import logger

# Your API keys
ETHERSCAN_API_KEY = "YOUR_API_KEY_HERE"

# Optional: Custom settings
logger.info("Loaded custom configuration")
```

**Benefits:**
- ✅ Keeps secrets out of code
- ✅ Not tracked in git (add to .gitignore)
- ✅ Environment-specific configs
- ✅ Easy to switch between dev/prod

#### Method 3: Environment Variables

```bash
# Set environment variable
export ETHERSCAN_API_KEY="your_key_here"
```

```python
import os
import crypto_manager

api_key = os.getenv("ETHERSCAN_API_KEY")
crypto_manager.init(etherscan_api_key=api_key)
```

#### Method 4: .env File

Create `.env` in project root:
```
ETHERSCAN_API_KEY=your_key_here
```

Load it:
```python
from dotenv import load_dotenv
import os
import crypto_manager

load_dotenv()
api_key = os.getenv("ETHERSCAN_API_KEY")
crypto_manager.init(etherscan_api_key=api_key)
```

### API Rate Limits

| Service | Free Tier | Pro Tier |
|---------|-----------|----------|
| Etherscan | 5 calls/sec | 100+ calls/sec |
| Blockstream (BTC) | Unlimited* | - |
| TronGrid | ~100 calls/sec | - |

*Reasonable use expected

**Handling Rate Limits:**

```python
import time
from requests.exceptions import HTTPError

def safe_api_call(func, *args, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")

# Usage
result = safe_api_call(get_account_info_eth, "0x...")
```

## Proxy Configuration

Use proxies for Bitcoin queries to avoid IP-based rate limiting or access geo-restricted APIs.

### SOCKS5 Proxy

```python
from crypto_manager.bitcoin import get_account_info

proxy_config = {
    "type": "socks5",
    "host": "proxy.example.com",
    "port": 1080,
    "username": "user",      # Optional
    "password": "password"   # Optional
}

wallet = get_account_info(
    "bc1qwrvfsrn2mt0srfkc7petwxfer70y533sac6y2e",
    proxy_info=proxy_config
)
```

### HTTP/HTTPS Proxy

```python
proxy_config = {
    "type": "http",
    "host": "proxy.example.com",
    "port": 8080,
    "username": "user",      # Optional
    "password": "password"   # Optional
}
```

### Rotating Proxies

For high-volume applications:

```python
import random

proxy_list = [
    {"type": "socks5", "host": "proxy1.com", "port": 1080},
    {"type": "socks5", "host": "proxy2.com", "port": 1080},
    {"type": "socks5", "host": "proxy3.com", "port": 1080},
]

def get_btc_with_rotation(address):
    proxy = random.choice(proxy_list)
    return get_account_info(address, proxy_info=proxy)
```

## Performance Optimization

### 1. Incremental Syncing

Only fetch new transactions since last sync:

```python
from crypto_manager.bitcoin import get_account_info

# First sync
wallet = get_account_info("bc1q...")
latest_blocks = wallet['latest_block_per_address']

# Save latest_blocks to database or file

# Later syncs - much faster!
wallet = get_account_info(
    "bc1q...",
    latest_block_per_address=latest_blocks
)
```

### 2. Skip Linked Addresses

Bitcoin's linked address discovery is slow. Skip it if not needed:

```python
wallet = get_account_info(
    "bc1q...",
    skip_linked_addresses=True  # 5-10x faster
)
```

### 3. Caching Exchange Rates

Exchange rates don't change every second:

```python
import time

class ExchangeRateCache:
    def __init__(self, ttl=300):  # 5 minutes
        self.cache = {}
        self.ttl = ttl
    
    def get_rate(self, currency):
        now = time.time()
        if currency in self.cache:
            rate, timestamp = self.cache[currency]
            if now - timestamp < self.ttl:
                return rate
        
        rate = get_exchange_rate(currency)
        self.cache[currency] = (rate, now)
        return rate

cache = ExchangeRateCache(ttl=300)
btc_rate = cache.get_rate("BTC")
```

### 4. Parallel Queries

Query multiple addresses simultaneously:

```python
from concurrent.futures import ThreadPoolExecutor

addresses = [
    "bc1q...",
    "bc1q...",
    "bc1q..."
]

def fetch_wallet(address):
    return get_account_info(address)

with ThreadPoolExecutor(max_workers=5) as executor:
    wallets = list(executor.map(fetch_wallet, addresses))

total_balance = sum(w['balance'] for w in wallets)
```

### 5. Database Storage

Store results in SQLite for fast access:

```python
import sqlite3
import json

def save_wallet(address, wallet_data):
    conn = sqlite3.connect('wallets.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            address TEXT PRIMARY KEY,
            data TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        INSERT OR REPLACE INTO wallets (address, data)
        VALUES (?, ?)
    ''', (address, json.dumps(wallet_data)))
    
    conn.commit()
    conn.close()
```

## Error Handling

### Comprehensive Error Handling

```python
from loguru import logger
import requests
from crypto_manager.bitcoin import get_account_info

def safe_get_wallet(address):
    try:
        return get_account_info(address)
    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching {address}")
        return None
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error for {address}")
        return None
    except ValueError as e:
        logger.error(f"Invalid response: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return None

wallet = safe_get_wallet("bc1q...")
if wallet:
    print(f"Balance: {wallet['balance']}")
else:
    print("Failed to fetch wallet")
```

### Logging Configuration

```python
from loguru import logger

# Remove default handler
logger.remove()

# Add custom handlers
logger.add(
    "crypto_manager.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO"
)

logger.add(
    lambda msg: print(msg, end=""),
    colorize=True,
    level="DEBUG"
)
```

## Production Deployment

### Configuration Checklist

- [ ] API keys stored securely (not in code)
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Rate limiting respected
- [ ] Caching enabled
- [ ] Database for persistence
- [ ] Monitoring/alerting setup
- [ ] Backup strategy defined

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml ./
COPY crypto_manager ./crypto_manager

# Install dependencies
RUN uv sync

# Run your script
CMD ["python", "-m", "your_script"]
```

Build and run:
```bash
docker build -t crypto-manager .
docker run -e ETHERSCAN_API_KEY=your_key crypto-manager
```

### Systemd Service (Linux)

Create `/etc/systemd/system/crypto-manager.service`:

```ini
[Unit]
Description=Crypto Manager Service
After=network.target

[Service]
Type=simple
User=crypto
WorkingDirectory=/opt/crypto-manager
Environment="ETHERSCAN_API_KEY=your_key"
ExecStart=/usr/bin/python3 /opt/crypto-manager/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable crypto-manager
sudo systemctl start crypto-manager
sudo systemctl status crypto-manager
```

### Environment Variables (Production)

```bash
# .env.production
ETHERSCAN_API_KEY=your_production_key
LOG_LEVEL=INFO
CACHE_TTL=300
DB_PATH=/var/lib/crypto-manager/wallets.db
```

### Security Best Practices

1. **Never commit API keys** - Use `.gitignore`
2. **Use HTTPS only** - All API calls over secure connections
3. **Validate addresses** - Check format before querying
4. **Sanitize inputs** - Prevent injection attacks
5. **Regular updates** - Keep dependencies updated
6. **Audit logs** - Track all API calls

---

Need more help? Check the [Onboarding Guide](ONBOARDING.md) or [open an issue](https://github.com/brendadeeznuts1111/crypto-manager/issues)!

