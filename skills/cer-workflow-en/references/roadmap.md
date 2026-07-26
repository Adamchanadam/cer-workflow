# User Checkpoints And Roadmap

## Two Different Surfaces

- The **inline visualizer roadmap** is the standard progress surface for long-running,
  multi-stage, or multi-batch CER work without requiring user action. Layout, stage count, and
  extra fields adapt to the project. Do not use a fixed four-box or fixed-table template as a
  substitute for real task information. Minimum content is defined under "Display Priority".
- The **four-color bear card** is a checkpoint signal. It answers whether the user must preview,
  decide, handle a blocker, or accept a result. It is not the roadmap or a continuous tracker.

Both may appear in one message, but they do not repeat content: the roadmap shows global
position, while the card names the current checkpoint.

## Standard Inline Visualizer Timing

1. When C classifies work as multi-stage or multi-batch, show the initial roadmap before the
   first real batch.
2. Update it after C reads back and accepts a result that changes the stage, batch, or next
   checkpoint.
3. Update it when a user decision changes direction/scope/deliverable shape, or when R evidence
   changes risk or acceptance state.
4. Show the matching terminal state at staged delivery, final acceptance, or closeout.

Do not update it for ordinary internal reads, E1 substeps, polling, unadjudicated candidates, or
details that do not change user-view progress. Progress comes only from a bounded read after
direct-push and C adjudication.

## Fixed Checkpoint Card

```text
   ()_()     CER Workflow
 ( ◕ᴥ◕ )    🔵 Plan preview
   > ^ <     checkpoint ready
```

Replace the second line for the situation:

- `🔵 Plan preview`
- `🟡 Direction decision`
- `🔴 Major blocker`
- `🟢 Staged delivery / final acceptance`

## Bear Card Timing

CER is a continuous loop, but it does not show a card for every small step:

1. At the start of long-running/multi-batch CER work or restart of a resumable stage, use one
   `🔵 Plan preview` as a startup receipt. The inline roadmap in the same message carries the
   full stage information.
2. Use `🟡 Direction decision` when the user must choose a material direction, scope,
   deliverable shape, cost, knowledge source, or acceptance standard.
3. Use `🔴 Major blocker` when a communication path, session/thread coordinate, permission,
   source of truth, knowledge foundation, platform capability, or safety condition is
   insufficient for reliable continuation.
4. Use `🟢 Staged delivery` when an observable stage is ready for user acceptance after C
   adjudication or risk-based R review.
5. At user closeout or final acceptance, use `🟢 Final acceptance` to show the result,
   `writer closed`, durable-source updates, and limits on continuation in a new session.

Do not show a card for ordinary internal reads, low-risk small edits, E1 substeps, ordinary batch
acceptance, R completion that creates no user checkpoint, or a clear next action. Update only the
inline roadmap when progress changed.

## Display Priority

The inline roadmap shows at minimum: a testable destination; ordered stages with
complete/current/pending state; overall progress; the current action and verified evidence or
blocker; C/E1/R state; the next checkpoint; and knowledge-foundation state only for
knowledge-heavy work. A bear card reduces the current situation to a preview, decision,
blocker, or acceptance checkpoint. Both derive from existing project plan/progress or verified
execution state and do not create a second progress source.

1. When Codex exposes a callable in-conversation visualization capability, create an inline HTML visualization by default and use the capability's official rendering instruction, such as `::codex-inline-vis{file="..."}`.
2. Mermaid does not satisfy the first layer. Use Mermaid only when inline visualization is unavailable, not callable, cannot write to its required visual directory, or fails to render.
3. Use fixed Markdown or plain text only when Mermaid is also unavailable.
4. State the fallback reason in one sentence. Do not silently downgrade, and do not block the project because visualization is unavailable.

Plain-text fallback:

```text
Goal: <destination>
[✓] Complete -> [● Now] Current stage -> [○] Later stage -> [○] Final delivery / closeout
Current: <one sentence>
Next checkpoint: <one sentence>
Knowledge foundation: <confirmed / source missing / not applicable>
Roles: C=<state> | E1=<state> | R=<not created / reviewing / complete>
```

## Roadmap Source

Use the highest available authority and do not create a second progress record:

1. If the target project has an authoritative progress source or roadmap, derive from it.
2. If it has only an accepted plan, derive temporary state from that plan plus verified execution evidence.
3. If it has no plan, derive temporary state from the current user request and verified role/blocker facts, and label it `initial / pending convergence`.

When `$project-context-workflow` is also in use, read only its accepted plan and progress. Do not repeat its five-step process or create a duplicate consensus gate.

Do not show cards for ordinary implementation detail. Use yellow for material direction or
deliverable-shape choices, red for reliability blockers, and green for observable staged results
and final acceptance. Ordinary batch progress updates only the inline roadmap.
