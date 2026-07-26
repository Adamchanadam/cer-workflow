# CER Core v1 Fresh UAT

The user must manually create a new task in a clean project for UAT. A task created, forked, or delegated by C in the source project carries source context and is not fresh.

A successful title change, fork, delegation, one-way message, or tool parameter does not prove a closed loop. E1 must direct-push both `ready` and `result`.

## Installation Scenario

- The target contains only this Skill, with no source handoff or source-project context.
- A new C can start from only the Skill and the user's overall task.
- `/CER-start` and `Start CER` trigger CER; a plain start/work message does not.
- `/CER-close` and `Close CER` trigger CER close; a plain close/finish message does not close CER and does not map to `/CER-stop`.

## Full Flow

1. The user submits a clear multi-batch task or existing plan using `Start CER: ...` or `/CER-start ...`.
2. C identifies the main task with a `🚀 C:` title or first-line label and completes Controller preflight. A complete task passes directly; sourced `confirmed` items and `safe inference` items that pass the counterfactual test do not block; missing critical endpoint/permission/acceptance information produces a yellow checkpoint with at most three questions.
3. C completes communication preflight, creates or reuses a proven persistent `E1:` task, and receives a `ready` direct-push containing session/thread coordinates.
4. C maps existing target-project sources of truth and the task knowledge foundation without creating fixed CER documents.
5. C shows the initial roadmap with a real inline visualization, explicitly confirming that it is not Mermaid-only.
6. C uses bear cards and inline visualization only at startup or before the first batch, material decisions, major blockers, staged delivery, and closeout. Ordinary E1 substeps do not show cards.
7. The same E1 completes at least two implementation batches. Low-risk batches do not create R. E1 uses C's frozen task contract and does not expand scope or acceptance on its own.
8. A fresh `R1:` independently challenges one high-risk core promise against the same knowledge foundation and frozen task contract, and re-reviews only the affected boundary.
9. C stops for the user when a material direction or deliverable shape changes, delivers observable staged results, and obtains final user acceptance.
10. The user says `Close CER.` or `/CER-close`. The same E1 updates required existing sources of truth and marks `writer closed`. If no durable source exists, CER does not claim full cross-session recovery.
11. Run a separate composition scenario with `$project-context-workflow`: CER does not rebuild documents or take over consensus gates, and the context workflow does not create C/E1/R.
12. Run a separate stop scenario with `/CER-stop`: C sends no new E1/R work and, if E1 is writing, reaches `writer closed` or a major blocker before returning to one thread.

## Remote Controller Scenarios

- When an explicit Remote `/CER-start` or equivalent CER-qualified start designates a receiver task, that receiver first direct-pushes candidate `C_READY` with threadId, hostId, target_root, and return target/path.
- The sender/local startup gate uses the official task/thread list or platform-equivalent tool to fully enumerate this start's participating hosts, reads back candidate root/`🚀 C:` identity/active state, and explicitly states that it has not assigned the same root to another C. After that, it sends `C_ACCEPTED` over the same path, and the receiver becomes active `🚀 C:` only after receiving it.
- If participating-host enumeration is incomplete, candidate root/identity/state cannot be read back, coordinates are incomplete, or evidence conflicts, stop.
- If an active C already exists, reuse it, or transfer only after the old C explicitly hands off/closes and that evidence is read back. If the sender was the active C, it must hand off/close before sending `C_ACCEPTED`.
- Benign cross-task E1/R wording must not be treated as a Remote C conflict when the batch remains self-contained and returns by direct-push.

## Review Convergence Scenarios

