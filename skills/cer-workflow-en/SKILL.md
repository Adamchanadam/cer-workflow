---
name: cer-workflow-en
description: "Run standalone CER, or use local /CER-auto to select the minimum sufficient ordinary, Goal, CER-gated, or blocked route. Use only for explicit CER-qualified commands or equivalent meaning; use it for long-running, multi-batch, interruption-prone work needing one writer, fresh Reviewers, self-contained dispatch, persistence, and on-demand parallel candidate analysis. Plain start/work or close/finish messages are not CER triggers. This Skill does not prescribe project documents."
---

# CER Workflow

CER Core v1 is for Codex only. Claude Code requires a separate Skill that has not been provided. Do
not claim that this Skill or repository currently supports Claude Code.

## Entry Routing

1. For local `/CER-auto`, before any CER identity exists, read only "Execution Profile Gate" in
   [core-runtime.md](references/core-runtime.md), plus the user request and target-project truth needed
   for routing; when their paths are known, load them under that owner's single bounded-read
   requirement. If ordinary execution or Goal is selected, stop loading CER references. If
   CER-gated Goal/E1 is selected, read `core-runtime.md` and
   [roadmap.md](references/roadmap.md) in full only at the promotion point and use the current
   CER gate startup. A blocked route reports the missing condition and stops. Remote `/CER-auto` is unsupported in this first version.
2. Before accepting `/CER-start`, read [core-runtime.md](references/core-runtime.md) and
   [roadmap.md](references/roadmap.md) in full.
3. For `/CER-close`, read only "Roles", "Bear-Card Package Version", and "Standalone
   Persistence And Closeout" in `core-runtime.md`, plus "Fixed Lifecycle Cards" in `roadmap.md`.
4. For `/CER-stop`, read only "Roles", "Bear-Card Package Version", and "Stop CER" in
   `core-runtime.md`, plus "Fixed Lifecycle Cards" in `roadmap.md`; read only the relevant roadmap
   section for another checkpoint.
5. Expand reading only when role coordinates or terminal-state evidence are incomplete or contradictory, or target-project rules require it. Do not reread all references merely because the command is stop or close.
6. After CER is active, if target `AGENTS.md` routes Kit full closeout or governance bridge intent,
   read only the matching rule in "Self-Contained Dispatch" and do not redesign the Kit procedure.
7. Read [uat.md](references/uat.md) in full only for installation acceptance or fresh UAT.
8. Before C evaluates or uses parallel candidate producers, read
   [parallel-producers.md](references/parallel-producers.md) in full; it is the sole complete owner.

## Commands

Slash commands are text aliases. If the platform has no command UI, pasting the same text still works.

| Command | Natural language | Effect |
|---|---|---|
| `/CER-auto <task, constraints, priorities>` | `Run CER adaptively: ...` | In a local task, select ordinary execution, Goal, CER-gated Goal/E1, or blocked first; no C exists before the route decision. Remote is unsupported in this first version. |
| `/CER-start <task, constraints, priorities>` | `Start CER: ...` | Start CER; a local task or explicit Remote receiver may become the only C. Plain start/work messages do not start CER. |
| `/CER-stop` | `Stop CER and continue in one thread.` | Stop CER after the runtime brings any active writer to a verifiable state. |
| `/CER-close` | `Close CER.` | Close CER and prove writer closed under the runtime. Plain close/finish messages do not close CER. |
| `/CER-status` | `Show CER status.` | Report only C's known state, coordinates, checkpoint, and blockers; do not poll. |
| `/CER-help` | `Show CER commands.` | Show this table. |

## Entry Boundaries

- The complete unique-C startup gate is owned by `core-runtime.md`: Candidate `C_READY` plus sender readback is still insufficient; the receiver becomes the active Controller (C) only after actually receiving `C_ACCEPTED`.
- Formal E/R tasks must be visible in the same Codex project sidebar and created through the official `create_thread`. Do not downgrade to an inline sub-agent, fork, or delegate. Every `CER-start` cycle creates a brand-new E1; Later batches in the same cycle keep reusing that E1. Every R is a fresh new task. Full topology, writer, Reviewer, batch, direct-push, result-disposition, authority-promotion, persistence, and close rules are defined only in `core-runtime.md`.
- Display labels are only identifiers: `🚀 C:01｜...`, `E1:01｜...`, `R1:01｜...`, `R2:01｜...`, and
  `E2:01｜...`. `00` may identify only an unreconstructable legacy cycle; new cycles use `01` or higher
  and never show a question-mark cycle label. The cycle number is sidebar display only; the full threadId remains authoritative. A close rename failure is only a `title sync warning`. Card text and VERSION
  loading are owned by `roadmap.md` and `core-runtime.md`.
- Truth-source intake is owned only by Controller preflight in `core-runtime.md`. `/CER-auto` route selection, recheck, and safe transition are owned only by its "Execution Profile Gate". The long-task drift checkpoint is owned only by its outcome-anchor and progress gate. This entry does not restate profile, Reviewer, YAGNI, or stop rules.

## Version And Blueprint Boundary

`v1` is the workflow generation, not the package version; package version comes only from `VERSION`
beside `SKILL.md`. Root `01_CER_Workflow_Human_Overview.en.md` and
`02_CER_Workflow_AI_Protocol.en.md` are internal requirements and acceptance blueprints; Skill
references are operating procedures. They align but do not own each other, and runtime rules are not
copied into this entry router.
