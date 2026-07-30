# Parallel Candidate Producers

<!-- cer-parallel-producers-owner -->

This file is the sole complete rule owner for CER parallel candidate producers. It defines how C
may use an inline, informal capability on demand while preserving formal roles, the single writer,
fresh Reviewers, source-based adjudication, and stop boundaries.

## Contents

- [Position And Role Boundary](#position-and-role-boundary)
- [Keep User Operation Simple](#keep-user-operation-simple)
- [Activation Eligibility](#activation-eligibility)
- [Frozen Lane Contract](#frozen-lane-contract)
- [Modes And Write Boundary](#modes-and-write-boundary)
- [Mechanical Scratch-Root Boundary](#mechanical-scratch-root-boundary)
- [Candidate Return](#candidate-return)
- [C Readback, Adjudication, And Convergence](#c-readback-adjudication-and-convergence)
- [Failure, Drift, And Lifecycle](#failure-drift-and-lifecycle)
- [Prohibitions](#prohibitions)

## Position And Role Boundary

- CER has only the formal roles C, E1, R, and E2. A parallel candidate producer is not a fifth
  role and receives no formal title, cycle, ready, result, batch lifecycle, or Reviewer identity.
- A producer is C's inline, informal, on-demand candidate capability. It adds no slash command,
  lock, registry, run id, resident mode, or background service.
- A producer does not replace E1 for writes to the formal project, replace R for independent
  challenge, or communicate directly with E1, E2, or R.
- The formal project still has only one writer, E1. E2 may take over only after the existing
  takeover conditions hold. No producer, C, or R becomes a parallel project writer.

## Keep User Operation Simple

Normal CER use keeps the existing explicit trigger and five commands. The user does not configure
producers, lanes, scratch roots, hashes, roles, or extra review procedures and does not need to
learn the term "parallel candidate producer." C decides internally whether parallel work is
worthwhile, assigns lanes, and verifies isolation. When value or safety cannot be proven, C uses
zero producers and returns to serial analysis. Report only results, unknowns, blockers, or risks
that materially affect the user, without exposing internal lane ceremony.

## Activation Eligibility

C may start two or more parallel lanes only when every condition below holds:

1. At least two work lanes are independent and need no result from each other, shared mutable
   state, or fixed execution order.
2. Each lane's input and source identity is frozen.
3. C has non-duplicative critical analysis, gating, or adjudication work to do concurrently and
   does not degrade into a candidate organizer.
4. C can independently verify each candidate against authoritative sources.
5. Expected net time savings materially exceed startup, readback, hashing, deduplication, and
   adjudication costs.
6. Required parallel execution slots are available without reducing capacity needed by formal E1
   or a fresh R.

If any condition fails, is uncertain, or one bounded read is sufficient, `producer_count=0` and C
completes the analysis serially. This is normal auto-idle, not degradation, an error, or a mode the
user must configure.

## Frozen Lane Contract

Before a lane starts, C freezes all of the following:

- `lane_label`, used only to identify this candidate and not as a formal role or run id.
- `mode`, which must be either `read_only` or `isolated_artifact`.
- One objective.
- Input identity and version, source identity, and verifiable source coordinates.
- Allowed and forbidden scope.
- Expected candidate output.
- Acceptance method.
- Stop condition.
- For `isolated_artifact`, a lane-specific `scratch_root` explicitly supplied by C and already
  accepted by the mechanical boundary check.

A lane does not start, or becomes invalid immediately, when its contract is unfrozen,
contradictory, or rewritten by the producer. A producer cannot expand its objective, sources,
permissions, output, or acceptance.

## Modes And Write Boundary

### `read_only`

- The lane must perform zero writes everywhere, including the project, scratch space, temporary
  storage, external systems, and the producer's visible workspace.
- It may read only inputs and sources assigned by C and return a text candidate.

### `isolated_artifact`

- The lane may write only to its task-owned, lane-specific `scratch_root` explicitly supplied by C.
- It must not write the target project, formal sources of truth, another lane, a user root, system
  location, external service, or any unlisted target.
- An artifact is a candidate, not a formal project result. Only C may read it back, recompute its
  hash, and converge it. A producer cannot send it directly to E1 or R for use.

## Mechanical Scratch-Root Boundary

Before an artifact lane starts, C resolves the actual absolute path and proves every condition:

1. `scratch_root` and the target project do not contain each other; neither is an ancestor of the
   other.
2. `scratch_root` is not a drive root, user root, system root, or equivalent high-risk root.
3. The existing path chain contains no symlink, junction, Windows reparse point, mount, or other
   link that redirects writes to an unverified location.
4. Lane roots are distinct, are not ancestors of one another, and do not overlap formal sources
   of truth, another lane, or an external system.
5. Actual tool permissions allow only that lane's explicit root. Relative paths, wildcards,
   environment fallback, or a producer-selected location cannot expand the boundary.

If any condition cannot be proven, the lane does not start. Do not fall back to staging inside the
project, shared scratch space, a user root, or another more dangerous location.

## Candidate Return

Every naturally arriving candidate includes at least:

- `lane_label`.
- Frozen input identity.
- Actual source coordinates.
- `claims`, with each candidate claim verifiable from its source.
- `unknowns`, covering missing, conflicting, unverified, or restricted material.

An `isolated_artifact` candidate also lists the actual absolute path and SHA-256 for each artifact.
A return is not a formal CER ready/result, uses no formal batch identity, and is not acceptance,
progress, or Reviewer evidence.

## C Readback, Adjudication, And Convergence

- C personally reads back sources and artifacts supporting critical claims; a producer summary is
  not a substitute.
- C recomputes SHA-256 for every artifact and verifies that its path remains under the accepted
  scratch root, input identity has not drifted, and source coordinates are replayable.
- When sources or candidates conflict, C adjudicates from user decisions, project sources of
  truth, and authoritative sources required by the task. C must not accept by vote, quantity,
  completion order, or matching answers.
- C converges only material still inside the intake boundary with unchanged sources and hashes
  that can be independently verified.
- Only after C completes readback, deduplication, conflict adjudication, and convergence may it
  form a formal self-contained batch for E1. E1 receives only that C-converged batch and must not
  use raw producer communication, lane summaries, or unconverged scratch artifacts directly.
- R still challenges the frozen original evidence independently. A producer candidate cannot
  impersonate fresh R evidence.

## Failure, Drift, And Lifecycle

- C does not wait, poll, or background-monitor producers. It uses only candidates that arrive
  naturally while the intake boundary remains open.
- A late candidate is invalid after intake closes, the formal batch is frozen, or `/CER-stop` or
  `/CER-close` begins. It cannot reopen an adjudicated batch.
- Input or source drift discards only lanes that depend on that identity. Unaffected lanes do not
  rerun.
- An out-of-bounds artifact path, hash drift, tamper, unreplayable source, or lane-contract drift
  fails closed and cannot be converged.
- If producer creation fails, subagent capability is unavailable, a producer times out, no result
  arrives naturally, or a candidate cannot be verified, C returns to ordinary serial analysis and
  does not repeat the same failure. CER blocks only when the missing evidence is itself a task
  blocker.
- `/CER-stop` and `/CER-close` do not wait for producers. C stops accepting new candidates, lets
  late material expire, and follows the formal E1/R lifecycle for stop or close.

## Prohibitions

- A producer impersonates C, E1, R, E2, or a fresh Reviewer.
- A producer uses a formal title, cycle, ready, result, slash, lock, registry, or run id.
- C, R, or a producer writes the target project, or any shared-workspace writer exists besides E1.
- A `read_only` lane writes anything.
- An `isolated_artifact` lane writes outside its accepted lane root or uses a project-contained or
  ancestral path, drive root, user root, system root, link, junction, reparse point, mount, or
  overlapping lane.
- A producer sends a candidate directly to E1, E2, or R, or E1 uses unconverged scratch.
- Producer count, votes, speed, or matching answers replace C's source-based adjudication.
- The user must configure lanes, scratch roots, hashes, roles, review procedures, or a new command.
- C polls or background-monitors producers, delays stop/close to wait for them, or accepts a late,
  drifted, tampered, or out-of-bounds candidate.
