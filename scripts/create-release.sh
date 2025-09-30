#!/bin/bash
# Create GitHub Release
# Usage: ./scripts/create-release.sh [version] [prerelease]
# Examples:
#   ./scripts/create-release.sh v0.1.0-alpha true
#   ./scripts/create-release.sh v0.2.0 false

set -e

VERSION=${1:-"v0.1.0-alpha"}
PRERELEASE=${2:-"true"}
REPO="brendadeeznuts1111/crypto-manager"

echo "🚀 Creating GitHub Release"
echo ""
echo "Version: $VERSION"
echo "Pre-release: $PRERELEASE"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed"
    echo "Please install it first: brew install gh"
    exit 1
fi

# Check authentication
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub"
    echo "Please run: gh auth login"
    exit 1
fi

# Check if tag already exists
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    echo "⚠️  Tag $VERSION already exists!"
    echo "To delete: git tag -d $VERSION && git push origin :refs/tags/$VERSION"
    exit 1
fi

# Get current commit
COMMIT=$(git rev-parse HEAD)
echo "📝 Current commit: $COMMIT"
echo ""

# Extract release notes from CHANGELOG
echo "📋 Extracting release notes from CHANGELOG.md..."
RELEASE_NOTES=$(awk "/## \[$VERSION\]/,/## \[/" CHANGELOG.md | sed '1d;$d' | sed '/^$/d' || echo "See CHANGELOG.md for details")

if [ -z "$RELEASE_NOTES" ]; then
    RELEASE_NOTES="## Release $VERSION

See [CHANGELOG.md](https://github.com/$REPO/blob/main/CHANGELOG.md) for full details.

### Quick Start

\`\`\`bash
# Clone the repository
git clone git@github.com:$REPO.git
cd crypto-manager

# Install dependencies
pip install loguru requests

# Run example
python -m crypto_manager.bitcoin
\`\`\`

### Documentation

- [README](https://github.com/$REPO#readme)
- [Onboarding Guide](https://github.com/$REPO/blob/main/docs/ONBOARDING.md)
- [Setup Guide](https://github.com/$REPO/blob/main/docs/SETUP.md)
- [Contributing](https://github.com/$REPO/blob/main/CONTRIBUTING.md)
"
fi

echo "$RELEASE_NOTES"
echo ""

# Create git tag
echo "🏷️  Creating git tag..."
git tag -a "$VERSION" -m "Release $VERSION"
echo "✅ Tag created"
echo ""

# Push tag
echo "📤 Pushing tag to GitHub..."
git push origin "$VERSION"
echo "✅ Tag pushed"
echo ""

# Create release
echo "🎉 Creating GitHub release..."
if [ "$PRERELEASE" = "true" ]; then
    gh release create "$VERSION" \
        --repo "$REPO" \
        --title "Crypto Manager $VERSION" \
        --notes "$RELEASE_NOTES" \
        --prerelease
else
    gh release create "$VERSION" \
        --repo "$REPO" \
        --title "Crypto Manager $VERSION" \
        --notes "$RELEASE_NOTES"
fi

echo ""
echo "✅ Release created successfully!"
echo ""
echo "🌐 View release:"
echo "   https://github.com/$REPO/releases/tag/$VERSION"
echo ""
echo "📦 To publish to PyPI (future):"
echo "   python -m build"
echo "   python -m twine upload dist/*"

