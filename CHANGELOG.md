# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Added

- `assert_no_if` function in audit.py
- `assert_no_for` function in audit.py
- `assert_no_while` function in audit.py
- `assert_no_loops` function in audit.py

### Changed

- always set status to "failed" on error

### Removed

- `count_while_loops()` function in audit.py


## [1.2.1] - 2025-09-07

### Added

- meta.py module about submission metadata
- `submission_closed()` function in meta.py
- `__all__` in coverage.py (for convenience)

### Changed

- renamed `within_deadline()` to `submission_open()`
- moved `get_username()`, `submission_open()`, and `postpone_tests()` to meta.py


## [1.2.0] - 2025-09-06

### Added

- support for `ruff` style checker
- `get_source_code()` function in audit.py
- `count_comments()` function in audit.py
- `within_deadline()` function in common.py
- `postpone_tests()` function in common.py

### Fixed

- the `build` command ignores files in cache dirs

### Changed

- setup.sh installs same version of jmu_pytest_utils


## [1.1.0] - 2025-08-14

### Added

- leaderboard functionality via test function (#1)
- regex auditing (from `jmu_gradescope_utils`)
- `count_while_loops()` function in audit.py
- `REQUIREMENTS_TXT` configuration option (#2)
- `get_username()` function in common.py (#3)
- pyproject.toml (will be required by pip 25.3)
- this CHANGELOG.md file

### Fixed

- allow students to submit any type of file (#4)
- `count_calls()` also counts methods (#5)

### Changed

- Use semantic versioning (added third digit)


## [1.0] - 2024-12-30

Initial release; see [v1.0 HISTORY.md](https://github.com/JMU-CS/jmu_pytest_utils/blob/v1.0/HISTORY.md)


[unreleased]: https://github.com/JMU-CS/jmu_pytest_utils/compare/v1.2.1...HEAD
[1.2.1]: https://github.com/JMU-CS/jmu_pytest_utils/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/JMU-CS/jmu_pytest_utils/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/JMU-CS/jmu_pytest_utils/compare/v1.0...v1.1.0
[1.0]: https://github.com/JMU-CS/jmu_pytest_utils/releases/tag/v1.0
