# Flake8 Secure Coding Standard Plugin

[![PyPI version](https://badge.fury.io/py/flake8-secure-coding-standard.svg)](https://badge.fury.io/py/flake8-secure-coding-standard) ![CI Build](https://github.com/Takishima/flake8-secure-coding-standard/actions/workflows/ci.yml/badge.svg) ![CodeQL](https://github.com/Takishima/flake8-secure-coding-standard/actions/workflows/codeql-analysis.yml/badge.svg)

flake8 plugin that enforces some secure coding standards.

## Installation

    pip install flake8-secure-coding-standard

## Flake8 codes

| Code   | Description                                                                                              |
|--------|----------------------------------------------------------------------------------------------------------|
| SCS100 | Use of `os.path.abspath()` and `os.path.relpath()` should be avoided in favor of `os.path.realpath()`    |
| SCS101 | Use of `eval()` and `exec()` represent a security risk and should be avoided                             |
| SCS102 | Use of `os.system()` should be avoided                                                                   |
| SCS103 | Use of `shell=True` in subprocess functions should be avoided                                            |
| SCS104 | Use of `tempfile.mktemp()` should be avoided, prefer `tempfile.mkstemp()`                                |
| SCS105 | Use of `yaml.load()` should be avoided, prefer `yaml.safe_load()` or `yaml.load(xxx, Loader=SafeLoader)` |
| SCS106 | Use of `jsonpickle.decode()` should be avoided                                                           |
| SCS107 | Use of debugging code shoud not be present in production code (e.g. `import pdb`)                        |
| SCS108 | `assert` statements should not be present in production code                                             |

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
