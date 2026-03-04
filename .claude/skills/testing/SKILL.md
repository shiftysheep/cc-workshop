---
name: testing
description: MUST BE USED when writing tests, planning test strategy, or evaluating coverage
---

# Testing Skill

## When to Use

Load this skill when writing tests, planning test strategy, evaluating coverage, or
following TDD methodology during implementation. Applied by the implementation agent
and referenced by the validation agent when assessing test quality.

## TDD Methodology: Red-Green-Refactor

1. **Red**: Write a failing test that describes the desired behavior
2. **Green**: Write the minimal code to make the test pass
3. **Refactor**: Improve the code while keeping tests green

Never write implementation code before a failing test exists.

## Running Tests

```bash
uv run pytest                          # run all tests
uv run pytest tests/test_foo.py       # run specific file
uv run pytest -k "test_name"          # run by name pattern
uv run pytest --cov=src               # with coverage
uv run pytest -v                       # verbose output
```

## Test File Conventions

- Test files: `tests/test_<module>.py` (mirrors `src/<module>.py`)
- Test functions: `test_<behavior_being_tested>()`
- Test classes: `Test<ClassName>` (only when grouping related tests)

## Pytest Best Practices

- **Fixtures over setup/teardown**: Use `@pytest.fixture` for test dependencies
- **Parametrize for variants**: Use `@pytest.mark.parametrize` for multiple input cases
- **Mock external calls only**: Only mock at system boundaries (HTTP, DB, filesystem, time)
- **One assertion per logical concept**: Multiple asserts are fine if testing one thing
- **Descriptive test names**: `test_user_creation_fails_with_duplicate_email`

## Coverage Requirements

- New code must have tests
- Aim for meaningful coverage, not 100% line coverage
- Focus on behavior coverage: happy paths, edge cases, error conditions

## Example Test Structure

```python
import pytest
from src.module import function_under_test


@pytest.fixture
def sample_data():
    return {"key": "value"}


def test_function_returns_expected_result(sample_data):
    result = function_under_test(sample_data)
    assert result == expected_value


@pytest.mark.parametrize("input,expected", [
    ("case1", "result1"),
    ("case2", "result2"),
])
def test_function_handles_variants(input, expected):
    assert function_under_test(input) == expected
```

## Related

- **code-review** — tests are a core code review dimension; use code-review skill for severity classification when evaluating test quality
- **documentation-standards** — test files follow the same naming conventions; fixture and coverage documentation follows frontmatter standards
