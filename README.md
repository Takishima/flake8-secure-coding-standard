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
| SCS107 | Use of debugging code should not be present in production code (e.g. `import pdb`)                            |
| SCS108 | `assert` statements should not be present in production code                                                  |
| SCS109 | Use of builtin `open` for writing is discouraged in favor of `os.open` to allow for setting file permissions  |
| SCS110 | Avoid using `os.popen()` as it internally uses `subprocess.Popen` with `shell=True`                           |
| SCS111 | Use of `shlex.quote()` should be avoided on non-POSIX platforms                                               |
| SCS112 | Avoid using `os.open()` with unsafe file permissions                                                          |
| SCS113 | Avoid using `pickle.load()` and `pickle.loads()`                                                              |
| SCS114 | Avoid using `marshal.load()` and `marshal.loads()`                                                            |
| SCS115 | Avoid using `shelve.open()`                                                                                   |
| SCS116 | Avoid using `os.mkdir` and `os.makedirs` with unsafe file permissions                                         |
| SCS117 | Avoid using `os.mkfifo` with unsafe file permissions                                                          |
| SCS118 | Avoid using `os.mknod` with unsafe file permissions                                                           |
| SCS119 | Avoid using `os.chmod` with unsafe file permissions (W ^ X for group and others)                              |


### Mode-like options

Mode-like options are configuration options for errors/warnings that relate to some function that accepts a `mode`
parameter (or similar) that control some file or directory permissions. This is typically valid for the followiing
warnings (corresponding command-line option name in parentheses):

- SCS112 (`os-open-mode`)
- SCS116 (`os-mkdir-mode`)
- SCS117 (`os-mkfifo-mode`)
- SCS118 (`os-mknod-mode`)

Since these warnings can be quite disruptive, they are turned off by default.

For those kind of options, the plugin understands a variety of values that must be specified as `string`. They will then
be parsed into a list of allowed mode values:

- Any positive, non-zero (octal or decimal) integer value specifies the maximum value for the mode value
- A comma-separated list of (octal or decimal) integers indicates the list of allowed mode values
- 'y', 'yes', 'true' (case-insensitive) will turn on the warnings using the default value of `0o755`
- 'n', 'no', 'false' (case-insensitive) will turn off the warnings

Example of values:
```toml
    [flake8]
    os-open-mode = '0'            # check disabled
    os-open-mode = 'no'           # check disabled
    os-open-mode = '493'          # all modes from 0 to 493 (=0o755)
    os-open-mode = '0o755'        # all modes from 0 to 0o755
    os-open-mode = '0o755,'       # only 0o755 (notice the comma)
    os-open-mode = '0o644,0o755'  # only 0o644 and 0o755
```

You can also specify those options directly on the command line:

```sh
python3 -m flake8 --os-open-mode='0o755'
```

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
