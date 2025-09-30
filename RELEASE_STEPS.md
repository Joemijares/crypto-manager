# 🎯 Step-by-Step Alpha Release Guide

Complete guide to releasing Crypto Manager v0.1.0-alpha

## 📊 Progress Tracker

- [ ] Step 1: Commit all release files
- [ ] Step 2: Setup GitHub repository
- [ ] Step 3: Create alpha release
- [ ] Step 4: Verify and test
- [ ] Step 5: Announce

---

## Step 1: Commit Release Files 📝

### What we have ready:
✅ CHANGELOG.md - Version history  
✅ pyproject.toml - Updated to v0.1.0-alpha with metadata  
✅ LICENSE - MIT License  
✅ README.md - Comprehensive documentation  
✅ docs/ONBOARDING.md - User guide  
✅ docs/SETUP.md - Configuration guide  
✅ docs/RELEASE.md - Release process documentation  
✅ CONTRIBUTING.md - Contribution guidelines  
✅ scripts/setup-github-repo.sh - Repository setup automation  
✅ scripts/create-release.sh - Release creation automation  

### Action Required:

```bash
cd /Users/nolarose/Downloads/crypto-manager-main

# Make scripts executable
chmod +x scripts/setup-github-repo.sh
chmod +x scripts/create-release.sh

# Stage all changes
git add .

# Commit
git commit -m "🎉 Prepare for v0.1.0-alpha release

- Add CHANGELOG.md with version history
- Update pyproject.toml with full metadata
- Add release automation scripts
- Add RELEASE.md documentation
- Update version to 0.1.0-alpha
- Configure optional dependencies (history, dev)
- Add PyPI classifiers and keywords"

# Push to GitHub
git push origin main
```

**Expected Result:** All files committed and pushed to GitHub main branch

---

## Step 2: Setup GitHub Repository ⚙️

Configure repository settings, topics, and description.

### Option A: Automated (Recommended)

```bash
# Ensure GitHub CLI is installed and authenticated
gh auth status

# If not authenticated:
gh auth login

# Run setup script
./scripts/setup-github-repo.sh
```

**What this does:**
- ✅ Sets repository description
- ✅ Adds 24 relevant topics
- ✅ Enables Issues
- ✅ Enables Discussions
- ✅ Enables Wiki
- ✅ Enables Projects

### Option B: Manual Setup

1. **Go to repository settings:**
   https://github.com/brendadeeznuts1111/crypto-manager/settings

2. **Update "About" section** (click ⚙️ gear icon):
   - **Description:**
     ```
     A comprehensive Python library for managing and tracking cryptocurrency wallets across multiple blockchain networks. Monitor balances, transaction history, and exchange rates for Bitcoin, Ethereum, and various altcoins.
     ```
   
   - **Topics** (click "Topics"):
     ```
     cryptocurrency, bitcoin, ethereum, blockchain, wallet, 
     crypto-tracker, bitcoin-api, ethereum-api, python, python3,
     transaction-history, exchange-rates, erc20-tokens, trc20,
     portfolio-tracker, crypto-portfolio, blockchain-api, usdt,
     usdc, dogecoin, litecoin, solana, polkadot, tron
     ```

3. **Enable Features** (in Settings → General):
   - ✅ Issues
   - ✅ Discussions
   - ✅ Projects
   - ✅ Wiki

**Expected Result:** Repository looks professional with proper topics and description

---

## Step 3: Create Alpha Release 🚀

Create the v0.1.0-alpha release on GitHub.

### Pre-Release Verification

```bash
# Verify we're on the latest commit
git status

# Should show: "Your branch is up to date with 'origin/main'"
# Should show: "nothing to commit, working tree clean"

# Verify version in pyproject.toml
grep "version =" pyproject.toml
# Should show: version = "0.1.0-alpha"

# Quick test of modules
python -m crypto_manager.bitcoin --help || python -c "from crypto_manager import bitcoin; print('✅ Bitcoin module OK')"
python -c "from crypto_manager import ethereum; print('✅ Ethereum module OK')"
python -c "from crypto_manager import tron; print('✅ Tron module OK')"
```

### Create Release

```bash
# Run release script
./scripts/create-release.sh v0.1.0-alpha true
```

**What this does:**
1. Creates git tag `v0.1.0-alpha`
2. Pushes tag to GitHub
3. Creates GitHub release with changelog
4. Marks as pre-release (alpha)

### Alternative: Manual Release Creation

If script doesn't work:

```bash
# Create and push tag
git tag -a v0.1.0-alpha -m "Release v0.1.0-alpha"
git push origin v0.1.0-alpha

# Create release using gh CLI
gh release create v0.1.0-alpha \
  --title "Crypto Manager v0.1.0-alpha" \
  --notes "First alpha release! See CHANGELOG.md for details." \
  --prerelease

# Or create manually on GitHub:
# https://github.com/brendadeeznuts1111/crypto-manager/releases/new
```

**Expected Result:** Release visible at https://github.com/brendadeeznuts1111/crypto-manager/releases

---

## Step 4: Verify and Test ✅

### Verify Release

1. **Check GitHub Release:**
   - Visit: https://github.com/brendadeeznuts1111/crypto-manager/releases/tag/v0.1.0-alpha
   - Verify: Badge shows "Pre-release"
   - Verify: Release notes are visible
   - Verify: Tag is correct

