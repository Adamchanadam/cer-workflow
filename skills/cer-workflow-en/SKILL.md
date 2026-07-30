---
name: cer-workflow-en
description: "Run the standalone CER multi-agent workflow in English for long-running, multi-batch, or interruption-prone work that needs a Controller, one persistent Executor, risk-based fresh Reviewers, self-contained cross-task delegation, direct return, checkpoints, staged delivery, and on-demand parallel candidate analysis. Use only for explicit CER-qualified commands or equivalent meaning, such as /CER-start, Start CER, /CER-stop, /CER-close, Close CER, or explicit CER roles and closed-loop execution. Plain start/work or close/finish messages are not CER triggers. This Skill does not prescribe project documents."
---

# CER Workflow

CER Core v1 is a standalone workflow for Codex only. Claude Code requires a separate Skill
that has not been provided. Do not claim that this Skill or repository currently supports
Claude Code.

## Start

When the user explicitly says `/CER-start <overall task, constraints, priorities>`, `Start CER: ...`, or an equivalent CER-qualified start:

1. Before accepting `/CER-start`, read [core-runtime.md](references/core-runtime.md) and
   [roadmap.md](references/roadmap.md) in full.
2. For `/CER-close`, read only "Roles", "Bear-Card Package Version", and "Standalone
   Persistence And Closeout" in `core-runtime.md`, plus "Fixed Lifecycle Cards" in
   `roadmap.md`.
3. For `/CER-stop`, read only "Roles", "Bear-Card Package Version", and "Stop CER" in
   `core-runtime.md`, plus "Fixed Lifecycle Cards" in `roadmap.md`. For another bear-card
   checkpoint, read only the relevant `roadmap.md` section.
4. Expand reading only when role coordinates or terminal-state evidence are incomplete or
   contradictory, or when target-project rules require it. Do not reread all references merely
   because the command is stop or close.
5. After CER is active, when the target `AGENTS.md` clearly routes Kit full-closeout or
   governance-bridge intent, read only the matching rule in "Self-Contained Dispatch" and do not
   redesign the Kit procedure.
6. Read [uat.md](references/uat.md) in full only for installation acceptance or fresh UAT.
7. Before C evaluates or uses parallel candidate producers, read
   [parallel-producers.md](references/parallel-producers.md) in full. It is the sole complete
   rule owner for this capability.

## Commands

Slash commands are stable text aliases. Register them in a slash-command, snippet, Snap, or searchable command interface when the platform supports one. Otherwise, the user can paste the same text.

| Command | Natural language | Effect |
|---|---|---|
| `/CER-start <task, constraints, priorities>` | `Start CER: ...` | Start CER v1; a local task or explicit remote receiver task may become the only C. Plain start/work messages do not start CER. |
| `/CER-stop` | `Stop CER and continue in a single thread.` | Stop CER and send no new E1/R work. If E1 is writing, first bring the writer to a verifiable state. |
| `/CER-close` | `Close CER.` | Close CER. The same E1 updates only required existing sources of truth and marks `writer closed`. Plain close/finish messages do not close CER. |
| `/CER-status` | `Show CER status.` | Report only C's known state, role coordinates, next checkpoint, and blockers. Do not poll. |
| `/CER-help` | `Show CER commands.` | Show this command table. |

## Invariants

- A local task or explicit remote receiver task must pass the complete unique-C startup gate in [core-runtime.md](references/core-runtime.md). Candidate `C_READY` plus sender readback is still insufficient; the receiver becomes the active Controller (C) only after actually receiving `C_ACCEPTED`.
- Every successfully accepted `CER-start` first shows the fixed open-eye start card from
  [roadmap.md](references/roadmap.md), including simple single-batch work. Before showing any
  bear card, read `VERSION` from this Skill root. A blocked start shows the open-eye red blocker
  card and never a closed-eye success card.
- Formal E/R roles must be independent new tasks/threads in the same Codex project sidebar,
  created through the official `create_thread` tool. Do not downgrade to an inline sub-agent,
  fork, or delegate.
- Every `CER-start` cycle creates a brand-new E1. Later batches in the same cycle keep reusing
  that same E1 as the only writer. E2 is created as another new task only after takeover
  conditions are met.
- Create Reviewer (R) only for high risk or when C cannot reliably disprove a claim. Every R
  must be a fresh new task, read-only and bounded; do not reuse an old R.
- C may use inline parallel candidate producers on demand under
  [parallel-producers.md](references/parallel-producers.md). They are not formal roles and must
  not become shared-workspace writers, replace E/R, communicate directly with E1/R, or produce
  formal ready/result. When parallel work is not suitable, producer count is zero and C analyzes
  serially.
