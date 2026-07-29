# Release Notes

Scope note: each version section records release history for that version; the runtime authority is the Skill references bundled with the version the user has installed.

## v0.2.5

This release hardens delivery reliability for long-running, multi-batch CER work and makes same-provenance evidence reuse plus risk-tiered acceleration the default adaptive schedule:

- Formal messages and batches use stable `messageId`, `batchId`, monotonically increasing `batchSeq`, and immutable `payloadDigest`; the same identity with different content blocks immediately
- An ambiguous `create_thread` or `send_message` result cannot be retried blindly; CER first performs one bounded reconciliation and relies on actual `threadId`, `hostId`, zero-write `READY`, or an authoritative receipt
- A revised batch first moves the old batch into terminal `SUPERSEDED`; delayed delivery or replay of that old batch is rejected and cannot restart writes
- Same-provenance evidence can be reused across dependent work while source identity and freshness remain unchanged; no-state-change batches stop at preflight, new facts are collected together, and acceptance commands run with counterexamples
- A fresh Reviewer is created only after a complete high-risk candidate exists; adaptive acceleration turns itself off whenever communication, writer, evidence, dependency, or batch-lifecycle state is unclear
- When the platform does not automatically wake an idle Controller, CER uses bounded event waits only for declared state transitions; snapshots, commentary, and task completion cannot substitute for direct-push results
- Release readiness completed two independent AI real workflow UAT cycles covering duplicate delivery, batch supersession, delayed-old-batch rejection, Reviewer-blocked repair, and writer close; post-release user manual UAT remains unrun and separately reported

## v0.2.4

This release makes CER pass through Agent Handoff Kit commands to the target workspace authority when that workspace is already governed by Kit:

- When the target `AGENTS.md` clearly routes `收工`, `Wrap up Agent Handoff`, or equivalent session-closeout intent, C gives the same E1 only the user's original instruction, target root, same-E1 / return coordinates, and required non-durable state
- C does not restate, decompose, expand, predict, pre-execute, or create another Kit full-closeout / governance-bridge procedure, checklist, file list, maintenance decision, tests, or completion claim
- Until Kit full-closeout authoritative terminal evidence passes, or while it reports blocked, C does not claim `writer closed`, synchronize title `✓`, or show the CER close card; CER lifecycle close follows only after that evidence passes
- After the same E1 returns verifiable Kit terminal evidence, C performs only required result readback and does not rerun the Kit procedure or checks; missing or contradictory evidence returns to the same E1 for completion
- Governance bridge completion keeps CER active; `/CER-close` remains a CER-only command and does not trigger Kit full closeout in reverse

## v0.2.3

This release makes CER's pre-implementation public alignment and lifecycle prompts visible checkpoints:

- Long-running, multi-batch, or new product, flow, design, content, or experience work shows an inline visualizer roadmap before the first real E1 batch; simple work with one clear endpoint shows only a short summary
- Safe inference no longer follows technical risk alone; when the opposite assumption would change user flow, collaboration, data handling, output, or cause major rework, C must align first or ask the key questions
- The public task summary shows the goal, scope, assumptions, smallest observable outcome, technical acceptance and fit validation, and the next user checkpoint
- Bear cards keep the complete three-line art, with version and status after the foot on the third line rather than a separate line

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
