## Summary

_Describe the change and the user-facing or developer-facing impact._

## Related Issues

Closes #(issue number) or Relates to #(issue number)

## What Changed

- _Summarize the code, tests, docs, or tooling changes._
- _Call out any API, CLI, or behavior changes explicitly._

## Type of Change

- **Bugfix**: Fix an existing feature
- **Feature**: Introduces new functionality without breaking changes
- **Enhancement**: Improves existing functionality
- **Breaking Change**: Introduces breaking changes that require migration
- **Refactoring**: Code restructuring without behavioral changes
- **Build/Infrastructure**: Build system, CI/CD, dependencies, Docker
- **Documentation**: Documentation, comments, or changelog updates

## Validation

- `./tools/lint.sh --changed`
- `./tools/test.sh -q`
- `./tools/docs.sh` (if docs or public API changed)
- `python -m build` (if packaging or release files changed)
- Manual testing described below when automated coverage is not enough

## Breaking Changes

_Describe any migration, compatibility, or deprecation impact. Write `None` if not applicable._

## Notes for Reviewers

_Call out anything that deserves extra attention: edge cases, tradeoffs, follow-up work, or known limitations._

## Checklist

- Code follows project style guidelines
- Self-review completed
- Comments added for complex logic
- No breaking changes without documentation
- Commit messages follow semantic convention: `{type}({scope}): {message}`
