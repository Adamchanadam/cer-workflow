# Release Notes

Scope note: each version section records release history for that version; the runtime authority is the Skill references bundled with the version the user has installed.

## v0.2.2

This release fixes two CER usage issues confirmed after v0.2.1:

- Bear-card feet now use `╰ ^ ╯`, so a leading `>` is not rendered as a Markdown quote
- `/CER-close` preserves `writer closed`, required readback, title sync/warning, and history-only close conditions
- When this cycle's C/E/R tasks are known, CER-close reads back the relevant roles directly instead of scanning the whole project by default
- State-only close uses targeted readback; checks widen only when evidence is missing, state conflicts, the core workflow is affected, or project rules require it
- v0.2.2 CER-close UAT has passed; post-release user manual UAT remains separately reported

## v0.2.1

This release converges the Full-Audit-passed release-ready candidate:

- Bear lifecycle cards now display the package version from the Skill `VERSION`, with corrected start, stop, and close timing
- Formal C/E/R use the official sidebar-visible task topology, preserving same-cycle E1 reuse, fresh Reviewers, and cross-cycle isolation
- Short numeric cycle titles, CER-close `✓` rename, and the `title sync warning` boundary are fully captured in the execution surface
- C reapplies the acceptance-validity/proportion rule before making or reusing acceptance, repair, or release conclusions; unaffected evidence can be retained, failed premises reopen only their conclusions, breadth follows traceable causal coverage, and depth follows consequence/uncertainty rather than task label or file count
- Codex-only install/upgrade prompts are split by language to avoid installing another language or another agent version
- Release-readiness evidence includes the full static corpus audit and two-cycle AI real workflow UAT; post-release user manual UAT remains separately reported

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
