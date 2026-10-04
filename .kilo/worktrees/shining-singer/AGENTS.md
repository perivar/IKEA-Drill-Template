# AGENTS.md

This file provides guidance to AI coding agents working with code in this repository.

## Important Guidelines

- **Never take action unless explicitly told to** - Wait for user confirmation before making changes
- **Never make assumptions** - Ask clarifying questions when requirements are unclear

---

## Task Completion Checklist (MANDATORY)

Before calling `attempt_completion`, the following MUST pass:

1. [ ] Run `./scripts/lint_and_fix.sh` - must pass with no errors
2. [ ] Only then call `attempt_completion`
