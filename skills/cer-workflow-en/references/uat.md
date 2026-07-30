# CER Core v1 Fresh UAT

Fresh UAT must run in an independent clean project through sidebar-visible official new tasks. A
task created, forked, or delegated by C in the source project carries source context and is not
fresh.

A successful title change, fork, delegation, one-way message, or tool parameter does not prove a closed loop. E1 must direct-push both `ready` and `result`.

For this Codex project's Full Audit, when official `create_thread` task tools and a clean UAT
workspace are available, AI real workflow UAT is required and cannot be replaced by a sub-agent,
fork, or text simulation. If the tools or clean workspace are proven unavailable, the only allowed
downgrade claim is `Full Audit passed (static corpus only; AI real workflow UAT unavailable)`, and
it must not claim AI UAT passed. Post-release user manual UAT is a separate layer for public
installation and user experience, reported separately as `not run`, `passed`, or `failed`; AI UAT
must not be reported as manual UAT.

AI real workflow UAT evidence must list actual thread ids for both cycles and perform mechanical
comparison: same-cycle batches keep the same E1 threadId; C2 threadId differs from C1; cycle-2 E1
threadId differs from cycle-1 E1; every cycle-2 R is a new threadId that differs from every cycle-1
R and does not reuse an earlier R in the same cycle. Text that merely says fresh is insufficient.

All C/E/R titles in the same cycle must use the same short cycle number, such as
`🚀 C:01｜...`, `E1:01｜...`, and `R1:01｜...`; the next cycle uses a new number. New cycles after
this rule is active must use `01` or higher, not `00`. `00` may appear only in an explicit
legacy/migration fixture for a cycle that started before cycle numbering and whose original cycle
number cannot be reliably reconstructed. The cycle number is sidebar display only, not a lock, run
ID, unique-C proof, or thread identity. If a new cycle cannot reliably enumerate or set the title,
keep the shortest role title and report a real `title sync warning`; do not show a question-mark
cycle label or guess a number.

## Installation Scenario

- The target contains only this Skill, with no source handoff or source-project context.
- This Skill is for Codex only. Do not claim that this repository currently provides a
  Claude Code Skill.
- The Skill root `VERSION` is one stable-semver line, currently `0.2.6`. Read it again before
  every bear card, and show `version unverified` when it is invalid.
- A new C can start from only the Skill and the user's overall task.
- `/CER-start` and `Start CER` trigger CER; a plain start/work message does not.
- `/CER-close` and `Close CER` trigger CER close; a plain close/finish message does not close CER and does not map to `/CER-stop`.

## Full Flow

1. The user submits a clear multi-batch task or existing plan using `Start CER: ...` or `/CER-start ...`.
2. C identifies the main task with a `🚀 C:01｜<very short task name>` title or first-line label and completes Controller preflight. A complete task passes directly; sourced `confirmed` items and `safe inference` items that pass the counterfactual test do not block; missing critical endpoint/permission/acceptance information produces a yellow checkpoint with at most three questions.
3. C completes communication preflight, uses official `create_thread` to create a brand-new
   sidebar-visible persistent `E1:01｜...` task in the same Codex project, reads back its title, thread
   ID, and formal return path, and receives a `ready` direct-push containing session/thread
   coordinates. If the actual platform does not automatically wake an idle C, C may use one
   bounded event wait on that E1; the wait snapshot is not ready evidence.
4. C maps existing target-project sources of truth and the task knowledge foundation without creating fixed CER documents.
5. For every successfully accepted `CER-start`, C's first user-visible success receipt is the
   fixed open-eye `CER Workflow v0.2.6` / `🔵 CER started` card using the `╰ ^ ╯` foot, keeping the
   complete three-line bear with version and status after its foot on the third line, separated by
   fixed `·` markers rather than a separate line, including single-batch work. Multi-stage,
   multi-batch, or first-public-alignment work then shows the initial roadmap with a real inline
   visualization and explicitly confirms that it is not Mermaid-only.
