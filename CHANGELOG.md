# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v1.4.0] - 2023-02-06

### Changed

-   Changed minimum Python version to 3.8.X
-   Add support for flake8 6.0.0+

### Updated

-   Update GitHub release publishing workflow
-   Added some more pre-commit hooks:
    -   doc8
    -   codespell
    -   yamllint
    -   blacken-docs
    -   pyupgrade

### Repository

-   Remove soon to be deprecated `version` in GitHub workflows
-   Update `thomaseizinger/keep-a-changelog-new-release` GitHub action to v1.3.0
-   Update `Lucas-C/pre-commit-hooks` hook to v1.4.2
-   Update `asottile/pyupgrade` to v3.2.0
-   Update `black` hook to v22.12.0
-   Update `blacken-docs` hook to v1.13.0
-   Update `codespell` hook to v2.2.2
-   Update `flake8` hook to v5.0.4
-   Update `isort` hook to v5.12.0
-   Update `pre-commit/mirrors-pylint` to v3.0.0a5
-   Update `pre-commit/pre-commit-hooks` to v4.4.0
-   Update `pyupgrade` hook to v3.3.1
-   Update `yamllint` hook to v1.29.0

## [1.3.0] - 2022-06-02

### Added

-   Added SCS112 to avoid using `os.open()` with unsafe permissions
-   Added SCS113 to avoid using `pickle.load()` and `pickle.loads()`
-   Added SCS114 to avoid using `marshal.load()` and `marshal.loads()`
-   Added SCS115 to avoid using `shelve.open()`
-   Added SCS116 to avoid using `os.mkdir` and `os.makedirs` with unsafe file permissions
-   Added SCS117 to avoid using `os.mkfifo` with unsafe file permissions
-   Added SCS118 to avoid using `os.mknod` with unsafe file permissions
-   Added SCS119 to avoid using `os.chmod` with unsafe file permissions (W ^ X for group and others)

### Fixed

-   Fix typos found by `codespell`
-   Fix issues discovered by `yamllint`

### Repository

-   Add Python 3.10 to the list of configurations for testing
-   Add `codespell` pre-commit hook
-   Add `yamllint` configuration file and pre-commit hook

## [1.2.2] - 2022-05-24

### Updated

-   Update GitHub release publishing workflow

### Fixed

-   Fix issue with recognizing YAML load function calls (thanks to [@D-Bhatta](https://github.com/D-Bhatta))

### Repository

-   Update `dangoslen/changelog-enforcer` GitHub action to v3
-   Update `isort` hook to v5.10.1
-   Update `black` hook to v22.3.0
-   Update `check-manifest` hook to v0.48
-   Update `flake8` hook to v4.0.1
-   Update `Lucas-C/pre-commit-hooks` hook to v1.2.0
-   Update `pre-commit/pre-commit-hooks` to v4.2.0
-   Update `thomaseizinger/create-pull-request` GitHub action to v1.2.2
-   Update `thomaseizinger/keep-a-changelog-new-release` GitHub action to v1.3.0
-   Update GitHub's CodeQL action to v2

## [1.2.1] - 2021-07-19

-   Reworded SCS103 and extend it to include a few more cases:
    -   `subprocess.getoutput()`
    -   `subprocess.getstatusoutput()`
    -   `asyncio.create_subprocess_shell()`
    -   `loop.subprocess_shell()`

## [1.2.0] - 2021-07-19

-   Added SCS110 to avoid using `os.popen()` as it internally uses `subprocess.Popen` with `shell=True`
-   Added SCS111 to avoid using `shlex.quote()` on non-POSIX platforms.

## [1.1.0] - 2021-07-02

### Added

-   Added SCS109 to prefer `os.open()` to the builtin `open` when in writing mode

### Repository

-   Update pre-commit configuration

## [1.0.1] - 2021-06-21

### Updated

-   Updated error messages to be more in line with README
-   Updated README

## [1.0.0] - 2021-06-20

Initial release

[Unreleased]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.4.0...HEAD

[v1.4.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.3.0...v1.4.0

[1.3.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.2.2...v1.3.0

[1.2.2]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.2.1...v1.2.2

[1.2.1]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.2.0...v1.2.1

[1.2.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.1.0...v1.2.0

[1.1.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.0.1...v1.1.0

[1.0.1]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.0.0...v1.0.1

[1.0.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/c18cc7130a40405bd92e49b22675e8ddbe0bc8cd...v1.0.0
