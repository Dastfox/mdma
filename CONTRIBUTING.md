# Contributing

## Branching

- Branch off `main`, one topic per branch.
- Name branches `type/short-description` (e.g. `feat/add-parser`, `fix/null-check`).

## Commits

- Write clear, imperative commit messages ("Add X", "Fix Y", not "Added X" or "Fixes").
- Keep commits focused; squash fixup commits before opening a PR.

## Pull requests

- Fill out the PR template completely.
- Keep PRs small and scoped to a single change.
- Link the related issue, if any.
- Ensure CI passes before requesting review.
- Rebase onto `main` to resolve conflicts rather than merging `main` in, unless the repo's history already favors merge commits.

## Review

- At least one approval is required before merging.
- Address all review comments, or explain in-thread why not.
- Squash-merge unless preserving individual commit history is explicitly useful.

## Code quality

- Add or update tests for any behavior change.
- Update documentation when public behavior changes.
- Do not merge with failing CI checks.
