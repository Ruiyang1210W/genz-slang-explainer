# Contributing to Gen Z Slang Explainer

Thank you for your interest in contributing to the Gen Z Slang Explainer project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- Clear description of the enhancement
- Use cases and benefits
- Potential implementation approach (if you have ideas)

### Adding New Slang Terms

To add new slang terms to the knowledge base:

1. Fork the repository
2. Add entries to `api/data/slang_pairs.jsonl` in the format:
   ```json
   {"term": "example", "definition": "The definition", "example": "Usage example"}
   ```
3. Submit a pull request

### Code Contributions

#### Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/yourusername/genz-slang-explainer.git
   cd genz-slang-explainer
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Code Standards

- Follow PEP 8 style guide
- Use Black for code formatting: `black api/src api/tests`
- Use Ruff for linting: `ruff check api/src api/tests`
- Add type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions focused and concise

#### Testing

- Write tests for all new features
- Ensure all tests pass: `pytest`
- Maintain or improve code coverage
- Run tests before submitting PR:
  ```bash
  cd api
  pytest --cov=src --cov-report=term-missing
  ```

#### Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Run code formatting and linting
5. Update CHANGELOG.md (if applicable)
6. Create a pull request with:
   - Clear title and description
   - Reference to related issues
   - Summary of changes
   - Screenshots/examples (if applicable)

### Commit Messages

Write clear, concise commit messages:
- Use present tense ("Add feature" not "Added feature")
- Start with a verb ("Fix", "Add", "Update", "Remove")
- Keep first line under 50 characters
- Add detailed description if needed

Examples:
```
Add support for multi-word slang terms

Update README with Docker deployment instructions

Fix parsing issue with special characters
```

## Development Workflow

1. **Check existing issues** - Someone might already be working on it
2. **Create an issue** - Discuss major changes before implementing
3. **Fork and branch** - Create a feature branch from `main`
4. **Develop** - Write code, tests, and documentation
5. **Test** - Run all tests and linters
6. **Submit PR** - Create a pull request for review
7. **Address feedback** - Make requested changes
8. **Merge** - Maintainers will merge when ready

## Project Structure

```
genz-slang-explainer/
├── api/                    # FastAPI service
│   ├── src/               # Source code
│   ├── tests/             # Unit tests
│   └── data/              # Knowledge base
├── models/                # Model adapters
├── training/              # Training code and data
└── demo/                  # Demo scripts
```

## Questions?

If you have questions, feel free to:
- Open an issue with the "question" label
- Reach out via email (see README for contact info)

Thank you for contributing!