- Make every cross-task batch self-contained. E1 and R do not automatically inherit C's conversation.
- When creating or identifying tasks or threads, the Controller uses a visible title or equivalent first-line label in the form `🚀 C:01｜...`. E1/R/E2 still use `E1:01｜...`, `R1:01｜...`, `R2:01｜...`, or `E2:01｜...` without the rocket. Tasks in the same cycle share the same short cycle number; a later cycle uses a new number. `00` may identify only a legacy/migration cycle that started before cycle numbering and cannot be reliably reconstructed; new cycles use `01` or higher and never show a question-mark cycle label. The cycle number is sidebar display only, not uniqueness evidence; the full threadId remains authoritative. Every return target must include a verifiable session/thread ID or platform-equivalent coordinate.
- Before creating a task or starting validation, use real tools to prove the identity source, required parameters, send path, recipient, session/thread coordinates, and adjudication point. If any link is missing, stop that delegation architecture. Document review, after-the-fact thread reads, and assumptions do not replace communication proof.
- When create/send reports failure, timeout, or a partial result, mark it `outcome_unknown` instead of treating it as definite failure and retrying immediately. C performs one bounded authoritative reconciliation. Duplicate roles receive no formal work until one task is selected and every other task is proven stopped with zero writes. If any duplicate writer may have worked or written, block and recover a one-writer state first.
- Every formal batch uses a stable `batchId`, monotonic `batchSeq`, and immutable `payloadDigest`; every control, receipt, and result message uses a stable `messageId`. The recipient deduplicates and recovers by registered, running, result-ready, result-accepted, or unknown state. The same identity with different content always blocks, and no revision starts before the old batch is canceled, terminated, or recovered.
- Adaptive batch acceleration is the default scheduling strategy, not a Turbo mode or another slash command. It operates only while communication, batch lifecycle, single-writer state, evidence validity, and the task contract are known; uncertainty disables it automatically without weakening safety, independent review, or acceptance.
- E1 and R direct-push results. If the platform does not automatically wake an idle C, C may arm one bounded event wait on the known unique thread and current cursor for each declared expected direct-push state transition; `BATCH_RECEIVED` and the final result are separate transitions. A wait snapshot, completion status, or commentary is not ready/result evidence. After timeout, the same transition gets one recovery wait only after reconciliation and the single controlled resend with the same `messageId`; it then blocks rather than polling or monitoring.
- C does not write the workspace. E1's output remains a candidate until C reads it back and adjudicates it.
- Respect the target project's existing sources of truth, plans, and progress. CER does not create a fixed document set or present its role state as the project plan.
- For complex medical, legal, financial, investment, policy, academic, commercial, design, operational, or other knowledge-heavy work, C first defines the required knowledge foundation. E1 works only within that scope, and R independently tests claims against the same scope.
- Stop in the user's main task when a material direction, deliverable shape, or cost is undecided. After execution, deliver observable results at sensible stages.
- Scale roles, batches, Reviewers, checkpoints, and acceptance to risk. Do not substitute more agents, documents, reviews, or ceremony for a clear target and testable acceptance.
- Choose model and effort from capability, cost, and user limits. They are not fixed CER version blockers.
- After one `/CER-close` completes in a workspace, that cycle's C/E/R tasks remain history
  only and the whole set must not receive work for a later cycle. A later cycle must use a
  new task that passes the unique-C gate, create a brand-new E1, and use only fresh
  Reviewers. It must not reuse any E/R coordinate from the closed cycle.
- On successful `/CER-close`, first prove `writer closed` and required readback, then use the
  official title tool to append `✓` to the cycle number in every verifiable C/E/R title and read
  it back. Rename failure only reports `title sync warning`; it must not be claimed as renamed.
  Only after that does C show the closed-eye close card.

## Version Boundary

This Skill contains Codex-only CER Core v1; `v1` is the workflow generation, not the currently
installed package version. Bear-card package versions come only from this Skill's `VERSION`.
Every release or upgrade must update `VERSION` first. After the `skills` CLI updates the whole
Skill, cards naturally read the new version.

Root `01_CER_Workflow_Human_Overview.en.md` and `02_CER_Workflow_AI_Protocol.en.md` are internal requirements and acceptance blueprints for this source project, maintained separately from this Skill's execution surface. Skill references are the actual operating procedure. The two layers align through requirements and acceptance, but neither owns the other.

When the user needs to turn a fuzzy idea into a blueprint, requirements, R&D, a plan, and progress, `$project-context-workflow` may be used separately. It is not a CER prerequisite. CER reads only its accepted sources of truth and does not create a second document set or duplicate consensus gate.
