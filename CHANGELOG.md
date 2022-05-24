# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.2.2...HEAD

[1.2.2]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.2.1...v1.2.2

[1.2.1]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.2.0...v1.2.1

[1.2.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.1.0...v1.2.0

[1.1.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.0.1...v1.1.0

[1.0.1]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.0.0...v1.0.1

[1.0.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/c18cc7130a40405bd92e49b22675e8ddbe0bc8cd...v1.0.0
