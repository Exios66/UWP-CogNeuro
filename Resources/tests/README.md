# Tests

This directory contains test suites for validating the functionality of the Cognitive Neuroscience Organization's codebase.

## Test Structure

The tests are organized into two main categories:

- **Unit Tests**: Tests for individual functions and classes
- **Integration Tests**: Tests for interactions between different components

## Running Tests

We use [pytest](https://docs.pytest.org/) as our testing framework. To run the tests:

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_preprocessing.py

# Run tests with coverage report
pytest --cov=cog_neuro
```

## Writing Tests

When writing new tests, please follow these guidelines:

1. **Test Organization**: Place unit tests in the `unit` directory and integration tests in the `integration` directory
2. **Naming Convention**: Name test files with the prefix `test_` and test functions with the prefix `test_`
3. **Test Coverage**: Aim for comprehensive test coverage of all functionality
4. **Test Data**: Use small, synthetic datasets for testing when possible
5. **Fixtures**: Use pytest fixtures for setup and teardown

## Continuous Integration

Our tests are automatically run on all pull requests and commits to the main branch using GitHub Actions. The configuration for these workflows can be found in the `.github/workflows` directory.
