# CER Workflow

[繁體中文](README.md)

CER Workflow is for AI work that is long-running, split across batches, easy to interrupt, or important enough to need extra care.

It keeps the work clear: one coordinator confirms the goal, constraints, and acceptance; one steady executor makes the actual file changes; and an independent reviewer is added only when risk calls for a second look. Small tasks can still stay in one ordinary task.

![CER Workflow overview](assets/cer-workflow-infographic.en.png)

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
| `/CER-start <task, constraints, priorities>` | `Start CER: ...` | Start CER mode. |
| `/CER-stop` | `Stop CER and continue in one task.` | Stop using CER and return to ordinary work; this does not mean the task is complete. |
| `/CER-close` | `Close CER.` | Formally close CER; summarize the result, remaining work, and state to keep. |
| `/CER-status` | `Show CER status.` | Show current progress, the next stopping point, and known issues. |
| `/CER-help` | `Show CER commands.` | Show the available commands. |

A plain close/finish message does not close CER and is not treated as `/CER-stop`.

## How CER Works

1. The coordinator first confirms the goal, what is out of scope, what information must be read, and when the work should stop for your decision.
2. Once that is clear, the same executor handles the actual changes. Long work does not keep switching who writes files.
3. If the work is riskier, or if another perspective is needed, the coordinator asks an independent reviewer to check the affected scope.
4. The coordinator comes back to you only for direction decisions, missing input, major issues, or acceptance.
5. CER does not create a fixed set of project documents, and it does not treat its own process notes as your project records.

When CER starts, it first confirms that the working tasks can return messages to each other. If that cannot be confirmed, CER stops and tells you instead of pretending it has started.

## CER Compared With One Thread

One ordinary task is better for a small one-time edit, or when you want to guide the AI step by step.

CER is better for work that is longer, split into batches, easy to interrupt, or needs steadier delivery. The point is not to add roles for their own sake. The point is to keep one executor responsible for file changes and add an independent review only when it helps.

CER spends a little more time at the start confirming the task and return path. That avoids discovering halfway through that the goal, responsibility, or acceptance is unclear.

## Stop Versus Close CER

`/CER-stop` stops using CER. Use it when you want to return to one ordinary task partway through. It only means CER is no longer coordinating the work; it does not mean the task is complete.

`/CER-close` formally closes this CER run. Use it when the task is complete, or when you want the current result, risks, and remaining work summarized clearly. After close, that CER run is kept as history and does not take the next cycle of work.

## Included

- [`skills/cer-workflow/`](skills/cer-workflow/): Traditional Chinese CER Skill
- [`skills/cer-workflow-en/`](skills/cer-workflow-en/): English CER Skill
- [`RELEASE_NOTES.en.md`](RELEASE_NOTES.en.md): English release notes
- [`RELEASE_NOTES.md`](RELEASE_NOTES.md): Traditional Chinese release notes

This repository contains only public, installable CER Skill content.