6. C uses the matching bear card only for startup, material decisions, major blockers, staged
   delivery, successful stop, and successful close. Ordinary E1 substeps do not show cards.
7. The same E1 completes at least two implementation batches. Low-risk batches do not create R.
   Later batches in the same cycle reuse the same E1 from step 3 rather than rebuilding or
   replacing it. E1 uses C's frozen task contract and does not expand scope or acceptance on its
   own.
8. A sidebar-visible fresh `R1:01｜...` new task created through official `create_thread` independently
   challenges one high-risk core promise against the same knowledge foundation and frozen task
   contract, and re-reviews only the affected boundary.
9. C stops for the user when a material direction or deliverable shape changes, delivers observable staged results, separates technical acceptance from fit validation, and obtains applicable user acceptance.
10. The user says `Close CER.` or `/CER-close`. The same E1 updates required existing sources
    of truth and marks `writer closed`. After required readback, C uses the official title tool to
    rename verifiable titles to `🚀 C:01✓｜...`, `E1:01✓｜...`, and `R1:01✓｜...`, then reads them
    back; on failure, it reports `title sync warning` with failed coordinates. Only after that does
    C show the fixed closed-eye `🟢 CER closed` / `writer closed` card. If no durable source exists,
    CER does not claim full cross-session recovery.
11. Run a separate composition scenario with `$project-context-workflow`: CER does not rebuild documents or take over consensus gates, and the context workflow does not create C/E1/R.
12. Run a separate stop scenario with `/CER-stop`: C sends no new E1/R work and, if E1 is
    writing, reaches `writer closed` or a major blocker. Only after proving no active writer and
    completing required readback may C show the fixed closed-eye `⚪ CER stopped` /
    `CER inactive` card and return to one thread.

## Remote Controller Scenarios

- When an explicit Remote `/CER-start` or equivalent CER-qualified start designates a receiver task, that receiver first direct-pushes candidate `C_READY` with threadId, hostId, target_root, and return target/path.
- The sender/local startup gate uses the official task/thread list or platform-equivalent tool to fully enumerate this start's participating hosts, reads back candidate root/`🚀 C:` identity/active state, and explicitly states that it has not assigned the same root to another C. After that, it sends `C_ACCEPTED` over the same path, and the receiver becomes active `🚀 C:` only after receiving it.
- If participating-host enumeration is incomplete, candidate root/identity/state cannot be read back, coordinates are incomplete, or evidence conflicts, stop.
- If an active C already exists, reuse it, or transfer only after the old C explicitly hands off/closes and that evidence is read back. If the sender was the active C, it must hand off/close before sending `C_ACCEPTED`.
- Benign cross-task E1/R wording must not be treated as a Remote C conflict when the batch remains self-contained and returns by direct-push.

## Cross-Cycle Isolation Scenarios

- After a successful `/CER-close` in one workspace, the old C/E/R tasks may remain as history,
  but the whole set must not receive work for a later cycle.
- A new task's `CER-start` becomes valid only after the unique-C gate reads back that the old C
  is `closed`/`handed-off`, no active C exists, and every participating host is verifiable.
- The new cycle creates a brand-new E1 and only fresh Reviewers. It must not reuse any E1 or R
  task/coordinate from the previous closed C. Evidence must compare cycle numbers and threadIds:
  same-cycle E1 threadId is unchanged; the second-cycle label is different; C/E1/R threadIds are
  different; and the old-cycle title prefix has `✓` or a real `title sync warning`.
- AI real workflow UAT in a clean project must use numeric `01` or higher for new cycles. `00` may
  appear only in an explicit legacy migration fixture. Any visible question-mark cycle title fails.
- If old C state or any participating host cannot be verified, startup is blocked and shows the
  open-eye red blocker card.

## Codex Task Topology Scenarios

- E1, E2, and every R are sidebar-visible independent new tasks/threads in the same Codex
  project, created through official `create_thread`; ready/result receipts read back title,
  thread ID, and formal return path.
- Later batches in the same cycle keep reusing that cycle's same E1. Only after E1 has stopped
  writing, the workspace is in a known state, and C issues a takeover batch may C create E2
  through `create_thread`.
