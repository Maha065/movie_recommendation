# Contributing to Movie Recommendation API

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/repo.git`
3. Create a branch: `git checkout -b feature/amazing-feature`
4. Make changes and test
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Development Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

## Code Standards

- Follow PEP 8
- Use Black for formatting
- Use isort for imports
- Add tests for new features
- Update documentation

## Testing
```bash
pytest
pytest --cov=movies
```

## Commit Messages

- Use present tense
- Be descriptive
- Reference issues: "Fixes #123"
- Examples:
  - `Add trending movies endpoint`
  - `Fix caching bug in recommendations`
  - `Update API documentation`

## Pull Request Process

1. Update README.md if needed
2. Add tests for new features
3. Ensure tests pass: `pytest`
4. Keep PR focused on one feature
5. Update CHANGELOG.md

## Questions?

Open a discussion or issue on GitHub.
