# Contributing to ContentMultiplier

Thank you for your interest in contributing to ContentMultiplier! This document provides guidelines for contributing.

## How Can I Contribute?

### Reporting Bugs
- Check if the bug is already reported in [Issues](https://github.com/ferdinands-molt-bot/money-maker/issues)
- If not, create a new issue with:
  - Clear title and description
  - Steps to reproduce
  - Expected vs actual behavior
  - Screenshots if applicable

### Suggesting Features
- Open an issue with the "feature request" label
- Describe the feature and its use case
- Explain why it would be valuable

### Code Contributions

#### Setting Up Development Environment

```bash
# 1. Fork the repository
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/money-maker.git
cd money-maker

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python app.py
```

#### Making Changes

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
3. Test thoroughly
4. Commit with clear messages:
```bash
git commit -m "Add: feature description"
```

5. Push and create Pull Request:
```bash
git push origin feature/your-feature-name
```

### Commit Message Convention

Use prefixes for clarity:
- `Add:` - New feature
- `Fix:` - Bug fix
- `Update:` - Modification to existing feature
- `Docs:` - Documentation changes
- `Refactor:` - Code refactoring
- `Test:` - Test additions/changes

Examples:
```
Add: TikTok script generation support
Fix: Character count calculation for Twitter
Update: Improve LinkedIn post formatting
Docs: Add API authentication examples
```

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Write docstrings for functions

### Testing

- Write tests for new features
- Ensure existing tests pass
- Test on multiple platforms if possible

## Areas We Need Help With

### High Priority
- [ ] Real AI integration (OpenAI/Claude)
- [ ] User authentication system
- [ ] Payment integration (Stripe)
- [ ] Mobile responsiveness improvements

### Medium Priority
- [ ] Additional platform support (TikTok, Pinterest)
- [ ] More tone/style options
- [ ] Language translations
- [ ] Chrome extension

### Low Priority (But Welcome!)
- [ ] UI/UX improvements
- [ ] Documentation improvements
- [ ] Performance optimizations
- [ ] Marketing materials

## Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Added to "Contributors" page (coming soon)

## Questions?

- Open an issue for questions
- Email: contribute@contentmultiplier.com

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards others

Thank you for contributing! 🚀