- Every R is a fresh new task. Do not reuse an old R in the same cycle or across cycles.
- C may use an inline "Exploration Helper" for read-only exploration, evidence organization, or
  candidate analysis. It must not write the workspace, replace E or R, produce formal
  ready/result, or count as CER Reviewer acceptance evidence.
- If `create_thread`, sidebar-visible title, verifiable thread ID, or formal return path is
  missing, E/R delegation is blocked. Do not downgrade to an inline sub-agent, fork, delegate, or
  existing task.

## Ambiguous Tool Outcome And Batch Deduplication Scenarios

- When `create_thread` reports an error or timeout but one bounded official enumeration finds one
  new task matching the pre-create snapshot, C does not retry creation. Official metadata plus that
  task's zero-write `ready` confirms it.
- When one bounded reconciliation finds no candidate after an ambiguous `create_thread`, the state
  is `blocked`. An immediate zero-candidate listing does not authorize automatic retry. Before a
  later resume, startup, or creation of the same role, reconciliation runs again so a delayed task
  is not treated as nonexistent.
- When three candidates exist for the same role/cycle/root, all three remain zero-write. C selects
  one and sends `STOP_ZERO_WRITE` to the other two. Formal work starts only after both direct-push
  stop confirmation.
- When one of three zero-write candidates cannot direct-push stop confirmation, only an officially
  readable non-working terminal state may substitute. Without either proof, the flow is `blocked`
  and no other candidate starts work.
- When a task self-reports host `local` but official metadata shows another current actual hostId,
  routing uses official metadata. The mismatch is reconciled before work; a display alias is not
  authoritative identity.
- When any duplicate E1 may have received a formal batch or written, C stops new dispatch and reads
  back writer and workspace state. Only after every writer stops and workspace state is determinate
  may one writer recover or E2 be created under takeover rules. Merely selecting one and canceling
  the others is insufficient.
- When E1 returns `BATCH_RECEIVED` and stops before work begins, the batch remains
  `RECEIVED_ZERO_WRITE`. Delivery of the same `batchId` continues the original batch once rather
  than starting a second execution.
- When E1 stops after partial writes and batch state cannot be proven, mark `STATE_UNKNOWN`, stop
  writing, and recover single-writer/workspace state before any rerun.
- Repeated delivery of a `RESULT_READY` batch replays the same result. Only after C returns
  `RESULT_ACCEPTED` does another delivery return just `DUPLICATE_IGNORED`.
- A controlled resend after an ambiguous first send preserves identical content, `batchId`, and
  `batchSeq`, and `payloadDigest`. Any acceptance or task-contract change uses a new `batchId` and
  higher `batchSeq`.
- The same `batchId` with a different `payloadDigest` blocks immediately. C cannot accept an old
  batch result as the result of a new revision.
- When old batch B1 has ambiguous delivery and a new contract needs B2, C first sends
  `BATCH_SUPERSEDE B1 -> B2`. The recipient records B1 as `SUPERSEDED` and confirms it; delayed B1
  is then rejected. If B1 started or may have written, stop and recover the workspace before
  starting B2 with its higher `batchSeq`.
- When any ready, `C_ACCEPTED`, stop, batch-state, result, or `RESULT_ACCEPTED` send is ambiguous,
  the sender first performs one bounded receipt/destination readback for the same `messageId`.
  If needed, only one controlled resend of the identical message is allowed; the receiver
  deduplicates and replays its prior confirmation.
- When E1 completed work but result push is ambiguous, C obtains the candidate through destination
  readback for the same `messageId` or a duplicate result, then returns the same
  `RESULT_ACCEPTED`. The flow neither waits forever nor accepts twice.
- Failure readback for an exact `messageId` may run before push is received, but proves only that
  message's delivery. It neither establishes the full ready/accept communication chain nor expands
  into polling.
- When the platform does not automatically wake an idle C, C uses one bounded event wait on the
  known unique E1. Only E1's direct-push READY interrupting the wait allows continuation. A wait
  snapshot, completion state, or commentary without direct-push still fails.
