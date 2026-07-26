---
name: cer-workflow-en
description: "Run the standalone CER multi-agent workflow in English for long-running, multi-batch, or interruption-prone work that needs a Controller, one persistent Executor, risk-based fresh Reviewers, self-contained cross-task delegation, direct return, checkpoints, and staged delivery. Use only for explicit CER-qualified commands or equivalent meaning, such as /CER-start, Start CER, /CER-stop, /CER-close, Close CER, or explicit CER roles and closed-loop execution. Plain start/work or close/finish messages are not CER triggers. This Skill does not prescribe project documents."
---

# CER Workflow

CER Core v1 runs as a standalone workflow.

## Start

When the user explicitly says `/CER-start <overall task, constraints, priorities>`, `Start CER: ...`, or an equivalent CER-qualified start:

1. Read [core-runtime.md](references/core-runtime.md) in full.
2. Read [roadmap.md](references/roadmap.md) in full when showing the initial roadmap or a four-color checkpoint.
3. Read [uat.md](references/uat.md) in full only for installation acceptance or fresh UAT.

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
- Use one persistent, visible, reusable Executor (E1) as the only writer for the task. Do not substitute a one-off temporary subagent.
- Create a fresh, read-only, bounded Reviewer (R) only for high risk or when C cannot reliably disprove a claim.
- Make every cross-task batch self-contained. E1 and R do not automatically inherit C's conversation.
- When creating or identifying tasks or threads, the Controller uses a visible title or equivalent first-line label beginning with `🚀 C:`. E1/R/E2 still use `E1:`, `R1:`, `R2:`, or `E2:` without the rocket. Every return target must include a verifiable session/thread ID or platform-equivalent coordinate.
- Before creating a task or starting validation, use real tools to prove the identity source, required parameters, send path, recipient, session/thread coordinates, and adjudication point. If any link is missing, stop that delegation architecture. Document review, after-the-fact thread reads, and assumptions do not replace communication proof.
- If create, fork, send, or title only partly succeeds and E1 does not direct-push `ready` and `result`, treat the communication chain as unproven. C may report a major blocker but must not send real work or claim a closed loop.
- E1 and R direct-push results. C does not use waiting, polling, or background monitoring to discover them.
- C does not write the workspace. E1's output remains a candidate until C reads it back and adjudicates it.
- Respect the target project's existing sources of truth, plans, and progress. CER does not create a fixed document set or present its role state as the project plan.
- For complex medical, legal, financial, investment, policy, academic, commercial, design, operational, or other knowledge-heavy work, C first defines the required knowledge foundation. E1 works only within that scope, and R independently tests claims against the same scope.
- Stop in the user's main task when a material direction, deliverable shape, or cost is undecided. After execution, deliver observable results at sensible stages.
- Scale roles, batches, Reviewers, checkpoints, and acceptance to risk. Do not substitute more agents, documents, reviews, or ceremony for a clear target and testable acceptance.
- Choose model and effort from capability, cost, and user limits. They are not fixed CER version blockers.

## Version Boundary

This Skill contains CER Core v1 only.

Root `01_CER_Workflow_Human_Overview.en.md` and `02_CER_Workflow_AI_Protocol.en.md` are internal requirements and acceptance blueprints for this source project, maintained separately from this Skill's execution surface. Skill references are the actual operating procedure. The two layers align through requirements and acceptance, but neither owns the other.

When the user needs to turn a fuzzy idea into a blueprint, requirements, R&D, a plan, and progress, `$project-context-workflow` may be used separately. It is not a CER prerequisite. CER reads only its accepted sources of truth and does not create a second document set or duplicate consensus gate.
