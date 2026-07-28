# CER Core v1 Runtime

## Roles

- Controller (C): the only controller accepted through the local or Remote startup gate. C owns global judgment, source-of-truth mapping, batch adjudication, candidate readback, and user communication. C does not write the workspace.
- Executor (E1): a sidebar-visible independent new task/thread created in the same Codex project
  through the official `create_thread` tool for every `CER-start` cycle, and the only writer for
  that cycle. Later batches in the same cycle keep reusing that same E1. E1 executes only C's
  self-contained batches, validates the work, and returns a candidate.
- Reviewer (R): created only for high risk, core promises, data integrity, safety, uncertain
  external capability, or when C cannot reliably disprove a claim. Every R must be a fresh new
  task/thread created through official `create_thread`, read-only and bounded. R does not edit
  files or direct E1, and old R tasks must not be reused.
- E2: may be created as another new task/thread through official `create_thread` only after the
  original E1 has verifiably stopped writing, the workspace is in a known state, and C has issued
  a takeover batch. Parallel writers are forbidden.

C may use an inline sub-agent for read-only exploration, evidence organization, or candidate
analysis. It is not a formal CER C/E/R role, must not write the workspace, must not replace E or
R, must not produce formal ready/result, and must not count as CER Reviewer acceptance evidence.

## Knowledge Foundation

CER is not limited to engineering. When a task depends on medicine, law, finance, investment, policy, academia, business, design, operations, content, or other specialist knowledge, C defines a risk-proportionate knowledge foundation first: domain scope, authoritative sources, terminology, data year or version, quality standard, choices AI cannot make for the user, and uncertainty that must be disclosed. Prefer existing project sources of truth and user-provided sources. If a critical source is missing, stop and label the unknown. Do not turn general knowledge into a professional conclusion.

An E1 batch contains only the knowledge-foundation summary, source coordinates, and boundaries needed for that batch. R independently tests high-risk claims, source use, reasoning, and conclusions against the same foundation, rather than checking format alone. Do not create a knowledge-foundation document for a simple low-risk task; include the necessary content in the self-contained dispatch or checkpoint.

## Bear-Card Package Version

Before showing any lifecycle or checkpoint bear card, read `VERSION` from this Skill root next
to `SKILL.md`. Accept only complete content matching stable semver `X.Y.Z`; when valid, render it
in the card header as `vX.Y.Z`. If `VERSION` is missing, unreadable, or malformed, show
`version unverified` in the card header.

Do not fall back to `v1`, and do not guess from the network, a Git tag, GitHub Release,
`skills` CLI lock metadata, or other external state. `CER Core v1` names only the workflow
generation. Every release or upgrade must update `VERSION` first. After the whole Skill is
updated, the next card naturally reads the new version.

## Commands

CER v1 accepts natural-language and slash-command entry points. Slash commands are stable text aliases that can be saved in an AI terminal, snippet, Snap, or searchable command interface. If the platform does not support them, pasting the same text still works.

| Command | Natural language | Effect |
|---|---|---|
| `/CER-start <task, constraints, priorities>` | `Start CER: ...` | Start CER v1 and make the local user task C, or make an explicitly designated Remote receiver task the only C for that target_root after the `C_READY` loop is proven. Plain start/work messages do not start CER. |
| `/CER-stop` | `Stop CER and continue in a single thread.` | Stop CER mode and send no new E1/R work. If E1 is writing, first ask E1 to stop or return a verifiable state. |
| `/CER-close` | `Close CER.` | Close CER. The same E1 updates only required existing sources of truth and marks `writer closed`. Plain close/finish messages do not close CER. |
| `/CER-status` | `Show CER status.` | Report C's known goal, C/E1/R coordinates, next checkpoint, and blockers. Do not poll for status. |
| `/CER-help` | `Show CER commands.` | Show the available commands and natural-language equivalents. |

## Controller Preflight

Before creating this cycle's E1, reusing the existing E1 in the same cycle, or dispatching any real E1/R batch, C completes an adaptive task contract. This is not a form-filling ceremony. For simple low-risk work with one clear endpoint, C may complete it internally and proceed with a short summary. For long-running, multi-batch, or new product, flow, design, content, or experience work, compress the necessary answers into a first-public-alignment roadmap and self-contained dispatch.

C judges only five items, each marked `confirmed`, `safe inference`, or `critical missing`:

