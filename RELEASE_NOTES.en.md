# Release Notes

Scope note: each version section records release history for that version; unreleased content that
has not entered an authorized release flow is explicitly marked as a candidate. If the release is
aborted, the affected content must be marked as candidate again or removed. Runtime authority
remains the Skill references bundled with the version the user has installed.

## v0.3.10

This release closes the result-disposition loop after batch results return, so candidates,
diagnostics, derived outputs, and Reviewer PASS results are not accidentally promoted into
authoritative input, mainline progress, or next-batch decision sources.

- When C accepts a result, it must state `accepted_as`, `authority_effect`,
  `progress_effect`, `permitted_next_use`, `forbidden_next_use`, and whether existing
  target-project persistence is required
- Bare `RESULT_ACCEPTED` means only that the batch was adjudicated and communication can
  deduplicate it; it is not authority promotion, mainline progress, or permission for the next
  batch to use the result as authoritative input
- Candidates, drafts, diagnostics, derived outputs, and review-only results default to
  `working_material` only; promotion to `authoritative_input` requires an explicit user decision
  or a read-back target-project owner anchor, promotion evidence, and readback evidence
- When a later batch uses a prior result, the dispatch packet must classify
  `prior_result_use: working_material | authority_input`; if it is `authority_input`, it must
  include `promotion_evidence` and `project_owner_anchor`
- Reviewer verdicts are split into `content_verdict`, `implementation_verdict`,
  `outcome_verdict`, and `authority_promotion_verdict`; content or technical PASS does not
  automatically become outcome PASS, authority-promotion PASS, or mainline progress, and
  `out_of_scope` is not PASS
- If a result changes current phase, artifact role, next product route, authoritative source,
  progress claim, or later batch input, C must first update and read back the target project's
  existing persistence; when persistence is unsynchronized or contradictory, the next batch stays
  at `dispatch_blocked`
- The bilingual runtime, UAT, and Skill validators add fixed counterexamples for result
  disposition, authority promotion, prior-result consumption, and
  persistence-before-next-dispatch; each package has 316 mutation cases
- Release-readiness completed full static review and two AI real workflow UAT cycles before
  publication. Post-release user manual UAT remains a separate follow-up

## v0.3.9

This release folds the create-prompt lifecycle weakness proven by true A/B/C dry-runs into the
runtime. The focus is to separate "create a new E1/R task" from "dispatch formal work", so READY,
work output, duplicate handling, and acceptance evidence do not get mixed by putting the full
corpus or formal batch payload into the first task-creation prompt.

- A new E1/R `create_thread` initial prompt may only be a zero-write ready handshake: state the
  role, cycle/title, target root, C return target, no-write/no-start-work boundary, and ask for the
  assignee's own coordinates or source availability
- The `create_thread` initial prompt must not include a complete source corpus, candidate work
  content, or a formal batch payload, and must not ask E1/R to process content before READY
- If pre-ready content processing already happened, C must treat it as a `pre-batch payload leak` /
  batch lifecycle violation and stop or refreeze; a later same-digest duplicate ack is not normal
  efficient communication
- When the assignee cannot read an authorized source directly, C sends the formal `sendable_packet`
  once after READY; if the content is too long or crosses risk boundaries, C splits it by semantic
  or risk unit
- When the assignee can read an authorized source, formal dispatch should prefer coordinates,
  digest, required excerpts, and no-go boundaries instead of repasting the whole corpus
- The A/B/C dry-runs did not prove that this CER Skill over-microbatches, uses harmful over-coarse
  batching, over-retains, hits long-prompt send failure, or progresses unreasonably slowly; this
  release fixes only the evidence-backed create-prompt / formal-dispatch boundary
- The bilingual runtime, UAT, and Skill validators add fixed counterexamples for create-prompt
  payload leakage; each package has 283 mutation cases
- This release records `Full Audit passed (static corpus only; AI real workflow UAT unavailable)`
- Post-release user manual UAT remains a separate follow-up

