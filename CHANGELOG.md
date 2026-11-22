# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Changes that are not released yet are stored as fragments in the [changelog.d](changelog.d/README.md) directory.

<!-- towncrier release notes start -->

## [v1.5.2](https://github.com/Takishima/flake8-secure-coding-standard/releases/tag/v1.5.2) - 2026-11-22

### Repository

- Add a `breaking` changelog fragment type, which makes the release workflow propose a major version
- Publish releases to PyPI with trusted publishing so that the uploaded files carry provenance attestations

## [v1.5.1](https://github.com/Takishima/flake8-secure-coding-standard/releases/tag/v1.5.1) - 2026-11-22

### Fixed

- Build Python 3 only wheels (`py3-none-any`) instead of universal `py2.py3` ones
- Fix code inside of `with` and `async with` statements not being checked
- Fix crash when the `os-*-mode` options are set in a flake8 configuration file instead of on the command line
- Report `shell=True` (SCS103) for subprocess functions imported with `from subprocess import ...` or through `import subprocess as ...`

### Repository

- Add `AGENTS.md` and `CLAUDE.md` with instructions for AI coding tools
- Allow uploading to PyPI using trusted publishing
- Build the release from the merged commit using `SETUPTOOLS_SCM_PRETEND_VERSION` instead of a temporary Git tag
- Check that pull requests add a changelog fragment and do not edit `CHANGELOG.md` directly (replaces the `dangoslen/changelog-enforcer` GitHub Action)
- Deduce the next version from the changelog fragments when drafting a release (`auto`, `patch`, `minor`, `major` or an explicit, validated version), using a tested script in `.github/scripts/`
- Delete the release branch once the release is published
- Fix the pre-release detection when creating the GitHub release
- Generate the changelog fragments of pre-commit.ci pull requests with a script from this repository, also when pre-commit.ci updates its pull request
- Manage the CHANGELOG with [towncrier](https://towncrier.readthedocs.io): each pull request adds a fragment to `changelog.d/` and the fragments are collected into `CHANGELOG.md` when a release is drafted
- Open the release pull request automatically every Monday if user-facing changes are waiting to be released
- Split the release publishing workflow into separate build, PyPI upload and GitHub release jobs with minimal permissions; the GitHub release is only created once the PyPI upload succeeded
- Use the `peter-evans/create-pull-request`, `softprops/action-gh-release` and `taiki-e/install-action` GitHub Actions in the release workflows (replacing `stefanzweifel/git-auto-commit-action`, `thomaseizinger/create-pull-request` and hand-written shell code)

## [v1.5.0] - 2026-11-21

### Changed

- Drop support for Python 3.8 and 3.9 (both end-of-life); Python 3.10 is now the minimum version

### Fixed

- Support for Python 3.14 (removed usage of `ast.Str` and `ast.Num`)

### Repository

- Update `action/setup-python` GitHub Action to v7
- Update `action/checkout` GitHub Action to v7
- Update GitHub Action `thomaseizinger/create-pull-request` to v1.4.0
- Update GitHub Action `stefanzweifel/git-auto-commit-action` to v7
- Update GitHub Action `EndBug/add-and-commit` to v11
- Update GitHub Action `github/codeql-action` to v4
- Run CI for Python 3.10 to 3.15 on all platforms (Python 3.8 and 3.9 are not available on `ubuntu-latest` anymore)
- Upload coverage data using the `coverallsapp/github-action` GitHub Action
- Group Dependabot updates into a single pull request and do not require a CHANGELOG entry for them
- Pass GitHub event data to workflow scripts through environment variables
- Fix the CHANGELOG parsing check on release pull requests (strip the leading `v` from the version)
- Update `adrienverge/yamllint.git` hook to v1.38.0
- Update `astral-sh/ruff-pre-commit` hook to v0.17.5
- Update `codespell-project/codespell` hook to v2.4.3
- Update `Lucas-C/pre-commit-hooks` hook to v1.5.6
- Update `pre-commit/pre-commit-hooks` hook to v6.0.0
- Remove the `doc8` and `blacken-docs` hooks (no reStructuredText files or Python code blocks to check)
- Rename the `ruff` hook to `ruff-check` and run it before `ruff-format`
- Move the ruff linter settings to the `lint` section, target Python 3.10 and drop removed rules

## [v1.4.1] - 2024-01-07

### Changed

- Bump maximal allowed `flake8` version to v7.x

### Repository

- Replace most Python pre-commit hooks with [ruff](https://beta.ruff.rs/docs/)
- Update release drafting GitHub workflow
- Modify pull requests workflow to automatically update CHANGELOG file if it was created by pre-commit.ci
- Update GitHub Action `github/codeql-action` from v2 to v3
- Update GitHub Action `stefanzweifel/git-auto-commit-action` from v4 to v5
- Update `thomaseizinger/create-pull-request` GitHub Action to v1.3.1
- Update `Lucas-C/pre-commit-hooks` hook to v1.5.4
- Update `asottile/blacken-docs` hook to v1.16.0
- Update `astral-sh/ruff-pre-commit` to v0.1.9
- Update `codespell-project/codespell` hook to v2.2.6
- Update `pre-commit/pre-commit-hooks` hook to v4.5.0
- Update `yamllint` hook to v1.33.0

## [v1.4.0] - 2023-02-06

### Changed

- Changed minimum Python version to 3.8.X
- Add support for flake8 6.0.0+

### Updated

- Update GitHub release publishing workflow
- Added some more pre-commit hooks:
  - doc8
  - codespell
  - yamllint
  - blacken-docs
  - pyupgrade

### Repository

- Remove soon to be deprecated `version` in GitHub workflows
- Update `thomaseizinger/keep-a-changelog-new-release` GitHub action to v1.3.0
- Update `Lucas-C/pre-commit-hooks` hook to v1.4.2
- Update `asottile/pyupgrade` to v3.2.0
- Update `black` hook to v22.12.0
- Update `blacken-docs` hook to v1.13.0
- Update `codespell` hook to v2.2.2
- Update `flake8` hook to v5.0.4
- Update `isort` hook to v5.12.0
- Update `pre-commit/mirrors-pylint` to v3.0.0a5
- Update `pre-commit/pre-commit-hooks` to v4.4.0
- Update `pyupgrade` hook to v3.3.1
- Update `yamllint` hook to v1.29.0

## [v1.3.0] - 2022-06-02

### Added

- Added SCS112 to avoid using `os.open()` with unsafe permissions
- Added SCS113 to avoid using `pickle.load()` and `pickle.loads()`
- Added SCS114 to avoid using `marshal.load()` and `marshal.loads()`
- Added SCS115 to avoid using `shelve.open()`
- Added SCS116 to avoid using `os.mkdir` and `os.makedirs` with unsafe file permissions
- Added SCS117 to avoid using `os.mkfifo` with unsafe file permissions
- Added SCS118 to avoid using `os.mknod` with unsafe file permissions
- Added SCS119 to avoid using `os.chmod` with unsafe file permissions (W ^ X for group and others)

### Fixed

- Fix typos found by `codespell`
- Fix issues discovered by `yamllint`

### Repository

- Add Python 3.10 to the list of configurations for testing
- Add `codespell` pre-commit hook
- Add `yamllint` configuration file and pre-commit hook

## [v1.2.2] - 2022-05-24

### Updated

- Update GitHub release publishing workflow

### Fixed

- Fix issue with recognizing YAML load function calls (thanks to [@D-Bhatta](https://github.com/D-Bhatta))

### Repository

- Update `dangoslen/changelog-enforcer` GitHub action to v3
- Update `isort` hook to v5.10.1
- Update `black` hook to v22.3.0
- Update `check-manifest` hook to v0.48
- Update `flake8` hook to v4.0.1
- Update `Lucas-C/pre-commit-hooks` hook to v1.2.0
- Update `pre-commit/pre-commit-hooks` to v4.2.0
- Update `thomaseizinger/create-pull-request` GitHub action to v1.2.2
- Update `thomaseizinger/keep-a-changelog-new-release` GitHub action to v1.3.0
- Update GitHub's CodeQL action to v2

## [v1.2.1] - 2021-07-19

- Reworded SCS103 and extend it to include a few more cases:
  - `subprocess.getoutput()`
  - `subprocess.getstatusoutput()`
  - `asyncio.create_subprocess_shell()`
  - `loop.subprocess_shell()`

## [v1.2.0] - 2021-07-19

- Added SCS110 to avoid using `os.popen()` as it internally uses `subprocess.Popen` with `shell=True`
- Added SCS111 to avoid using `shlex.quote()` on non-POSIX platforms.

## [v1.1.0] - 2021-07-02

### Added

- Added SCS109 to prefer `os.open()` to the builtin `open` when in writing mode

### Repository

- Update pre-commit configuration

## [v1.0.1] - 2021-06-21

### Updated

- Updated error messages to be more in line with README
- Updated README

## [v1.0.0] - 2021-06-20

Initial release

[v1.0.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/c18cc7130a40405bd92e49b22675e8ddbe0bc8cd...v1.0.0
[v1.0.1]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.0.0...v1.0.1
[v1.1.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.0.1...v1.1.0
[v1.2.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.1.0...v1.2.0
[v1.2.1]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.2.0...v1.2.1
[v1.2.2]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.2.1...v1.2.2
[v1.3.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.2.2...v1.3.0
[v1.4.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.3.0...v1.4.0
[v1.4.1]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.4.0...v1.4.1
[v1.5.0]: https://github.com/Takishima/flake8-secure-coding-standard/compare/v1.4.1...v1.5.0
