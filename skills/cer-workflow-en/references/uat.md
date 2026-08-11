# CER Core v1 Fresh UAT

## Contents

- [Installation Scenario](#installation-scenario)
- [Adaptive Execution Profile Scenarios](#adaptive-execution-profile-scenarios)
- [Full Flow](#full-flow)
- [Remote Controller Scenarios](#remote-controller-scenarios)
- [Cross-Cycle Isolation Scenarios](#cross-cycle-isolation-scenarios)
- [Codex Task Topology Scenarios](#codex-task-topology-scenarios)
- [Ambiguous Tool Outcome And Batch Deduplication Scenarios](#ambiguous-tool-outcome-and-batch-deduplication-scenarios)
- [Adaptive Batch Acceleration Scenarios](#adaptive-batch-acceleration-scenarios)
- [Parallel Candidate Producer Counterexamples](#parallel-candidate-producer-counterexamples)
- [Review Convergence Scenarios](#review-convergence-scenarios)
- [Controller Preflight QC Scenarios](#controller-preflight-qc-scenarios)
- [Controller Long-Task Challenge Scenarios](#controller-long-task-challenge-scenarios)
- [Outcome Anchor And Progress Scenarios](#outcome-anchor-and-progress-scenarios)
- [Unexpected Failure And Scope-Exception Scenarios](#unexpected-failure-and-scope-exception-scenarios)
- [Acceptance Validity Scenarios](#acceptance-validity-scenarios)
- [Proportionate Close Scenarios](#proportionate-close-scenarios)
- [Kit Authority Pass-Through Scenarios](#kit-authority-pass-through-scenarios)
- [Failure Conditions](#failure-conditions)

Fresh UAT must run in an independent clean project through sidebar-visible official new tasks. A
task created, forked, or delegated by C in the source project carries source context and is not
fresh.

A successful title change, fork, delegation, one-way message, or tool parameter does not prove a closed loop. E1 must direct-push both `ready` and `result`.

AI real workflow UAT PASS is the closed-loop evidence above, not an obligation to wait. After
the bounded wait, reconciliation, or controlled resend permitted by this file is exhausted, if
the assignee still has not direct-pushed a zero-write `ready` or `result`, C must adjudicate
that UAT attempt as FAIL or `delivery_unavailable` according to the evidence and stop that
attempt. Do not create repeated same-shape tasks, poll, keep background waiting, or fill the
gap with a sub-agent, fork, or text simulation as PASS. Use the static-only downgrade below
only when the required task/delivery toolchain or clean workspace is proven unavailable for
that run; ordinary non-completion or missing evidence is not a downgrade.

For this Codex project's Full Audit, when official `create_thread` task tools and a clean UAT
workspace are available, AI real workflow UAT is required and cannot be replaced by a sub-agent,
fork, or text simulation. If the required task/delivery toolchain or clean workspace is proven unavailable, the only allowed
downgrade claim is `Full Audit passed (static corpus only; AI real workflow UAT unavailable)`, and
it must not claim AI UAT passed. Post-release user manual UAT is a separate layer for public
installation and user experience, reported separately as `not run`, `passed`, or `failed`; AI UAT
must not be reported as manual UAT.

AI real workflow UAT evidence must list actual thread ids for both cycles and perform mechanical
comparison: same-cycle batches keep the same E1 threadId; C2 threadId differs from C1; cycle-2 E1
threadId differs from cycle-1 E1; every cycle-2 R is a new threadId that differs from every cycle-1
R and does not reuse an earlier R in the same cycle. Text that merely says fresh is insufficient.

Each outer UAT cycle C is also a delegated assignee of the release dispatcher: before cycle work
starts it must direct-push a zero-write `ready` to the main-session return target; at completion,
blockage, or checkpoint it must direct-push a structured `AI_UAT_CYCLE_N: PASS/FAIL` result to the
same main target before ending. The dispatcher must not automatically use `wait_threads` or
`read_thread` to wait, wake itself, track, or read outer UAT. After dispatch it enters
`POST_DISPATCH_PARKED` until direct-push becomes main-session input. Only after receiving that
direct-push may it perform one bounded readback for verification or adjudication; a one-time check
explicitly requested by the user in the same turn is diagnostic only, not formal delivery evidence.
A child-C final answer, wait
snapshot, passive thread read, task title, or user-relayed notice that the UAT task is done is not
formal delivery evidence and cannot satisfy AI real workflow UAT or release-readiness by itself. If
the outer return protocol is missing, the dispatcher may request one bounded delivery-repair push
from the same cycle C using its existing final evidence; until that push is received, the cycle is
`delivery_incomplete`, not a passed UAT cycle.

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
- The Skill root `VERSION` is one stable-semver line. Read it again before every bear card,
  replace the `{package_version}` template completely, and show `version unverified` when it is
  invalid. Never display the placeholder itself.
- A new C can start from only the Skill and the user's overall task.
- The default prompt says to create a fresh Reviewer in proportion to risk; it does not force a
  Reviewer for simple work.
- `/CER-auto` and `Run CER adaptively` trigger the local execution profile gate; no C exists before the route decision.
- `/CER-start` and `Start CER` trigger CER; a plain start/work message does not.
- `/CER-close` and `Close CER` trigger CER close; a plain close/finish message does not close CER and does not map to `/CER-stop`.

## Adaptive Execution Profile Scenarios

- For local `/CER-auto`, a low-risk task with clear authority, one writer, reversible changes, no external side effect, and sufficient existing acceptance outputs one `Route: ordinary execution — <reason>` line, creates no C/E/R identity, shows no bear card, and stops loading other CER references.
- When the execution-profile gate and decision sources have known paths, share one safe read boundary, and have no permission or scope difference, obtain them in one bounded read with no selector-only read roundtrip. Keep them separate when safety or boundaries differ; speed does not permit broader or unauthorized reading.
- Ordinary execution may use an ordinary subagent under target-project rules, but that subagent receives no formal E/R identity, ready/result lifecycle, or Reviewer effect.
- When an existing current-state owner has already decided the target state and only local, reversible metadata reconciliation by one writer remains in the same workspace, with no official-acceptance decision, model recalculation, or external consequence and direct readback is sufficient to disprove error, `/CER-auto` may remain ordinary execution. A persistent-state file alone must not create C/E/R.
- For local `/CER-auto`, a longer, multi-step, or closed-loop task whose endpoint, verification loop, stop condition, and known authority sources are clear, and that does not yet accept the result as formal data, model input, a report paragraph, a decision gate, handoff truth, a release/readiness claim, or a public/external claim, outputs one `Route: Goal — <clear endpoint and verification loop>` line. Goal receives no C/E/R identity, sole writer, Reviewer effect, or authority owner.
- If the endpoint, acceptance loop, stop condition, or authority source is still vague, use ordinary diagnostic/narrowing or `Route: blocked — <missing authority/safety/acceptance condition>` instead of entering Goal directly.
- For local `/CER-auto`, when a Goal or E1 output is about to be accepted as formal data, model input, a report paragraph, a decision gate, handoff truth, a release/readiness claim, a public/external claim, or would cause an external/irreversible/permission/paid effect, output one `Route: CER Workflow — <why CER is needed and where to stop>` line only at that point that needs CER, then load the runtime/roadmap in full and perform the current CER startup.
- If authority sources, safety boundaries, acceptance conditions, root/permission, Goal capability with no safe fallback, reversibility, or authorization for an external/irreversible operation are missing, output one `Route: blocked — <missing authority/safety/acceptance condition>` line and do not present process completion as outcome completion.
- If metadata reconciliation still decides the owner, artifact role, accepted outcome, official acceptance, model result, or external consequence, ordinary execution cannot reliably disprove the risk and must select CER Workflow or block. An unresolved truth conflict must not be relabeled as a mechanical correction to step down.
- Multiple files, long text, or a long-task label with low consequence and reversible work do not independently select CER Workflow. A one-line task involving deletion, release, official acceptance, or a high-consequence decision selects CER Workflow or blocks. Token pressure does not override safety or an owner.
- Treating source count, schema, hash, or receipt as authority evidence must fail. Citing `CER_docs/09` as runtime routing authority must also fail because runtime ownership stays in `core-runtime.md`.
- If one task contains a low-risk source map followed later by formal model/report/handoff acceptance, the source-map stage remains ordinary or Goal and only the later point that needs CER selects CER Workflow; do not promote the entire task to CER just because a later gate exists. If Goal is unavailable but bounded ordinary execution can safely finish, do not automatically block. If an external claim is only background context and not a formal claim, do not automatically select CER Workflow.
- Explicit `/CER-start` is never adaptively downgraded. It still enters full CER with the existing unique-C, start-card, E1, Reviewer, result-disposition, stop, and close semantics.
- Remote `/CER-auto` must stop as unsupported in the first version and must not create or guess a Remote C. Explicit Remote `/CER-start` still follows the existing Remote Controller scenarios.
- Adaptive recheck occurs only when user requirements/authority/consequences change, at a phase boundary, when result disposition changes carry-forward/progress/authority effect, or before an external/public/irreversible/high-consequence operation. Ordinary small steps and token pressure do not trigger a recheck.
- Existing Reviewer ownership still decides whether R is required, and the target project's existing release owner still decides release assurance. The adaptive route decision cannot force, skip, or replace either owner, and Goal cannot replace the Reviewer, release owner, or official-acceptance owner.
- Before CER entered through `/CER-auto` steps down to ordinary execution or Goal, there is no active batch, E1 has stopped writing, results and result disposition are read back, required persistence is read back, and no truth conflict remains. The transition does not impersonate `/CER-stop` or `/CER-close` and shows no stop/close card.
- Before ordinary execution or Goal steps up to CER Workflow, stop and read back the ordinary/Goal writer. Ordinary drafts, diagnostics, Goal output, and subagent output remain working material. Only a source explicitly accepted by an existing target-project owner retains authority, and E1 rereads the workspace baseline before its first write.
- After `/CER-auto` selects CER Workflow, it still follows the existing startup order in full: before a valid zero-write E1 `ready` is direct-pushed and read back, it shows no successful startup card and dispatches no formal batch.
- A transition in the same task with no material artifact, adjudication, or risk carry-forward creates no checkpoint. A cross-task/session/context transition or material carry-forward puts the checkpoint only in an existing handoff/current-state owner or the next self-contained dispatch; it creates no new file, fixed YAML, schema, or registry.
- A required checkpoint reads back the direction and reason, current objective and outcome owner, unfinished condition and next observable delta, latest result disposition, accepted facts versus working material and forbidden carry-forward, writer/persistence/baseline readback, and open risk plus next allowed action. It does not rewrite an owner. Missing or conflicting required readback keeps the next write or dispatch blocked.

## Full Flow

1. The user submits a clear multi-batch task or existing plan using `Start CER: ...` or `/CER-start ...`.
2. C identifies the main task with a `🚀 C:01｜<very short task name>` title or first-line label and completes Controller preflight. A complete task passes directly; sourced `confirmed` items and `safe inference` items that pass the counterfactual test do not block; missing critical endpoint/permission/acceptance information produces a yellow checkpoint with at most three questions.
3. C completes communication preflight, uses official `create_thread` to create a brand-new
   sidebar-visible persistent `E1:01｜...` task in the same Codex project. After the
   `create_thread` receipt, C immediately uses the official title tool, currently
   `set_thread_title` in Codex, to set or rename the title and read it back; the initial prompt,
   model-generated title, or first-line label does not substitute for this when the title tool is
   available. C then reads back the thread ID and formal return path, and receives a `ready` direct-push containing threadId or
   platform-equivalent coordinates. sessionId is recorded only when the active tool schema/receipt
   explicitly requires or provides it, and never substitutes for threadId or derives hostId. If the actual platform does not automatically wake an idle C, C still stays
   `POST_DISPATCH_PARKED` and must not wait by itself; a wait snapshot is not ready evidence.
4. C maps existing target-project sources of truth and the task knowledge foundation without creating fixed CER documents.
5. For every successfully accepted `CER-start`, C's first user-visible success receipt is the
   fixed open-eye `CER Workflow v{package_version}` / `🔵 CER started` card. Before output,
   replace the placeholder from `VERSION`; keep the complete three-line ASCII bear with version on
   the first line, status on the second line, and only the bear base line on the third line; output it as
   a standalone fenced `text` code block, including single-batch work. Multi-stage,
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
    back; on failure, it reports `title sync warning` with failed coordinates. If the cycle has
    complete, read-back, adjudicated R tasks, C may archive those R tasks while keeping C and E1
    visible; the close summary states that archive is not deletion and the tasks remain available
    from archived tasks. Only after that does C show the fixed closed-eye `🟢 CER closed` /
    `writer closed` card. If no durable source exists, CER does not claim full cross-session
    recovery.
11. Run a separate composition scenario with `$project-context-workflow`: CER does not rebuild documents or take over consensus gates, and the context workflow does not create C/E1/R.
12. Run a separate stop scenario with `/CER-stop`: C sends no new E1/R work and, if E1 is
    writing, reaches `writer closed` or a major blocker. Only after proving no active writer and
    completing required readback may C show the fixed closed-eye `⚪ CER stopped` /
    `CER inactive` card and return to one thread.

## Remote Controller Scenarios

- When an explicit Remote `/CER-start` or equivalent CER-qualified start designates a receiver task, that receiver first direct-pushes candidate `C_READY` with threadId or a platform-equivalent coordinate, target_root, return target/path, and any return or routing coordinate explicitly required by the active tool schema/receipt; it must not guess hostId.
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
- C may use inline parallel candidate producers under
  [parallel-producers.md](parallel-producers.md). They are not formal roles, do not enter role
  titles, cycles, or lifecycle cards, and cannot replace E or R.
- If `create_thread`, official title-tool set/readback evidence after `create_thread`,
  sidebar-visible title, verifiable thread ID, or formal return path is
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
- When the platform does not automatically wake an idle C, C still does not use `wait_threads` or
  `read_thread` to wait by itself; after dispatch it stays `POST_DISPATCH_PARKED`. Only when E1's
  direct-push READY/result becomes main-session input may C perform one bounded readback for
  verification or adjudication.
- When one batch needs `BATCH_RECEIVED` and then a final result, each must arrive by its own
  direct-push. The first direct-push does not mean the final result has arrived and does not
  authorize C to wait automatically for the next state transition.
- The create prompt for a new E1/R is a zero-write ready handshake; a complete corpus or formal
  batch payload is sent exactly once in the formal `sendable_packet` after ready, or split into
  multiple formal batches by semantic/risk unit.
- If the create prompt already contains the complete corpus and causes E1 to process content
  before ready, the ready is not qualifying zero-write even when the later formal batch uses the
  same digest and E1 can deduplicate it; C stops or refreezes, and does not treat the duplicate ack
  as normal efficient communication.
- After timeout for one expected message, only reconciliation plus the single controlled resend
  with the same `messageId` is allowed; after the resend C still stays `POST_DISPATCH_PARKED`.
  Extra control messages or renaming cannot reopen a wait or polling budget.
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

## Parallel Candidate Producer Counterexamples

- When two lanes are independent, inputs are frozen, C has non-duplicative concurrent work,
  candidates are independently verifiable, net time savings are material, and execution slots
  are available, two candidates may arrive naturally and C may converge them.
- For a simple bounded read, no subagent capability, uneconomic parallel cost, or any uncertain
  eligibility condition, `producer_count=0`; C completes serially and the user does not configure
  lanes, scratch roots, hashes, or roles.
- A `read_only` lane that attempts any write is invalid.
- An artifact scratch root inside the project or one of its ancestors, at a drive root, user root,
  system root, symlink, junction, reparse point, mount, equal to or ancestral to another lane, or
  used for an out-of-bounds write does not start or fails closed.
- When frozen input drifts in only one lane, discard only the dependent candidate and do not rerun
  unaffected candidates.
- When sources conflict, C adjudicates from authoritative sources and not by vote, completion
  order, or matching majority answers.
- A late candidate, producer failure, unreplayable source, or artifact hash tamper invalidates the
  candidate. Producer failure alone does not block CER unless the missing evidence is the task
  blocker.
- A producer impersonating E/R, sending directly to E1, E1 using unconverged scratch, or
  C/R/producer writing the target project makes the whole dependent candidate fail closed.
- `/CER-stop` or `/CER-close` does not wait for a producer; a late candidate cannot reopen a
  closed intake.
- Producers receive no formal title, cycle, ready, result, slash, lock, registry, or run id.
  Roadmap role columns and lifecycle cards still contain formal roles only.

## Review Convergence Scenarios

- After R first reports a defect, related findings are grouped by common root cause and user consequence. C performs one bounded impact check to find this round's current owners, affected surfaces, and check locations.
- After a frozen objective already has a material E/R result, C must not create another E/R task or task branch for the same root cause unless it can identify a new falsifying question and show that the branch is the smallest necessary way to advance the original goal or handle a verified blocker; otherwise C consolidates, stops, or adjudicates directly.
- When one set of findings contains two issues that differ only in wording or sentence order but share the same root cause and user consequence, plus one issue with a different root cause, different user consequence, or a new regression caused by the latest repair, C merges the first two into one convergence scope and batch while keeping the third as a valid expansion.
- C freezes acceptance and the counterexample family, and the same E1 repairs the whole affected boundary in one batch. After the repair, R re-tests only the frozen scope.
- Synonymous wording does not open another sentence-by-sentence repair cycle. C accepts and stops after the frozen counterexample family passes with no material new defect.

## Controller Preflight QC Scenarios

- When the user gives a natural-language task that is sufficient to start a small batch but omits reversible details that would not materially change the outcome, C may mark them `safe inference` and continue.
- If missing information has multiple reasonable answers and different answers would materially change the deliverable, permissions/risk, acceptance, or cause major rework, C must mark the item `critical missing` and stop for questions.
- For a fuzzy but startable multi-batch task, C creates a living task brief that preserves confirmed requirements/exclusions, safe inferences, critical gaps, latest user feedback, current batch freeze, and the next observable preview or decision point. C freezes only the next safely executable batch; it does not require the user to write a complete specification first, does not treat `$project-context-workflow` as a prerequisite, and does not create fixed project documents.
- After the user sees an intermediate result and changes direction or adds a constraint, C first updates the living task brief and roadmap delta. If an already-dispatched batch is affected, C uses a new `batchId`/`payloadDigest` or supersedes the old batch before returning to the same E1. It does not continue with stale assumptions.
- R reviews against the latest task brief, current batch freeze, candidate identity, and delivery evidence; it must not review only against the initial prompt or stale assumptions.
- C's current batch freeze and E1/R dispatches preserve the three states, required source anchors, and counterfactual results. They must not invent user confirmation.
- Before a non-simple formal implementation batch, C can answer each truth-source intake question: who owns it, who actually uses it, how it takes effect, and what counterexample can disprove it. The answers are only a Controller preflight and self-contained-dispatch summary, not a second rule owner.
- If C cannot answer any truth-source intake question, or if an answer depends on an unread required source, that completion condition is `critical missing`. C does not dispatch a formal implementation batch and only performs necessary read-only diagnosis, narrows the acceptance scope, or stops for user decision.
- A formal packet for long-running, multi-batch, high-risk, or non-simple formal implementation work includes compact `pre_dispatch_evidence` that reads back the `outcome_anchor` pointer, target unfinished condition, expected outcome difference, truth-source intake four-question summary with source anchors, required-source read/unknown disposition, work-lane classification, and drift checkpoint conclusion or no-trigger reason; if it is missing, E1/R only returns a zero-write `BATCH_BLOCKED_MISSING_PRE_DISPATCH_EVIDENCE`.

## Controller Long-Task Challenge Scenarios

This section composes the existing preflight, `outcome_anchor`, drift, YAGNI, and result-disposition owners for QA. It adds no runtime field or new workflow:

- When the user's task lacks a measurable or readable endpoint and materially different completions are plausible, C performs only necessary diagnosis, narrows the next observable acceptance point, or stops for questions; it does not dispatch a production batch and invent the specification afterward.
- When required authority, allowed boundaries, or counterexample evidence is insufficient, C does not promote an ordinary draft, search output, or its own inference. A safely bounded diagnostic may remain ordinary; otherwise the route blocks.
- When a plausible adjacent request, process improvement, or substitute deliverable appears mid-task, C first decides whether it serves an unfinished `outcome_anchor` condition. It must not replace the mainline or contaminate mainline progress.
- Missing specification, risk, or acceptance uncertainty is not a reason for defensive expansion. C does not invent a registry, governance document, whole-repo review, fixed Reviewer, Full Audit, or more roles instead of narrowing the problem.
- After the user changes a requirement, boundary, or acceptance condition that affects the outcome, C updates the living brief and current batch freeze first. A candidate that depends on the old condition cannot retain its old acceptance identity.
- The same long task rechecks only at the defined material boundaries. Small steps, one test result, token pressure, or demonstrating the process must not cause ordinary/CER route thrashing.

## Outcome Anchor And Progress Scenarios

- Long multi-batch work fixes `outcome_anchor` before the first batch, preserving the user's final outcome, source pointers for completion conditions, unacceptable substitute outcomes, and exclusions. E1 or R cannot rewrite it in later batches.
- An implementation batch with zero expected outcome improvement and no necessary-prerequisite role is rejected. C may relabel it as diagnostic, stop for questions, or choose a batch that improves a completion condition.
- A diagnostic batch may run and produce a handoff prerequisite, but it is classified as `diagnostic` and does not increase mainline progress.
- Technical checks, format, file consistency, or review may pass, but when `outcome_anchor` has no accepted outcome difference, the batch is not marked as successful progress.
- After two consecutive unresolved attempts in the same failure class, a third same-class repair is intercepted. Renaming, version changes, repackaging, or redispatching the same method is still treated as the same retry class.
- R must reject a batch that diverges from the original outcome, is only technical activity, repeats rework, or substitutes another deliverable shape for what the user asked for.
- `mechanism_improvement` or `governance_self_improvement` does not contaminate mainline progress; it becomes a mainline blocker only when proven necessary for completing `outcome_anchor`.
- Adjacent improvement failure does not automatically block the original task. C either records it separately or proves that its absence makes the mainline unsafe to accept.
- For long-running, multi-batch, or context-pollution-prone work, C performs one bounded drift checkpoint at resume/context transition, after two consecutive batches with no accepted outcome difference, on the second same-class failure, when E1/R proposes an adjacent direction change or substitute deliverable, when the user changes direction or adds constraints, and before close/release/major delivery. If C cannot identify which unfinished `outcome_anchor` condition the next batch improves, the readable outcome difference success will create, or whether E1/R's adjacent proposal is replacing the mainline, C does not dispatch a formal implementation batch and only switches to diagnostics, narrows acceptance, stops for user decision, terminates the route, or creates a fresh R in proportion to risk.
- A drift checkpoint, living task brief, or roadmap update does not count as outcome progress and does not trigger background monitoring, polling, automatic `wait_threads`, fixed R, or fixed Full Audit.
- Simple, one-step, low-risk work with one clear endpoint still uses lightweight summary and C readback. Do not force an outcome-anchor table, R, or roadmap.
- Completion reporting lists accepted outcome differences and unfinished conditions, not batch, task, review, or candidate counts as completion evidence.
- When a Reviewer passes candidate content, C may accept it as `working_candidate` or `evidence_only`, but must not classify it as `authoritative_input` merely because content passed.
- When a `derived_output` is listed by the next batch as `authority_input` without an explicit user decision, target-project owner anchor, or promotion readback, C must stay at `dispatch_blocked`; if E1/R receives an unclassified prior result as authority input, it returns only a zero-write blocker.
- When `prior_result_use: authority_input` is missing `promotion_evidence` or `project_owner_anchor`, C must not hand the prior result to the next batch; `prior_result_use: working_material` permits only editing, comparison, review, or refinement, not decision authority.
- When a candidate is used only as refinement working material, C may set `prior_result_use` to `working_material` and continue, while `authority_effect` and `progress_effect` remain `none`.
- When a Phase 1 candidate completes only a non-terminal checkpoint, the legal disposition is `accepted_as=working_candidate`, `authority_effect=none`, and `progress_effect=none`; put phase and Phase-2-only use limits in the existing `phase`/`status` and `permitted_next_use`.
- When Reviewer technical PASS has outcome FAIL, or authority promotion was not reviewed, C must not report mainline progress or authority promotion.
- When Reviewer provides only `content_verdict: pass` or `implementation_verdict: pass`, while `outcome_verdict` is `fail`/`not_reviewed` or `authority_promotion_verdict` is `out_of_scope`, C may adjudicate only the reviewed dimensions and must not expand that into outcome PASS or authority-promotion PASS.
- When handoff, plan, progress, or another target-project source of truth conflicts about artifact role, next action, or authority source, the next batch is not dispatched until the existing owner synchronizes and C reads it back.
- When result disposition changes current phase, artifact role, next product route, authoritative source, progress claim, or later batch input, but target-project persistence has not been updated and read back under existing rules, `next_dispatch` must be `blocked`.
- When the final batch produced a correct deliverable but the target-project current-state owner still records the old phase, no terminal deliverable, or a stale next action, C must not accept a `terminal_deliverable`, report progress, or claim completion even though there is no next batch.
- When the model, report, and current-state owner in one terminal set are synchronized but a `RUN_RESULT` classified as a `terminal_deliverable` still says persistence pending, unaccepted, or an old phase, C must not accept the set; it must demote that file to `evidence_only` / exclude it, or correct and revalidate it under the original acceptance. If it was explicitly classified from the start as pre-persistence `evidence_only` outside the terminal set, its historical state may remain unchanged.
- When the user's endpoint itself is a draft, candidate, or sample, the candidate may validly become `terminal_deliverable`; without a separate owner basis, it still must not become an authoritative source.

## Unexpected Failure And Scope-Exception Scenarios

These scenarios only test the unexpected-failure gate in
[core-runtime.md](core-runtime.md); they do not define another rule:

<!-- cer-uat-unexpected-failure:gate-off -->
- An ordinary batch with no unexpected failure does not activate the gate or add a baseline,
  form, or reporting procedure.
<!-- cer-uat-unexpected-failure:caused -->
- The current batch directly caused a regression and the repair preserves frozen meaning, owner,
  source, and permission: E1 may repair it in the current batch. A purely technical refactor that
  preserves output, sources, owners, and cross-subsystem behavior may also continue.
<!-- cer-uat-unexpected-failure:preexisting -->
- A comparable pre-batch baseline proves the failure already existed: E1 reports without repair.
<!-- cer-uat-unexpected-failure:unknown -->
- No comparable baseline is available, or a flaky test, environment, or dependency leaves
  causality unknown: E1 stops further writes without a guessed repair.
<!-- cer-uat-unexpected-failure:semantic-boundary -->
- A file is in allowed scope, but repair would change another owner, authoritative source,
  fallback, admission condition, or cross-subsystem behavior: E1 stops. Tests or an allowlist/diff
  check that pass only because of that expansion are still false-green.
<!-- cer-uat-unexpected-failure:acceptance-boundary -->
- A direct acceptance test may be wrong, or full regression outside direct acceptance fails: E1
  attributes and reports without changing product meaning or automatically repairing adjacent
  behavior. Full regression in frozen acceptance may block the candidate but still does not expand
  repair authority.

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
- After successful close, complete, read-back, C-adjudicated R tasks may be archived to reduce
  sidebar clutter; C and E1 remain visible by default. Active, blocked, not-returned, or
  unadjudicated R tasks are not archived. Archive is not deletion and must not count as stop,
  review, or closeout evidence; when archiving happens, the close summary states in the same output
  language that the tasks remain available from archived tasks.
- Every CER bear card uses the Handoff Kit layout-style three-line ASCII card. The card must be
  output as a standalone fenced `text` code block so the Markdown container cannot change its
  alignment.
- Keep the complete three-line bear: version only on the first line, status only on the second
  line, and only the bear base line on the third line.

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
- A parallel candidate producer writes the target project, produces formal ready/result, replaces
  E/R, or is counted as CER Reviewer acceptance evidence.
- E1/R lacks official `create_thread` creation evidence, official title-tool set/readback
  evidence after `create_thread`, sidebar-visible title, verifiable thread ID, or formal return
  path, but work still starts.
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
- `/CER-auto` claims C before the route decision, preloads all CER references, or shows a CER bear card on ordinary execution.
- After `/CER-auto` selects CER, it shows a successful startup card or dispatches a formal batch before a valid zero-write E1 `ready` is direct-pushed and read back.
- Explicit `/CER-start` is automatically downgraded to ordinary execution, or Remote `/CER-auto` is treated as supported and creates a Remote C.
- File count, word count, a long-task label, or token pressure alone changes the route; or token saving bypasses safety, authority, persistence, external authorization, the Reviewer owner, or the release owner.
- The route steps down to ordinary execution while an active batch/writer, incomplete result disposition, unread required persistence, or a truth conflict remains.
- An ordinary draft, diagnostic, or ordinary-subagent output becomes authoritative input when stepping up to CER, or E1 writes before rereading the workspace baseline.
- Every small step or same-task transition with no material carry-forward is forced to create a checkpoint, or a cross-task/session/context material carry-forward lacks the required checkpoint.
- A route-transition checkpoint creates a new file, fixed YAML/schema/registry, rewrites an outcome/authority owner, or allows the next write or dispatch while required readback is missing or conflicting.
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
- The initial prompt is treated as an immutable complete specification for the whole cycle, or C dispatches the next batch after a user direction change without updating the living task brief and roadmap delta.
- E1 treats provisional later direction as a complete specification and implements an unfrozen future batch, or R rejects a candidate only against the initial prompt or stale assumptions.
- The living task brief is written as another process, fixed document set, or new role instead of being part of the existing Controller preflight and roadmap.
- The current batch freeze or dispatch writes an unsupported assumption as `confirmed`.
- A non-simple formal implementation batch has not answered who owns it, who actually uses it, how it takes effect, and what counterexample can disprove it, but C still creates/reuses E1 or dispatches the implementation batch.
- C expands the truth-source intake gate into default full-text ingestion, whole-repo review, fixed Full Audit, a second rule owner, or a fixed form workflow.
- A long-running, multi-batch, high-risk, or non-simple formal implementation packet lacks `pre_dispatch_evidence`, or only says "C already judged" without readable support, and E1/R still writes, reviews, or fills in C's missing judgment.
- C dispatches instead of stopping when critical endpoint, permission, or acceptance information is missing.
- Long multi-batch work lacks `outcome_anchor`, or later E1/R rewrites the final outcome, completion conditions, substitute outcomes, or exclusions.
- An implementation batch with zero expected outcome improvement and no necessary-prerequisite role is still dispatched.
- Diagnostics, candidates, reviews, format pass, file consistency, logged issues, design completion, renaming, or version changes are automatically counted as mainline outcome progress.
- Technical checks pass but there is no `outcome_anchor` outcome difference, and C reports successful progress.
- After two consecutive unresolved same-class attempts, C dispatches a third same-class repair, or hides a same-method retry by renaming, versioning, or repackaging it.
- R checks only technical validity and does not check whether the batch serves the original outcome, is only activity or rework, or substitutes for the user's requested deliverable.
- Generic mechanism improvement or governance self-improvement contaminates mainline progress, or its failure blocks the original task before a necessary dependency is proven.
- After two consecutive batches with no accepted outcome difference, C dispatches another mainline implementation batch without a drift checkpoint.
- After E1/R proposes an adjacent direction change, substitute deliverable, or out-of-scope blocker, C rewrites the next mainline batch without classifying whether that proposal replaces the mainline outcome.
- A drift checkpoint, living task brief, or roadmap update is counted as outcome progress.
- A drift checkpoint triggers background monitoring, polling, automatic `wait_threads`, fixed R, or fixed Full Audit.
- Simple, one-step, low-risk work with one clear endpoint is forced to run a drift checkpoint.
- Completion reporting lists only batch, task, Reviewer, or candidate counts without accepted outcome differences.
- C sends bare `RESULT_ACCEPTED` and treats the candidate as mainline progress, authoritative input, or a source consumable by the next batch.
- A candidate/draft/diagnostic/derived_output/review_only result is listed by a later batch as `authoritative_input` without promotion evidence.
- R gives only content or technical PASS, and C derives outcome PASS, authority promotion PASS, or `accepted_outcome_delta`.
- A result that changes phase, artifact role, next route, authoritative source, progress claim, or later batch input has not been persisted and read back under target-project rules, but C still dispatches the next batch.
- Because the final batch has no next batch, C accepts a `terminal_deliverable`, reports progress, or claims completion while the current-state owner is still contradictory or stale.
- C includes an artifact that still says persistence pending, unaccepted, an old phase, or an old next action in the accepted terminal artifact set, then claims completion because the other files and current-state owner are synchronized.
- C uses an out-of-contract synonym in an actual result disposition, such as `accepted_as=terminal_outcome`, instead of one of the four existing `accepted_as` values, while Reviewer or the current-state owner still treats it as a valid terminal adjudication.
- C or the writer synthesizes Phase 1 scope as `progress_effect=accepted_outcome_delta_for_phase1_only` or another out-of-contract value and writes it to persistent truth instead of blocking before persistence.
- E1 treats a test failure as new modification authority, or treats an allowed file as authority to
  change every meaning in that file.
- E1 continues writing while causality is unknown or repair would widen an owner, authoritative
  source, fallback, or admission condition, then treats passing tests as proof of correctness.
- Full-regression failure automatically triggers an adjacent repair, or E1 expands scope without C
  refreezing and dispatching a new batch.
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
- A formal `sendable_packet` still contains `<...>` placeholders, or lacks actual `threadId` /
  platform-equivalent coordinate, `returnTarget`, `messageId`, `batchId`, `batchSeq`,
  `payloadDigest`, or routing coordinates explicitly required by the active tool schema/receipt,
  but is still self-rated PASS.
- When the active tool schema requires only `threadId`, Controller still hard-requires `hostId`, or
  derives hostId from `local`, title, sessionId, threadId shape, or an error message, then self-rates
  PASS.
- A formal dispatch uses sessionId instead of threadId as the formal dispatch coordinate, or asks
  the recipient to derive threadId/hostId from sessionId before continuing.
- A formal dispatch uses relative wording such as `same E1`, `the E1 above`, or `next sequence`
  instead of verifiable concrete values.
- R dispatch lacks actual `candidateIdentity`, `candidateManifest`, or candidate delivery evidence,
  but still asks the Reviewer to review.
- A new E1/R create prompt contains the complete source corpus, candidate work content, or formal
  batch payload, causing E1/R to process content before ready.
- The same complete large input is sent in both the create prompt and formal `sendable_packet`,
  and treated as normal efficient communication.
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
- A formal batch lacks a stable `batchId` or does not bind it to the selected threadId /
  platform-equivalent coordinate, routing coordinates explicitly required by the active tool
  schema/receipt, cycle, target root, monotonically increasing `batchSeq`, and immutable
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
- A `messageId` is merely placed in a prompt, dispatch packet, summary, or receipt-like text and
  treated as proof that a thread was created, a turn started, a tool was called, a write was
  triggered, or authority was granted; or without an actual tool call and verifiable tool result
  or delivery evidence, the message is still claimed as delivered or the work as executed.
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
- A new task lacks a visible `E1:`/`R1:` title or first-line label, or receipts omit threadId or platform-equivalent coordinates.
- C automatically uses `wait_threads` or `read_thread` after dispatch as the receiving mechanism,
  wraps waiting as a bounded wakeup, tracks progress/commentary/finals, waits again after timeout,
  discovers results by polling, or accepts a wait snapshot, task completion state, commentary, or
  summary as ready/result evidence.
- C receives `BATCH_RECEIVED` and therefore automatically waits for the final result, or treats the
  first direct-push as authorization to wait for the next state transition.
- A controlled resend with the same `messageId` is treated as a new logical send and can reopen a
  wait or polling budget.
- The platform does not automatically wake an idle C, so C uses `wait_threads` or `read_thread`
  under the name of wakeup to follow an assignee, then advances state or dispatches the next batch
  without direct-push.
- A knowledge-heavy task lacks a defined knowledge foundation, or R checks only format instead of challenging specialist claims.
- Every internal step gets a card, or a material decision, blocker, or staged delivery gets no card.
- A bear card does not first read this Skill's `VERSION`, treats `v1` as the package version, or
  guesses from the network, a Git tag, GitHub Release, or lock metadata.
- A missing, unreadable, or malformed `VERSION` does not render `version unverified`.
- A start card does not preserve the complete three-line ASCII bear, does not put version on the
  first line, does not put status on the second line, or its third line is not only the bear base line.
- Any CER bear card is not a standalone fenced `text` code block, or its Markdown container causes
  visible misalignment.
- A release or upgrade does not update `VERSION` first.
- A single-batch `CER-start` has no fixed start card, or its start card wrongly uses closed eyes.
- Stop/close shows a closed-eye success card before proving the writer stopped and completing
  required readback; close shows the closed-eye card before reading back title sync or
  `title sync warning`; a failed title rename is claimed as renamed; or a blocked state omits the
  open-eye red blocker card.
- C archives active, blocked, not-returned, or unadjudicated R tasks, or archives C/E1 by default.
- C archives R tasks without saying archive is not deletion, or treats archive state as stop,
  review, or closeout evidence.
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
- The default prompt requires a fresh Reviewer for every task, every item, or all work.
- CER creates a fixed five-document project set or parallel progress source.
- `$project-context-workflow` is treated as a CER installation prerequisite.
- `/CER-stop` is followed by new E1/R work, or single-thread work resumes before an active writer is proven stopped.
- `/CER-status` triggers polling or background monitoring.
- Only documentation or a local technical step succeeds, without a real deliverable.