- When one batch expects `BATCH_RECEIVED` and then a final result, they use separate
  `eventWaitKey` values and the latest cursor, each with one initial wait. The first receipt does
  not consume the final-result wait budget.
- After timeout for one expected message, only reconciliation plus the single controlled resend
  with the same `messageId` permits one recovery wait. Another timeout blocks; extra control
  messages or renaming cannot reopen the budget.
- When the platform has no idempotency key or authoritative operation receipt, CER uses bounded
  reconciliation and `batchId` deduplication without inventing a platform receipt; the batch
  identifier is used only for duplicate-delivery protection.

## Adaptive Batch Acceleration Scenarios

- Within one checkpoint, when the reviewed object, requirements, direct dependencies/environment,
  delivery artifact, and validation method remain unchanged with no credible contradiction,
  common-source evidence is read and located once and reused across dependent work.
- A change to requirements, sources, direct dependencies, environment premises, delivery artifact,
  or validation method immediately invalidates affected evidence and rebuilds only the minimum
  sufficient evidence for that conclusion.
- When current authoritative readback already proves acceptance before writing,
  `no_material_delta` stops that write batch. Review, evidence, audit, and failure-recovery batches
  are not skipped merely because they write no files.
- New facts in one checkpoint are collected together and advance the validity window at most once.
  Credible contradiction still reopens the affected conclusion after consolidation.
- Compatible acceptance commands and counterexamples may run in one batch while retaining separate
  output, exit status, provenance, and adjudication. Order-dependent or shared-mutable-state checks
  run separately.
- One fresh R reviews the complete stable high-risk candidate. An irreversible or high-consequence
  action receives its required R before action, never after it for batching convenience.
- Ambiguous communication or batch lifecycle, duplicate roles, unknown single-writer state,
  uncertain evidence identity/freshness, or a required user decision sets acceleration to `off`
  and restores normal CER.
- A fresh R independently reads and challenges frozen raw evidence. C/E summaries may locate
  evidence but do not replace it.

## Exploration Helper Auto-Scheduling Scenarios

- A simple task that can be completed and accepted in one bounded read remains `auto-idle` and
  uses zero Exploration Helpers.
- A small number of helpers starts automatically only when at least two independent read-only
  lanes, frozen inputs, non-duplicative concurrent C work, independently verifiable candidates,
  and clear net time savings all hold. No slash command is added.
- While helpers run, C concurrently completes different critical analysis, gating, or
  adjudication work and personally reads back key sources. C does not degrade into a candidate
  organizer.
- When candidates contradict each other, C adjudicates from authoritative sources rather than
  helper count, matching answers, or completion order.
- Partial drift in frozen inputs invalidates only candidates that depend on that version.
  Unaffected candidates are not rerun.
- A successfully created helper that lacks its assigned source returns a blocked candidate with
  zero writes. C may continue other adjudication.
- When creation tooling or a required capability is unavailable, or a helper fails or times out,
  that candidate becomes unavailable and C falls back to normal read-only analysis without
  repeating the same failure. CER blocks only when the missing evidence is itself a blocker.
- Helpers remain idle when dispatch, readback, deduplication, and adjudication cost is not lower
  than expected savings, or any activation condition is uncertain.

## Review Convergence Scenarios

- After R first reports a defect, related findings are grouped by common root cause and user consequence. C performs one bounded impact check to find this round's current owners, affected surfaces, and check locations.
- When one set of findings contains two issues that differ only in wording or sentence order but share the same root cause and user consequence, plus one issue with a different root cause, different user consequence, or a new regression caused by the latest repair, C merges the first two into one convergence scope and batch while keeping the third as a valid expansion.
- C freezes acceptance and the counterexample family, and the same E1 repairs the whole affected boundary in one batch. After the repair, R re-tests only the frozen scope.
- Synonymous wording does not open another sentence-by-sentence repair cycle. C accepts and stops after the frozen counterexample family passes with no material new defect.