## v0.3.8

This release publishes two runtime tightenings completed after v0.3.7: readable pre-dispatch
evidence, and the post-dispatch `POST_DISPATCH_PARKED` no-wait state. The focus is to make C's
judgment and result-return path verifiable, so long-running CER work does not drift through
waiting, verbal assurance, or handoff along the wrong direction.

- Long-running, multi-batch, high-risk, or non-simple formal implementation dispatch packets must
  include compact `pre_dispatch_evidence`. It compresses the existing Controller preflight,
  `outcome_anchor`, and drift judgment into evidence E1/R can read back; it is not a new source of
  truth, table, monitoring process, or Full Audit
- `pre_dispatch_evidence` must at least state the outcome anchor, the unfinished condition this
  batch improves, the readable outcome difference success should create, the truth-source intake
  summary and source anchors, required sources read or missing-source disposition, the work lane,
  and the drift checkpoint conclusion or no-trigger reason
- If required pre-dispatch evidence is missing, contradictory, dependent on unread required truth,
  or only says "already judged" without a readable summary, C stays at `dispatch_blocked`; E1/R may
  only return a zero-write blocker and must not start writing, reviewing, or completing C's judgment
- After dispatch, task creation, or send, C immediately enters `POST_DISPATCH_PARKED`. In that
  state, C must not automatically use `wait_threads`, `read_thread`, waiting, polling, commentary
  reads, child finals, or status probing to discover ready, progress, checkpoints, or results
- C may read the related task only for a one-time diagnostic check explicitly requested by the user
  in the same turn, or for one bounded readback/adjudication after a direct-push has been received.
  Without a direct-push, a wait snapshot, completion state, commentary, child final, or passive read
  cannot advance lifecycle, trigger the next batch, or become formal delivery evidence
- The bilingual runtime, UAT, and Skill validators add fixed counterexamples for pre-dispatch
  evidence and `POST_DISPATCH_PARKED` no-wait behavior; each package has 275 mutation cases
- Post-release user manual UAT remains a separate follow-up

## v0.3.7

This release publishes three generic runtime fixes completed after public v0.3.6. The focus is to
keep long-running CER loops from losing the user's outcome through waiting, adjacent proposals,
briefing activity, or repeated batches.

- After dispatch, C must not automatically use `wait_threads` or `read_thread` as the result
  receiving mechanism. Formal results must be actively direct-pushed by the assigned task to the
  specified return target. A single bounded wait or read is allowed only for a declared direct-push
  state transition, or after a direct-push has arrived for wakeup, readback, or adjudication
- Controller preflight now includes a truth-source intake gate. Before a non-simple formal
  implementation batch, C must be able to answer who owns the completion condition, who actually
  uses it, how it takes effect, and what counterexample could disprove it. If any answer is
  missing or depends on unread required truth, C must not dispatch formal implementation work and
  may only run necessary read-only diagnosis, narrow acceptance scope, or stop for user decision
- The long-task drift checkpoint is owned only by the outcome-anchor progress gate. On
  resume/context transition, two consecutive no-delta batches, a second same-class failure,
  adjacent or substitute E1/R proposals, a user direction or constraint change, and before
  close/release/major delivery, C must prove the next batch still improves the `outcome_anchor`
- A checkpoint, brief, or roadmap is not outcome progress by itself, and it must not trigger
  background monitoring, polling, automatic `wait_threads`, a fixed Reviewer, or a fixed Full
  Audit. Simple, one-step, low-risk work can still use the lightweight flow
- The bilingual runtime, UAT, and Skill validators add fixed counterexamples for the wait-auto
  delivery guard, truth-source intake gate, and drift checkpoint; each package has 259 mutation
  cases
- Release-readiness completed full static review and AI real workflow UAT before publication.
  Post-release user manual UAT remains a separate follow-up

## v0.3.6

This release fixes a long-running multi-batch CER failure mode where batch activity could be
mistaken for progress toward the user's final outcome.

