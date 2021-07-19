# Flake8 Secure Coding Standard Plugin

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-secure-coding-standard?label=Python) [![PyPI version](https://badge.fury.io/py/flake8-secure-coding-standard.svg)](https://badge.fury.io/py/flake8-secure-coding-standard) [![CI Build](https://github.com/Takishima/flake8-secure-coding-standard/actions/workflows/ci.yml/badge.svg)](https://github.com/Takishima/flake8-secure-coding-standard/actions/workflows/ci.yml) [![CodeQL](https://github.com/Takishima/flake8-secure-coding-standard/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Takishima/flake8-secure-coding-standard/actions/workflows/codeql-analysis.yml) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Takishima/flake8-secure-coding-standard/main.svg)](https://results.pre-commit.ci/latest/github/Takishima/flake8-secure-coding-standard/main) [![Coverage Status](https://coveralls.io/repos/github/Takishima/flake8-secure-coding-standard/badge.svg?branch=main)](https://coveralls.io/github/Takishima/flake8-secure-coding-standard?branch=main)


flake8 plugin that enforces some secure coding standards.

## Installation

    pip install flake8-secure-coding-standard

## Flake8 codes

| Code   | Description                                                                                                   |
|--------|---------------------------------------------------------------------------------------------------------------|
| SCS100 | Use of `os.path.abspath()` and `os.path.relpath()` should be avoided in favor of `os.path.realpath()`         |
| SCS101 | Use of `eval()` and `exec()` represent a security risk and should be avoided                                  |
| SCS102 | Use of `os.system()` should be avoided                                                                        |
| SCS103 | Use of `shell=True` in subprocess functions or use of functions that internally set this should be avoided    |
| SCS104 | Use of `tempfile.mktemp()` should be avoided, prefer `tempfile.mkstemp()`                                     |
| SCS105 | Use of `yaml.load()` should be avoided, prefer `yaml.safe_load()` or `yaml.load(xxx, Loader=SafeLoader)`      |
| SCS106 | Use of `jsonpickle.decode()` should be avoided                                                                |
| SCS107 | Use of debugging code shoud not be present in production code (e.g. `import pdb`)                             |
| SCS108 | `assert` statements should not be present in production code                                                  |
| SCS109 | Use of builtin `open` for writing is discouraged in favor of `os.open` to allow for setting file permissions  |
| SCS110 | Avoid using `os.popen()` as it internally uses `subprocess.Popen` with `shell=True`                           |
| SCS111 | Use of `shlex.quote()` should be avoided on non-POSIX platforms                                               |

## Pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/PyCQA/flake8g
    rev: 3.7.8
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-secure-coding-standard]
```
