# 🧪 Testing Guide

Comprehensive test suite for Crypto Manager.

## 📋 Test Structure

```
tests/
├── __init__.py
├── test_bitcoin.py          # Bitcoin module tests
├── test_ethereum.py         # Ethereum module tests
├── test_ltc_doge.py         # Litecoin & Dogecoin tests
├── test_transactions.py     # Exchange rate tests
├── test_config.py           # Configuration tests
├── test_integration.py      # Integration tests (real API calls)
└── README.md               # This file
```

## 🚀 Running Tests

### Run All Unit Tests

```bash
# Using Python's unittest
python -m unittest discover tests

# Using pytest (if installed)
pytest tests/

# With coverage
pip install pytest-cov
pytest tests/ --cov=crypto_manager --cov-report=html
```

### Run Specific Test Files

```bash
# Test Bitcoin module only
python -m unittest tests.test_bitcoin

# Test Ethereum module only
python -m unittest tests.test_ethereum

# Test LTC/DOGE modules
python -m unittest tests.test_ltc_doge
```

### Run Specific Test Classes

```bash
# Test Bitcoin constants only
python -m unittest tests.test_bitcoin.TestBitcoinConstants

# Test proxy configuration
python -m unittest tests.test_bitcoin.TestProxyUrlFor
```

### Run Integration Tests

Integration tests make real API calls and are disabled by default.

```bash
# Enable and run integration tests
export CRYPTO_MANAGER_RUN_INTEGRATION_TESTS=1
python -m unittest tests.test_integration
```

## 📊 Test Coverage

Current test coverage by module:

| Module | Coverage | Tests |
|--------|----------|-------|
| bitcoin.py | ~70% | 15+ tests |
| ethereum.py | ~65% | 12+ tests |
| ltc.py | ~60% | 6+ tests |
| doge.py | ~60% | 6+ tests |
| transactions.py | ~75% | 8+ tests |
| config.py | ~80% | 2+ tests |

**Total: 49+ test cases**

## 🎯 Test Types

### Unit Tests
Mock external API calls to test internal logic:
- ✅ Constants validation
- ✅ Function logic
- ✅ Error handling
- ✅ Data parsing

### Integration Tests
Make real API calls (disabled by default):
- ✅ Bitcoin API integration
- ✅ Exchange rate APIs
- ✅ Module imports

### Smoke Tests
Quick sanity checks:
- ✅ All modules import correctly
- ✅ Constants have correct values
- ✅ Functions exist

## 💡 Writing New Tests

### Example Unit Test

```python
import unittest
from unittest.mock import patch, MagicMock

from crypto_manager import bitcoin


class TestMyFeature(unittest.TestCase):
    """Test my new feature."""
    
    @patch('crypto_manager.bitcoin.requests.get')
    def test_feature(self, mock_get):
        """Test that feature works correctly."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response
        
        # Act
        result = bitcoin.my_function()
        
        # Assert
        self.assertEqual(result, "expected")
```

### Example Integration Test

```python
import unittest
import os

from crypto_manager import bitcoin


@unittest.skipUnless(
    os.getenv("CRYPTO_MANAGER_RUN_INTEGRATION_TESTS") == "1",
    "Integration tests disabled"
)
class TestFeatureIntegration(unittest.TestCase):
    """Integration test for feature."""
    
    def test_real_api_call(self):
        """Test with real API."""
        result = bitcoin.get_account_info("real_address")
        self.assertIsNotNone(result)
```

## 🐛 Debugging Tests

### Verbose Output

```bash
# Show all test names
python -m unittest discover tests -v

# Show even more detail
python -m unittest discover tests -v -v
```

### Run Failed Tests Only

```bash
# Using pytest
pytest tests/ --lf  # Last failed
pytest tests/ --ff  # Failed first
```

### Debug Single Test

```python
# Add to test method
import pdb; pdb.set_trace()

# Or use pytest
pytest tests/test_bitcoin.py::TestBitcoinConstants::test_one_btc_value -s
```

## 📝 Test Best Practices

### ✅ DO:
- Write descriptive test names
- Test one thing per test
- Use mocks for external APIs
- Clean up resources in tearDown
- Add docstrings to test methods
- Test both success and failure cases

### ❌ DON'T:
- Make real API calls in unit tests
- Have tests depend on each other
- Use hardcoded values without explanation
- Ignore test failures
- Skip writing tests for complex logic

## 🔧 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - run: pip install -r requirements.txt
    - run: python -m unittest discover tests
```

## 📊 Coverage Reports

### Generate HTML Coverage Report

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run -m unittest discover tests

# Generate HTML report
coverage html

# Open report
open htmlcov/index.html
```

### Coverage Targets

- **Current**: ~68% overall coverage
- **Target**: 80% coverage for stable release
- **Minimum**: 70% for new features

## 🚨 Common Issues

### Issue: Tests fail with API rate limits
**Solution**: Use mocks for unit tests, run integration tests sparingly

### Issue: Import errors
**Solution**: Ensure crypto_manager is in PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: Tests pass locally but fail in CI
**Solution**: Check for hardcoded paths, environment variables, or timezone issues

## 📚 Additional Resources

- [Python unittest docs](https://docs.python.org/3/library/unittest.html)
- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock guide](https://docs.python.org/3/library/unittest.mock.html)

---

**Happy Testing!** 🧪✨

