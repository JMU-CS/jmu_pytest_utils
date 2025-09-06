# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Added

- support for `ruff` style checker
- `get_source_code()` function in audit.py
- `count_comments()` function in audit.py
- `within_deadline()` function in common.py
- `postpone_tests()` function in common.py

### Fixed

- don't include files in cache dirs


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


[unreleased]: https://github.com/JMU-CS/jmu_pytest_utils/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/JMU-CS/jmu_pytest_utils/compare/v1.0...v1.1.0
[1.0]: https://github.com/JMU-CS/jmu_pytest_utils/releases/tag/v1.0