## Controller Preflight QC Scenarios

- When the user gives a natural-language task that is sufficient to start a small batch but omits reversible details that would not materially change the outcome, C may mark them `safe inference` and continue.
- If missing information has multiple reasonable answers and different answers would materially change the deliverable, permissions/risk, acceptance, or cause major rework, C must mark the item `critical missing` and stop for questions.
- C's frozen task contract and E1/R dispatches preserve the three states, required source anchors, and counterfactual results. They must not invent user confirmation.

## Acceptance Validity Scenarios

- A version-only or release-docs-only change may retain unaffected runtime UAT, but must validate
  version, docs, links, and delivery-artifact readback.
- When current external authority contradicts an install claim, reopen only the affected public
  install claim and its dependent delivery surface, even when local runtime did not change.
- A source/package or install artifact mismatch requires artifact readback before a release or
  install conclusion.
- A `high risk`/release label, file count, or change size without a premise-to-conclusion causal
  chain does not authorize whole-project re-review.
- Credible evidence that old validation was false-green reopens the affected conclusion and
  rebuilds the minimum sufficient evidence.
- Fresh context that cannot access prior evidence must not silently retain the old conclusion; it
  must read back the evidence, mark continuity limited, or rebuild affected evidence.

## Proportionate Close Scenarios

- When this cycle's C/E/R threadIds are complete and writer state is directly readable, C reads
  terminal state, required sources, and title sync from those known roles. It does not first
  enumerate the whole project or create R merely for close.
- A status-only close updates only existing sources actually required for this close and uses
  targeted structural/content readback. When no durable source needs an update, verify only the
  actual deliverable and `writer closed`; do not require a fixed document set.
- When role coordinates are incomplete or contradictory, or writer state is unknown, C enumerates
  within the relevant project and expands readback. Proportionality must not hide an unknown
  terminal state.
- Run the relevant full validator or doctor when this cycle changed governance, schema, or core
  flow; credible contradiction or false-green evidence exists; source and delivery artifact
  differ; or project rules require it. Do not run it automatically merely because the command is
  close.
- Every CER bear card uses `╰ ^ ╯` for the foot. It must not use a leading `>` that Markdown can
  render as a block quote. Keep the complete three-line bear; version and status follow the foot
  on its third line with fixed `·` markers, not a separate line.

## Kit Authority Pass-Through Scenarios

- When the target workspace's `AGENTS.md` routes `Wrap up Agent Handoff`, `收工`, or equivalent
  session-closeout intent to Kit full closeout, C's batch to the same E1 preserves the user's
  original instruction, correct root, role/return coordinates, and required non-durable state.
  It does not restate the Kit closeout procedure, file list, maintenance decision, or extra tests.
- Until Kit authoritative terminal evidence passes, or while it reports blocked, C does not claim
  `writer closed`, synchronize title `✓`, or show the CER close card. CER lifecycle close follows
  only after that terminal evidence passes.
- When the same E1 has returned verifiable authoritative Kit terminal evidence, C performs only
  required result readback. It does not search for another CLI, rerun `closeout-status`, or copy
  other Kit checks; only missing or contradictory evidence returns to the same E1 for completion.
- `/CER-close` performs CER close only and does not trigger Kit full closeout in reverse.
- When the target `AGENTS.md` routes `治理打通`, `connect this document to Agent Handoff Kit`, or
  equivalent document-governance intent to an existing governance-bridge workflow, C gives the
  same E1 only the original instruction, specified document, and required coordinates. CER remains
  active after completion.
- If the Kit authority is unreadable, the same E1 cannot be verified, or another writer exists,
  pass-through is blocked. C must not guess, simulate, or create another Kit procedure.

## Failure Conditions

- A temporary subagent substitutes for persistent E1.
- An inline sub-agent, fork, delegate, or existing task is treated as formal E1, E2, or R.
- C's inline sub-agent writes the workspace, produces formal ready/result, replaces E/R, or is
  counted as CER Reviewer acceptance evidence.
