# 📦 Release Process

This document outlines the release process for Crypto Manager.

## 🎯 Release Philosophy

We follow [Semantic Versioning](https://semver.org/) (SemVer):

- **MAJOR** version (1.0.0): Incompatible API changes
- **MINOR** version (0.1.0): New functionality, backwards-compatible
- **PATCH** version (0.1.1): Backwards-compatible bug fixes
- **Pre-release** tags: alpha, beta, rc (e.g., 0.1.0-alpha, 1.0.0-beta.1)

## 📋 Pre-Release Checklist

Before creating a release, ensure:

### 1. Code Quality ✅
- [ ] All features are implemented and tested
- [ ] No critical bugs or issues
- [ ] Code is properly documented
- [ ] Examples work as expected

### 2. Documentation ✅
- [ ] README.md is up to date
- [ ] CHANGELOG.md is updated with new changes
- [ ] API documentation reflects current code
- [ ] Migration guides (if breaking changes)

### 3. Testing ✅
- [ ] Manual testing completed
- [ ] Example scripts run successfully
- [ ] Tested with Python 3.10, 3.11, 3.12
- [ ] Tested on different operating systems (if possible)

### 4. Dependencies ✅
- [ ] All dependencies are up to date
- [ ] No security vulnerabilities
- [ ] pyproject.toml version is correct
- [ ] Lock file is regenerated

### 5. Repository ✅
- [ ] All commits are pushed
- [ ] Branch is clean (no uncommitted changes)
- [ ] CI/CD passes (if configured)
- [ ] No merge conflicts

## 🚀 Release Steps

### Step 1: Update Version

1. **Update pyproject.toml**
   ```toml
   [project]
   name = "crypto-manager"
   version = "0.1.0-alpha"  # Update this
   ```

2. **Update CHANGELOG.md**
   ```markdown
   ## [0.1.0-alpha] - 2024-09-30
   
   ### Added
   - New feature X
   - New feature Y
   
   ### Fixed
   - Bug fix Z
   ```

3. **Commit changes**
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "chore: bump version to 0.1.0-alpha"
   git push origin main
   ```

### Step 2: Run Pre-Release Tests

```bash
# Test Bitcoin module
python -m crypto_manager.bitcoin

# Test Ethereum module (requires API key)
python -m crypto_manager.ethereum

# Test Tron module
python -m crypto_manager.tron

# Test exchange rates
python -m crypto_manager.transactions
```

### Step 3: Configure GitHub Repository

Run the setup script:

```bash
chmod +x scripts/setup-github-repo.sh
./scripts/setup-github-repo.sh
```

Or manually:
1. Go to https://github.com/brendadeeznuts1111/crypto-manager/settings
2. Add description and topics
3. Enable Issues, Discussions, Wiki, Projects

### Step 4: Create Release

#### Option A: Using Script (Recommended)

```bash
# Make script executable
chmod +x scripts/create-release.sh

# Create alpha release
./scripts/create-release.sh v0.1.0-alpha true

# Create stable release (when ready)
./scripts/create-release.sh v1.0.0 false
```

#### Option B: Manual Process

1. **Create and push tag**
   ```bash
   git tag -a v0.1.0-alpha -m "Release v0.1.0-alpha"
   git push origin v0.1.0-alpha
   ```

2. **Create release on GitHub**
   ```bash
   gh release create v0.1.0-alpha \
     --title "Crypto Manager v0.1.0-alpha" \
     --notes-file CHANGELOG.md \
     --prerelease
   ```

   Or manually at: https://github.com/brendadeeznuts1111/crypto-manager/releases/new

### Step 5: Announce Release

1. **GitHub Release**
   - Release is automatically published
   - Subscribers get notifications

2. **Social Media** (optional)
   - Twitter/X: "Released Crypto Manager v0.1.0-alpha! 🎉"
   - Reddit: r/Python, r/CryptoCurrency
   - Dev.to: Write a release article

3. **Community** (optional)
   - Post in GitHub Discussions
   - Update project website
   - Email newsletter

## 🏷️ Release Types

### Alpha Release (0.1.0-alpha)
- **Purpose**: Early testing, feedback gathering
- **Stability**: Unstable, breaking changes expected
- **Audience**: Developers, early adopters
- **Support**: Limited, community-driven
- **Example**: v0.1.0-alpha, v0.2.0-alpha

### Beta Release (0.1.0-beta)
- **Purpose**: Feature complete, bug fixing
- **Stability**: Mostly stable, minor changes possible
- **Audience**: Testers, power users
- **Support**: Bug reports tracked
- **Example**: v0.9.0-beta, v1.0.0-beta.1

### Release Candidate (1.0.0-rc.1)
- **Purpose**: Final testing before stable
- **Stability**: Stable, no new features
- **Audience**: Everyone
- **Support**: Full support
- **Example**: v1.0.0-rc.1, v1.0.0-rc.2

### Stable Release (1.0.0)
- **Purpose**: Production-ready
- **Stability**: Fully stable
- **Audience**: Everyone, production use
- **Support**: Full support, LTS
- **Example**: v1.0.0, v1.2.3

## 📊 Post-Release Tasks

### Immediate (Same Day)
- [ ] Verify release on GitHub
- [ ] Test installation from release tarball
- [ ] Monitor for issues
- [ ] Update project board

### Short-term (Within Week)
- [ ] Gather user feedback
- [ ] Triage new issues
- [ ] Update roadmap
- [ ] Start next version planning

### Long-term (Within Month)
- [ ] Analyze usage metrics
- [ ] Write blog post/tutorial
- [ ] Update dependencies
- [ ] Plan next release

## 🔄 Version Progression Example

```
0.1.0-alpha   → Initial alpha release
0.1.0-alpha.2 → Bug fixes in alpha
0.1.0-beta    → Move to beta
0.1.0-beta.2  → More testing
0.1.0-rc.1    → Release candidate
0.1.0         → Stable release
0.1.1         → Patch release
0.2.0         → Minor release (new features)
1.0.0         → Major release (breaking changes)
```

## 🐛 Hotfix Process

For critical bugs in released versions:

1. **Create hotfix branch**
   ```bash
   git checkout -b hotfix/0.1.1 v0.1.0
   ```

2. **Fix the bug**
   ```bash
   # Make fixes
   git add .
   git commit -m "fix: critical security issue in transaction parsing"
   ```

3. **Update version**
   - Update pyproject.toml to 0.1.1
   - Add entry to CHANGELOG.md

4. **Create release**
   ```bash
   git push origin hotfix/0.1.1
   ./scripts/create-release.sh v0.1.1 false
   ```

5. **Merge back**
   ```bash
   git checkout main
   git merge hotfix/0.1.1
   git push origin main
   ```

## 📝 Release Checklist Template

Copy this for each release:

```markdown
## Release v0.1.0-alpha Checklist

### Pre-Release
- [ ] Update version in pyproject.toml
- [ ] Update CHANGELOG.md
- [ ] Test all modules
- [ ] Update documentation
- [ ] Review open issues
- [ ] Check dependencies

### Release
- [ ] Commit version changes
- [ ] Run setup-github-repo.sh
- [ ] Run create-release.sh
- [ ] Verify release on GitHub
- [ ] Test download/install

### Post-Release
- [ ] Announce on social media
- [ ] Update project board
- [ ] Monitor issues
- [ ] Gather feedback
```

## 🔐 Security Releases

For security vulnerabilities:

1. **Do NOT create public issue**
2. Use GitHub Security Advisories
3. Fix in private
4. Coordinate disclosure
5. Release with security notice
6. Update all affected versions

## 📚 Additional Resources

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Python Packaging](https://packaging.python.org/)

---

**Questions?** Open an issue or discussion on GitHub!

