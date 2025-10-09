# 🤝 Contributing to Spaceflights

Thank you for your interest in contributing to Spaceflights! This document provides guidelines for contributing to this MLOps template project.

## 📋 Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR-USERNAME/spaceflights.git
cd spaceflights
```

### 2. Set Up Development Environment

```bash
# Start development environment
./start.sh development

# Or local setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Development Guidelines

### Code Style

- **Python**: Follow PEP 8
- **Line length**: 88 characters (Black formatter)
- **Docstrings**: Google style
- **Type hints**: Use for function signatures

### Linting

```bash
# Run linter
docker-compose exec jupyter-lab ruff check src/

# Auto-fix
docker-compose exec jupyter-lab ruff check --fix src/

# Format code
docker-compose exec jupyter-lab ruff format src/
```

### Testing

```bash
# Run all tests
docker-compose exec jupyter-lab pytest

# With coverage
docker-compose exec jupyter-lab pytest --cov=src/spaceflights

# Specific test
docker-compose exec jupyter-lab pytest tests/pipelines/data_science/
```

### Documentation

- Update relevant docs/ files
- Add docstrings to new functions
- Update README.md if adding major features
- Include examples in documentation

## 🔄 Contribution Workflow

### 1. Make Changes

- Write clear, focused code
- Follow existing code patterns
- Add tests for new features
- Update documentation

### 2. Test Your Changes

```bash
# Run tests
pytest

# Check linting
ruff check src/

# Test Docker build
docker-compose build

# Test pipeline execution
kedro run
```

### 3. Commit Changes

Use conventional commit messages:

```bash
git commit -m "feat: add new data validation pipeline"
git commit -m "fix: correct date parsing in preprocessing"
git commit -m "docs: update setup guide with new requirements"
git commit -m "test: add tests for model training"
```

#### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### 4. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference to related issues
- List of changes
- Screenshots (if UI changes)

## 📌 Pull Request Guidelines

### PR Title

Use conventional commit format:
```
feat: add data validation pipeline
fix: resolve date parsing issue
docs: improve Docker setup guide
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Docker build succeeds

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)
```

## 🎯 Areas for Contribution

### Priority Areas

- **Documentation**: Improve guides and examples
- **Testing**: Increase test coverage
- **Pipelines**: Add new example pipelines
- **Integrations**: Add new tool integrations
- **Examples**: Add Jupyter notebooks with examples

### Feature Requests

Open an issue first to discuss:
- Describe the feature
- Explain use case
- Propose implementation

### Bug Reports

Include:
- Error message
- Steps to reproduce
- Expected vs actual behavior
- System information
- Docker/Kedro versions

## 🧪 Testing Guidelines

### Unit Tests

```python
# tests/pipelines/data_processing/test_nodes.py
def test_preprocess_companies():
    # Arrange
    input_data = pd.DataFrame(...)
    
    # Act
    result = preprocess_companies(input_data)
    
    # Assert
    assert result.shape == (10, 5)
    assert "company_name" in result.columns
```

### Integration Tests

```python
# tests/test_pipeline.py
def test_full_pipeline_execution():
    with KedroSession.create() as session:
        session.run()
    # Verify outputs exist
```

### Test Coverage

- Minimum 70% coverage for new code
- 100% for critical functions
- Add tests for edge cases

## 📚 Documentation Guidelines

### Markdown Files

- Use clear headings
- Include code examples
- Add diagrams where helpful
- Keep language simple and clear

### Code Documentation

```python
def preprocess_companies(companies: pd.DataFrame) -> pd.DataFrame:
    """Preprocesses raw company data.
    
    Removes rows with missing values and standardizes
    company names for consistency.
    
    Args:
        companies: Raw company data with columns:
            - name: Company name
            - iata_approved: Boolean approval status
            
    Returns:
        Cleaned company data with standardized names.
        
    Example:
        >>> df = pd.DataFrame({"name": ["SpaceX"], "iata_approved": ["t"]})
        >>> result = preprocess_companies(df)
        >>> result["iata_approved"].dtype
        dtype('bool')
    """
    # Implementation
```

## 🐳 Docker Changes

If modifying Docker configuration:

1. Test build:
   ```bash
   docker-compose build --no-cache
   ```

2. Test all profiles:
   ```bash
   ./start.sh development
   ./start.sh production
   ./start.sh airflow
   ```

3. Document changes in docs/docker.md

## 🔄 Kedro Pipeline Changes

When adding/modifying pipelines:

1. Follow Kedro conventions
2. Add to pipeline_registry.py
3. Update conf/base/catalog.yml
4. Document in docs/pipelines.md
5. Add tests

## ⚙️ Configuration Changes

- Don't hardcode values
- Use parameters in conf/base/parameters*.yml
- Document in relevant docs
- Provide sensible defaults
- Use environment variables for secrets

## 🚫 What Not to Commit

- `.env` file
- `docker-compose.override.yml`
- `data/` directory contents
- `logs/` directory
- `sessions/` directory
- IDE-specific files
- Credentials or secrets

## 📦 Release Process

(For maintainers)

1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Create git tag
4. Push to GitHub
5. Create release notes

## 🎓 For Students

Special considerations for student contributions:

- Learning is the priority
- Ask questions - no question is too basic
- Start with small contributions
- Documentation improvements are valuable
- Share your learning journey

## 💡 Getting Help

- Open an issue for questions
- Check existing documentation
- Review [docs/troubleshooting.md](./docs/troubleshooting.md)
- Ask in discussions

## 🙏 Recognition

Contributors will be:
- Listed in project contributors
- Credited in release notes
- Part of the MLOps community

## 📞 Contact

- GitHub Issues: For bugs and features
- GitHub Discussions: For questions
- Email: [maintainer email]

---

Thank you for contributing to making Spaceflights better! 🚀

