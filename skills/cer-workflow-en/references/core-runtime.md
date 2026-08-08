# CER Core v1 Runtime

## Contents

- [Roles](#roles)
- [Knowledge Foundation](#knowledge-foundation)
- [Bear-Card Package Version](#bear-card-package-version)
- [Commands](#commands)
- [Controller Preflight](#controller-preflight)
- [Outcome Anchor And Progress Gate](#outcome-anchor-and-progress-gate)
- [Ambiguous Tool Outcomes, Role Reconciliation, And Batch Deduplication](#ambiguous-tool-outcomes-role-reconciliation-and-batch-deduplication)
- [Startup](#startup)
- [Self-Contained Dispatch](#self-contained-dispatch)
- [Delivery](#delivery)
- [Execution Loop](#execution-loop)
- [Adaptive Batch Acceleration](#adaptive-batch-acceleration)
- [YAGNI And Stop](#yagni-and-stop)
- [Standalone Persistence And Closeout](#standalone-persistence-and-closeout)
- [Stop CER](#stop-cer)

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

CER has only the formal roles C, E1, R, and E2. C may use an inline, informal, on-demand
capability under [Parallel Candidate Producers](parallel-producers.md), but it is not a fifth
role and does not change the single E1 writer, fresh R, or E2 takeover boundaries. Only that
reference owns the complete activation, isolation, candidate convergence, and fail-closed rules.

## Knowledge Foundation

CER is not limited to engineering. When a task depends on medicine, law, finance, investment, policy, academia, business, design, operations, content, or other specialist knowledge, C defines a risk-proportionate knowledge foundation first: domain scope, authoritative sources, terminology, data year or version, quality standard, choices AI cannot make for the user, and uncertainty that must be disclosed. Prefer existing project sources of truth and user-provided sources. If a critical source is missing, stop and label the unknown. Do not turn general knowledge into a professional conclusion.

An E1 batch contains only the knowledge-foundation summary, source coordinates, and boundaries needed for that batch. R independently tests high-risk claims, source use, reasoning, and conclusions against the same foundation, rather than checking format alone. Do not create a knowledge-foundation document for a simple low-risk task; include the necessary content in the self-contained dispatch or checkpoint.

## Bear-Card Package Version

Before showing any lifecycle or checkpoint bear card, read `VERSION` from this Skill root next
to `SKILL.md`. Accept only complete content matching stable semver `X.Y.Z`; when valid, render it
in the card header as `vX.Y.Z`. If `VERSION` is missing, unreadable, or malformed, show
`version unverified` in the card header.

The card shape must use only the Handoff Kit layout-style ASCII bear templates in
[roadmap.md](roadmap.md), output as a standalone fenced `text` code block. Do not put a card in a
bullet, block quote, or ordinary paragraph.

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

Before creating this cycle's E1, reusing the existing E1 in the same cycle, or dispatching any real E1/R batch, C completes an adaptive task contract. This is not a form-filling ceremony. For simple low-risk work with one clear endpoint, C may complete it internally and proceed with a short summary. For long-running, multi-batch, or new product, flow, design, content, or experience work, C maintains a living task brief and compresses the necessary answers into a first-public-alignment roadmap and self-contained dispatch. The living task brief is not a new workflow and does not create fixed project documents; it is only C's working surface for the currently adjudicated task state inside this CER cycle.

C judges only five items, each marked `confirmed`, `safe inference`, or `critical missing`:

- Endpoint: what observable endpoint exists, and what is explicitly out of scope.
- Sources: what must be read before completion can be judged, what has been read, and what key unknowns remain.
- Root cause and boundary: why CER is needed, and what the smallest acceptable E1 batch is.
- Permissions and stops: what AI can handle directly, whether first public alignment is needed, and what truly requires user decision or stopping.
- Acceptance and proportion: what evidence can disprove the approach, and whether acceptance is just sufficient rather than defensive expansion.

The three states have evidence boundaries. `confirmed` may come only from an explicit user statement or an authoritative source C has actually read, and C must be able to point to the source anchor. An unsupported assumption must not be labeled `confirmed`. A `safe inference` must pass a counterfactual test: if the opposite assumption were true, the deliverable, user flow, collaboration method, data handling, permissions/risk, acceptance, and rework would still not materially change. If multiple reasonable answers would produce materially different outcomes, the item is `critical missing`.

<!-- cer-truth-source-intake-gate-owner -->
The truth-source intake gate is the sole owner inside Controller preflight; do not create another document, role, or fixed table for it. For any completion condition that could materially affect this batch's outcome, permissions, acceptance, owner, or protected meaning, C must answer four items before dispatching a formal implementation batch: who owns it; who actually uses it; how it takes effect; and what counterexample can disprove it. `Who owns it` means the source anchor in a user decision, project source of truth, rule, file, or external authority. `Who actually uses it` means how E1, R, the deliverable, install surface, public surface, later batch, or user flow consumes that condition. `How it takes effect` means how it changes this batch's dispatch, deliverable content, permissions, acceptance, or outcome judgment. `What counterexample can disprove it` means the readback, test, Reviewer question, or counterexample that would make this batch unable to count as successful. If any item cannot be answered, or if the answer depends on a required source C has not read, the condition is `critical missing`; C must not dispatch a formal implementation batch and may only perform necessary read-only diagnosis, narrow the acceptance scope, or use a `🟡 User decision` stop. Simple, one-step, low-risk work with one clear endpoint may pass this gate internally, but only when omitted answers would not materially change the result. Do not expand this gate into default full-text ingestion, whole-repo review, or fixed Full Audit.

For work that needs first public alignment or mid-course convergence, the living task brief lists at least: confirmed requirements/exclusions, safe inferences, critical gaps, latest user feedback, current batch freeze, next observable preview or decision point, and what changed from the previous version. C freezes only the next safely executable batch. Later direction may stay provisional until the user sees an intermediate result, adds information, or R produces contrary evidence. When user feedback, source readback, or R evidence changes direction, scope, deliverable shape, or acceptance, C first updates the living task brief and roadmap delta before dispatching the next batch. If an already-dispatched batch is affected, C refreezes with a new `batchId`/`payloadDigest` or supersedes the old batch first under the batch-deduplication rules.

Before dispatch, C performs one short QC pass: check that every `confirmed` item has a source, that every `safe inference` passes the counterfactual result, and that the current batch freeze has not promoted an assumption into `confirmed`. If QC fails, C must not create/reuse E1 or dispatch real work. C may only perform necessary read-only investigation, or use a `🟡 User decision` stop with at most three questions that would materially change the result.

`critical missing` means C cannot safely judge or dispatch. C may only perform necessary read-only investigation. If information that would materially change the result is still missing, use a `🟡 User decision` stop and ask at most three questions. Only after preflight passes does C verify communication coordinates and `ready`. E1/R dispatches use the latest living task brief and current batch freeze; assignees may report contradictions, blockers, or candidate corrections, but must not expand the goal, sources, permissions, or acceptance on their own.

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

## Outcome Anchor And Progress Gate

For long-running, multi-batch, or rework-prone CER work, C fixes an immutable `outcome_anchor` before the first real dispatch. It stores only the user's request and coordinates to read project authorities; it does not interpret or rewrite professional content. It includes at least: the user-facing accepted outcome, authoritative source pointers for completion conditions, unacceptable substitute outcomes, and explicit exclusions. A new anchor may be created only after the user explicitly changes the target, an authoritative source changes, or C obtains a required checkpoint decision; the new anchor must state the delta from the previous anchor. E1, R, and adjacent mechanism work must not rewrite `outcome_anchor` on their own.

C classifies each work lane as `mainline_outcome`, `diagnostic`, `mechanism_improvement`, or `governance_self_improvement`. Only `mainline_outcome` may increase mainline progress. Diagnostic work may create a necessary prerequisite for a later batch, but it does not count as outcome progress. Generic mechanism or governance self-improvement must prove it is the smallest necessary way to remove a blocker to the original outcome; otherwise it is recorded separately and does not block the mainline.

Before any non-exploratory real batch, C must be able to answer: which unfinished condition this batch improves; what readable before/after difference success will create; whether dependencies, authoritative sources, and handoff path exist; and, if success would still not improve `outcome_anchor`, why it is still a necessary blocker-removal prerequisite. An implementation batch with zero expected outcome improvement and no necessary-prerequisite role must not be dispatched. Batches that only create diagnostics, evidence, candidates, designs, or reviews must be labeled as non-mainline progress.

Activity is not outcome. Candidate creation, review completion, structural or format pass, file consistency, issue logging, design completion, version renaming, or packaging changes do not automatically increase mainline progress. C may report outcome progress only after reading back and accepting a difference against one of the user's completion conditions. Final reporting prioritizes accepted outcomes, not batch, task, or review counts.

<!-- cer-result-disposition-gate-owner -->
The result disposition gate is the sole owner in this section. Before C accepts a candidate, reports progress, updates target-project sources of truth, or hands a prior result to the next batch, C must state the effect of that adjudication. A low-risk small batch may use one short summary; a high-risk or multi-batch handoff must be readable: `accepted_as` is `evidence_only`, `working_candidate`, `terminal_deliverable`, or `authoritative_input`; `authority_effect` is `none` or `existing_authority_updated`; `progress_effect` is `none` or `accepted_outcome_delta`; and `permitted_next_use`, `forbidden_next_use`, and whether existing target-project persistence is required are explicit. Carry-forward use of a prior result must also classify `prior_result_use` as `working_material` or `authority_input`; if it is `authority_input`, C must list `promotion_evidence` and `project_owner_anchor`. Bare `RESULT_ACCEPTED` means only that C adjudicated this batch and that communication can deduplicate it; it does not mean global authority promotion, mainline outcome progress, or permission for a later batch to use the result as authoritative input.

Candidates, drafts, diagnostics, derived outputs, and review-only results default to `working_material` only. To promote one to `authoritative_input`, C needs an explicit user decision or an actually read target-project owner anchor, promotion evidence, and readback evidence; if any is missing, the next batch stays at `dispatch_blocked`. When C uses a Reviewer verdict as an adjudication basis, it must separate `content_verdict`, `implementation_verdict`, `outcome_verdict`, and `authority_promotion_verdict`; a content or technical PASS does not automatically become an outcome PASS, authority-promotion PASS, or mainline progress. Any dimension R did not review is only `not_reviewed` / `out_of_scope`, `out_of_scope` is not PASS, and C must not expand R's original review scope. Only when the `outcome_anchor` itself asks for a draft, candidate, or sample as the endpoint may a `working_candidate` become a valid `terminal_deliverable`; that still does not promote it into an authoritative source.

If a result changes the current phase, artifact role, next product route, authoritative source, progress claim, or later batch input, C must first have the proper writer update the target project's existing persistence surface and read it back under that project rules. While persistent truths conflict, are not synchronized, or the artifact role cannot be determined, `next_dispatch` must be `blocked`. CER does not prescribe a fixed handoff, docs, registry, or database; it requires only a readable synchronized terminal state from the target-project owner.

<!-- cer-controller-drift-checkpoint-owner -->
The long-task drift checkpoint is the sole owner in this section; do not create another monitoring role, background process, or fixed table for it. For long-running, multi-batch, or context-pollution-prone work, C performs one bounded drift checkpoint at resume/context transition, after two consecutive batches with no accepted outcome difference, on the second same-class failure, when E1/R proposes an adjacent direction change or substitute deliverable, when the user changes direction or adds constraints, and before close/release/major delivery: whether the next batch still improves an unfinished `outcome_anchor` condition; what readable outcome difference success will create; and whether E1/R or adjacent improvements are replacing the mainline outcome. If any item cannot be answered, C must not dispatch a formal implementation batch and may only switch to diagnostic work, narrow acceptance, stop for user decision, terminate the route, or create a fresh R when C cannot reliably disprove the risk and the risk level justifies it. A checkpoint, living task brief, or roadmap update does not count as outcome progress; it must not trigger background monitoring, polling, automatic `wait_threads`, fixed R, fixed Full Audit, or apply to simple, one-step, low-risk work with one clear endpoint.

A same failure class is judged by shared root cause, user consequence, affected completion condition, and method. Renaming, version changes, repackaging, wording changes, or redispatching the same fix do not create a new class. After two consecutive unresolved attempts in one class, C must not dispatch a third same-class repair or same-method retry. C must return to root cause analysis, use a materially different method, narrow validator claims, stop for user decision, or terminate that route.

## Ambiguous Tool Outcomes, Role Reconciliation, And Batch Deduplication

This section applies to side-effecting task/thread creation and to ready, accept, stop, formal
dispatch, batch-state, result, and acceptance control messages. C uses only `confirmed`, `pending`,
`outcome_unknown`, `duplicate`, and `blocked` for each operation. A tool failure, timeout, partial
result, or non-authoritative alias must not be treated as proof that the operation did not happen.

- Before creating a role, C takes one bounded pre-create snapshot over the participating hosts,
  project, target root, cycle, and role for this cycle. The snapshot is transient reconciliation
  evidence and must not become a lock, central registry, or CER run ID.
- Creation is `confirmed` only when an official receipt or authoritative readback provides the
  actual coordinates required by the active tool schema, project, and target root. This usually
  includes at least threadId; hostId is used only when the active tool schema or receipt requires
  or provides it. A `clientThreadId`, timeout, error, or
  partial result leaves the operation `pending` or `outcome_unknown`, not definitely failed.
- `outcome_unknown` forbids automatic retry. C performs one bounded control-plane reconciliation:
  compare the pre-create snapshot with official task/thread listings from every participating host,
  matching candidates by project, target root, cycle, role, and creation intent. One reconciliation
  may include authoritative snapshots before and after a platform-known settle interval. This is
  failure recovery, not result polling.
- Zero candidates after the settle interval still means `blocked` and does not authorize another
  automatic create. Before any later resume, startup, or creation of the same role, the pending
  operation must receive another authoritative reconciliation so a delayed orphan task is found.
  One candidate still requires official metadata plus zero-write `ready`. More than one candidate
  means `duplicate`.
- Canonical routing coordinates come from C's official readback under the active tool schema:
  threadId plus any routing coordinate the receipt explicitly requires. Do not make hostId a hard
  requirement. Do not derive hostId from a task's self-reported `local` value, display alias, title,
  sessionId, threadId shape, or an error message. `ready` still identifies role, target root, and
  return target. A mismatch with official metadata requires reconciliation before formal work.
- When duplicate roles exist, every candidate stays zero-write. C may select one only after every
  candidate is proven not to have received formal work and to have made zero writes. Unselected
  candidates receive `STOP_ZERO_WRITE` and prove stop through direct-push confirmation or an
  officially readable non-working terminal state. Archive state, title, or merely sending the stop
  instruction is not stop proof. Missing stop evidence for any candidate means `blocked`; availability
  pressure does not weaken this boundary.
- If any duplicate E1/E2 may have received formal work or written, C stops all new dispatch and
  reads back writer and workspace state. First send a stop instruction with a stable `messageId` to
  every possible writer, then prove every writer stopped through direct-push or official terminal
  readback. Next determine touched surfaces, candidate outputs, and workspace consistency. Only
  after state is determinate may C select one existing writer to recover or, after every old writer
  has stopped, create E2 under the existing takeover rule. Do not roll back automatically or simply
  choose one and continue.
- Every formal batch uses a unique stable `batchId` for the cycle, bound to the cycle, role,
  C-selected threadId or platform-equivalent coordinate, routing coordinates explicitly required by
  the active tool schema/receipt, target root, a recipient-local monotonically
  increasing `batchSeq` for the cycle, and immutable `payloadDigest`. The digest covers the complete
  self-contained dispatch. Any content or task-contract change uses a new `batchId` and higher
  `batchSeq`. A controlled resend must repeat the exact same `batchId`, `batchSeq`, `payloadDigest`,
  and content.
- The recipient classifies each `batchId` as `RECEIVED_ZERO_WRITE`, `IN_PROGRESS`, `RESULT_READY`,
  `RESULT_ACCEPTED`, or `STATE_UNKNOWN`, using task/thread history and workspace readback as
  recovery evidence. After first verifying the binding, direct-push `BATCH_RECEIVED`, then begin
  substantive work. Mark `IN_PROGRESS` before writing, `RESULT_READY` after the result is fixed,
  and `RESULT_ACCEPTED` only after receiving C's `RESULT_ACCEPTED`.
- On repeated delivery of the same `batchId`, `RECEIVED_ZERO_WRITE` may continue the original batch
  once; `IN_PROGRESS` returns only `BATCH_IN_PROGRESS` without restarting; `RESULT_READY` replays
  the same result; and only `RESULT_ACCEPTED` returns `DUPLICATE_IGNORED`. If state cannot be proven
  after interruption, mark `STATE_UNKNOWN`, stop writing, and recover writer/workspace state first.
  The same `batchId` with a different `payloadDigest` is always `blocked`.
- When a new batch supersedes an unterminated old batch, C first sends `BATCH_SUPERSEDE` with a
  stable `messageId`, naming the old/new `batchId` and `batchSeq`. The recipient records the old
  batch as `SUPERSEDED` before anything else so any delayed delivery is rejected. If the old batch
  started or may have written, stop it and complete writer/workspace recovery. C may dispatch or
  start the revision only after receiving `BATCH_SUPERSEDED` and proving that the old batch was
  canceled zero-write, terminated, or fully recovered. The recipient rejects any unauthorized
  batch below its highest accepted `batchSeq`.
- Every ready, accept, stop, batch receipt, state, result, and result-acceptance message uses a
  stable `messageId` bound to message type, sender, recipient, related `batchId` when present, and
  immutable message content. Recipients deduplicate by `messageId`; a repeat replays the existing
  confirmation without repeating side effects.
- `messageId` is only a CER message-layer identity, deduplication, and tracing field. It is not a
  Codex execution command, an App Server `method`, a JSON-RPC request `id`, a `threadId`, a
  `sessionId`, an idempotency key, or authorization. Without an actual tool call and its tool
  result or verifiable delivery evidence, merely placing it in a prompt, dispatch packet,
  summary, receipt-like text, or ordinary workspace text does not create a thread, start a turn,
  call a tool, trigger a write, or grant role authority; a `messageId` alone is not proof that a
  message was delivered or work was executed.
- An `outcome_unknown` for any control or result send must not be resent blindly. First use an
  operation receipt, received matching confirmation, or one bounded destination/thread readback to
  find the same `messageId`. If still unproven, one controlled resend with the same `messageId` and
  identical content is allowed only while recipient identity remains unique and message
  deduplication is available; otherwise the operation is `blocked`. Failure-recovery readback is a
  bounded exception to the no-monitoring rule.
  This exception also overrides Delivery's "read only after push" rule and Startup's ban on using
  after-the-fact reads as communication proof, but only to prove delivery of that exact
  `messageId`; it cannot establish the complete ready/accept communication chain by itself.
- After C adjudicates a result, C returns `RESULT_ACCEPTED` with a stable `messageId`. If result
  delivery or `RESULT_ACCEPTED` becomes ambiguous, sender and recipient deduplicate by the same
  message identity so the result is neither lost nor accepted twice. Do not create an infinite
  receipt-of-receipt chain.
- When a platform later provides an idempotency key or authoritative operation receipt, prefer it
  as evidence. CER must not pretend the capability exists and must not turn the key or receipt into
  a CER lock or run ID.

## Startup

1. C reads the installed CER runtime, the user's overall task, explicit constraints, and authoritative rules that actually exist in the target workspace.
2. The startup gate is owned by the Remote sender or the local start task. A receiver task may only return candidate `C_READY`; it must not blanket-reject Remote C solely because the message came from another task, and it must not use silence, no response, or its own inability to see other tasks as proof of unique C.
3. The startup gate judges unique C only inside the actual collaboration domain for this start: use the official task/thread list or a platform-equivalent tool to enumerate every participating host this start will use; for readable candidates, verify resolved target_root/cwd, `🚀 C:` identity, and active/idle/closed/handed-off state; also require the sender to explicitly state that it has not assigned the same root to another C. Only when all participating hosts are enumerable and no active C exists may the gate judge no active C. Do not scan outside-platform or non-participating hosts, but also do not treat invisible tasks as nonexistent.
4. A known active C may only be reused within the same cycle. Transfer requires an actual message or state readback showing the old C explicitly handed off/closed. After `/CER-close`, the old C and its E/R tasks remain history only and the whole set must not receive work for a later cycle in the same workspace. A later cycle must use a new task as C; the gate reads back that the old C is `closed`/`handed-off`, that no active C exists, and that every participating host is verifiable. If any participating host cannot be enumerated, old C state or candidate root/identity/state cannot be read back, coordinates are incomplete, or evidence conflicts, the state is unknown and the gate stops without creating a second C.
5. After an explicit Remote CER start, the Remote receiver task first direct-pushes candidate `C_READY`, including its threadId or platform-equivalent coordinate, target_root, return target/path, and any return or routing coordinate explicitly required by the active tool schema/receipt; it must not guess hostId. After the sender completes unique-C verification and actually reads back `C_READY`, the sender must send `C_ACCEPTED` to the receiver through the same usable return path. The receiver becomes active C and starts Controller preflight only after receiving `C_ACCEPTED`. Merely sending `C_READY`, failing to read back `C_READY`, or missing `C_ACCEPTED` leaves Remote C identity and communication path unestablished. If the sender was the active C, it must complete handoff/close before sending `C_ACCEPTED`.
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
   label failure into a fake lifecycle or identity failure. When the Codex title tool is available,
   the initial prompt, model-generated title, or first-line label must not substitute for sidebar
   rename. After a `create_thread` receipt, C immediately calls the official title tool, currently
   `set_thread_title` in the Codex schema, and reads the title back with `list_threads`,
   `read_thread`, or platform-equivalent readback. Before that readback, C must not accept that
   role's `ready` as qualifying or send a formal batch. C names or identifies its visible
   task/thread as `🚀 C:01｜<very short task name>`. If the platform cannot change the title, use an
   equivalent role label in the first visible message or checkpoint card. Plain `C:` is not an acceptable Controller title/label.
8. C completes Controller preflight, creates or updates the living task brief, and freezes only the next safely executable batch. If anything is `critical missing`, C may only perform necessary read-only investigation or stop for questions; C must not create/reuse E1 or dispatch real work.
9. After Controller preflight passes, C completes a communication preflight. Use available tools to prove the actual path, including identity source, target root, required parameters, send path, recipient, visible title or role label, return source available to the assignee, verifiable threadId or platform-equivalent coordinates, and C's adjudication point. sessionId is recorded only when the active tool schema/receipt explicitly requires or provides it, and never substitutes for threadId or derives hostId.
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
    threadId or platform-equivalent coordinates.
12. C creates a brand-new persistent E1 for this cycle through official `create_thread`. E1 first
    direct-pushes a zero-write `ready`. C must actually receive a qualifying zero-write `ready`
    with the correct role, cycle number, sidebar-visible title/label, thread coordinates, and
    return target. Later batches in the same cycle keep reusing that same E1 and the E1 threadId
    remains the same. A later cycle after a completed `/CER-close` uses a new cycle number, creates
    a brand-new E1 and only fresh Reviewers; it must not reuse any E/R task or coordinate from the
    previous closed C.
13. If any communication preflight link is missing, or the assignee does not actually direct-push a qualifying zero-write `ready`, C shows only the open-eye `🔴 Major blocker` card and stops. C must not show the successful start card. A wait snapshot, completion state, commentary, polling, after-the-fact reads, document review, successful forking, and successful one-way sends do not prove communication. If the platform does not automatically wake an idle C, C still must not wait by itself; the state remains `POST_DISPATCH_PARKED` / `delivery_incomplete` until direct-push becomes main-session input or the user explicitly requests a one-time check.
14. Only now is `CER-start` successfully accepted. C's first user-visible success receipt must be the fixed open-eye `🔵 CER started` card from [roadmap.md](roadmap.md). Keep the complete three-line ASCII bear: version on the first line, status on the second line, and only the bear base line on the third line; output it as a standalone fenced `text` code block. Single-batch and multi-batch starts use the same card. Do not use a closed-eye card or guess a version.
15. Later batches in the same cycle do not repeat the handshake while C, E1, the return target, and verifiable coordinates remain the same. Repeat `ready` whenever the coordinates or return target changes.
16. For long-running, multi-stage, multi-batch, or first-public-alignment work, show the initial progress surface under [roadmap.md](roadmap.md) after the fixed start card and before the first batch. A simple single-batch task with one clear endpoint needs only a short summary.
17. C may send the first real batch only after the fixed start card is shown and the required initial roadmap or short summary has been added.

If the user did not explicitly invoke CER and the work is one low-risk step, handle it normally. Once the user explicitly invokes CER, do not silently remove the role topology because the task appears simple. Plain start/work messages belong to the target workspace's existing governance and are not CER triggers.

## Self-Contained Dispatch

Each real E1 or R batch contains only what is needed:

- role and one objective;
- target root;
- required sources of truth and accepted background;
- summary of the truth-source intake four questions passed in Controller preflight: who owns it, who actually uses it, how it takes effect, and what counterexample can disprove it;
- `outcome_anchor`, work-lane classification, target completion condition, and expected outcome difference;
- when this batch uses a prior E/R result, the Result Disposition Gate's adjudicated `prior_result_use: working_material | authority_input`, whether it is working material only; if it is `authority_input`, include `promotion_evidence`, `project_owner_anchor`, readback evidence, and forbidden uses;
- allowed and forbidden scope;
- acceptance checks and a counterexample that can disprove the solution;
- stop conditions;
- the stable `batchId`, monotonically increasing `batchSeq`, immutable `payloadDigest`, and bound cycle, recipient threadId or platform-equivalent coordinate, routing coordinates explicitly required by the active tool schema/receipt, and target root;
- the living task brief and current batch freeze, including handling of any `confirmed`, `safe inference`, or `critical missing` item, required source anchors, and counterfactual results;
- C direct-push return target and threadId or platform-equivalent coordinates; sessionId is recorded only when the active tool schema/receipt explicitly requires or provides it, and never substitutes for threadId or derives hostId;
- the knowledge foundation, source coordinates, unknowns, and no-go boundaries needed for the batch;
- a short result format.

The initial `create_thread` prompt for a new E1/R is not a formal batch. It may carry only a
zero-write ready handshake: role, cycle/title, target root, C return target, no-write and
do-not-start-work instructions, and a request to report its own coordinates and source
availability. Do not put the complete source corpus, candidate work content, or formal batch
payload in the create prompt, and do not ask E1/R to process content before ready. If that has
happened, C treats it as a pre-batch payload leak / batch lifecycle violation and stops or
refreezes; C must not treat a later duplicate ack for the same digest as normal efficient
communication. If the assignee cannot read the large input from an authorized source of truth,
C sends it exactly once in the formal `sendable_packet`; inputs that are too long or cross risk
boundaries are split into multiple formal batches by semantic/risk unit. If the assignee can read
from an authorized source of truth, the dispatch packet prefers source coordinates, digest,
necessary excerpts, and no-go boundaries rather than repasting the entire corpus.

A `sendable_packet` for long-running, multi-batch, high-risk, or non-simple formal implementation work must include a compact `pre_dispatch_evidence` block. It is not a new source of truth, fixed form, background monitor, or Full Audit; it only makes C's existing Controller-preflight and `outcome_anchor`/drift judgments readable to the assignee. It includes at least: an `outcome_anchor` pointer or summary; the unfinished condition this batch improves and the readable outcome difference success should create; the truth-source intake four-question summary with source anchors; required sources read and the disposition of remaining unknowns; work-lane classification; and, when a drift checkpoint trigger exists, the checkpoint conclusion, or why no trigger applies. If it is missing, contradictory, depends on unread required sources, or merely says judgment was done without readable support, the packet is not sendable and C stays at `dispatch_blocked`. If E1/R receives a formal batch without required `pre_dispatch_evidence`, it must direct-push a zero-write blocker such as `BATCH_BLOCKED_MISSING_PRE_DISPATCH_EVIDENCE` and stop; it must not write, review, or fill in C's missing judgment. Simple, one-step, low-risk work with one clear endpoint may pass with a short summary and must not be forced into a large form.

Do not write "see above" or ask the assignee to reconstruct C's context. Add background and counterexamples for high-risk batches. Keep low-risk batches short and avoid oversized templates. E1 is authorized only to execute the current batch freeze; it must not treat provisional later direction as a complete specification or fill in future batches on its own. If E1/R finds a contradiction between the living task brief, current batch freeze, `outcome_anchor`, and sources, report a blocker or candidate correction first; do not rewrite the contract and continue alone. R reviews against the latest task brief, current batch freeze, candidate identity, and delivery evidence, and also checks the immutable `outcome_anchor`; it does not review against the initial prompt or stale assumptions. R must also answer whether the batch still serves the original outcome, whether it creates an acceptable outcome difference, whether it is only activity or rework, and whether it substitutes another deliverable shape for what the user originally asked for. A technically valid batch with no outcome improvement must not be reported as ordinary success progress.

A dispatch packet may remain a `draft_packet` inside C, but a sendable `sendable_packet` must not retain `<...>` placeholders. A real dispatch must fill actual `threadId` or platform-equivalent coordinate, `returnTarget`, `messageId`, `batchId`, `batchSeq`, `payloadDigest`, and any routing coordinate explicitly required by the active tool schema/receipt. sessionId is not a substitute for threadId as a formal dispatch coordinate. hostId is used only when the active tool schema or receipt requires or provides it; do not make hostId a cross-platform hard requirement, and do not derive hostId from `local`, title, sessionId, threadId shape, or an error message. Relative wording such as `same E1`, `the E1 above`, or `next sequence` is draft-only and must be replaced with verifiable concrete values before send. R dispatch must fill actual `candidateIdentity`, `candidateManifest`, and candidate delivery evidence. Missing any one of these leaves the packet at `dispatch_blocked` or `decision_blocked`; C must not self-rate it as sendable or ask E1/R to guess.

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

- E1 and R direct-push zero-write `ready` through the formal messaging tool before work. After a
  formal batch arrives, direct-push `BATCH_RECEIVED` with that batch's `batchId` and
  `payloadDigest`, then begin or recover work according to the batch lifecycle.
- `ready` includes the assignee's role, visible title or first-line label, threadId or
  platform-equivalent coordinates, received target root, return target, and whether required
  sources are available. sessionId is recorded only when the active tool schema/receipt explicitly
  requires or provides it, and never substitutes for threadId or derives hostId. Every message carries a stable `messageId`; `BATCH_RECEIVED` also includes routing
  coordinates explicitly required by the active tool schema/receipt and the binding-check result.
- On completion, blockage, or incomplete work, direct-push a short result to C before stopping.
  Include `messageId`, `batchId`, `payloadDigest`, and threadId or platform-equivalent coordinates so C cannot accept
  another task's, another batch's, or another revision's result by mistake. C returns
  `RESULT_ACCEPTED` after adjudication.
- On repeated delivery of the same `batchId`, recover according to `RECEIVED_ZERO_WRITE`,
  `IN_PROGRESS`, `RESULT_READY`, `RESULT_ACCEPTED`, or `STATE_UNKNOWN`; do not rerun blindly. The
  same identity with a different digest blocks immediately.
- Unless a participant has observed an explicit `outcome_unknown` and follows this section's
  failure-recovery rule for the exact `messageId`, C performs one bounded readback and adjudication
  only after receiving the push. Recovery readback may verify only whether that control message was
  delivered or misrouted; it must not expand into waiting, polling, background monitoring, or
  progress tracking.
- After dispatch, task creation, or send, C immediately enters `POST_DISPATCH_PARKED`. In this
  state, C must not automatically use `wait_threads`, `read_thread`, or a platform-equivalent tool
  to wait, wake itself, track progress, read commentary, read finals, probe status, or discover
  results. The normal path that may advance state is an assignee direct-push becoming actual input
  to C / the main session, or an authoritative delivery receipt from the tool.
- `POST_DISPATCH_PARKED` has only two read exceptions: a one-time thread check explicitly requested
  by the user in the same turn, or one bounded readback for verification/adjudication after C has
  received a direct-push. The first is user-directed diagnosis, not automatic coordination or formal
  delivery evidence; the second must not expand into another wait, polling, or commentary tracking.
- Without a direct-push, a wait snapshot, completion state, commentary, summary, child final, task
  title, user relay, or passive read cannot advance `pending` / `delivery_incomplete` to ready,
  done, PASS, RESULT_READY, or RESULT_ACCEPTED, and cannot trigger the next batch.
- A controlled resend of the same logical message is not a new formal send. After reconciliation,
  only the single same-`messageId`, identical-content resend allowed by this section may be used.
  After the resend, C returns to `POST_DISPATCH_PARKED`; extra control messages, renaming, cycle
  label changes, or repackaging must not reopen a wait budget.
- "No monitoring" forbids automatic waiting, repeated waiting, polling, background listening,
  repeated status probes, accepting a wait snapshot as a result, and passive thread reads before
  push. A user-explicit one-time check and one verification readback after push remain allowed.
- Unavailable delivery blocks delegation only. C may still perform authorized read-only research, analysis, and adjudication, but C may not write in E1's place.

## Execution Loop

1. C gives this cycle's same E1 one batch based on the user's task, `outcome_anchor`, the living task brief, the current batch freeze, and accepted project plan or sources of truth.
2. E1 completes only that batch, reads back and tests the work, then direct-pushes a candidate.

<!-- cer-unexpected-failure-gate-owner -->
An unexpected failure does not change the batch authority: tests produce evidence but do not grant
more modification authority. A file being in allowed scope does not authorize E1 to change another
owner, authoritative source, or protected meaning inside that file.
The gate stays inactive when an ordinary batch has no unexpected failure, or when a failure does
not motivate a new or expanded write.

Before any new or expanded write motivated by an unexpected failure, E1 performs bounded read-only
attribution:

- Reproducible evidence proves the current batch directly caused the failure, and the repair does
  not change the frozen owner, meaning, source, permission, or acceptance: E1 may repair it in the
  current batch.
- A comparable, verifiable pre-batch baseline proves the problem already existed: report it without
  repairing it.
- Causality cannot be proved; the failure comes from a flaky test, environment, or dependency;
  acceptance itself may be wrong; or repair would change another owner, authoritative source,
  admission condition, fallback, product or specialist meaning, or cross-subsystem behavior: stop
  further writes and return the current result, checks run, unknowns, and blocker to C.

Direct acceptance determines whether the batch candidate may be accepted. Full regression only
finds integration risk; its failure does not automatically authorize an adjacent repair. Even when
full regression is part of frozen acceptance, it blocks the candidate but does not expand E1's
repair authority.
Only C may refreeze the contract and expand scope by dispatching a new batch with a new
`batchId` and `payloadDigest`; C freezes the outcome and semantic boundary, not line-by-line
implementation.

3. C reads back the actual result, first judges whether it improves an unfinished condition in `outcome_anchor`, and then either adjudicates it or creates a fresh R through official `create_thread` according to risk.
4. R tests the specified risk, whether the whole result remains aligned to the original outcome, and product logic, not format alone.
<!-- cer-review-convergence -->
5. After R first reports a defect, C groups related findings by common root cause and user consequence, then performs one bounded read-only impact check to find the current sources of truth, delivery surfaces, and check locations that carry this round's contract.
6. C freezes this round's `owner/affected surfaces/acceptance/counterexample family` and gives the same E1 one batch to repair the whole affected boundary.
7. After the repair, R re-tests only the frozen scope. If a different root cause, different user consequence, or new regression caused by the latest repair appears, only C may attribute it, refreeze the boundary, and dispatch a new batch; E1 must not expand scope alone.
8. Changed wording, sentence order, or synonymous phrasing remains the same problem. Do not append rules or validator patterns sentence by sentence. If the same counterexample family keeps escaping a mechanical check, C changes the checking method or narrows the validator's claimed capability.
9. When the frozen counterexamples pass, no material new defect remains, and the outcome difference has been read back, C accepts the result under the Result Disposition Gate. Only then may E1 update an existing authoritative project-progress source; if none exists, do not create one.
10. C stops after required state is converged. List adjacent improvements separately without adding a Reviewer, governance layer, or whole-repository re-review. A batch may end only as accepted outcome, a necessary prerequisite with a clear next handoff, honest blockage that returns to route selection, or route termination; "make another same-class revision" is not the default next step.
11. For long-running, multi-stage, or multi-batch work, progress updates and bear-card checkpoints follow [roadmap.md](roadmap.md). Use only facts read back and adjudicated after direct-push; do not poll E1.

For an ordinary small change, C readback and proportionate tests are enough. Re-review only the affected boundary after a high-risk fix. More Reviewers do not replace clear acceptance conditions.

## Adaptive Batch Acceleration

Adaptive batch acceleration is C's default internal scheduling strategy, not a user mode, Turbo
setting, or slash command. It does not change C/E/R roles, the single-writer invariant, safety
gates, independent review, or acceptance standards:

- C establishes an evidence-validity window at each checkpoint. One read and location pass may be
  reused across dependent work only while the reviewed object, requirements, direct dependencies
  and environment premises, delivery artifact, and validation method are unchanged or proven
  equivalent, with no credible contradiction. A fresh R independently reads the frozen raw
  evidence; C/E summaries do not substitute for R evidence.
- `no_material_delta` may stop a planned write batch only when current authoritative readback
  already proves acceptance. Evidence gathering, review, audit, and failure-recovery batches must
  not be skipped merely because they make no file writes.
- New facts within one checkpoint may be collected together and advance the validity window at
  most once. Any change in requirements, sources, dependencies, environment, artifact, validation
  method, or credible counterevidence immediately invalidates the affected conclusion and reopens
  its minimum sufficient evidence.
- Compatible acceptance commands and counterexamples may be co-scheduled, but each check retains
  its own output, exit status, provenance, and adjudication. Checks that depend on order, share
  mutable state, contend for exclusive resources, or can contaminate each other remain separate.
- Create one fresh R for each stable risk boundary and let that R review the complete candidate.
  Irreversible or high-consequence action requires the relevant R before the action and must not be
  delayed for batch consolidation. The same round's R may re-test the frozen boundary after repair;
  do not create a new R for every small step.
- Acceleration automatically turns off when communication or batch lifecycle is `pending`,
  `outcome_unknown`, `duplicate`, or `STATE_UNKNOWN`; single-writer state is unknown; source
  freshness or evidence identity is uncertain; a user decision is required; or credible
  contradiction appears. Normal CER rules then apply.
  `/CER-status` may report `active`, `partial`, or `off` with the reason, but must not poll for it.

## YAGNI And Stop

- Add roles, batches, Reviewers, checkpoints, tests, and synchronization only when the current risk and deliverable require them. Under one objective, C dispatches added E/R work or a task branch only when it is the smallest necessary means to complete the original goal or address a verified blocker; otherwise C consolidates, stops, or adjudicates directly.
- Do not create R when C can reliably accept the work through readback and proportionate tests. Do not re-review accepted areas when a narrow fix is enough.
- Stop when the requirements are met, core counterexamples pass, and required risk is cleared. List adjacent improvements separately without expanding automatically.
- Adjacent mechanism improvement, governance self-improvement, or diagnostic failure does not automatically block the original task. It becomes a mainline blocker only when it is a necessary dependency for an unfinished `outcome_anchor` condition and its absence makes the mainline outcome unsafe to accept.
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
- Archiving this cycle's R tasks is UI cleanup only after a successful close. Only R tasks that
  are complete, read back, and adjudicated by C may be archived with the official archive tool; C
  and E1 stay visible by default. Active, blocked, not-returned, or unadjudicated R tasks must not
  be archived. Archive is not deletion, changes no threadId, content, or history, and is not stop,
  review, or closeout evidence.

When the user explicitly says `Close CER.` or `/CER-close` to C:

1. C stops new dispatch, adjudicates candidates that can be safely decided, and organizes accepted work, incomplete work, risk, evidence, and next action.
2. C gives the same E1 one self-contained closeout batch.
3. E1 updates only the necessary existing progress or decision sources under target-project rules, marks that E1 has stopped writing, reads back the result, and direct-pushes it. If no durable source exists, E1 reports only the actual deliverable and `writer closed`.
4. After C reads back the deliverable, required sources, and `writer closed`, C uses the official
   title tool to automatically append `✓` after this cycle's cycle number in every verifiable
   C/E/R title, such as `🚀 C:01✓｜...`, `E1:01✓｜...`, and `R1:01✓｜...`; legacy/migration `00`
   may likewise become `00✓`. C then reads back the titles. This is a built-in display-only
   CER-close rename and does not ask the user again. It changes no threadId, content, or history.
   Partial or total rename failure does not overturn the proven writer close, but C must report
   `title sync warning` with failed coordinates and must not claim the title was renamed.
5. After writer close, required readback, and completed title sync or warning, if the official
   archive tool is available, C archives this cycle's complete, read-back, adjudicated R tasks.
   C must not archive C, E1, active R, blocked R, not-returned R, or unadjudicated R tasks. Archive
   failure does not overturn writer close, but C must report an archive notice with failed
   coordinates.
6. Only after any available R archiving is completed or reported, show the fixed closed-eye
   `🟢 CER closed` card from [roadmap.md](roadmap.md). It uses the package version read for this
   card and retains `writer closed`; then report the result, any title sync warning, R archive
   outcome, and continuity limits. If any R tasks were archived, the summary must say in the current
   output language: "Archived <count> Reviewer tasks for this cycle; archive is not deletion, and
   they remain available from archived tasks." The closed-eye card proves only writer close and
   required readback, not all-green title sync or R archiving. If `writer closed` or required
   readback is missing, show only the open-eye `🔴 Major blocker` card, do not show the closed-eye
   close card, and do not archive R tasks to create a clean-looking state.
7. After successful close, that cycle's C/E/R task set becomes history-only and must not receive work for another cycle in the same workspace. A later cycle uses a new task through the unique-C gate, creates a brand-new E1, and uses only fresh Reviewers.

A new session may recover only from target-project sources that actually exist. If evidence is insufficient, label continuity as limited. If E1 coordinates cannot be verified, first prove that the original writer stopped before creating E2.

## Stop CER

When the user explicitly says `Stop CER and continue in a single thread.` or `/CER-stop`:

1. C stops sending new E1/R batches.
2. If there is no active writer, C continues in a normal single thread.
3. If E1 has started writing, C first asks E1 to stop, return the current result or blocker, and state whether the writer is closed.
4. Only after C reads back a verifiable state with no active writer or a stopped writer, show the fixed closed-eye `⚪ CER stopped` card from [roadmap.md](roadmap.md). It uses the package version read for this card and retains `CER inactive`; then return to single-thread work.
5. If the writer cannot be proven stopped or required readback is incomplete, show only the open-eye `🔴 Major blocker` card. Do not show the closed-eye stop card or assume the workspace is safe.

`/CER-stop` is not `/CER-close`. The first turns off the CER collaboration topology. The second performs CER closeout and required persistence. Plain close/finish messages belong to the target workspace's existing governance and do not map to CER stop or close.
