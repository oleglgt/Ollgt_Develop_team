# CLAUDE.md — Instructions for AI Development Team

## Project Overview
This is a multi-agent software development system. Three agents collaborate to build Python applications based on user requirements described in GitHub Issues.

## Agents

### Architect (Leader)
- Reads new issues with label `role:architect`
- Creates detailed specs in `specs/` directory
- Breaks down tasks into subtasks (GitHub Issues with appropriate labels)
- After all subtasks pass testing → merges PRs and creates GitHub Release
- Sends Telegram notifications on key events

### Developer (Teammate)
- Picks up issues with label `role:developer`
- Reads the spec from `specs/` directory
- Writes Python code in `src/` directory
- Creates a feature branch and opens a Pull Request
- Reports completion to the Architect

### Tester (Teammate)
- Picks up issues with label `role:tester`
- Reads the spec and reviews the PR diff
- Writes tests in `tests/` directory
- Runs tests with pytest
- Approves (moves to Release) or Returns (moves back to Development) with comments
- After release: performs final verification

## Code Standards
- Language: Python 3.11+
- Style: PEP 8, type hints required
- Tests: pytest, minimum 80% coverage for new code
- Docs: docstrings for all public functions
- Git: feature branches, meaningful commit messages

## Comment Format
All agents write structured comments in GitHub Issues:

```
<!-- agent:{role} action:{action_type} -->
## {Human-readable title}

{Details}
```

Actions: `spec_ready`, `subtasks_created`, `code_ready`, `pr_created`, `test_passed`, `test_failed`, `release_created`, `release_verified`

## File Structure
- `specs/` — Specifications (one .md file per feature)
- `src/` — Application source code
- `tests/` — Test files (mirror src/ structure with test_ prefix)
- `agents/` — Agent configurations (do not modify during tasks)

## Communication Protocol
- Agents communicate through GitHub Issues comments and label changes
- Status changes are tracked via GitHub Project column moves
- Critical events trigger Telegram notifications