- Endpoint: what observable endpoint exists, and what is explicitly out of scope.
- Sources: what must be read before completion can be judged, what has been read, and what key unknowns remain.
- Root cause and boundary: why CER is needed, and what the smallest acceptable E1 batch is.
- Permissions and stops: what AI can handle directly, whether first public alignment is needed, and what truly requires user decision or stopping.
- Acceptance and proportion: what evidence can disprove the approach, and whether acceptance is just sufficient rather than defensive expansion.

The three states have evidence boundaries. `confirmed` may come only from an explicit user statement or an authoritative source C has actually read, and C must be able to point to the source anchor. An unsupported assumption must not be labeled `confirmed`. A `safe inference` must pass a counterfactual test: if the opposite assumption were true, the deliverable, user flow, collaboration method, data handling, permissions/risk, acceptance, and rework would still not materially change. If multiple reasonable answers would produce materially different outcomes, the item is `critical missing`.

Before dispatch, C performs one short QC pass: check that every `confirmed` item has a source, that every `safe inference` passes the counterfactual result, and that the frozen task contract has not promoted an assumption into `confirmed`. If QC fails, C must not create/reuse E1 or dispatch real work. C may only perform necessary read-only investigation, or use a `🟡 User decision` stop with at most three questions that would materially change the result.

`critical missing` means C cannot safely judge or dispatch. C may only perform necessary read-only investigation. If information that would materially change the result is still missing, use a `🟡 User decision` stop and ask at most three questions. Only after preflight passes does C verify communication coordinates and `ready`. E1/R dispatches use the same frozen task contract; assignees may report contradictions, blockers, or candidate corrections, but must not expand the goal, sources, permissions, or acceptance on their own.

The acceptance-validity and proportion rule is reapplied before C makes or reuses any acceptance,
repair, or release conclusion; it does not rerun validation by default. C first identifies the
concrete conclusion, the evidence supporting that conclusion, and the premises behind that evidence.
Existing evidence may be retained only while the reviewed
object, requirements, direct dependencies/environment, delivery artifact, and validation method
still apply or have been verified equivalent, and no credible contradictory evidence exists. Fresh
context must not assume inaccessible evidence remains valid. If a premise fails, rebuild only the
minimum sufficient evidence for the affected conclusion. Widen only with a traceable
premise-to-conclusion causal chain, cross-surface coupling, cumulative interaction,
artifact/source mismatch, or credible reason that the old validation was false-green. Breadth
follows causal coverage; depth follows failure consequence and evidence uncertainty. Task labels,
file counts, change size, or `high risk` wording alone neither widen nor narrow acceptance. This
rule governs scope once evidence is known; it does not replace targeted checks needed to discover
unstable external claims or verify actual release/install artifacts.

## Startup

1. C reads the installed CER runtime, the user's overall task, explicit constraints, and authoritative rules that actually exist in the target workspace.
2. The startup gate is owned by the Remote sender or the local start task. A receiver task may only return candidate `C_READY`; it must not blanket-reject Remote C solely because the message came from another task, and it must not use silence, no response, or its own inability to see other tasks as proof of unique C.
3. The startup gate judges unique C only inside the actual collaboration domain for this start: use the official task/thread list or a platform-equivalent tool to enumerate every participating host this start will use; for readable candidates, verify resolved target_root/cwd, `🚀 C:` identity, and active/idle/closed/handed-off state; also require the sender to explicitly state that it has not assigned the same root to another C. Only when all participating hosts are enumerable and no active C exists may the gate judge no active C. Do not scan outside-platform or non-participating hosts, but also do not treat invisible tasks as nonexistent.
4. A known active C may only be reused within the same cycle. Transfer requires an actual message or state readback showing the old C explicitly handed off/closed. After `/CER-close`, the old C and its E/R tasks remain history only and the whole set must not receive work for a later cycle in the same workspace. A later cycle must use a new task as C; the gate reads back that the old C is `closed`/`handed-off`, that no active C exists, and that every participating host is verifiable. If any participating host cannot be enumerated, old C state or candidate root/identity/state cannot be read back, coordinates are incomplete, or evidence conflicts, the state is unknown and the gate stops without creating a second C.
5. After an explicit Remote CER start, the Remote receiver task first direct-pushes candidate `C_READY`, including its threadId, hostId, target_root, and return target/path. After the sender completes unique-C verification and actually reads back `C_READY`, the sender must send `C_ACCEPTED` to the receiver through the same usable return path. The receiver becomes active C and starts Controller preflight only after receiving `C_ACCEPTED`. Merely sending `C_READY`, failing to read back `C_READY`, or missing `C_ACCEPTED` leaves Remote C identity and communication path unestablished. If the sender was the active C, it must complete handoff/close before sending `C_ACCEPTED`.
6. Do not add a lock file, central registry, run ID, conflict engine, new role, or test exception for unique C; uniqueness is judged only from existing sources, official enumeration, explicit coordinates, and this-turn actual return/readback evidence.
7. C assigns a short project-local cycle number for sidebar recognition on every CER-start. New
   cycles after this rule is active must not use `00`; C uses the official project task/title
   enumeration to read back existing numeric cycle labels and chooses the next unused positive
   integer, displayed with at least two digits such as `01` and `02`. Values above 99 may expand
   naturally. Do not add a central registry, lock, or run ID. `00` means only a legacy/migration
   cycle that started before cycle numbering and whose original cycle number cannot be reliably
   reconstructed. It is display-only like every other cycle number, not a lock, run ID, unique-C
   proof, or thread identity; the full threadId remains authoritative. If a new cycle cannot
   reliably enumerate or set the title, keep the shortest role title and report a real
   `title sync warning`; do not show a question-mark cycle label, guess a number, or turn display
   label failure into a fake lifecycle or identity failure. C names or identifies its visible
   task/thread as `🚀 C:01｜<very short task name>`. If the platform cannot change the title, use an
   equivalent role label in the first visible message or checkpoint card. Plain `C:` is not an acceptable Controller title/label.
