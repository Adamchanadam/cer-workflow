# CER Core v1 Runtime

## Roles

- Controller (C): the only controller accepted through the local or Remote startup gate. C owns global judgment, source-of-truth mapping, batch adjudication, candidate readback, and user communication. C does not write the workspace.
- Executor (E1): one persistent, user-visible, reusable independent task for the same job and the only writer. E1 executes only C's self-contained batches, validates the work, and returns a candidate.
- Reviewer (R): created only for high risk, core promises, data integrity, safety, uncertain external capability, or when C cannot reliably disprove a claim. R is fresh, read-only, and bounded. R does not edit files or direct E1.
- E2: may be created only after the original E1 has verifiably stopped writing, the workspace is in a known state, and C has issued a takeover batch. Parallel writers are forbidden.

## Knowledge Foundation

CER is not limited to engineering. When a task depends on medicine, law, finance, investment, policy, academia, business, design, operations, content, or other specialist knowledge, C defines a risk-proportionate knowledge foundation first: domain scope, authoritative sources, terminology, data year or version, quality standard, choices AI cannot make for the user, and uncertainty that must be disclosed. Prefer existing project sources of truth and user-provided sources. If a critical source is missing, stop and label the unknown. Do not turn general knowledge into a professional conclusion.

An E1 batch contains only the knowledge-foundation summary, source coordinates, and boundaries needed for that batch. R independently tests high-risk claims, source use, reasoning, and conclusions against the same foundation, rather than checking format alone. Do not create a knowledge-foundation document for a simple low-risk task; include the necessary content in the self-contained dispatch or checkpoint.

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

Before creating or reusing E1, or before dispatching any real E1/R batch, C completes an adaptive task contract. This is not a form-filling ceremony. For simple low-risk work, C may complete it internally and proceed. For long-running or multi-batch work, compress the necessary answers into the initial roadmap or self-contained dispatch.

C judges only five items, each marked `confirmed`, `safe inference`, or `critical missing`:

- Endpoint: what observable endpoint exists, and what is explicitly out of scope.
- Sources: what must be read before completion can be judged, what has been read, and what key unknowns remain.
- Root cause and boundary: why CER is needed, and what the smallest acceptable E1 batch is.
- Permissions and stops: what AI can handle directly, and what truly requires user decision or stopping.
- Acceptance and proportion: what evidence can disprove the approach, and whether acceptance is just sufficient rather than defensive expansion.

The three states have evidence boundaries. `confirmed` may come only from an explicit user statement or an authoritative source C has actually read, and C must be able to point to the source anchor. An unsupported assumption must not be labeled `confirmed`. A `safe inference` must pass a counterfactual test: if the opposite assumption were true, the deliverable, permissions/risk, acceptance, and rework would still not materially change. If multiple reasonable answers would produce materially different outcomes, the item is `critical missing`.

Before dispatch, C performs one short QC pass: check that every `confirmed` item has a source, that every `safe inference` passes the counterfactual result, and that the frozen task contract has not promoted an assumption into `confirmed`. If QC fails, C must not create/reuse E1 or dispatch real work. C may only perform necessary read-only investigation, or use a `🟡 User decision` stop with at most three questions that would materially change the result.

`critical missing` means C cannot safely judge or dispatch. C may only perform necessary read-only investigation. If information that would materially change the result is still missing, use a `🟡 User decision` stop and ask at most three questions. Only after preflight passes does C verify communication coordinates and `ready`. E1/R dispatches use the same frozen task contract; assignees may report contradictions, blockers, or candidate corrections, but must not expand the goal, sources, permissions, or acceptance on their own.

## Startup