- E1/R lacks official `create_thread` creation evidence, sidebar-visible title, verifiable
  thread ID, or formal return path, but work still starts.
- Controller uses plain `C:` instead of `🚀 C:01｜...` as the visible title or first-line label.
- E1/R/E2 titles or first-line labels are wrongly prefixed with `🚀`.
- Second-cycle E1 is named `E2:`, role ordinal and cycle number are mixed, same-cycle C/E/R labels
  use inconsistent cycle numbers, or a later cycle reuses the same cycle number.
- The cycle number is treated as a lock, run ID, unique-C proof, or thread identity; threadIds are
  missing but the flow still passes.
- A new cycle uses `00`; any visible question-mark cycle title appears; or title enumeration /
  setting failure shows a fake label or guessed number instead of keeping the shortest role title
  and reporting a real `title sync warning`.
- A plain start/work message starts CER, or a plain close/finish message triggers CER close/stop.
- C rewrites a Kit full-closeout or governance-bridge procedure, file list, maintenance decision,
  or tests into the E1 dispatch.
- C reruns a Kit procedure or check after the same E1 has returned verifiable authoritative Kit
  terminal evidence.
- C claims `writer closed`, synchronizes title `✓`, or shows the CER close card before Kit full
  closeout has authoritative successful terminal evidence.
- An explicit CER-qualified start or close equivalent does not trigger the corresponding CER behavior.
- Controller preflight is incomplete, or a `critical missing` item still creates/reuses E1 or dispatches real work.
- Safely inferable details are wrongly upgraded into a blocking form, or simple work is forced to display governance ceremony.
- C labels an assumption as `confirmed` without an explicit user statement or an authoritative source C has read.
- C labels an item `safe inference` and dispatches even though the opposite assumption would materially change the deliverable, permissions/risk, acceptance, or cause major rework.
- The frozen task contract or dispatch writes an unsupported assumption as `confirmed`.
- C dispatches instead of stopping when critical endpoint, permission, or acceptance information is missing.
- Missing root cause leads to a quick fix, or acceptance counterexamples expand into defensive whole-project review.
- A task expands into whole-project re-review only because of a `high risk`/release label, file
  count, or change size.
- Current external authority, artifact/source mismatch, credible false-green evidence, or
  inaccessible old evidence has invalidated a premise, but C silently retains the old acceptance,
  repair, or release conclusion.
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
- An ambiguous create timeout, error, or partial result is retried before bounded authoritative
  reconciliation.
- An immediate zero-candidate listing after ambiguous create is treated as definite failure and
  automatically creates again.
- A pending create is not authoritatively reconciled before a later resume, startup, or creation of
  the same role, so a delayed orphan task is missed.
- A task's self-reported `local` alias is used as authoritative routing when official metadata
  disagrees.
- Formal work is sent to a selected duplicate before every candidate is proven zero-write, proven
  not to have received formal work, and every unselected candidate confirms stop.
- Archive state, title, or merely sending a stop instruction substitutes for direct-push stop
  confirmation.
- A duplicate candidate has neither direct-push stop confirmation nor an official non-working
  terminal state, but another candidate starts work.
- A duplicate E1 may have written, but work continues without restoring one writer and reading back
  workspace state.
- A formal batch lacks a stable `batchId` or does not bind it to the selected threadId, current
  actual hostId, cycle, target root, monotonically increasing `batchSeq`, and immutable
  `payloadDigest`.
- The same `batchId` carries different content or `payloadDigest`, or changed content keeps the old
  `batchId`.
- A batch is treated as complete immediately after `BATCH_RECEIVED`, or every repeated `batchId` is
  blindly ignored or blindly rerun without consulting lifecycle state.
- An `IN_PROGRESS` interruption or partial write reruns the batch without `STATE_UNKNOWN` and
  writer/workspace recovery.
- A repeated `RESULT_READY` delivery does not replay the stored result, or the batch is permanently
  ignored before `RESULT_ACCEPTED`.
- A ready, accept, stop, state, result, or result-acceptance message lacks stable `messageId`, or an
  ambiguous outcome causes blind resend or permanent waiting.
