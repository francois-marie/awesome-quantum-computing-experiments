# Contributing Guide

Thank you for your interest in contributing to the Awesome Quantum Computing Experiments project! This document provides guidelines and instructions for contributions.

## Types of Contributions

### 1. Adding New Experiments

To add new experiments to the database:

1. Identify the appropriate CSV file in the `data/` directory
2. Add a new row with the following information:
   - Article Title
   - Link (preferably arXiv or DOI)
   - Year
   - Platform
   - Relevant measurements
   - Any additional notes

#### Data Quality Guidelines

- Use consistent platform names
- Include full article titles
- Use standardized format for code parameters (e.g., `[[n,k,d]]`)
- Provide source links that are stable and accessible
- Include relevant notes for special cases or important details

### 2. Code Contributions

1. Fork the repository
2. Create a new branch for your feature
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

#### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Include docstrings for all functions and classes
- Add comments for complex logic

### 3. Documentation

Help improve our documentation by:
- Fixing typos or unclear explanations
- Adding examples
- Improving installation or usage instructions
- Adding tutorials

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/francois-marie/awesome-quantum-computing-experiments.git
cd awesome-quantum-computing-experiments
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[test]"  # Install package and test dependencies
```

4. Run tests to verify setup:
```bash
make test
```

## Pull Request Process

1. Update documentation for any new features
2. Add tests for new functionality
3. Update the README.md if needed
4. Ensure all tests pass
5. Submit a pull request with a clear description of changes

## Data Validation

Before submitting new data:
1. Verify all required fields are present
2. Check for consistent formatting
3. Validate links are accessible
4. Ensure platform names match existing conventions

## Questions?

If you have questions about contributing:
1. Check existing issues
2. Create a new issue for discussion
3. Tag with appropriate labels
