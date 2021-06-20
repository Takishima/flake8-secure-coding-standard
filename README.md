# Flake8 Secure Coding Standard Plugin

flake8 plugin that enforces some secure coding standards.

## Installation

    pip install flake8-secure-coding-standard

## Flake8 codes

| Code   | Description |
|--------|-------------|
| SCS100 | Blablabla   |

## Rationale

Enforce certain coding practices that aim at making Python code safer.

### First

Avoid
```python
```
in favor of
```python
```

## Pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://gitlab.com/pycqa/flake8
    rev: 3.7.8
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-secure-coding-standard]
```