- After R first reports a defect, related findings are grouped by common root cause and user consequence. C performs one bounded impact check to find this round's current owners, affected surfaces, and check locations.
- When one set of findings contains two issues that differ only in wording or sentence order but share the same root cause and user consequence, plus one issue with a different root cause, different user consequence, or a new regression caused by the latest repair, C merges the first two into one convergence scope and batch while keeping the third as a valid expansion.
- C freezes acceptance and the counterexample family, and the same E1 repairs the whole affected boundary in one batch. After the repair, R re-tests only the frozen scope.
- Synonymous wording does not open another sentence-by-sentence repair cycle. C accepts and stops after the frozen counterexample family passes with no material new defect.

## Controller Preflight QC Scenarios

- When the user gives a natural-language task that is sufficient to start a small batch but omits reversible details that would not materially change the outcome, C may mark them `safe inference` and continue.
- If missing information has multiple reasonable answers and different answers would materially change the deliverable, permissions/risk, acceptance, or cause major rework, C must mark the item `critical missing` and stop for questions.
- C's frozen task contract and E1/R dispatches preserve the three states, required source anchors, and counterfactual results. They must not invent user confirmation.

## Failure Conditions

- A temporary subagent substitutes for persistent E1.
- Controller uses plain `C:` instead of `🚀 C:` as the visible title or first-line label.
- E1/R/E2 titles or first-line labels are wrongly prefixed with `🚀`.
- A plain start/work message starts CER, or a plain close/finish message triggers CER close/stop.
- An explicit CER-qualified start or close equivalent does not trigger the corresponding CER behavior.
- Controller preflight is incomplete, or a `critical missing` item still creates/reuses E1 or dispatches real work.
- Safely inferable details are wrongly upgraded into a blocking form, or simple work is forced to display governance ceremony.
- C labels an assumption as `confirmed` without an explicit user statement or an authoritative source C has read.
- C labels an item `safe inference` and dispatches even though the opposite assumption would materially change the deliverable, permissions/risk, acceptance, or cause major rework.
- The frozen task contract or dispatch writes an unsupported assumption as `confirmed`.
- C dispatches instead of stopping when critical endpoint, permission, or acceptance information is missing.
- Missing root cause leads to a quick fix, or acceptance counterexamples expand into defensive whole-project review.
- E1/R rewrites C's frozen task contract and continues.
- Every wording or sentence-order variation adds a validator pattern, Reviewer, or repair batch.
- Holes are patched before this round's current owners are fully identified.
- Review or repair expands without a different root cause, different user consequence, or new regression caused by the latest repair.
- A different root cause, different user consequence, or new regression caused by the latest repair is wrongly merged into the existing counterexample family, causing a material new defect to be missed.
- An explicit Remote C is blanket rejected because the message came from another task.
- A second C is created while an active C already exists for the same target_root.
- C is created while active C status is unknown.
- Remote C identity or communication path is claimed after merely sending candidate `C_READY`, without the sender actually receiving it, reading it back, and returning `C_ACCEPTED`.
- A lock file, central registry, run ID, conflict engine, new role, or test exception is added for unique C.
- A cross-task prompt depends on prior conversation.
- Work starts before the delivery chain is proven.
- Only title, fork, or one-way send is proven, without E1 `ready/result` direct-pushes.
- A fork carrying source context is counted as fresh UAT.
- The assignee does not return `ready/result`, but the loop is still claimed.
- A new task lacks a visible `E1:`/`R1:` title or first-line label, or receipts omit session/thread coordinates.
- C discovers results by polling.
- A knowledge-heavy task lacks a defined knowledge foundation, or R checks only format instead of challenging specialist claims.
- Every internal step gets a card, or a material decision, blocker, or staged delivery gets no card.
- Mermaid is substituted for available inline visualization instead of being supplemental.
- Ordinary small changes always create fresh R or trigger full-project review.
- CER creates a fixed five-document project set or parallel progress source.
- `$project-context-workflow` is treated as a CER installation prerequisite.
- `/CER-stop` is followed by new E1/R work, or single-thread work resumes before an active writer is proven stopped.
- `/CER-status` triggers polling or background monitoring.
- Only documentation or a local technical step succeeds, without a real deliverable.