8. C completes Controller preflight and freezes this task contract. If anything is `critical missing`, C may only perform necessary read-only investigation or stop for questions; C must not create/reuse E1 or dispatch real work.
9. After Controller preflight passes, C completes a communication preflight. Use available tools to prove the actual path, including identity source, target root, required parameters, send path, recipient, visible title or role label, return source available to the assignee, verifiable session/thread ID or platform-equivalent coordinates, and C's adjudication point.
10. If the official `create_thread` tool for new tasks is unavailable, or C cannot read back a
    sidebar-visible title, verifiable thread ID, and formal return path, E/R delegation is
    blocked. Do not downgrade to an inline sub-agent, fork, delegate, or existing task as a
    formal E/R substitute.
11. When creating E1, R, or E2, titles or first-line labels must begin in the form
    `E1:01｜<very short task name>`, `R1:01｜<very short review name>`/`R2:01｜...`, or
    `E2:01｜...` without the rocket. The role ordinal is before the colon and the cycle number is
    after the colon, so second-cycle E1 is not mistaken for E2. All C/E/R tasks in the same cycle
    use the same cycle number; the next cycle uses a new cycle number. A legacy/migration cycle may
    use `00`. Every dispatch, `ready` receipt, and result receipt must include sender role,
    recipient, return target, and
    session/thread ID or platform-equivalent coordinates.
12. C creates a brand-new persistent E1 for this cycle through official `create_thread`. E1 first
    direct-pushes a zero-write `ready`. C must actually receive a qualifying zero-write `ready`
    with the correct role, cycle number, sidebar-visible title/label, thread coordinates, and
    return target. Later batches in the same cycle keep reusing that same E1 and the E1 threadId
    remains the same. A later cycle after a completed `/CER-close` uses a new cycle number, creates
    a brand-new E1 and only fresh Reviewers; it must not reuse any E/R task or coordinate from the
    previous closed C.
13. If any communication preflight link is missing, or the assignee does not actually direct-push a qualifying zero-write `ready`, C shows only the open-eye `🔴 Major blocker` card and stops. C must not show the successful start card. Waiting, polling, after-the-fact reads, document review, successful forking, and successful one-way sends do not prove communication.
14. Only now is `CER-start` successfully accepted. C's first user-visible success receipt must be the fixed open-eye `🔵 CER started` card from [roadmap.md](roadmap.md). Keep the complete three-line bear; render version and status after the foot on its third line with fixed `·` markers rather than a separate line. Single-batch and multi-batch starts use the same card. Do not use a closed-eye card or guess a version.
15. Later batches in the same cycle do not repeat the handshake while C, E1, the return target, and verifiable coordinates remain the same. Repeat `ready` whenever the coordinates or return target changes.
16. For long-running, multi-stage, multi-batch, or first-public-alignment work, show the initial progress surface under [roadmap.md](roadmap.md) after the fixed start card and before the first batch. A simple single-batch task with one clear endpoint needs only a short summary.
17. C may send the first real batch only after the fixed start card is shown and the required initial roadmap or short summary has been added.

If the user did not explicitly invoke CER and the work is one low-risk step, handle it normally. Once the user explicitly invokes CER, do not silently remove the role topology because the task appears simple. Plain start/work messages belong to the target workspace's existing governance and are not CER triggers.

## Self-Contained Dispatch