The new `outcome_anchor` is fixed before the first real dispatch for long-running, multi-batch, or
rework-prone tasks. It preserves the user's final outcome, source pointers for completion
conditions, unacceptable substitute outcomes, and explicit exclusions. Later E1, R, or adjacent
mechanism work cannot rewrite that anchor on their own; when the user or an authoritative source
changes the target, C must state the difference between the old and new anchors.

- Before dispatching any non-exploratory batch, C must identify which unfinished condition the
  batch improves, what readable before/after difference success will create, and whether
  dependencies, authoritative sources, and handoff path exist. An implementation batch with zero
  expected outcome improvement and no necessary-prerequisite role must not be dispatched
- Candidate creation, review completion, structural or format pass, file consistency, issue
  logging, design completion, version renaming, and packaging changes are activity only. C may
  count mainline progress only after reading back and accepting an outcome difference against one
  of the user's completion conditions
- A same failure class is judged by shared root cause, user consequence, affected completion
  condition, and method. Renaming, version changes, or repackaging do not create a new class; after
  two unresolved attempts, C must not dispatch a third same-class repair
- Reviewer must also check whether the batch still serves the original outcome, creates an
  acceptable outcome difference, is only technical activity or rework, or substitutes another
  deliverable shape for what the user asked for
- CER now separates `mainline_outcome`, `diagnostic`, `mechanism_improvement`, and
  `governance_self_improvement`. Diagnostics and generic mechanism work do not contaminate
  mainline progress and do not automatically block the original task when they fail
- Bilingual runtime, roadmap, UAT, and Skill validators add fixed regressions for the outcome
  anchor, activity/outcome separation, retry circuit breaker, Reviewer outcome checks, and work-lane
  isolation; each package grows from 172 to 201 mutation cases
- The outer C for each AI real workflow UAT cycle must now direct-push
  `AI_UAT_CYCLE_N: PASS/FAIL` back to the main release dispatcher; `wait_threads`, `read_thread`,
  child-task finals, task titles, or user-relayed completion notices alone cannot mark
  release-readiness as passed
- Post-release user manual UAT remains a separate follow-up

## v0.3.5

This release adds two runtime root fixes.

First, the `messageId` identity boundary is explicit: it is a CER message-layer
identity, deduplication, and tracing field, not a Codex execution command, an App Server
`method`, a JSON-RPC request `id`, a thread/session identity, an idempotency key, or authorization.
Only an actual tool call and verifiable tool result or delivery evidence can advance a delivery or
execution decision.

Second, Controller preflight and the roadmap now include the living task brief. A fuzzy but
startable multi-batch task does not require the user to write a complete specification first. C
separates confirmed requirements/exclusions, safe inferences, critical gaps, latest feedback,
current batch freeze, and the next observable preview or decision point, then freezes only the next
safely executable batch. When mid-work feedback changes direction, C updates the brief and roadmap
delta before using a new batch identity or supersede flow with the same E1. R reviews against the
latest task brief and current batch freeze, not a stale initial prompt. Any user-visible brief must
carry CER identity and C/E1/R context so it is not mistaken for a native Codex internal feature.

- The bilingual runtime owner now rejects treating a `messageId` written only in a prompt, dispatch
  packet, summary, or ordinary workspace text as proof of thread creation, turn start, tool call,
  write, or authorization
- Bilingual runtime, roadmap, UAT, and Skill validators add living-brief and CER visible-style
  counterexamples and fixed regressions; each package grows from 141 to 172 mutation cases
- Released on GitHub and installable through the skills CLI; post-release user manual UAT remains
  a separate follow-up

## v0.3.4

This release consolidates four reusable runtime corrections confirmed in real CER use. It adds no
commands, roles, or single-project rules:

- After a `create_thread` receipt, when the current Codex title tool is available, C must set or
  rename the title with the official tool and read it back before accepting ready or sending a
  formal batch. When title tooling is unavailable, the honest `title sync warning` remains
