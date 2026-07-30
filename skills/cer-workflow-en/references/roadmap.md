# User Checkpoints And Roadmap

## Two Different Surfaces

- The **inline visualizer roadmap** is the standard progress surface for long-running,
  multi-stage, multi-batch, or first-public-alignment CER work without requiring user action. Layout, stage count, and
  extra fields adapt to the project. Do not use a fixed four-box or fixed-table template as a
  substitute for real task information. Minimum content is defined under "Display Priority".
- The **four-color bear card** is a checkpoint signal. It answers whether the user must preview,
  decide, handle a blocker, or accept a result. It is not the roadmap or a continuous tracker.

Both may appear in one message, but they do not repeat content: the roadmap shows global
position, while the card names the current checkpoint.

## Standard Inline Visualizer Timing

1. When C classifies work as multi-stage, multi-batch, or a new product, flow, design, content,
   or experience deliverable that needs first public alignment, show the initial roadmap before
   the first real batch.
2. Update it after C reads back and accepts a result that changes the stage, batch, or next
   checkpoint.
3. When a user decision, an actual new constraint, or R evidence materially changes direction,
   scope, deliverable shape, risk, or acceptance state, show the difference from the prior version
   before updating it.
4. Show the matching terminal state at staged delivery, technical acceptance, fit check, or closeout.

Do not update it for ordinary internal reads, E1 substeps, polling, unadjudicated candidates, or
details that do not change user-view progress. Progress comes only from a bounded read after
direct-push and C adjudication.

## Fixed Lifecycle Cards

Before showing any lifecycle or checkpoint bear card, read `VERSION` again from this Skill root.
Stable semver `X.Y.Z` renders as `vX.Y.Z`; a missing, unreadable, or malformed value renders as
`version unverified`. The cards below reflect the current `VERSION` value `0.2.6`; they do not
hard-code the workflow generation.

```text
   ()_()
 ( ◕ᴥ◕ )
   ╰ ^ ╯ · CER Workflow v0.2.6 · 🔵 CER started
```

Every successfully accepted `CER-start`, including simple single-batch work, uses this fixed
open-eye start card. Keep the complete three-line bear; render version and status after the foot
on the third line, separated by fixed `·` markers rather than a separate line.

A successful `/CER-stop` uses this fixed closed-eye stop card:

```text
   ()_()
 ( ᴗᴥᴗ )
   ╰ ^ ╯ · CER Workflow v0.2.6 · ⚪ CER stopped · CER inactive
```

A successful `/CER-close` uses this fixed closed-eye close card:

```text
   ()_()
 ( ᴗᴥᴗ )
   ╰ ^ ╯ · CER Workflow v0.2.6 · 🟢 CER closed · writer closed
```

A closed-eye card is proof of a verified terminal state, not an intent receipt. Show the stop
card only after proving no active writer or a stopped writer and completing required readback.
Show the close card only after proving `writer closed`, completing required readback, and reading
back either a `✓` appended to this cycle's cycle number in every verifiable C/E/R title or a
`title sync warning`. The closed-eye close card proves writer close and required readback, not
all-green title sync. When any evidence is missing, use the open-eye red blocker card:

```text
   ()_()
 ( ◕ᴥ◕ )
   ╰ ^ ╯ · CER Workflow v0.2.6 · 🔴 Major blocker · checkpoint blocked
```

## Other Fixed Checkpoint Cards

Non-lifecycle checkpoints keep the open-eye bear and add version and status after its foot on the
third line with fixed `·` markers. If the version is invalid, they also show `version unverified`. Replace the status for the
situation:

- `🟡 Direction decision`
- `🔴 Major blocker`
- `🟢 Staged delivery / final acceptance`

## Bear Card Timing

CER is a continuous loop, but it does not show a card for every small step:

1. Every successfully accepted `CER-start` first uses one fixed `🔵 CER started` card as the
   startup receipt, including single-batch work. Long-running, multi-batch, or first-public-
   alignment work adds the full inline roadmap in the same message.
2. Use `🟡 Direction decision` when the user must choose a material direction, scope,
   deliverable shape, cost, knowledge source, or acceptance standard.
3. Use `🔴 Major blocker` when a communication path, session/thread coordinate, permission,
   source of truth, knowledge foundation, platform capability, or safety condition is
   insufficient for reliable continuation.
4. Use `🟢 Staged delivery` when an observable stage is ready for user acceptance after C
   adjudication or risk-based R review.
5. A successful `/CER-stop` shows the fixed closed-eye `⚪ CER stopped` card. A successful
   `/CER-close` shows the fixed closed-eye `🟢 CER closed` card. Ordinary final acceptance may
   still use the open-eye `🟢 Final acceptance` checkpoint and must not impersonate a lifecycle
   terminal state.

Do not show a card for ordinary internal reads, low-risk small edits, E1 substeps, ordinary batch
acceptance, R completion that creates no user checkpoint, or a clear next action. Update only the
inline roadmap when progress changed.

## Display Priority

The inline roadmap shows at minimum: a testable destination; ordered stages with
complete/current/pending state; overall progress; the current action and verified evidence or
blocker; C/E1/R state; the next checkpoint; and knowledge-foundation state only for
knowledge-heavy work. First public alignment also shows scope/exclusions, key assumptions, the
smallest observable result, whether technical acceptance and fit check apply, and whether a user
decision is needed. A bear card reduces the current situation to a preview, decision,
blocker, or acceptance checkpoint. Both derive from existing project plan/progress or verified
execution state and do not create a second progress source.

1. When Codex exposes a callable in-conversation visualization capability, create an inline HTML visualization by default and use the capability's official rendering instruction, such as `::codex-inline-vis{file="..."}`.
2. Mermaid does not satisfy the first layer. Use Mermaid only when inline visualization is unavailable, not callable, cannot write to its required visual directory, or fails to render.
3. Use fixed Markdown or plain text only when Mermaid is also unavailable.
4. State the fallback reason in one sentence. Do not silently downgrade, and do not block the project because visualization is unavailable.

Plain-text fallback:

```text
Goal: <destination>
Scope/exclusions: <in scope / not doing now>
Key assumptions: <confirmed / safe inference / decision needed>
[Public alignment: <confirmed / safe inference / decision needed>]
[✓] Complete -> [● Now] Current stage -> [○] Later stage -> [○] Final delivery / closeout
Current: <one sentence>
Smallest observable outcome: <next thing the user will see>
Acceptance: technical acceptance=<condition / not applicable>; fit check=<condition / not applicable>
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
deliverable-shape choices, open-eye red for reliability blockers, and open-eye green for
observable staged results and ordinary final acceptance. Only a proven stop/close terminal state
uses a closed-eye card. Ordinary batch progress updates only the inline roadmap.
