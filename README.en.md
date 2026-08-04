# CER Workflow

[繁體中文](README.md)

CER = Controller, Executor, Reviewer.

CER separates coordination, file changes, and review into independent Codex tasks, then has the Controller connect them into one closed loop. It is for work that is long-running, split across batches, easy to interrupt, or important enough to need independent checking. Small tasks can still stay in one ordinary conversation.

You mainly stay with the Controller. The Controller comes back to you for direction, permissions, cost, publication, major issues, or final acceptance.

![CER workflow diagram: Controller, Executor, and Reviewer handle coordination, file changes, and review](assets/cer-workflow-infographic.en.png)

## Goal And CER: 10 Practical Differences

Goal and CER can both begin with a short request, and both let you add information, change constraints, and check progress along the way. Goal is usually the simpler choice when the endpoint is clear and you want Codex to carry the work through independently. CER is more suitable when the result needs to converge through intermediate versions, or when you want a Controller to manage implementation, checkpoints, and review.

CER is closer to human-guided co-development: Codex does the work, while you take part in decisions that would materially change the result. The first prompt does not need to be a complete specification. The Controller separates confirmed facts, safe assumptions, and critical gaps, then resolves important gaps before delegating implementation.

| # | Point of comparison | Goal | CER |
|---:|---|---|---|
| 1 | First prompt | The `/goal` text becomes both the first prompt and the completion criteria. If the direction is still unclear, you can use `/plan` first. | The Controller separates confirmed facts, safe assumptions, and critical gaps. It asks before delegating when a gap would materially change the result. |
| 2 | Working rhythm | Codex keeps moving toward the same Goal, which suits long tasks that need less intervention. | The Controller divides the work into reviewable batches and decides the next batch after reading back the current one. |
| 3 | Feedback during the work | In the same chat, `Steer` can change the current run and `Queue` can hold a message for the next run. You can also pause or edit the Goal. | You give feedback to the Controller. It identifies the affected scope, updates the roadmap, and sends a new batch to the same Executor. |
| 4 | Progress display | The desktop app shows a Goal progress row, and you can ask Codex for a progress recap. | Long or multi-stage work uses an inline roadmap showing the current stage, accepted results, blockers, and the next user checkpoint. |
| 5 | Previews and checkpoints | You can ask to inspect, explain, or adjust the work at any time. Preview timing usually comes from the prompt or the immediate need. | The roadmap marks points that need a preview or decision. When direction, deliverable shape, or acceptance changes, it shows what changed. |
| 6 | Your place in the workflow | You set the Goal and can intervene at any time, while Codex chooses the next step. It pauses when it needs a decision or approval. | You mainly stay in the Controller chat, adding requirements or changing direction after seeing intermediate work. The Controller carries those decisions into the implementation track. |
| 7 | Task and agent structure | The main chat can work alone or use native, sidebar-visible subagents. Roles and handoffs depend on the task. | Each cycle has a fixed C for coordination and the same E1 for file changes. A fresh, read-only R is created only when risk warrants it. |
| 8 | File ownership | The main agent or an authorized subagent may make changes. Parallel work must avoid writing to the same source. | Only E1 writes files during a cycle. C and R stay read-only, avoiding concurrent changes from different roles. |
| 9 | Independent review | You can request a review, such as `/review`, or ask a subagent to check the work, but it is not a fixed part of every Goal. | A fresh R is used only for important, high-risk work or when independent evidence is needed. C groups the findings and returns them to the same E1. |
| 10 | Best fit | The endpoint is stable, the completion criteria can be stated clearly, and you want Codex to carry the work through continuously. | The result needs several previews to converge, or you want stronger human control, explicit role boundaries, and independent review. |

