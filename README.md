# CER Workflow

CER Workflow is a small Codex skill for work that takes more than one pass.

Use it when a task needs planning, execution, checking, and a clear point for you to step in. It is useful for long fixes, multi-file changes, research-backed decisions, publishing work, and jobs that may be interrupted.

## Install With One Prompt

Paste this into your agent:

```text
請從 https://github.com/Adamchanadam/cer-workflow 安裝 cer-workflow skill，安裝後用 $cer-workflow 啟動。
```

The agent should install `skills/cer-workflow` into its Codex skills folder and tell you when it is ready.

## Start A CER Task

After installation, start with:

```text
CER 工作法啟動：<你想完成的事、限制、優先順序>
```

Example:

```text
CER 工作法啟動：檢查這個 repo 的發佈準備，修好文件和驗證問題。不要推送，除非我明確批准。
```

## How It Works

CER uses three roles.

- `C:` Controller keeps the whole task in view, speaks with you, and decides what is accepted.
- `E1:` Executor does the actual work in the project. The same E1 stays with the task.
- `R1:` Reviewer is opened only when risk is high or an independent check is needed.

Every handoff must include enough context for the next task to work without guessing. If the platform cannot prove where a message goes, who receives it, and how the result returns, CER stops and tells you the blocker.

## Checkpoints

CER uses a small four-color checkpoint card only when it helps you make a decision or understand progress.

- Blue: plan preview
- Yellow: direction choice
- Red: blocker
- Green: staged delivery or final acceptance

Small internal steps do not need a card.

## What Is Included

- `skills/cer-workflow/` - installable Codex skill for CER Core v1
- `01_CER工作法_人類概覽.md` - human overview
- `02_CER工作法_AI執行協議.md` - portable Markdown protocol for environments without the skill

## Current Boundary

This public package ships CER Core v1.

v1 runs as a standalone workflow. It does not write Agent Handoff Kit files and it does not perform Kit closeout. The Markdown protocol includes a v2 appendix so readers can see the future Kit adapter boundary, but the installed skill stays v1 only.

## When To Use It

Good fit:

- Long or multi-batch work
- Work with a real risk of interruption
- Tasks where one agent should write and another should review
- Professional tasks that need a clear knowledge base before execution
- Publishing, migration, release, or governance work where a false pass would hurt

Lightweight tasks can be handled directly.

