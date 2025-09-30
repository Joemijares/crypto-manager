#!/bin/bash
# Setup GitHub Repository Configuration
# This script configures topics, description, and settings for the crypto-manager repository

set -e

REPO="brendadeeznuts1111/crypto-manager"
DESCRIPTION="A comprehensive Python library for managing and tracking cryptocurrency wallets across multiple blockchain networks. Monitor balances, transaction history, and exchange rates for Bitcoin, Ethereum, and various altcoins."

echo "🚀 Setting up GitHub repository: $REPO"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed"
    echo ""
    echo "Please install it:"
    echo "  macOS:   brew install gh"
    echo "  Linux:   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg"
    echo "  Windows: winget install --id GitHub.cli"
    echo ""
    echo "Or configure manually on GitHub:"
    echo "  https://github.com/$REPO/settings"
    exit 1
fi

# Check authentication
echo "🔐 Checking GitHub authentication..."
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub"
    echo "Please run: gh auth login"
    exit 1
fi

echo "✅ Authenticated"
echo ""

# Set repository description
echo "📝 Setting repository description..."
gh repo edit "$REPO" --description "$DESCRIPTION" || {
    echo "⚠️  Could not set description (may require permissions)"
}
echo ""

# Add topics
echo "🏷️  Adding repository topics..."
TOPICS=(
    "cryptocurrency"
    "bitcoin"
    "ethereum"
    "blockchain"
    "wallet"
    "crypto-tracker"
    "bitcoin-api"
    "ethereum-api"
    "python"
    "python3"
    "transaction-history"
    "exchange-rates"
    "erc20-tokens"
    "trc20"
    "portfolio-tracker"
    "crypto-portfolio"
    "blockchain-api"
    "usdt"
    "usdc"
    "dogecoin"
    "litecoin"
    "solana"
    "polkadot"
    "tron"
)

for topic in "${TOPICS[@]}"; do
    echo "  + $topic"
    gh repo edit "$REPO" --add-topic "$topic" 2>/dev/null || true
done
echo ""

# Enable features
echo "⚙️  Configuring repository features..."
echo "  • Enabling Issues"
gh repo edit "$REPO" --enable-issues || true

echo "  • Enabling Discussions"
gh repo edit "$REPO" --enable-discussions || true

echo "  • Enabling Wiki"
gh repo edit "$REPO" --enable-wiki || true

echo "  • Enabling Projects"
gh repo edit "$REPO" --enable-projects || true
echo ""

echo "✅ Repository configuration complete!"
echo ""
echo "🌐 View your repository:"
echo "   https://github.com/$REPO"
echo ""
echo "📊 Next steps:"
echo "   1. Review settings at: https://github.com/$REPO/settings"
echo "   2. Create first release: ./scripts/create-release.sh"
echo "   3. Enable branch protection: Settings → Branches → Add rule"

