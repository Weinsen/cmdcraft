Changelog
=========

v0.0.7
----------

- Move packaging metadata into ``pyproject.toml`` and remove ``setup.py`` plus ``requirements.txt``.
- Add shared tooling helpers and dedicated ``lint`` / ``test`` scripts that honor the repository virtual environment and base ref.
- Expand GitHub Actions coverage to Python 3.13, release-candidate branches, editable installs, and draft PR handling.
- Reorganize the Sphinx docs for Read the Docs, add API documentation pages, and document the updated contributor workflow.

v0.0.6
------

- Handle args and kwargs
- Configure workflow
- Update config.py
- Update documentation
- Improve testing coverage
- Fix positional suggestions

v0.0.5
------

- Handle positional parameters
- Improve help method
- Fix issue with empty inputs
- Fix issue README.rst syntax
- Clean code

v0.0.4
------

- Change naming: `Method`` to `Command`
- Change naming: `Interpreter`` to `Prompter`
- Improve linting

Fixed issues:
*************
#2: Exception while typing quoted arguments

v0.0.3
------

- Adopt ruff as linter
- Improve documentation

v0.0.2

Fixed issues:
*************
#1: Input mishandling options

- Input handling

v0.0.1
------

Features:
*********

Initial release