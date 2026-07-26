# About

CER Workflow helps an agent handle long work without losing the thread.

It gives the user one Controller, one persistent Executor, and fresh Reviewers only when the risk justifies it. The workflow is strict about return paths. If the agent cannot prove that a task can receive instructions and send results back, it stops before real work starts.

The main user benefit is a quieter handoff. The user gives the goal to C, then C handles task splitting, execution follow-up, checks, and ordinary mid-task problems. The user comes back in at real checkpoints.

Repository description:

```text
Standalone CER workflow skill for long-running AI work with Controller, persistent Executor, and risk-based Reviewers.
```
