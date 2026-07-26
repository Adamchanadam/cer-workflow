# CER Workflow

[中文](README.md)

CER Workflow gives long tasks a steadier way to run.

You give the goal, limits, and priorities to `C:` Controller. C understands the task, sends real work to `E1:` Executor, and opens `R1:` Reviewer only when a risky part needs an independent check. Routine problems stay inside the loop. C comes back to you for real decisions, missing input, blockers, staged delivery, and final acceptance.

![CER Workflow overview](assets/cer-workflow-infographic.png)

## Install With One Prompt

Paste this into your agent:

```text
Please install the cer-workflow skill from https://github.com/Adamchanadam/cer-workflow, then start it with $cer-workflow.
```

Your agent should install `skills/cer-workflow` into its skills folder and tell you when it is ready.

## Start A CER Task

After installation, start with natural language or a slash command:

```text
CER 工作法啟動：<goal, limits, priorities>
```

```text
/CER-start <goal, limits, priorities>
```

Example:

```text
CER 工作法啟動：Check this repo for release readiness, fix the docs and validation issues. Do not push unless I explicitly approve it.
```

## Commands

These slash commands are stable text aliases. If your AI terminal supports slash commands, snippets, or Snap, save them there. If it does not, paste the same text into the chat.

| Command | Natural language | Use |
|---|---|---|
| `/CER-start <task, limits, priorities>` | `CER 工作法啟動：...` | Start CER. |
| `/CER-stop` | `Stop CER and continue in a single thread.` | Turn CER off and stop sending new E1/R work. |
| `/CER-close` | `CER closeout.` / `收工。` | Finish CER and have the same E1 mark `writer closed`. |
| `/CER-status` | `Show CER status.` | Show known state and the next checkpoint without polling. |
| `/CER-help` | `Show CER commands.` | Show the command list. |

## How It Compares With One Thread And Sub-Agents

The common approach is to stay in one thread and guide every step. The assistant does a bit of work, asks you what to do next, and you decide whether to open sub-agents, what to ask them, and whether to trust what comes back. This is fine for short work.

CER moves that coordination into C. C first proves that tasks can send and return messages. Then C sends self-contained work to the same E1. E1 returns results to C. C reads the result, decides what is acceptable, asks R1 for a check when risk is high, and brings only meaningful checkpoints back to you.

Benefits:

- You do not have to split every step yourself.
- C handles ordinary mid-task questions before coming back to you.
- You usually see direction choices, blockers, staged results, and final acceptance.
- Long work is less likely to drift when context is interrupted.
- Professional work starts with a defined knowledge base.

Costs:

- Startup takes longer than a normal single-thread task.
- The platform must prove task/thread identity, send path, and return coordinates.
- Creating a thread, changing a title, or sending one message is not enough. CER needs E1 `ready/result` receipts.
- Small tasks are usually faster without CER.
- C is still an AI controller. You keep the decision rights for direction, permission, cost, publishing, and acceptance.

## Is The Closed Loop Real?

Yes, when the platform can prove the return path.

CER v1 requires C to prove:

- who C, E1, and R1 are;
- where the work is sent;
- how E1 returns `ready` and results;
- where C makes the decision.

If any part is missing, C stops at a red blocker. This keeps the workflow honest. A sent prompt alone does not count as a working loop.

## Can I Turn CER On Or Off Inside A Project?

Yes.

Start CER when the work is long, risky, multi-batch, research-heavy, or publish-facing:

```text
CER 工作法啟動：...
```

or:

```text
/CER-start ...
```

To stop CER and continue in one thread, say:

```text
Stop CER and continue in a single thread.
```

or:

```text
/CER-stop
```

If E1 is already writing, C should first confirm that the writer has stopped or that the work is in a readable handoff state. That avoids two writers changing the same workspace at the same time.

Use `/CER-close` or `CER closeout.` when you want to finish CER properly. The same E1 writes any required existing project state and marks `writer closed`.

## When A Single Thread Is Better

Use a normal thread for:

- one small edit;
- a change where you already know the exact target;
- work with no cross-task, review, or publishing risk;
- sessions where you want to guide every step yourself.

## What Is Included

- `skills/cer-workflow/`: CER Core v1 skill
- `01_CER工作法_人類概覽.md`: human overview
- `02_CER工作法_AI執行協議.md`: Markdown protocol for environments without the skill

## Current Version

This repo ships CER Core v1.

v1 is a standalone workflow. It does not write Agent Handoff Kit files and does not perform Kit closeout. `02_CER工作法_AI執行協議.md` includes a v2 appendix so readers can see the Kit Adapter boundary. The installable skill stays v1 only.