Each real E1 or R batch contains only what is needed:

- role and one objective;
- target root;
- required sources of truth and accepted background;
- allowed and forbidden scope;
- acceptance checks and a counterexample that can disprove the solution;
- stop conditions;
- the frozen task contract, including handling of any `confirmed`, `safe inference`, or `critical missing` item, required source anchors, and counterfactual results;
- C direct-push return target and session/thread ID or platform-equivalent coordinates;
- the knowledge foundation, source coordinates, unknowns, and no-go boundaries needed for the batch;
- a short result format.

Do not write "see above" or ask the assignee to reconstruct C's context. Add background and counterexamples for high-risk batches. Keep low-risk batches short and avoid oversized templates. If E1/R finds a contradiction between the frozen contract and the sources, report a blocker or candidate correction first; do not rewrite the contract and continue alone.

While CER is active, if the target workspace's `AGENTS.md` clearly routes the user's intent to
Agent Handoff Kit full closeout (for example, `Wrap up Agent Handoff`, `收工`, or equivalent
session-closeout intent), or clearly routes a specified document to governance bridge, C gives
the same E1 only the user's original instruction, target root, same-E1 and return coordinates,
the specified document when present, and any adjudicated state that is not yet durable but the
target workflow must know. C must not restate, decompose, expand, predict, pre-execute, or create
another copy of that workflow's procedure, checklist, file list, maintenance decision, tests, or
completion claim. E1 executes under the current authority routed by the target `AGENTS.md` and
direct-pushes the actual terminal result or blocker.

C handles CER title `✓` and the close card only after authoritative Kit full-closeout evidence
passes; a blocked result must not claim `writer closed`. After the same E1 returns verifiable
authoritative Kit terminal evidence, C performs only required result readback and does not rerun
the Kit procedure or checks; only missing or contradictory evidence returns to the same E1 for
completion. Governance bridge returns through normal readback and adjudication while CER remains
active. `/CER-close` remains a CER-only command and does not trigger Kit full closeout in reverse.

## Delivery

- E1 and R direct-push `ready` through the formal messaging tool before work.
- `ready` includes the assignee's role, visible title or first-line label, session/thread ID or platform-equivalent coordinates, received target root, return target, and whether required sources are available.
- On completion, blockage, or incomplete work, direct-push a short result to C before stopping. Include session/thread coordinates so C cannot accept another task's result by mistake.
- C performs one bounded readback and adjudication only after receiving the push.
- "No monitoring" forbids waiting, polling, background listening, repeated status probes, and passive thread reads before a push arrives. One bounded read explicitly requested by the user, or a verification read after a push, remains allowed.
- Unavailable delivery blocks delegation only. C may still perform authorized read-only research, analysis, and adjudication, but C may not write in E1's place.

## Execution Loop

1. C gives this cycle's same E1 one batch based on the user's task and accepted project plan or sources of truth.
2. E1 completes only that batch, reads back and tests the work, then direct-pushes a candidate.
3. C reads back the actual result and either adjudicates it or creates a fresh R through official `create_thread` according to risk.
4. R tests only the specified risk and product logic, not format alone.
<!-- cer-review-convergence -->
5. After R first reports a defect, C groups related findings by common root cause and user consequence, then performs one bounded read-only impact check to find the current sources of truth, delivery surfaces, and check locations that carry this round's contract.
6. C freezes this round's `owner/affected surfaces/acceptance/counterexample family` and gives the same E1 one batch to repair the whole affected boundary.
7. After the repair, R re-tests only the frozen scope. Expansion is allowed only for a different root cause, a different user consequence, or a new regression caused by the latest repair.
8. Changed wording, sentence order, or synonymous phrasing remains the same problem. Do not append rules or validator patterns sentence by sentence. If the same counterexample family keeps escaping a mechanical check, C changes the checking method or narrows the validator's claimed capability.
9. When the frozen counterexamples pass and no material new defect remains, C accepts the result. Only then may E1 update an existing authoritative project-progress source; if none exists, do not create one.
10. C stops after required state is converged. List adjacent improvements separately without adding a Reviewer, governance layer, or whole-repository re-review.
11. For long-running, multi-stage, or multi-batch work, progress updates and bear-card checkpoints follow [roadmap.md](roadmap.md). Use only facts read back and adjudicated after direct-push; do not poll E1.

For an ordinary small change, C readback and proportionate tests are enough. Re-review only the affected boundary after a high-risk fix. More Reviewers do not replace clear acceptance conditions.

## YAGNI And Stop