- Lifecycle and checkpoint bear cards now use a fixed three-line layout in a standalone fenced
  `text` code block: version only on line one and status only on line two, preventing display drift
- After a frozen objective already has a material E/R result, C may add E/R work or a task branch
  only when it identifies a new falsifying question and proves that the branch is the smallest
  necessary way to complete the original goal or address a verified blocker; otherwise C
  consolidates, stops, or adjudicates directly
- After a successful `CER-close`, completed and adjudicated Reviewer tasks may be archived to
  reduce sidebar clutter. C/E1 stay visible, and the summary states that archive is not deletion
  and the tasks remain available from archived tasks
- Bilingual UAT and project governance validation now include fixed counterexamples for missing
  title set/readback, card layout, unnecessary same-root task branches, and treating archive as
  deletion or closeout evidence. Post-release user manual UAT remains reported separately

## v0.3.3

This release fixes the validation weakness confirmed after v0.3.2: the docs correctly said that
plain `start` / `close` wording belongs to Agent Handoff Kit semantics, but the Skill validator did
not mechanically prevent a future edit from turning a standalone close into a CER close trigger:

- The English and Traditional Chinese Skill validators now include a context-aware trigger matrix
  covering frontmatter, command tables, runtime startup/stop ownership, and UAT install/failure
  matrices
- The only valid CER commands remain `/CER-start`, `/CER-stop`, `/CER-close`, `/CER-status`, and
  `/CER-help`; plain `開工` / `收工` or `start` / `close` wording does not independently trigger CER
- UAT failure examples may still contain the intentionally wrong wording as counterexamples; the
  validator checks section context instead of using a global forbidden-string list, avoiding both
  false positives and false green results
- Each language package now has 141 mutation cases, up from 131. The new counterexamples fail when
  SKILL, core runtime, or UAT text drifts toward standalone close/start as a CER trigger
- This release does not change CER runtime trigger semantics, add commands, or add Keyring-specific
  or project-specific rules

## v0.3.2

This release fixes a formal-dispatch gap where a Controller could leave placeholders, relative
recipient identity, or missing Reviewer candidate evidence in a packet while still self-rating it
as ready to send:

- C may keep a `draft_packet` internally, but a real `sendable_packet` must fill actual
  `threadId` or a platform-equivalent coordinate, `returnTarget`, `messageId`, `batchId`,
  `batchSeq`, `payloadDigest`, and any routing coordinate explicitly required by the active tool
  schema/receipt
- `hostId` is used only when the active tool schema or receipt requires or provides it; it must not
  become a cross-platform hard requirement, and must not be derived from `local`, title, sessionId,
  threadId shape, or an error message
- `sessionId` must not replace `threadId` as the formal dispatch coordinate or be used to derive
  `hostId`
- Relative wording such as `same E1`, `the E1 above`, or `next sequence` is draft-only; before
  sending to E1 or R, it must be replaced with verifiable concrete values
- R dispatch must include actual `candidateIdentity`, `candidateManifest`, and candidate delivery
  evidence. Missing any one leaves the packet at `dispatch_blocked` or `decision_blocked`
- The bilingual UAT counterexamples and Skill validators now cover this reusable failure class.
  Each language package has 131 mutation cases, without replacing class-level QA with a
  one-prompt hard code
- AI real workflow UAT completed two cycles: the second cycle used new C/E1/R tasks and did not
  reuse the first cycle's C/E1/R. Post-release user manual UAT remains reported separately

## v0.3.1

This release fixes a generic CER Core gap where E1 could treat an unexpected test failure,
or a file allowlist, as authority to expand the batch's modification scope. It does not add
Keyring-specific semantics, roles, commands, modes, or helpers:

- The execution loop in `core-runtime.md` now states that an unexpected failure does not change
  the batch authority. Tests produce evidence but do not grant more modification authority. A file
  being in allowed scope does not authorize E1 to change another owner, authoritative source, or
  protected meaning inside that file