1. C reads the installed CER runtime, the user's overall task, explicit constraints, and authoritative rules that actually exist in the target workspace.
2. The startup gate is owned by the Remote sender or the local start task. A receiver task may only return candidate `C_READY`; it must not blanket-reject Remote C solely because the message came from another task, and it must not use silence, no response, or its own inability to see other tasks as proof of unique C.
3. The startup gate judges unique C only inside the actual collaboration domain for this start: use the official task/thread list or a platform-equivalent tool to enumerate every participating host this start will use; for readable candidates, verify resolved target_root/cwd, `🚀 C:` identity, and active/idle/closed/handed-off state; also require the sender to explicitly state that it has not assigned the same root to another C. Only when all participating hosts are enumerable and no active C exists may the gate judge no active C. Do not scan outside-platform or non-participating hosts, but also do not treat invisible tasks as nonexistent.
4. A known C may only be reused. Transfer requires an actual message or state readback showing the old C explicitly handed off/closed. If any participating host cannot be enumerated, candidate root/identity/state cannot be read back, coordinates are incomplete, or evidence conflicts, the state is unknown and the gate stops without creating a second C.
5. After an explicit Remote CER start, the Remote receiver task first direct-pushes candidate `C_READY`, including its threadId, hostId, target_root, and return target/path. After the sender completes unique-C verification and actually reads back `C_READY`, the sender must send `C_ACCEPTED` to the receiver through the same usable return path. The receiver becomes active C and starts Controller preflight only after receiving `C_ACCEPTED`. Merely sending `C_READY`, failing to read back `C_READY`, or missing `C_ACCEPTED` leaves Remote C identity and communication path unestablished. If the sender was the active C, it must complete handoff/close before sending `C_ACCEPTED`.
6. Do not add a lock file, central registry, run ID, conflict engine, new role, or test exception for unique C; uniqueness is judged only from existing sources, official enumeration, explicit coordinates, and this-turn actual return/readback evidence.
7. C names or identifies its visible task/thread as `🚀 C: <short task name>`. If the platform cannot change the title, use an equivalent role label in the first visible message or checkpoint card. Plain `C:` is not an acceptable Controller title/label.
8. C completes Controller preflight and freezes this task contract. If anything is `critical missing`, C may only perform necessary read-only investigation or stop for questions; C must not create/reuse E1 or dispatch real work.
9. After preflight passes, C completes a communication preflight. Use available tools to prove the actual path, including identity source, target root, required parameters, send path, recipient, visible title or role label, return source available to the assignee, verifiable session/thread ID or platform-equivalent coordinates, and C's adjudication point.
10. If the official create-task tool is unavailable, stop or reuse an existing same-platform task only when its send/return path and context boundary are already proven. A fork or delegation that carries source context cannot count as a fresh E1/R UAT.
11. When creating or reusing E1, R, or E2, titles or first-line labels must begin with `E1:`, `R1:`/`R2:`, or `E2:` without the rocket. Every dispatch, `ready` receipt, and result receipt must include sender role, recipient, return target, and session/thread ID or platform-equivalent coordinates.
12. If any communication link is missing, or the assignee does not actually direct-push `ready`, C issues `🔴 Major blocker`. Waiting, polling, after-the-fact reads, document review, successful forking, and successful one-way sends do not prove communication.
13. C creates or reuses one persistent E1. E1 first direct-pushes a zero-write `ready`. C sends real work only after receiving a `ready` with the correct role, title/label, session/thread coordinates, and return target.
14. Later batches do not repeat the handshake while C, E1, the return target, and verifiable coordinates remain the same. Repeat `ready` whenever the coordinates or return target changes.
15. When C classifies the task as long-running, multi-stage, or multi-batch, show the initial progress surface before the first batch under [roadmap.md](roadmap.md). A simple single-batch task does not require one.

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

## Delivery

- E1 and R direct-push `ready` through the formal messaging tool before work.
- `ready` includes the assignee's role, visible title or first-line label, session/thread ID or platform-equivalent coordinates, received target root, return target, and whether required sources are available.
- On completion, blockage, or incomplete work, direct-push a short result to C before stopping. Include session/thread coordinates so C cannot accept another task's result by mistake.
- C performs one bounded readback and adjudication only after receiving the push.
- "No monitoring" forbids waiting, polling, background listening, repeated status probes, and passive thread reads before a push arrives. One bounded read explicitly requested by the user, or a verification read after a push, remains allowed.
- Unavailable delivery blocks delegation only. C may still perform authorized read-only research, analysis, and adjudication, but C may not write in E1's place.

## Execution Loop

1. C gives the same E1 one batch based on the user's task and accepted project plan or sources of truth.
2. E1 completes only that batch, reads back and tests the work, then direct-pushes a candidate.
3. C reads back the actual result and either adjudicates it or creates a fresh R according to risk.
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

When the user explicitly says `Close CER.` or `/CER-close` to C:

1. C stops new dispatch, adjudicates candidates that can be safely decided, and organizes accepted work, incomplete work, risk, evidence, and next action.
2. C gives the same E1 one self-contained closeout batch.
3. E1 updates only the necessary existing progress or decision sources under target-project rules, marks that E1 has stopped writing, reads back the result, and direct-pushes it. If no durable source exists, E1 reports only the actual deliverable and `writer closed`.
4. C reads back the deliverable and required sources, then reports `🟢 Staged delivery / final acceptance` with the result and continuity limits.

A new session may recover only from target-project sources that actually exist. If evidence is insufficient, label continuity as limited. If E1 coordinates cannot be verified, first prove that the original writer stopped before creating E2.

## Stop CER

When the user explicitly says `Stop CER and continue in a single thread.` or `/CER-stop`:

1. C stops sending new E1/R batches.
2. If there is no active writer, C continues in a normal single thread.
3. If E1 has started writing, C first asks E1 to stop, return the current result or blocker, and state whether the writer is closed.
4. C returns to single-thread work only after reading back a verifiable state. If the writer cannot be proven stopped, report `🔴 Major blocker` and do not assume the workspace is safe.

`/CER-stop` is not `/CER-close`. The first turns off the CER collaboration topology. The second performs CER closeout and required persistence. Plain close/finish messages belong to the target workspace's existing governance and do not map to CER stop or close.