- Add roles, batches, Reviewers, checkpoints, tests, and synchronization only when the current risk and deliverable require them.
- Do not create R when C can reliably accept the work through readback and proportionate tests. Do not re-review accepted areas when a narrow fix is enough.
- Stop when the requirements are met, core counterexamples pass, and required risk is cleared. List adjacent improvements separately without expanding automatically.
- Reduce the collaboration structure when agent and governance overhead exceeds task value. Do not add process to compensate for unclear acceptance.

## Standalone Persistence And Closeout

CER Core v1 does not prescribe project documents. It reuses the target project's authoritative plan, progress, and decision sources. If no durable source exists, do not claim that a new session can fully recover state.

CER-close has fixed completion conditions, while its evidence path adapts to the actual state:

- When the complete threadIds or platform-equivalent coordinates for this cycle's C/E/R roles are
  known, read terminal state directly from those roles instead of first enumerating the whole
  project's tasks. Enumerate within the relevant project only when coordinates are incomplete or
  contradictory, writer state is unknown, or target-project rules explicitly require it.
- E1 updates only existing target-project sources that this close actually requires. Do not require
  a fixed set of handoff, log, progress, or other files. When no durable source needs an update,
  read back only the actual deliverable and `writer closed`.
- A status-only close defaults to targeted structural and content readback sufficient to prove the
  terminal state. Run the relevant full validator or doctor only when this cycle changed governance,
  schema, or core flow; credible contradiction or false-green evidence exists; source and delivery
  artifact differ; or project rules require it.
- Do not create a Reviewer merely because the command is close. Create a fresh R only when the
  close conclusion itself has high-consequence risk that needs independent challenge. Review
  breadth follows causal coverage; depth follows failure consequence and evidence uncertainty.

When the user explicitly says `Close CER.` or `/CER-close` to C:

1. C stops new dispatch, adjudicates candidates that can be safely decided, and organizes accepted work, incomplete work, risk, evidence, and next action.
2. C gives the same E1 one self-contained closeout batch.
3. E1 updates only the necessary existing progress or decision sources under target-project rules, marks that E1 has stopped writing, reads back the result, and direct-pushes it. If no durable source exists, E1 reports only the actual deliverable and `writer closed`.
4. After C reads back the deliverable, required sources, and `writer closed`, C uses the official
   title tool to automatically append `✓` after this cycle's cycle number in every verifiable
   C/E/R title, such as `🚀 C:01✓｜...`, `E1:01✓｜...`, and `R1:01✓｜...`; legacy/migration `00`
   may likewise become `00✓`. C then reads back the titles. This is a built-in display-only
   CER-close rename and does not ask the user again. It
   changes no threadId, content, or history. Partial or total rename failure does not overturn the
   proven writer close, but C must report `title sync warning` with failed coordinates and must not
   claim the title was renamed.
5. Only after writer close, required readback, and completed title sync or warning, show the fixed
   closed-eye `🟢 CER closed` card from [roadmap.md](roadmap.md). Its header uses the package
   version read for this card and retains `writer closed`; then report the result, any title sync
   warning, and continuity limits. The closed-eye card proves only writer close and required
   readback, not all-green title sync. If `writer closed` or required readback is missing, show only
   the open-eye `🔴 Major blocker` card and do not show the closed-eye close card.
6. After successful close, that cycle's C/E/R task set becomes history-only and must not receive work for another cycle in the same workspace. A later cycle uses a new task through the unique-C gate, creates a brand-new E1, and uses only fresh Reviewers.

A new session may recover only from target-project sources that actually exist. If evidence is insufficient, label continuity as limited. If E1 coordinates cannot be verified, first prove that the original writer stopped before creating E2.

## Stop CER

When the user explicitly says `Stop CER and continue in a single thread.` or `/CER-stop`:

1. C stops sending new E1/R batches.
2. If there is no active writer, C continues in a normal single thread.
3. If E1 has started writing, C first asks E1 to stop, return the current result or blocker, and state whether the writer is closed.
4. Only after C reads back a verifiable state with no active writer or a stopped writer, show the fixed closed-eye `⚪ CER stopped` card from [roadmap.md](roadmap.md). Its header uses the package version read for this card and retains `CER inactive`; then return to single-thread work.
5. If the writer cannot be proven stopped or required readback is incomplete, show only the open-eye `🔴 Major blocker` card. Do not show the closed-eye stop card or assume the workspace is safe.

`/CER-stop` is not `/CER-close`. The first turns off the CER collaboration topology. The second performs CER closeout and required persistence. Plain close/finish messages belong to the target workspace's existing governance and do not map to CER stop or close.