The Goal details above follow OpenAI's [Long-running work](https://learn.chatgpt.com/docs/long-running-work), [Prompting](https://learn.chatgpt.com/docs/prompting), and [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) documentation. The CER details follow this repo's [Controller Preflight](skills/cer-workflow-en/references/core-runtime.md#controller-preflight), [Execution Loop](skills/cer-workflow-en/references/core-runtime.md#execution-loop), and [inline roadmap](skills/cer-workflow-en/references/roadmap.md#two-different-surfaces).

## Roles

**Controller (C): coordination and decisions**
Understands the goal, constraints, and completion criteria; assigns work and judges results. The Controller does not modify project files.

**Executor (E1): implementation and file changes**
The only role that modifies files. It implements in batches, tests, and returns candidate results with evidence. The same E1 stays in use throughout one CER cycle, so file changes do not come from several roles at once.

**Reviewer (R1): independent review**
An independent Codex task that checks in read-only mode, gives conclusions, and does not write files. It is used only for important or high-risk work, or when independent verification is needed.

Sidebar labels such as `C:01`, `E1:01`, and `R1:01` mark the roles in the same CER cycle.

## Exploration Helpers: Accelerating Controller Analysis

CER still has only three formal roles: C, E, and R. Medium and large tasks often require several
kinds of preparation at once, such as finding information, comparing options, exploring interface
ideas, and identifying possible problems early. When the Controller handles every direction one
by one, this preparation can slow down the whole workflow.

The Controller may therefore start a small number of Exploration Helpers to examine and organize
different information at the same time. Exploration Helpers support C; they are not a fourth
formal role. They cannot change the project, replace the Executor or Reviewer, or declare the
work complete. The Controller still checks the information, resolves different answers, and makes
the final decision, so the existing writing and independent-review arrangements do not change.

![CER Exploration Helpers decision tree: C decides first, small tasks stay with C, medium-large tasks may use Exploration Helpers, candidates return to C, E1 writes, and R reviews read-only only when risk requires](assets/cer-exploration-helper-architecture.en.png)

Helpers remain idle by default. They suit medium and large tasks where the sources are clear,
the work can be checked in separate parts, and doing those parts together offers a worthwhile
time saving. The Controller decides automatically whether to start them. The complete conditions
are defined only in the
[complete Exploration Helper rules](skills/cer-workflow-en/references/parallel-producers.md#activation-eligibility)
so separate documents do not drift apart.

Simple tasks use no helpers. If the information changes, only the affected part is redone. If a
helper cannot start, times out, or cannot find the required information, the Controller continues
the analysis directly instead of needlessly stopping the whole CER workflow.

In one practical test using a medium-sized task, two information-gathering jobs would have taken
about 71 seconds if completed one after the other. Running them together took about 43 seconds,
reducing the wait by roughly two-fifths. During that time, the Controller also checked the
information and workflow rules. This shows that Exploration Helpers can save real time on suitable
tasks, but it is one test example and does not promise the same improvement for every project.

## Install Or Upgrade With One Prompt

Paste this into Codex:

```text
Use the skills CLI to install or upgrade the English CER Skill for Codex: skills/cer-workflow-en from https://github.com/Adamchanadam/cer-workflow. If an existing install is managed by the CLI, upgrade it. If it is not installed, install it. If files already exist at the target location but the CLI cannot confirm it can manage them, stop and report before overwriting or deleting anything. When finished, read back the install path, source, and VERSION. Stop there; do not start CER. Wait for my separate CER command.
```

## Start CER

After installation, use an explicit CER command:

```text
Start CER: <goal, constraints, priorities>
```

or:

```text
/CER-start <goal, constraints, priorities>
```

A plain start/work message does not start CER. It remains available for your usual way of working.

## Commands

| Command | Natural language | Use |
|---|---|---|
| `/CER-start <task, constraints, priorities>` | `Start CER: ...` | Start CER, with the Controller coordinating the work. |
| `/CER-stop` | `Stop CER and continue in one ordinary conversation.` | Stop using CER and stop assigning new Executor or Reviewer work; this does not mean the task is complete. |
| `/CER-close` | `Close CER.` | Formally end this CER cycle; summarize the result, risks, and remaining work. |
| `/CER-status` | `Show CER status.` | Show current progress, the next stopping point, and known issues. |
| `/CER-help` | `Show CER commands.` | Show the available commands. |

A plain close/finish message does not close CER and is not treated as `/CER-stop`.

## How CER Works

1. You give the full task to the Controller, including the goal, constraints, and priorities.
2. The Controller confirms the completion criteria, sources, and stopping points, then sends implementation work to the Executor.
3. The Executor changes files, tests the work, and returns candidate results with evidence to the Controller.
4. For important or risky work, the Controller asks the Reviewer to perform an independent read-only check.
5. The Controller groups issues, decides what should be fixed, and returns the result, risks, and decisions that need you.

Issues with the same cause are grouped into one batch and sent back to the same Executor. The scope widens only for a different problem, a new effect, or a new risk.

When CER starts, it first confirms that the working tasks can return messages to each other. If that cannot be confirmed, CER stops and tells you instead of pretending it has started.

## Stop Versus Close CER

`/CER-stop` stops using CER and returns to one ordinary conversation. It means the Controller will not assign new Executor or Reviewer work; it does not mean the task is complete.

`/CER-close` formally ends this CER cycle. The Controller summarizes the result, risks, and remaining work, and confirms that the Executor has stopped writing. After close, the old C/E/R tasks are history only; the next cycle uses new role tasks.

## Included

- [`skills/cer-workflow/`](skills/cer-workflow/): Traditional Chinese CER Skill
- [`skills/cer-workflow-en/`](skills/cer-workflow-en/): English CER Skill
- [`RELEASE_NOTES.en.md`](RELEASE_NOTES.en.md): English release notes
- [`RELEASE_NOTES.md`](RELEASE_NOTES.md): Traditional Chinese release notes

This repository contains only public, installable CER Skill content.