- An ambiguous send uses a new `messageId` or `batchId` to bypass deduplication.
- A higher-`batchSeq` revision is dispatched or started before the old batch is canceled zero-write,
  terminated, or fully recovered, or a delayed `SUPERSEDED`/lower-sequence batch still executes.
- "Read only after push" is used to refuse bounded exact-`messageId` failure recovery and wait
  forever, or failure readback is used as a substitute for complete communication preflight.
- Adaptive acceleration remains active while communication, batch lifecycle, single-writer state,
  source freshness, or evidence identity is uncertain.
- Old evidence is reused after the reviewed object, requirements, direct dependencies/environment,
  artifact, validation method, or credible counterevidence has changed.
- Review, evidence, audit, or failure recovery is skipped solely because of `no_material_delta` or
  zero file writes.
- Required fresh-R review for irreversible or high-consequence action is delayed until after action.
- Co-scheduled checks lose individual output, exit status, provenance, or adjudication, or
  order-dependent/shared-mutable-state checks are mixed together.
- A fork carrying source context is counted as fresh UAT.
- The assignee does not return `ready/result`, but the loop is still claimed.
- A new task lacks a visible `E1:`/`R1:` title or first-line label, or receipts omit session/thread coordinates.
- C repeats event waits, waits again after timeout, discovers results by polling, or accepts a wait
  snapshot, task completion state, commentary, or summary as ready/result evidence.
- The `BATCH_RECEIVED` wait wrongly consumes the final-result wait budget, leaving a direct-pushed
  result unable to advance.
- A controlled resend with the same `messageId` is treated as a new logical send and can reopen
  event waits indefinitely.
- The platform requires an event wait to wake an idle C, but C absolutely forbids the single bounded
  event wait, so an already direct-pushed READY/result cannot advance.
- A knowledge-heavy task lacks a defined knowledge foundation, or R checks only format instead of challenging specialist claims.
- Every internal step gets a card, or a material decision, blocker, or staged delivery gets no card.
- A bear card does not first read this Skill's `VERSION`, treats `v1` as the package version, or
  guesses from the network, a Git tag, GitHub Release, or lock metadata.
- A missing, unreadable, or malformed `VERSION` does not render `version unverified`.
- A start card puts version or status on a separate line, or does not preserve the complete three-line
  bear and fixed `·` markers after its foot on the third line.
- Any CER bear card still uses `>` for the foot and is rendered as a Markdown block quote.
- A release or upgrade does not update `VERSION` first.
- A single-batch `CER-start` has no fixed start card, or its start card wrongly uses closed eyes.
- Stop/close shows a closed-eye success card before proving the writer stopped and completing
  required readback; close shows the closed-eye card before reading back title sync or
  `title sync warning`; a failed title rename is claimed as renamed; or a blocked state omits the
  open-eye red blocker card.
- A new C after close reuses the previous cycle's E1 or R task/coordinate.
- The old-cycle title prefix has no `✓` and no real `title sync warning`, but close title sync is
  claimed complete; lifecycle close is accepted from title-only or text-only evidence.
- Complete role coordinates are known with no contradiction, but close alone causes broad project
  task enumeration, a fixed set of status-file updates, a full validator/doctor run, or a Reviewer.
- Role coordinates conflict or writer state is unknown, but proportionality is used to refuse
  wider readback.
- A later batch in the same cycle fails to reuse the same E1, and creates another writer before
  E2 takeover conditions are met.
- A second C starts while old C state or a participating host cannot be verified.
- Mermaid is substituted for available inline visualization instead of being supplemental.
- Ordinary small changes always create fresh R or trigger full-project review.
- CER creates a fixed five-document project set or parallel progress source.
- `$project-context-workflow` is treated as a CER installation prerequisite.
- `/CER-stop` is followed by new E1/R work, or single-thread work resumes before an active writer is proven stopped.
- `/CER-status` triggers polling or background monitoring.
- Only documentation or a local technical step succeeds, without a real deliverable.