2. **Test Download:**
   ```bash
   # In a temporary directory
   cd /tmp
   git clone --branch v0.1.0-alpha git@github.com:brendadeeznuts1111/crypto-manager.git crypto-manager-test
   cd crypto-manager-test
   
   # Verify files
   ls -la
   cat pyproject.toml | grep version
   
   # Install and test
   pip install loguru requests
   python -c "import crypto_manager; print('✅ Import successful')"
   
   # Cleanup
   cd ..
   rm -rf crypto-manager-test
   ```

3. **Check Repository Appearance:**
   - [ ] README displays properly
   - [ ] Topics are visible
   - [ ] About section is populated
   - [ ] License badge shows MIT
   - [ ] Release badge appears (optional)

### Test Core Functionality

```bash
# Test Bitcoin (public API, no key needed)
python -c "
from crypto_manager.bitcoin import get_account_info
wallet = get_account_info('bc1qwrvfsrn2mt0srfkc7petwxfer70y533sac6y2e', skip_linked_addresses=True)
print(f'✅ Bitcoin: {wallet[\"balance\"]} BTC')
"

# Test Ethereum (requires API key)
# Skip if you don't have Etherscan API key

# Test Exchange Rates
python -c "
from crypto_manager.transactions import get_exchange_rate
rate = get_exchange_rate('BTC')
print(f'✅ Exchange Rate: 1 BTC = \${rate[\"method_to_usd\"]:.2f} USD')
"
```

**Expected Result:** All tests pass, release is accessible

---

## Step 5: Announce Release 📣

### GitHub Announcement

1. **Create Discussion:**
   - Go to: https://github.com/brendadeeznuts1111/crypto-manager/discussions
   - Click "New Discussion"
   - Category: "Announcements"
   - Title: "🎉 Crypto Manager v0.1.0-alpha Released!"
   - Body:
     ```markdown
     We're excited to announce the first alpha release of Crypto Manager! 🚀
     
     ## What's Included
     
     ✅ Bitcoin wallet tracking with full transaction history
     ✅ Ethereum & ERC-20 token support (USDT, USDC, BUSD)
     ✅ Tron TRC-20 USDT support
     ✅ Real-time exchange rates
     ✅ Comprehensive documentation
     
     ## Getting Started
     
     Check out our [Quick Start Guide](https://github.com/brendadeeznuts1111/crypto-manager#quick-start)
     
     ## Feedback Welcome!
     
     This is an alpha release - we'd love your feedback! 
     Please report bugs and feature requests in the Issues section.
     
     **Release Notes:** https://github.com/brendadeeznuts1111/crypto-manager/releases/tag/v0.1.0-alpha
     ```

2. **Update README Badges** (optional):
   Add release badge:
   ```markdown
   [![Latest Release](https://img.shields.io/github/v/release/brendadeeznuts1111/crypto-manager?include_prereleases)](https://github.com/brendadeeznuts1111/crypto-manager/releases)
   ```

### Social Media (Optional)

**Twitter/X:**
```
🎉 Just released Crypto Manager v0.1.0-alpha!

📊 Track Bitcoin, Ethereum & more
💰 Monitor wallet balances & transactions
📈 Real-time exchange rates
🐍 Pure Python, MIT licensed

https://github.com/brendadeeznuts1111/crypto-manager

#Python #Cryptocurrency #OpenSource
```

**Reddit - r/Python:**
```
Title: [Project] Crypto Manager - Track cryptocurrency wallets in Python

Body: Just released the first alpha of Crypto Manager, a library for tracking 
cryptocurrency wallets across multiple blockchains...

[Link to GitHub]
```

**Expected Result:** Community is aware of the release

---

## 📊 Quick Reference

### Important URLs
- **Repository:** https://github.com/brendadeeznuts1111/crypto-manager
- **Releases:** https://github.com/brendadeeznuts1111/crypto-manager/releases
- **Issues:** https://github.com/brendadeeznuts1111/crypto-manager/issues
- **Discussions:** https://github.com/brendadeeznuts1111/crypto-manager/discussions

### Commands Summary
```bash
# Setup repository
./scripts/setup-github-repo.sh

# Create release
./scripts/create-release.sh v0.1.0-alpha true

# Test installation
git clone --branch v0.1.0-alpha [repo-url]

# Check version
python -c "import toml; print(toml.load('pyproject.toml')['project']['version'])"
```

### If Something Goes Wrong

**Delete and retry release:**
```bash
# Delete tag locally
git tag -d v0.1.0-alpha

# Delete tag on GitHub
git push origin :refs/tags/v0.1.0-alpha

# Delete release on GitHub
gh release delete v0.1.0-alpha

# Start over
./scripts/create-release.sh v0.1.0-alpha true
```

---

## ✅ Completion Checklist

After completing all steps:

- [ ] All files committed and pushed
- [ ] Repository configured (topics, description)
- [ ] Alpha release created (v0.1.0-alpha)
- [ ] Release tested and verified
- [ ] Announcement posted (optional)
- [ ] README displays correctly
- [ ] Documentation is accessible
- [ ] Examples work

## 🎯 Next Steps After Release

1. **Monitor Issues:** Check for bug reports
2. **Gather Feedback:** Ask users for suggestions
3. **Plan v0.2.0:** Start roadmap for next version
4. **Improve Docs:** Add more examples based on feedback
5. **Add Features:** Implement Litecoin, Dogecoin support

---

**🎊 Congratulations on your alpha release!** 🎊

