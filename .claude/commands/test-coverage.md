# /test-coverage - Test Coverage Analysis

Generate comprehensive test coverage report and identify gaps in the Unipress project.

## Usage

```
/test-coverage
```

## Implementation

1. **Install coverage if needed**
   ```bash
   uv add --dev coverage
   ```

2. **Run tests with coverage**
   ```bash
   echo "🧪 Running tests with coverage analysis..."
   uv run coverage run -m pytest
   ```

3. **Generate coverage report**
   ```bash
   echo "📊 Generating coverage report..."
   uv run coverage report --show-missing
   ```

4. **Generate HTML report**
   ```bash
   echo "🌐 Generating HTML coverage report..."
   uv run coverage html
   echo "HTML report available at: htmlcov/index.html"
   ```

5. **Coverage summary**
   ```bash
   echo "📈 Coverage Summary:"
   uv run coverage report --format=total
   ```

## Critical Gap Analysis

Based on TODO.md Priority 1 requirements:

**Current Status**: ~15% coverage (3 tests for 19 Python files)
**Target**: 80%+ coverage
**Gap**: 65% coverage improvement needed

### Missing Test Areas
- [ ] BaseGame class (core/base_game.py)
- [ ] Settings system (core/settings.py)
- [ ] SoundManager (core/sound.py)
- [ ] AssetManager (core/assets.py)
- [ ] HighScores system (core/high_scores.py)
- [ ] Messages/i18n (core/messages.py)
- [ ] Logger system (core/logger.py)
- [ ] Game server (core/game_server.py)
- [ ] Individual games (games/*/game.py)

## Recommendations

1. **Priority Order**: Start with core systems (BaseGame, Settings, Sound)
2. **Test Types**: Unit tests, integration tests, mocking
3. **Automation**: Add coverage to CI/CD pipeline
4. **Badges**: Add coverage badge to README.md

## Integration

- Essential for Priority 1 TODO.md completion
- Required before public release
- Part of professional development standards