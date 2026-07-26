# CER Workflow

[繁體中文](README.md)

CER Workflow gives long-running, multi-batch, or high-risk AI work clear responsibilities, one writer, and a verifiable return loop.

You give the goal, constraints, and priorities to the `🚀 C:` Controller. C clarifies the task and acceptance before sending real work to the same persistent `E1:` Executor. A fresh `R1:` Reviewer is created only when risk needs independent challenge. C returns to you for real direction decisions, missing input, blockers, and acceptance.

![CER Workflow overview](assets/cer-workflow-infographic.en.png)

## Install With One Prompt

Paste this into your agent:

```text
Install the English CER Skill (skills/cer-workflow-en) from https://github.com/Adamchanadam/cer-workflow. Use skills/cer-workflow for Traditional Chinese. Do not start CER automatically after installation; wait for my explicit CER command.
```

The Traditional Chinese and English Skills are complete, independently installable packages. Detailed operating procedure lives only in each package's `references/`.

## Start CER

After installation, use an explicit CER-qualified command:

```text
Start CER: <goal, constraints, priorities>
```

or:

```text
/CER-start <goal, constraints, priorities>
```

A plain start/work message does not start CER. It remains available to the workspace's existing workflow.

## Commands

| Command | Natural language | Use |
|---|---|---|
| `/CER-start <task, constraints, priorities>` | `Start CER: ...` | Start CER. |
| `/CER-stop` | `Stop CER and continue in a single thread.` | Leave CER mode; send no new E1/R work, but do not claim the task is complete. |
| `/CER-close` | `Close CER.` | Formally close CER; confirm the result, remaining work, and the same E1's `writer closed` state. |
| `/CER-status` | `Show CER status.` | Show known state, role coordinates, next checkpoint, and blockers without polling. |
| `/CER-help` | `Show CER commands.` | Show the available commands. |

A plain close/finish message does not close CER and is not treated as `/CER-stop`.

## How CER Works

1. Before real dispatch, C concisely checks the endpoint, sources, boundary, permissions/stops, and acceptance. An unsupported assumption cannot be presented as confirmed.
2. A local task or an explicitly designated Remote task may become the only C. A Remote receiver first returns candidate `C_READY`; only after the sender verifies that no other active C exists, reads the receipt, and returns `C_ACCEPTED` does the receiver become C.
3. C proves task/thread identity, send path, return coordinates, and adjudication point, then receives E1's zero-write `ready`.
4. The same persistent E1 is the only writer. Every batch is self-contained and does not depend on "see above."
5. E1 direct-pushes a candidate to C. C reads back, tests, and adjudicates instead of polling for results.
6. When R finds several issues, C groups findings that share the same cause and user impact, then repairs the whole affected boundary once. A separate scope is opened only for a different cause, different user impact, or a regression caused by the latest repair.

Long-running or multi-batch work uses an inline roadmap to show the endpoint, current position, next checkpoint, and role state. Direction decisions, major blockers, staged results, and final acceptance interrupt the user; ordinary substeps do not display process ceremony.

## CER Compared With One Thread

A normal single thread is faster for one small edit or work you want to guide step by step. CER is for long-running, multi-batch, interruption-prone work that needs one writer or independent challenge proportional to risk.

The trade-off is that CER must prove its communication loop before work starts. Creating a task, changing a title, or sending one message is not enough. Without `ready/result` receipts, CER stops honestly at a blocker.

## Stop Versus Close CER

`/CER-stop` leaves CER mode. Use it when you want to continue in a normal single thread. C sends no new work, and if E1 is writing, C first brings the writer to a verifiable state. It does not claim that the task is finished and does not create a formal CER closeout.

`/CER-close` formally ends this CER run. Use it when the task is complete or you want a final handoff. C converges the result, risks, and remaining work; the same E1 updates only required sources that already exist in the workspace and marks `writer closed`. CER does not create a fixed project document set or a parallel progress source.

## Included

- [`skills/cer-workflow/`](skills/cer-workflow/): Traditional Chinese CER Core v1 Skill
- [`skills/cer-workflow-en/`](skills/cer-workflow-en/): complete English mirror Skill
- [`RELEASE_NOTES.en.md`](RELEASE_NOTES.en.md): English release notes
- [`RELEASE_NOTES.md`](RELEASE_NOTES.md): Traditional Chinese release notes

This repository contains only public, installable CER Core v1 content.
