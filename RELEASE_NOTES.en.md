# Release Notes

Scope note: each version section records release history for that version; unreleased content is
explicitly marked as a candidate. Runtime authority remains the Skill references bundled with the
version the user has installed.

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