- Before any new or expanded write motivated by an unexpected failure, E1 must perform bounded
  read-only attribution. E1 may fix within the batch only when reproducible evidence proves the
  batch directly caused the failure and the fix preserves the frozen owner, meaning, source,
  permissions, and acceptance
- If causality is unclear, the failure may be flaky, environmental, or dependency-related, the
  acceptance itself may be wrong, or the fix would change another owner, authoritative source,
  admission condition, fallback, product/professional meaning, or cross-subsystem behavior, E1
  must stop further writes and return a blocker
- Direct acceptance decides whether the batch candidate can be accepted. Full regression only
  discovers integration risk. A full-regression failure may block the candidate, but it does not
  automatically authorize adjacent repair
- Only C may refreeze the contract and expand scope by dispatching a new batch with a new
  `batchId` and `payloadDigest`
- The bilingual UAT counterexamples and Skill validators now include fixed scenarios for this
  gate. Each language package has 109 mutation cases. Post-release user manual UAT remains
  reported separately

## v0.3.0

This release turns the Exploration Helpers introduced in v0.2.6 into a complete, mechanically
verifiable capability that can be reused across projects. It also fixes two issues that could add
unnecessary work or let validation pass when a core rule was missing:

- Users still only start CER; they configure no helper and learn no new command. The complete
  rules now live in the sole `parallel-producers.md` owner, while README remains an introduction
  instead of becoming a second rule source
- Simple work uses zero Exploration Helpers. C starts parallel exploration only when at least two
  lanes are independent, inputs are frozen, C has different important work to do concurrently,
  candidates can be checked separately, meaningful net time savings are expected, and execution
  capacity is available
- Exploration Helpers return candidates only. Read-only work performs zero writes. Candidate
  files may be created only in a verified isolated temporary area, with source coordinates and
  file hashes recorded before C personally reads back, deduplicates, and adjudicates them
- The default prompt no longer implies that every task requires a Reviewer. C performs
  proportionate checks for simple low-risk work and creates a fresh Reviewer only when risk or
  reliable disproof requires one. The validator requires the complete prompt to match the sole
  approved sentence exactly, so any appended or substituted contradiction fails without relying
  on a growing synonym blacklist
- The validator generates rule-deletion counterexamples from the same owner requirement list.
  Each language package now has 87 mutation cases. It rejects deletion of any of the eight
  parallel safety and evidence requirements and active, passive, or reordered wording that forces
  a Reviewer onto simple or low-risk work
- The English and Traditional Chinese Skills, READMEs, and new node infographics now present the
  same architecture. Public rules contain no project-specific name, path, or decision
- The Traditional Chinese global repair, both Skill structure checks, both 87-case self-tests,
  and final independent review of the public bilingual candidate have passed. Post-release user
  manual UAT has not been run and will be reported separately

## v0.2.6

This release adds Controller-managed Exploration Helpers without changing formal C/E/R
roles, the single-writer rule, or independent Reviewer boundaries:

- Exploration Helpers can help C find information, compare options, organize interface ideas, and
  identify possible problems at the same time. They are not a fourth formal role, cannot change
  the project or replace E1/R, and add no new command
- Helpers normally remain off. C starts them automatically only when the work can be split safely,
  the information and goal are clear, each result can be checked separately, and using helpers is
  expected to save meaningful time
- Simple tasks use no helpers. C still performs the main analysis and makes the final decision;
  matching answers from several helpers are not accepted automatically
- If information changes, only the affected part is redone. If a helper cannot start, times out,
  or cannot find the required information, C continues directly instead of needlessly stopping CER
- In one practical test using a medium-sized task, two jobs would have taken about 71 seconds one
  after the other. Running them together took about 43 seconds, reducing the wait by roughly
  two-fifths. This is one test example, not a promise of the same improvement for every project
- The local files, Skill structure, Kit health check, full static release review, and two AI real
  workflow UAT cycles have passed. Post-release user manual UAT has not been run and will be
  reported separately

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
