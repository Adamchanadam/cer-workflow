# Release Notes

## v0.2.0

This release converges CER into a complete bilingual public version:

- Complete, independently installable Traditional Chinese and English Skill packages
- Controller preflight before real dispatch; unsupported assumptions cannot be treated as confirmed
- Local or Remote startup for one unique Controller, verified with `C_READY` / `C_ACCEPTED`
- Explicit `/CER-start`, `/CER-stop`, and `/CER-close` boundaries; `/CER-stop` returns to ordinary single-thread work, and plain start/finish wording does not trigger CER
- `🚀 C:` as the visible Controller label while E1/R/E2 labels stay unchanged
- Review findings with the same cause and user impact converge into one affected-boundary repair; genuinely new defects stay separate
- Inline roadmap and proportionate checkpoints for long-running work
- Separate Traditional Chinese / English infographics and public documentation

## v0.1.1

Documentation and command update:

- Traditional Chinese README as the entry page
- English README page
- CER workflow infographic
- `/CER-start`, `/CER-stop`, `/CER-close`, `/CER-status`, and `/CER-help`
- Guidance for starting, stopping, and closing CER inside a project
- Plain-language comparison with single-thread work

## v0.1.0

Initial public preview:

- CER Core v1 as an installable Skill
- Persistent Executor and risk-based Reviewer roles
- Session/thread receipt rules for cross-task work
- Four-color checkpoint timing
- Knowledge-foundation scoping for specialist tasks
