#!/usr/bin/env python3
"""Validate the installed CER skill package using only the standard library."""

from __future__ import annotations

import argparse
import copy
import re
import sys
from pathlib import Path, PurePosixPath


EXPECTED_FILES = {
    "SKILL.md",
    "VERSION",
    "agents/openai.yaml",
    "references/core-runtime.md",
    "references/roadmap.md",
    "references/uat.md",
    "references/parallel-producers.md",
    "scripts/validate_cer_skill.py",
}
TEXT_FILES = EXPECTED_FILES - {"VERSION"}
SEMVER_RE = re.compile(r"(?<![0-9])\d+\.\d+\.\d+(?![0-9])")
OWNER_MARKER = "<!-- cer-parallel-producers-owner -->"
UNEXPECTED_FAILURE_OWNER_MARKER = "<!-- cer-unexpected-failure-gate-owner -->"
TRUTH_SOURCE_INTAKE_OWNER_MARKER = "<!-- cer-truth-source-intake-gate-owner -->"
DRIFT_CHECKPOINT_OWNER_MARKER = "<!-- cer-controller-drift-checkpoint-owner -->"
RESULT_DISPOSITION_OWNER_MARKER = "<!-- cer-result-disposition-gate-owner -->"
EXECUTION_PROFILE_OWNER_MARKER = "<!-- cer-execution-profile-gate-owner -->"
EXPECTED_DEFAULT_PROMPT = (
    "Use $cer-workflow-en with one writer for this work; create a fresh Reviewer in "
    "proportion to risk, and accelerate internally when useful without extra setup."
)
FORMAL_COMMANDS = {
    "/CER-auto",
    "/CER-start",
    "/CER-stop",
    "/CER-close",
    "/CER-status",
    "/CER-help",
}
MAX_ROUTER_BYTES = 6500

EN_TRIGGER_MATRIX_EXPECTATIONS = {
    "frontmatter": (
        "Use only for explicit CER-qualified commands or equivalent meaning",
        "/CER-auto",
        "Plain start/work or close/finish messages are not CER triggers",
    ),
    "auto_row": ("no C exists before the route decision", "CER Workflow enters full C/E/R, with R only when risk requires it", "Remote is unsupported in this first version"),
    "start_row": ("Plain start/work messages do not start CER",),
    "close_row": ("Plain close/finish messages do not close CER",),
    "auto_help_template": (
        "Show this table and the `/CER-auto` task shape",
        "goal + constraints/do-not-do + acceptance + authority/source/authorization boundary",
        "adapt it to the user's context rather than a fixed domain",
        "before a formal decision, payment, publication, or external commitment, stop and use CER Workflow",
    ),
    "startup_owner": ("Plain start/work messages belong to the target workspace's existing governance and are not CER triggers",),
    "stop_owner": ("Plain close/finish messages belong to the target workspace's existing governance and do not map to CER stop or close",),
    "uat_install_start": (
        "`/CER-start` and `Start CER` trigger CER",
        "a plain start/work message does not",
    ),
    "uat_install_auto": (
        "`/CER-auto` and `Run CER adaptively` trigger the local execution profile gate",
        "no C exists before the route decision",
    ),
    "uat_install_close": (
        "`/CER-close` and `Close CER` trigger CER close",
        "a plain close/finish message does not close CER and does not map to `/CER-stop`",
    ),
    "uat_failure": ("A plain start/work message starts CER, or a plain close/finish message triggers CER close/stop",),
    "uat_failure_auto": ("`/CER-auto` claims C before the route decision",),
}

EXECUTION_PROFILE_REQUIREMENTS = {
    "sole_owner": "This section is the sole runtime owner for `/CER-auto`",
    "local_only": "The first version supports only a local user task. Remote `/CER-auto` is unsupported",
    "pre_identity": "The entry task is not C before the route decision",
    "start_unchanged": "Explicit `/CER-start` keeps its existing meaning",
    "selective_read": "first read only this section plus the user request and target-project sources needed for the decision",
    "single_read_bundle": "obtain them in one bounded read instead of adding a selector-only read roundtrip",
    "minimum_strength": "Select the minimum sufficient collaboration strength between ordinary execution, Goal, CER Workflow, or blocked",
    "route_lines": "Route: CER Workflow — <why CER is needed and where to stop>",
    "blocked_route_line": "Route: blocked — <missing authority/safety/acceptance condition>",
    "ordinary_boundary": "Ordinary execution does not start CER, claim C/E/R identity, show a bear card, or load other CER references",
    "goal_boundary": "Goal does not provide CER's sole writer, C/E/R identity, or authority owner",
    "cer_boundary": "Only after selecting CER Workflow, and only at the point that needs CER, does the task read this file and `roadmap.md` in full",
    "decision_basis": "Judge the route by the next step's consequence, uncertainty, reversibility, and owner clarity",
    "source_evidence_boundary": "source count, schema, hash, or receipt cannot replace authority evidence",
    "goal_route": "the endpoint, verification loop, stop condition, and known authority sources are clear",
    "cer_gated_promotion": "formal data, model input, a report paragraph, a decision gate, handoff truth, a release/readiness claim, a public/external claim",
    "blocked_boundary": "Goal capability with no safe fallback",
    "bounded_reconciliation": "touching persistent state does not by itself select CER Workflow",
    "cost_boundary": "Cost never bypasses safety, authority, persistence, external authorization, the Reviewer owner, or the target release owner",
    "recheck_boundaries": "Recheck only at four material boundaries: a user-requirement, authority, or consequence change; a phase boundary; a result disposition that changes carry-forward, progress, or authority effect; and immediately before an external, public, irreversible, or other high-consequence operation",
    "no_step_recheck": "Do not recheck every small step; token pressure by itself is not an upgrade or downgrade reason",
    "existing_owners": "Existing Reviewer ownership still decides whether R is required, and the target project's existing release owner still decides release assurance",
    "safe_step_down": "there is no active batch, E1 has stopped writing, results have been read back and dispositioned, required persistence has been written and read back, and no truth conflict remains",
    "not_stop_close": "This is a route transition, not `/CER-stop` or `/CER-close`",
    "safe_step_up": "Its drafts, diagnostics, Goal outputs, and ordinary-subagent outputs default to working material",
    "baseline_readback": "E1 rereads the workspace baseline before its first write",
    "conditional_checkpoint": "Persist one short, non-authoritative route-transition checkpoint only when a transition crosses a task, session, or context, or carries a material artifact, adjudication, or risk",
    "no_new_structure": "Do not create a new file, schema, YAML object, or registry",
    "checkpoint_block": "Missing or contradictory required readback keeps the next write or dispatch blocked",
}

EXECUTION_PROFILE_UAT_REQUIREMENTS = {
    "ordinary_route": "clear authority, one writer, reversible changes, no external side effect, and sufficient existing acceptance",
    "single_read_bundle": "obtain them in one bounded read with no selector-only read roundtrip",
    "ordinary_subagent": "that subagent receives no formal E/R identity, ready/result lifecycle, or Reviewer effect",
    "bounded_reconciliation": "only local, reversible metadata reconciliation by one writer remains in the same workspace",
    "bounded_reconciliation_limit": "An unresolved truth conflict must not be relabeled as a mechanical correction to step down",
    "goal_route": "endpoint, verification loop, stop condition, and known authority sources are clear",
    "goal_no_promotion": "does not yet accept the result as formal data, model input, a report paragraph, a decision gate, handoff truth, a release/readiness claim, or a public/external claim",
    "goal_vague": "instead of entering Goal directly",
    "cer_route": "output one `Route: CER Workflow — <why CER is needed and where to stop>` line only at that point that needs CER",
    "blocked_route": "output one `Route: blocked — <missing authority/safety/acceptance condition>` line",
    "small_high_consequence": "A one-line task involving deletion, release, official acceptance, or a high-consequence decision selects CER Workflow or blocks",
    "false_evidence": "source count, schema, hash, or receipt as authority evidence",
    "no_09_runtime": "Citing `CER_docs/09` as runtime routing authority",
    "mixed_promotion": "only the later point that needs CER selects CER Workflow",
    "goal_unavailable_fallback": "If Goal is unavailable but bounded ordinary execution can safely finish, do not automatically block",
    "external_background": "If an external claim is only background context and not a formal claim, do not automatically select CER Workflow",
    "start_unchanged": "Explicit `/CER-start` is never adaptively downgraded",
    "remote_unsupported": "Remote `/CER-auto` must stop as unsupported in the first version",
    "bounded_recheck": "Ordinary small steps and token pressure do not trigger a recheck",
    "owner_boundary": "The adaptive route decision cannot force, skip, or replace either owner",
    "safe_step_down": "there is no active batch, E1 has stopped writing, results and result disposition are read back, required persistence is read back, and no truth conflict remains",
    "safe_step_up": "Ordinary drafts, diagnostics, Goal output, and subagent output remain working material",
    "startup_order": "before a valid zero-write E1 `ready` is direct-pushed and read back, it shows no successful startup card and dispatches no formal batch",
    "conditional_checkpoint": "A transition in the same task with no material artifact, adjudication, or risk carry-forward creates no checkpoint",
    "checkpoint_block": "Missing or conflicting required readback keeps the next write or dispatch blocked",
}

EXECUTION_PROFILE_FORBIDDEN = {
    "start_downgrade": "`/CER-start` may automatically downgrade to ordinary execution",
    "pre_identity": "`/CER-auto` is C before the route decision",
    "remote_supported": "Remote `/CER-auto` is supported",
    "file_count": "Many files always require CER Workflow",
    "token_bypass": "Saving tokens may bypass safety or an authority owner",
    "fixed_reviewer": "`/CER-auto` always creates a Reviewer",
    "unsafe_step_down": "An active batch may step down to ordinary execution",
    "draft_authority": "An ordinary draft automatically becomes authoritative_input",
    "goal_authority": "Goal automatically becomes the CER authority owner",
    "false_evidence": "Source count, schema, hash, or receipt is enough to prove authority",
    "cite_09_runtime": "`CER_docs/09` may be `/CER-auto` runtime routing authority",
    "whole_phase_cer": "A later point that needs CER means the whole task must be CER",
    "goal_unavailable_block": "Goal unavailable means blocked even when bounded ordinary execution can safely finish",
    "background_claim_gate": "An external claim used only as background must still select CER Workflow",
    "fixed_checkpoint": "Every route transition creates a fixed YAML checkpoint",
    "persistent_file_always_cer": "Every persistent-state file creates C/E/R",
    "unsafe_read_bundle": "Even different permissions or scope must be combined into one read",
}

REVIEWER_PROPORTIONALITY_COUNTEREXAMPLES = {
    "simple_fixed_fresh_reviewer": "Every simple task always creates a fresh Reviewer",
    "every_simple_task_reviewer": "A Reviewer is assigned by default to every simple task",
    "simple_task_fixed_r": "Simple work always gets R",
    "reverse_low_risk_fresh_reviewer": "A fresh Reviewer is used by default for all low-risk tasks",
    "passive_simple_task_reviewer": "An independent reviewer is always assigned to simple work",
    "low_risk_independent_reviewer": "Low-risk tasks always receive an independent reviewer",
}

OWNER_REQUIREMENTS = {
    "formal_roles": "CER has only the formal roles C, E1, R, and E2",
    "not_fifth_role": "not a fifth role",
    "no_new_lifecycle": "receives no formal title, cycle, ready, result, batch lifecycle, or Reviewer identity",
    "no_new_commands": "adds no slash command",
    "two_independent_lanes": "At least two work lanes are independent and need no result from each other, shared mutable state, or fixed execution order",
    "frozen_input_version": "Each lane's input and source identity is frozen",
    "concurrent_controller_work": "C has non-duplicative critical analysis, gating, or adjudication work to do concurrently",
    "independently_verifiable_candidates": "C can independently verify each candidate against authoritative sources",
    "material_time_saving": "Expected net time savings materially exceed startup, readback, hashing, deduplication, and adjudication costs",
    "available_execution_slots": "Required parallel execution slots are available without reducing capacity needed by formal E1 or a fresh R",
    "read_only": "`read_only`",
    "isolated_artifact": "`isolated_artifact`",
    "read_only_zero_write": "zero writes everywhere",
    "project_noncontainment": "`scratch_root` and the target project do not contain each other",
    "dangerous_roots": "not a drive root, user root, system root",
    "link_boundary": "symlink, junction, Windows reparse point, mount",
    "lane_nonoverlap": "Lane roots are distinct, are not ancestors of one another",
    "actual_tool_permission_boundary": "Actual tool permissions allow only that lane's explicit root. Relative paths, wildcards, environment fallback, or a producer-selected location cannot expand the boundary",
    "lane_contract_label": "`lane_label`",
    "lane_contract_goal": "One objective",
    "lane_contract_input": "Input identity and version, source identity, and verifiable source coordinates",
    "lane_contract_scope": "Allowed and forbidden scope",
    "lane_contract_output": "Expected candidate output",
    "lane_contract_acceptance": "Acceptance method",
    "lane_contract_stop": "Stop condition",
    "scratch_root": "`scratch_root`",
    "candidate_claims": "`claims`",
    "candidate_unknowns": "`unknowns`",
    "verifiable_source_coordinates": "Actual source coordinates",
    "candidate_hash": "actual absolute path and SHA-256",
    "controller_readback": "C personally reads back",
    "rehash": "recomputes SHA-256",
    "no_vote": "must not accept by vote",
    "merged_batch": "E1 receives only that C-converged batch",
    "no_direct_e1": "must not use raw producer communication",
    "no_wait_poll": "C does not wait, poll, or background-monitor producers",
    "late": "A late candidate",
    "input_drift": "Input or source drift",
    "tamper": "hash drift, tamper",
    "out_of_bounds": "out-of-bounds",
    "producer_failure": "producer creation fails",
    "stop_close": "`/CER-stop` and `/CER-close` do not wait for producers",
    "serial_fallback": "`producer_count=0`",
    "user_simplicity": "The user does not configure producers",
    "material_only_report": "Report only results, unknowns, blockers, or risks that materially affect the user",
}

UAT_REQUIREMENTS = {
    "default_prompt_risk_proportionate": "create a fresh Reviewer in proportion to risk",
    "default_prompt_simple_task": "does not force a Reviewer for simple work",
    "normal_two_lanes": "two lanes are independent",
    "auto_idle": "`producer_count=0`",
    "no_subagent": "no subagent capability",
    "cost_fallback": "uneconomic parallel cost",
    "read_only_write": "A `read_only` lane that attempts any write",
    "root_boundary": "inside the project or one of its ancestors, at a drive root, user root, system root",
    "link_boundary": "symlink, junction, reparse point, mount",
    "lane_overlap": "equal to or ancestral to another lane",
    "partial_drift": "discard only the dependent candidate",
    "source_conflict": "not by vote",
    "late_candidate": "A late candidate",
    "producer_failure": "producer failure",
    "artifact_tamper": "artifact hash tamper",
    "role_impersonation": "producer impersonating E/R",
    "direct_to_e1": "sending directly to E1",
    "unmerged_scratch": "E1 using unconverged scratch",
    "project_write": "C/R/producer writing the target project",
    "stop_close": "`/CER-stop` or `/CER-close` does not wait",
    "no_lifecycle_identity": "no formal title, cycle, ready, result, slash, lock, registry, or run id",
    "roadmap_boundary": "Roadmap role columns and lifecycle cards still contain formal roles only",
    "auto_wait_threads_forbidden": "automatically uses `wait_threads` or `read_thread` after dispatch as the receiving mechanism",
}

UNEXPECTED_FAILURE_REQUIREMENTS = {
    "test_not_authority": "tests produce evidence but do not grant more modification authority",
    "allowlist_not_semantics": "does not authorize E1 to change another owner, authoritative source, or protected meaning inside that file",
    "gate_off": "The gate stays inactive",
    "caused": "E1 may repair it in the current batch",
    "preexisting": "report it without repairing it",
    "unknown_or_boundary": "stop further writes",
    "regression_boundary": "does not expand E1's repair authority",
    "controller_only": "Only C may refreeze the contract and expand scope by dispatching a new batch with a new `batchId` and `payloadDigest`",
}

DELIVERY_REQUIREMENTS = {
    "post_dispatch_parked": "After dispatch, task creation, or send, C immediately enters `POST_DISPATCH_PARKED`",
    "no_auto_wait": "must not automatically use `wait_threads`, `read_thread`, or a platform-equivalent tool to wait, wake itself, track progress, read commentary, read finals, probe status, or discover results",
    "no_auto_progress_read": "read finals, probe status, or discover results",
    "read_exceptions": "has only two read exceptions: a one-time thread check explicitly requested by the user in the same turn, or one bounded readback for verification/adjudication after C has received a direct-push",
    "no_push_no_progress": "Without a direct-push, a wait snapshot, completion state, commentary, summary, child final, task title, user relay, or passive read cannot advance `pending` / `delivery_incomplete`",
    "no_push_no_advance": "cannot advance `pending` / `delivery_incomplete`",
    "no_automatic_waiting": "forbids automatic waiting, repeated waiting, polling, background listening",
}

DELIVERY_UAT_REQUIREMENTS = {
    "post_dispatch_parked_uat": "after dispatch it stays `POST_DISPATCH_PARKED`",
    "bounded_wakeup_wrapper_bad": "wraps waiting as a bounded wakeup",
    "no_push_next_batch_bad": "advances state or dispatches the next batch without direct-push",
}

TRUTH_SOURCE_INTAKE_REQUIREMENTS = {
    "sole_owner": "The truth-source intake gate is the sole owner inside Controller preflight",
    "four_questions": "who owns it; who actually uses it; how it takes effect; and what counterexample can disprove it",
    "owner_definition": "`Who owns it` means the source anchor in a user decision, project source of truth, rule, file, or external authority",
    "consumer_definition": "`Who actually uses it` means how E1, R, the deliverable, install surface, public surface, later batch, or user flow consumes that condition",
    "effect_definition": "`How it takes effect` means how it changes this batch's dispatch, deliverable content, permissions, acceptance, or outcome judgment",
    "disproof_definition": "`What counterexample can disprove it` means the readback, test, Reviewer question, or counterexample that would make this batch unable to count as successful",
    "missing_is_critical": "If any item cannot be answered, or if the answer depends on a required source C has not read, the condition is `critical missing`",
    "no_dispatch": "C must not dispatch a formal implementation batch and may only perform necessary read-only diagnosis, narrow the acceptance scope, or use a `🟡 User decision` stop",
    "not_full_audit": "Do not expand this gate into default full-text ingestion, whole-repo review, or fixed Full Audit",
}

TRUTH_SOURCE_INTAKE_UAT_REQUIREMENTS = {
    "four_questions_pass": "Before a non-simple formal implementation batch, C can answer each truth-source intake question",
    "missing_blocks": "If C cannot answer any truth-source intake question",
    "missing_still_dispatches": "A non-simple formal implementation batch has not answered who owns it, who actually uses it, how it takes effect, and what counterexample can disprove it, but C still creates/reuses E1 or dispatches the implementation batch",
    "overwide_gate": "C expands the truth-source intake gate into default full-text ingestion, whole-repo review, fixed Full Audit, a second rule owner, or a fixed form workflow",
}

CONTROLLER_CHALLENGE_UAT_REQUIREMENTS = {
    "section": "## Controller Long-Task Challenge Scenarios",
    "measurable_endpoint": "lacks a measurable or readable endpoint",
    "authority_boundary": "required authority, allowed boundaries, or counterexample evidence is insufficient",
    "adjacent_mainline": "plausible adjacent request, process improvement, or substitute deliverable",
    "defensive_expansion": "is not a reason for defensive expansion",
    "changed_contract": "cannot retain its old acceptance identity",
    "no_thrashing": "must not cause ordinary/CER route thrashing",
}

TRUTH_SOURCE_INTAKE_FORBIDDEN = {
    "missing_four_questions_dispatch": "when who owns it, who actually uses it, how it takes effect, and what counterexample can disprove it are unanswered, C may still dispatch a formal implementation batch",
    "full_ingestion_required": "the truth-source intake gate requires default full-text ingestion, whole-repo review, or fixed Full Audit",
}

UNEXPECTED_FAILURE_UAT_MARKERS = {
    "gate_off": "<!-- cer-uat-unexpected-failure:gate-off -->",
    "caused": "<!-- cer-uat-unexpected-failure:caused -->",
    "preexisting": "<!-- cer-uat-unexpected-failure:preexisting -->",
    "unknown": "<!-- cer-uat-unexpected-failure:unknown -->",
    "semantic_boundary": "<!-- cer-uat-unexpected-failure:semantic-boundary -->",
    "acceptance_boundary": "<!-- cer-uat-unexpected-failure:acceptance-boundary -->",
}

UNEXPECTED_FAILURE_FORBIDDEN = {
    "test_grants_authority": "A test failure grants E1 more modification authority",
    "allowlist_grants_semantics": "A file in the allowlist authorizes E1 to change every meaning in that file",
    "missing_baseline_guess": "Without a baseline, E1 should guess and repair",
    "executor_expands_scope": "E1 may expand scope without C refreezing a new batch",
    "controller_expands_without_new_identity": "C may expand scope while reusing the old `batchId` and `payloadDigest`",
}

SENDABLE_PACKET_REQUIREMENTS = {
    "draft_sendable_split": "`draft_packet`",
    "no_placeholders": "`sendable_packet` must not retain `<...>` placeholders",
    "truth_intake_summary": "summary of the truth-source intake four questions passed in Controller preflight: who owns it, who actually uses it, how it takes effect, and what counterexample can disprove it",
    "create_prompt_handshake_only": "The initial `create_thread` prompt for a new E1/R is not a formal batch",
    "create_prompt_no_full_payload": "Do not put the complete source corpus, candidate work content, or formal batch payload in the create prompt",
    "large_payload_once": "C sends it exactly once in the formal `sendable_packet`",
    "large_payload_split": "inputs that are too long or cross risk boundaries are split into multiple formal batches by semantic/risk unit",
    "pre_dispatch_evidence": "A `sendable_packet` for long-running, multi-batch, high-risk, or non-simple formal implementation work must include a compact `pre_dispatch_evidence` block",
    "pre_dispatch_not_new_owner": "It is not a new source of truth, fixed form, background monitor, or Full Audit",
    "pre_dispatch_fields": "It includes at least: an `outcome_anchor` pointer or summary; the unfinished condition this batch improves and the readable outcome difference success should create; the truth-source intake four-question summary with source anchors; required sources read and the disposition of remaining unknowns; work-lane classification; and, when a drift checkpoint trigger exists, the checkpoint conclusion, or why no trigger applies",
    "pre_dispatch_missing_blocks": "If it is missing, contradictory, depends on unread required sources, or merely says judgment was done without readable support, the packet is not sendable",
    "pre_dispatch_assignee_blocks": "If E1/R receives a formal batch without required `pre_dispatch_evidence`, it must direct-push a zero-write blocker such as `BATCH_BLOCKED_MISSING_PRE_DISPATCH_EVIDENCE` and stop",
    "concrete_bindings": "A real dispatch must fill actual `threadId` or platform-equivalent coordinate, `returnTarget`, `messageId`, `batchId`, `batchSeq`, `payloadDigest`, and any routing coordinate explicitly required by the active tool schema/receipt",
    "sessionid_not_threadid": "sessionId is not a substitute for threadId as a formal dispatch coordinate",
    "hostid_not_hard_required": "hostId is used only when the active tool schema or receipt requires or provides it",
    "no_hostid_inference": "do not derive hostId from `local`, title, sessionId, threadId shape, or an error message",
    "relative_identity_draft_only": "Relative wording such as `same E1`, `the E1 above`, or `next sequence` is draft-only",
    "review_manifest": "R dispatch must fill actual `candidateIdentity`, `candidateManifest`, and candidate delivery evidence",
    "missing_blocks": "Missing any one of these leaves the packet at `dispatch_blocked` or `decision_blocked`",
}

SENDABLE_PACKET_UAT_REQUIREMENTS = {
    "placeholder_self_pass": "A formal `sendable_packet` still contains `<...>` placeholders",
    "create_prompt_payload": "A new E1/R create prompt contains the complete source corpus, candidate work content, or formal",
    "double_large_payload": "The same complete large input is sent in both the create prompt and formal `sendable_packet`",
    "relative_identity": "A formal dispatch uses relative wording such as `same E1`, `the E1 above`, or `next sequence`",
    "hostid_hard_required": "Controller still hard-requires `hostId`",
    "hostid_inferred": "derives hostId from `local`, title, sessionId, threadId shape, or an error message",
    "sessionid_replaces_threadid": "A formal dispatch uses sessionId instead of threadId as the formal dispatch coordinate",
    "review_manifest_missing": "R dispatch lacks actual `candidateIdentity`, `candidateManifest`, or candidate delivery evidence",
    "pre_dispatch_missing": "packet lacks `pre_dispatch_evidence`",
    "pre_dispatch_claim_only": "only says \"C already judged\" without readable support",
}

SENDABLE_PACKET_FORBIDDEN = {
    "placeholder_allowed": "A sendable dispatch may retain `<...>` placeholders",
    "create_prompt_full_payload": "The create prompt may contain the complete source corpus or formal batch payload",
    "double_send_large_payload": "C may send the same complete large input in both the create prompt and formal `sendable_packet`",
    "relative_identity_allowed": "`same E1`, `the E1 above`, or `next sequence` may be used as formal dispatch identity",
    "hostid_always_required": "Every real dispatch must include `hostId` even when the active tool schema requires only `threadId`",
    "sessionid_infers_hostid": "hostId may be derived from sessionId, title, `local`, or an error message before continuing",
    "sessionid_replaces_threadid": "sessionId may replace threadId as formal dispatch coordinate",
    "review_manifest_optional": "R dispatch may omit `candidateManifest`",
    "draft_pass": "`draft_packet` may self-rate as sendable",
    "pre_dispatch_optional": "Long-running, multi-batch, high-risk, or non-simple formal implementation work does not need `pre_dispatch_evidence`",
    "assignee_fills_missing_pre_dispatch": "E1/R may fill in C's missing pre-dispatch evidence and continue writing",
}

MESSAGE_ID_BOUNDARY_REQUIREMENTS = (
    "`messageId` is only a CER message-layer identity, deduplication, and tracing field",
    "It is not a Codex execution command, an App Server `method`, a JSON-RPC request `id`, a `threadId`, a `sessionId`, an idempotency key, or authorization",
    "Without an actual tool call and its tool result or verifiable delivery evidence",
    "a `messageId` alone is not proof that a message was delivered or work was executed",
)

MESSAGE_ID_UAT_REQUIREMENTS = {
    "identity_not_command": "A `messageId` is merely placed in a prompt, dispatch packet, summary, or receipt-like text and treated as proof that a thread was created, a turn started, a tool was called, a write was triggered, or authority was granted",
}

MESSAGE_ID_FORBIDDEN = {
    "messageid_starts_operation": "A `messageId` alone can create a thread, start a turn, or call a tool",
    "messageid_is_authority": "A `messageId` itself is authorization or an idempotency key",
}

LIVING_BRIEF_REQUIREMENTS = (
    "C maintains a living task brief",
    "The living task brief is not a new workflow and does not create fixed project documents",
    "confirmed requirements/exclusions, safe inferences, critical gaps, latest user feedback, current batch freeze, next observable preview or decision point, and what changed from the previous version",
    "C freezes only the next safely executable batch",
    "E1/R dispatches use the latest living task brief and current batch freeze",
    "E1 is authorized only to execute the current batch freeze",
    "R reviews against the latest task brief, current batch freeze, candidate identity, and delivery evidence",
)

LIVING_BRIEF_ROADMAP_REQUIREMENTS = (
    "shows the living task brief, current batch freeze, and next observable checkpoint",
    "Any user-visible living-brief rendering must carry `CER` identity",
    "Do not present it as a Codex task brief, Goal plan, assistant plan, or unbranded internal feature",
    "CER roadmap | live brief",
    "CER live brief: confirmed=<...> | safe inference=<...> | decisions needed=<...>",
    "CER current batch freeze: <only what this batch will do>",
    "CER last feedback / change: <... / none>",
    "The living task brief also derives only from the highest available authority",
)

LIVING_BRIEF_UAT_REQUIREMENTS = {
    "fuzzy_start": "For a fuzzy but startable multi-batch task, C creates a living task brief",
    "no_full_spec_first": "does not require the user to write a complete specification first",
    "not_project_context_prereq": "does not treat `$project-context-workflow` as a prerequisite",
    "feedback_delta": "After the user sees an intermediate result and changes direction or adds a constraint, C first updates the living task brief and roadmap delta",
    "review_latest_brief": "R reviews against the latest task brief, current batch freeze, candidate identity, and delivery evidence",
}

LIVING_BRIEF_FORBIDDEN = {
    "new_workflow": "The living task brief is an independent new workflow",
    "initial_prompt_full_freeze": "The initial prompt is always the complete frozen specification for the cycle",
    "e1_unfrozen_future": "E1 may implement unfrozen future batches on its own",
    "r_initial_prompt_only": "R reviews only against the initial prompt",
}

OUTCOME_ANCHOR_REQUIREMENTS = (
    "immutable `outcome_anchor`",
    "unacceptable substitute outcomes",
    "`mainline_outcome`, `diagnostic`, `mechanism_improvement`, or `governance_self_improvement`",
    "zero expected outcome improvement and no necessary-prerequisite role must not be dispatched",
    "Activity is not outcome",
    "only after reading back and accepting a difference against one of the user's completion conditions",
    "same failure class is judged by shared root cause, user consequence, affected completion condition, and method",
    "Renaming, version changes, repackaging",
    "After two consecutive unresolved attempts in one class, C must not dispatch a third same-class repair",
    "A batch may end only as accepted outcome",
)

OUTCOME_ANCHOR_ROADMAP_REQUIREMENTS = (
    "accepted outcome difference against `outcome_anchor`",
    "Do not substitute batch, task, or review counts for outcome progress",
    "CER outcome anchor: unfinished=<completion condition> | accepted delta=<outcome difference / none>",
    "CER work lane: <mainline_outcome / diagnostic / mechanism_improvement / governance_self_improvement>",
)

OUTCOME_ANCHOR_UAT_REQUIREMENTS = {
    "anchor_fixed": "Long multi-batch work fixes `outcome_anchor` before the first batch",
    "zero_delta_rejected": "An implementation batch with zero expected outcome improvement and no necessary-prerequisite role is rejected",
    "diagnostic_not_progress": "A diagnostic batch may run and produce a handoff prerequisite, but it is classified as `diagnostic` and does not increase mainline progress",
    "technical_pass_not_progress": "Technical checks, format, file consistency, or review may pass, but when `outcome_anchor` has no accepted outcome difference, the batch is not marked as successful progress",
    "third_retry_intercepted": "After two consecutive unresolved attempts in the same failure class, a third same-class repair is intercepted",
    "rename_same_retry": "Renaming, version changes, repackaging, or redispatching the same method is still treated as the same retry class",
    "reviewer_rejects_drift": "R must reject a batch that diverges from the original outcome, is only technical activity, repeats rework, or substitutes another deliverable shape for what the user asked for",
    "mechanism_not_mainline": "`mechanism_improvement` or `governance_self_improvement` does not contaminate mainline progress",
    "adjacent_not_blocker": "Adjacent improvement failure does not automatically block the original task",
    "simple_lightweight": "Simple, one-step, low-risk work with one clear endpoint still uses lightweight summary and C readback",
    "completion_outcomes": "Completion reporting lists accepted outcome differences and unfinished conditions",
}

OUTCOME_ANCHOR_FORBIDDEN = {
    "zero_delta_dispatch": "An implementation batch with zero expected outcome improvement may be dispatched",
    "diagnostic_mainline": "A diagnostic batch increases mainline progress",
    "third_retry_allowed": "A third same-class repair may continue",
    "activity_completion": "Batch, task, Reviewer, or candidate counts are completion evidence",
}

DRIFT_CHECKPOINT_REQUIREMENTS = {
    "sole_owner": "The long-task drift checkpoint is the sole owner in this section",
    "no_new_monitor": "do not create another monitoring role, background process, or fixed table",
    "resume_trigger": "resume/context transition",
    "two_no_delta_trigger": "two consecutive batches with no accepted outcome difference",
    "same_failure_trigger": "the second same-class failure",
    "adjacent_trigger": "E1/R proposes an adjacent direction change or substitute deliverable",
    "user_change_trigger": "the user changes direction or adds constraints",
    "close_release_trigger": "before close/release/major delivery",
    "next_condition": "whether the next batch still improves an unfinished `outcome_anchor` condition",
    "readable_delta": "what readable outcome difference success will create",
    "mainline_replacement": "are replacing the mainline outcome",
    "no_dispatch": "C must not dispatch a formal implementation batch",
    "allowed_exits": "may only switch to diagnostic work, narrow acceptance, stop for user decision, terminate the route",
    "fresh_r_bounded": "when C cannot reliably disprove the risk and the risk level justifies it",
    "not_progress": "A checkpoint, living task brief, or roadmap update does not count as outcome progress",
    "no_monitoring": "must not trigger background monitoring, polling, automatic `wait_threads`, fixed R, fixed Full Audit",
    "simple_exempt": "simple, one-step, low-risk work with one clear endpoint",
}

DRIFT_CHECKPOINT_UAT_REQUIREMENTS = {
    "generic_trigger": "long-running, multi-batch, or context-pollution-prone work",
    "two_no_delta": "two consecutive batches with no accepted outcome difference",
    "same_failure": "the second same-class failure",
    "adjacent_change": "E1/R proposes an adjacent direction change or substitute deliverable",
    "next_condition": "which unfinished `outcome_anchor` condition the next batch improves",
    "not_progress": "A drift checkpoint, living task brief, or roadmap update does not count as outcome progress",
    "no_monitoring": "does not trigger background monitoring, polling, automatic `wait_threads`, fixed R, or fixed Full Audit",
    "missing_checkpoint_dispatch": "After two consecutive batches with no accepted outcome difference, C dispatches another mainline implementation batch without a drift checkpoint",
    "adjacent_rewrites_mainline": "After E1/R proposes an adjacent direction change, substitute deliverable, or out-of-scope blocker, C rewrites the next mainline batch without classifying whether that proposal replaces the mainline outcome",
    "checkpoint_as_progress": "A drift checkpoint, living task brief, or roadmap update is counted as outcome progress",
    "checkpoint_triggers_monitoring": "A drift checkpoint triggers background monitoring, polling, automatic `wait_threads`, fixed R, or fixed Full Audit",
    "simple_forced": "Simple, one-step, low-risk work with one clear endpoint is forced to run a drift checkpoint",
}

DRIFT_CHECKPOINT_FORBIDDEN = {
    "background_monitor": "a drift checkpoint starts background monitoring",
    "automatic_wait": "a drift checkpoint may automatically use `wait_threads`",
    "fixed_reviewer": "every drift checkpoint must create R",
    "fixed_full_audit": "every drift checkpoint triggers Full Audit",
    "progress_credit": "a drift checkpoint itself increases mainline outcome progress",
    "simple_required": "simple one-step work must run a drift checkpoint",
}

RESULT_DISPOSITION_REQUIREMENTS = {
    "sole_owner": "The result disposition gate is the sole owner in this section",
    "accepted_as": "`accepted_as` is `evidence_only`, `working_candidate`, `terminal_deliverable`, or `authoritative_input`",
    "bare_result": "Bare `RESULT_ACCEPTED` means only that C adjudicated this batch and that communication can deduplicate it",
    "prior_result_use_enum": "classify `prior_result_use` as `working_material` or `authority_input`",
    "authority_fields": "if it is `authority_input`, C must list `promotion_evidence` and `project_owner_anchor`",
    "default_working_material": "Candidates, drafts, diagnostics, derived outputs, and review-only results default to `working_material` only",
    "authority_requires_owner": "To accept one as `authoritative_input`, C needs an explicit user decision or an actually read target-project owner anchor",
    "reviewer_split": "separate `content_verdict`, `implementation_verdict`, `outcome_verdict`, and `authority_promotion_verdict`",
    "reviewer_pass_limited": "a content or technical PASS does not automatically become an outcome PASS, authority-promotion PASS, or mainline progress",
    "out_of_scope_not_pass": "`out_of_scope` is not PASS",
    "review_scope_limited": "C must not expand R's original review scope",
    "terminal_candidate": "Only when the `outcome_anchor` itself asks for a draft, candidate, or sample as the endpoint",
    "persistence_blocks_next": "persistent truths conflict, are not synchronized, or the artifact role cannot be determined, `next_dispatch` must be `blocked`",
    "terminal_persistence_blocks_acceptance": "even when there is no next batch, C must not accept the result as a `terminal_deliverable`, report progress, or claim completion",
    "terminal_artifact_set_consistency": "C must also read back the final-state claim of every artifact classified as a `terminal_deliverable`",
    "closed_vocabulary": "`accepted_as`, `authority_effect`, `progress_effect`, and `prior_result_use` values above are closed vocabularies",
    "validate_before_persistence": "Before persistence, the proper writer must validate these fields against this section",
}

RESULT_DISPOSITION_UAT_REQUIREMENTS = {
    "content_pass_candidate": "When a Reviewer passes candidate content",
    "derived_output_blocked": "When a `derived_output` is listed by the next batch as `authority_input`",
    "authority_input_missing_fields": "When `prior_result_use: authority_input` is missing `promotion_evidence` or `project_owner_anchor`",
    "working_material_use_limits": "`prior_result_use: working_material` permits only editing, comparison, review, or refinement, not decision authority",
    "working_material_allowed": "`prior_result_use` to `working_material`",
    "technical_pass_limited": "When Reviewer technical PASS has outcome FAIL",
    "split_verdict_limited": "When Reviewer provides only `content_verdict: pass` or `implementation_verdict: pass`",
    "authority_out_of_scope": "`authority_promotion_verdict` is `out_of_scope`",
    "truth_conflict_blocks": "handoff, plan, progress, or another target-project source of truth",
    "persistence_change_classes": "result disposition changes current phase, artifact role, next product route, authoritative source, progress claim, or later batch input",
    "terminal_stale_state": "the final batch produced a correct deliverable but the target-project current-state owner still records the old phase, no terminal deliverable, or a stale next action",
    "terminal_artifact_set_conflict": "a `RUN_RESULT` classified as a `terminal_deliverable` still says persistence pending, unaccepted, or an old phase",
    "accepted_as_synonym_rejected": "`accepted_as=terminal_outcome`",
    "phase1_legal_disposition": "When a Phase 1 candidate completes only a non-terminal checkpoint",
    "progress_effect_synonym_rejected": "`progress_effect=accepted_outcome_delta_for_phase1_only`",
    "draft_terminal_deliverable": "user's endpoint itself is a draft, candidate, or sample",
}

RESULT_DISPOSITION_FORBIDDEN = {
    "bare_result_promotes": "Bare `RESULT_ACCEPTED` means official acceptance",
    "candidate_auto_authority": "A candidate PASS automatically becomes authoritative input",
    "technical_pass_outcome": "R technical PASS is outcome PASS",
    "authority_without_promotion_fields": "`authority_input` may omit `promotion_evidence` or `project_owner_anchor`",
    "out_of_scope_pass": "`out_of_scope` counts as PASS",
    "unpersisted_next_dispatch": "C may dispatch the next batch before persistence",
    "unpersisted_terminal_acceptance": "The final batch may be accepted as a `terminal_deliverable` and completion claimed while persistent truth is stale",
    "contradictory_terminal_artifact_accepted": "A terminal set may include an artifact that still says persistence pending and still be accepted",
}


def read_texts(root: Path) -> dict[str, str]:
    texts: dict[str, str] = {}
    for relative in EXPECTED_FILES:
        path = root / Path(relative)
        if path.is_file():
            texts[relative] = path.read_text(encoding="utf-8-sig")
    return texts


def frontmatter_findings(skill_text: str) -> list[str]:
    findings: list[str] = []
    match = re.match(r"\A---\n([\s\S]*?)\n---\n", skill_text)
    if not match:
        return ["SKILL.md frontmatter is missing or malformed"]
    keys: list[str] = []
    for line in match.group(1).splitlines():
        key_match = re.match(r"^([a-z_]+):", line)
        if not key_match:
            findings.append(f"SKILL.md frontmatter malformed line: {line}")
            continue
        keys.append(key_match.group(1))
    if keys != ["name", "description"]:
        findings.append(f"SKILL.md frontmatter keys must be name,description; actual={keys}")
    if not re.search(r'^name:\s*cer-workflow-en\s*$', match.group(1), re.MULTILINE):
        findings.append("SKILL.md name must be cer-workflow-en")
    if "explicit CER-qualified" not in match.group(1) or "on-demand parallel candidate" not in match.group(1):
        findings.append("SKILL.md description lacks explicit CER trigger or on-demand parallel capability")
    return findings


def openai_yaml_findings(text: str) -> list[str]:
    findings: list[str] = []
    required_lines = (
        'interface:',
        '  display_name: "CER Workflow"',
        '  short_description: "',
        '  default_prompt: "',
        'policy:',
        '  allow_implicit_invocation: false',
    )
    for required in required_lines:
        if required not in text:
            findings.append(f"agents/openai.yaml missing required shape: {required}")
    if "$cer-workflow-en" not in text:
        findings.append("agents/openai.yaml default_prompt must include $cer-workflow-en")
    default_prompt_match = re.search(
        r'^\s+default_prompt:\s*"([^"]+)"\s*$', text, re.MULTILINE
    )
    if default_prompt_match:
        default_prompt = default_prompt_match.group(1)
        # This is controlled package metadata, so exact equality is safer than
        # an open-ended synonym blacklist.
        if default_prompt != EXPECTED_DEFAULT_PROMPT:
            findings.append(
                "agents/openai.yaml default_prompt must exactly match the canonical "
                "risk-proportionate prompt and must not force Reviewer for simple work"
            )
    if re.search(r"\b(?:producer|lane|scratch|hash)\b", text, re.IGNORECASE):
        findings.append("agents/openai.yaml must not expose producer setup vocabulary")
    if re.search(r"^\s*(?:icon_small|icon_large|brand_color|dependencies):", text, re.MULTILINE):
        findings.append("agents/openai.yaml contains an unprovided icon, brand or dependency")
    top_keys = re.findall(r"^([a-z_]+):\s*$", text, re.MULTILINE)
    if top_keys != ["interface", "policy"]:
        findings.append(f"agents/openai.yaml top-level keys mismatch: {top_keys}")
    for line in text.splitlines():
        if re.match(r"^\s+(?:display_name|short_description|default_prompt):", line):
            if not re.search(r':\s*"[^"]*"\s*$', line):
                findings.append(f"agents/openai.yaml interface value must be quoted: {line}")
    short_match = re.search(r'^\s+short_description:\s*"([^"]+)"\s*$', text, re.MULTILINE)
    if short_match and not 25 <= len(short_match.group(1)) <= 64:
        findings.append("agents/openai.yaml short_description must be 25-64 characters")
    return findings


def normalized_contains(text: str, snippet: str) -> bool:
    return re.sub(r"\s+", " ", snippet) in re.sub(r"\s+", " ", text)


def markdown_section(text: str, heading: str) -> str:
    match = re.search(
        rf"^{re.escape(heading)}[ \t]*\n([\s\S]*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE,
    )
    return match.group(1) if match else ""


def command_table_row(text: str, command: str) -> str:
    pattern = r"^\|\s*`" + re.escape(command) + r"(?:\s+[^`]*)?`\s*\|.*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(0) if match else ""


def assert_snippets_present(
    text: str,
    snippets: tuple[str, ...],
    label: str,
    findings: list[str],
) -> None:
    for snippet in snippets:
        if not normalized_contains(text, snippet):
            findings.append(f"trigger matrix missing {label}: {snippet}")


def trigger_matrix_findings(texts: dict[str, str]) -> list[str]:
    findings: list[str] = []
    skill = texts["SKILL.md"]
    core = texts["references/core-runtime.md"]
    uat = texts["references/uat.md"]

    frontmatter = re.match(r"\A---\n([\s\S]*?)\n---\n", skill)
    description = frontmatter.group(1) if frontmatter else ""
    assert_snippets_present(
        description,
        EN_TRIGGER_MATRIX_EXPECTATIONS["frontmatter"],
        "SKILL.md frontmatter trigger boundary",
        findings,
    )
    for label, source in (
        ("SKILL.md /CER-auto row", command_table_row(skill, "/CER-auto")),
        ("core-runtime.md /CER-auto row", command_table_row(core, "/CER-auto")),
    ):
        assert_snippets_present(
            source,
            EN_TRIGGER_MATRIX_EXPECTATIONS["auto_row"],
            label,
            findings,
        )
    for label, source in (
        ("SKILL.md /CER-start row", command_table_row(skill, "/CER-start")),
        ("core-runtime.md /CER-start row", command_table_row(core, "/CER-start")),
    ):
        assert_snippets_present(
            source,
            EN_TRIGGER_MATRIX_EXPECTATIONS["start_row"],
            label,
            findings,
        )
    for label, source in (
        ("SKILL.md /CER-close row", command_table_row(skill, "/CER-close")),
        ("core-runtime.md /CER-close row", command_table_row(core, "/CER-close")),
    ):
        assert_snippets_present(
            source,
            EN_TRIGGER_MATRIX_EXPECTATIONS["close_row"],
            label,
            findings,
        )
    assert_snippets_present(
        markdown_section(skill, "## Commands"),
        EN_TRIGGER_MATRIX_EXPECTATIONS["auto_help_template"],
        "SKILL.md /CER-auto task template help",
        findings,
    )
    assert_snippets_present(
        markdown_section(core, "## Startup"),
        EN_TRIGGER_MATRIX_EXPECTATIONS["startup_owner"],
        "core-runtime.md startup owner",
        findings,
    )
    assert_snippets_present(
        markdown_section(core, "## Stop CER"),
        EN_TRIGGER_MATRIX_EXPECTATIONS["stop_owner"],
        "core-runtime.md stop owner",
        findings,
    )
    install = markdown_section(uat, "## Installation Scenario")
    assert_snippets_present(
        install,
        EN_TRIGGER_MATRIX_EXPECTATIONS["uat_install_auto"],
        "uat.md installation auto matrix",
        findings,
    )
    assert_snippets_present(
        install,
        EN_TRIGGER_MATRIX_EXPECTATIONS["uat_install_start"],
        "uat.md installation start matrix",
        findings,
    )
    assert_snippets_present(
        install,
        EN_TRIGGER_MATRIX_EXPECTATIONS["uat_install_close"],
        "uat.md installation close matrix",
        findings,
    )
    assert_snippets_present(
        markdown_section(uat, "## Failure Conditions"),
        EN_TRIGGER_MATRIX_EXPECTATIONS["uat_failure"],
        "uat.md failure-condition matrix",
        findings,
    )
    assert_snippets_present(
        markdown_section(uat, "## Failure Conditions"),
        EN_TRIGGER_MATRIX_EXPECTATIONS["uat_failure_auto"],
        "uat.md auto failure-condition matrix",
        findings,
    )
    return findings


def link_findings(root: Path, texts: dict[str, str]) -> list[str]:
    findings: list[str] = []
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for relative, text in texts.items():
        if not relative.endswith(".md"):
            continue
        source = PurePosixPath(relative)
        for target in link_re.findall(text):
            target_path = target.split("#", 1)[0]
            if not target_path or "://" in target_path:
                continue
            resolved = (root / Path(str(source.parent / target_path))).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                findings.append(f"relative link escapes skill root: {relative} -> {target}")
                continue
            if not resolved.is_file():
                findings.append(f"relative link target missing: {relative} -> {target}")
    return findings


def validate_texts(root: Path, texts: dict[str, str]) -> list[str]:
    findings: list[str] = []
    missing = sorted(EXPECTED_FILES - set(texts))
    if missing:
        findings.append(f"required files missing: {missing}")
        return findings

    version = texts["VERSION"]
    if not re.fullmatch(r"\d+\.\d+\.\d+\n?", version):
        findings.append("VERSION must contain exactly one stable semver line")
    for relative in TEXT_FILES:
        matches = SEMVER_RE.findall(texts[relative])
        if matches:
            findings.append(f"concrete package semver outside VERSION: {relative}: {matches}")

    findings.extend(frontmatter_findings(texts["SKILL.md"]))
    findings.extend(openai_yaml_findings(texts["agents/openai.yaml"]))
    findings.extend(link_findings(root, texts))
    findings.extend(trigger_matrix_findings(texts))

    skill_commands = {
        match.group(1)
        for match in re.finditer(r"^\|\s*`(/CER-[a-z]+)(?:\s+[^`]*)?`", texts["SKILL.md"], re.MULTILINE)
    }
    if skill_commands != FORMAL_COMMANDS:
        findings.append(f"slash commands must remain exactly six: {sorted(skill_commands)}")

    all_markdown = "\n".join(
        texts[relative] for relative in sorted(texts) if relative.endswith(".md")
    )
    normalized_markdown = re.sub(r"\s+", " ", all_markdown)
    if all_markdown.count(OWNER_MARKER) != 1:
        findings.append("parallel producer owner marker must occur exactly once")
    if OWNER_MARKER not in texts["references/parallel-producers.md"]:
        findings.append("parallel producer owner marker is not in its sole owner")
    if all_markdown.count(UNEXPECTED_FAILURE_OWNER_MARKER) != 1:
        findings.append("unexpected-failure gate owner marker must occur exactly once")
    if UNEXPECTED_FAILURE_OWNER_MARKER not in texts["references/core-runtime.md"]:
        findings.append("unexpected-failure gate owner marker is not in core-runtime.md")
    if all_markdown.count(TRUTH_SOURCE_INTAKE_OWNER_MARKER) != 1:
        findings.append("truth-source intake owner marker must occur exactly once")
    if TRUTH_SOURCE_INTAKE_OWNER_MARKER not in texts["references/core-runtime.md"]:
        findings.append("truth-source intake owner marker is not in core-runtime.md")
    if all_markdown.count(DRIFT_CHECKPOINT_OWNER_MARKER) != 1:
        findings.append("drift checkpoint owner marker must occur exactly once")
    if DRIFT_CHECKPOINT_OWNER_MARKER not in texts["references/core-runtime.md"]:
        findings.append("drift checkpoint owner marker is not in core-runtime.md")
    if all_markdown.count(RESULT_DISPOSITION_OWNER_MARKER) != 1:
        findings.append("result disposition owner marker must occur exactly once")
    if RESULT_DISPOSITION_OWNER_MARKER not in texts["references/core-runtime.md"]:
        findings.append("result disposition owner marker is not in core-runtime.md")
    if all_markdown.count(EXECUTION_PROFILE_OWNER_MARKER) != 1:
        findings.append("execution profile owner marker must occur exactly once")
    if EXECUTION_PROFILE_OWNER_MARKER not in texts["references/core-runtime.md"]:
        findings.append("execution profile owner marker is not in core-runtime.md")

    owner = re.sub(r"\s+", " ", texts["references/parallel-producers.md"])
    for label, required in OWNER_REQUIREMENTS.items():
        if required not in owner:
            findings.append(f"parallel producer owner missing {label}")
    if "## Exploration Helper Auto-Scheduling" in all_markdown:
        findings.append("legacy exploration-helper owner section remains")

    skill = texts["SKILL.md"]
    core = texts["references/core-runtime.md"]
    uat = re.sub(r"\s+", " ", texts["references/uat.md"])
    roadmap = re.sub(r"\s+", " ", texts["references/roadmap.md"])
    core_normalized = re.sub(r"\s+", " ", core)
    execution_profile_match = re.search(
        r"^## Execution Profile Gate[ \t]*\n([\s\S]*?)(?=^## |\Z)",
        core,
        re.MULTILINE,
    )
    if not execution_profile_match:
        findings.append("core-runtime.md lacks the execution profile gate owner section")
    else:
        execution_profile_owner = re.sub(
            r"\s+", " ", execution_profile_match.group(1)
        )
        if EXECUTION_PROFILE_OWNER_MARKER not in execution_profile_owner:
            findings.append("execution profile marker is outside its owner section")
        for label, required in EXECUTION_PROFILE_REQUIREMENTS.items():
            if required not in execution_profile_owner:
                findings.append(f"execution profile owner missing {label}")
    preflight_match = re.search(
        r"^## Controller Preflight[ \t]*\n([\s\S]*?)(?=^## Startup|\Z)",
        core,
        re.MULTILINE,
    )
    if not preflight_match:
        findings.append("core-runtime.md lacks the Controller preflight owner section")
    else:
        preflight_owner = re.sub(r"\s+", " ", preflight_match.group(1))
        if TRUTH_SOURCE_INTAKE_OWNER_MARKER not in preflight_owner:
            findings.append("truth-source intake marker is outside Controller preflight")
        for label, required in TRUTH_SOURCE_INTAKE_REQUIREMENTS.items():
            if required not in preflight_owner:
                findings.append(f"truth-source intake owner missing {label}")
    unexpected_failure_match = re.search(
        r"^## Execution Loop[ \t]*\n([\s\S]*?)(?=^## |\Z)", core, re.MULTILINE
    )
    if not unexpected_failure_match:
        findings.append("core-runtime.md lacks the execution-loop owner section")
    else:
        unexpected_failure_owner = re.sub(
            r"\s+", " ", unexpected_failure_match.group(1)
        )
        if UNEXPECTED_FAILURE_OWNER_MARKER not in unexpected_failure_owner:
            findings.append("unexpected-failure gate marker is outside its owner section")
        for label, required in UNEXPECTED_FAILURE_REQUIREMENTS.items():
            if required not in unexpected_failure_owner:
                findings.append(f"unexpected-failure gate owner missing {label}")
    outcome_anchor_match = re.search(
        r"^## Outcome Anchor And Progress Gate[ \t]*\n([\s\S]*?)(?=^## |\Z)",
        core,
        re.MULTILINE,
    )
    if not outcome_anchor_match:
        findings.append("core-runtime.md lacks the outcome-anchor progress owner section")
    else:
        outcome_anchor_owner = re.sub(r"\s+", " ", outcome_anchor_match.group(1))
        if DRIFT_CHECKPOINT_OWNER_MARKER not in outcome_anchor_owner:
            findings.append("drift checkpoint marker is outside outcome-anchor progress section")
        if RESULT_DISPOSITION_OWNER_MARKER not in outcome_anchor_owner:
            findings.append("result disposition marker is outside outcome-anchor progress section")
        for label, required in DRIFT_CHECKPOINT_REQUIREMENTS.items():
            if required not in outcome_anchor_owner:
                findings.append(f"drift checkpoint owner missing {label}")
        for label, required in RESULT_DISPOSITION_REQUIREMENTS.items():
            if required not in outcome_anchor_owner:
                findings.append(f"result disposition owner missing {label}")
    self_contained_match = re.search(
        r"^## Self-Contained Dispatch[ \t]*\n([\s\S]*?)(?=^## |\Z)",
        core,
        re.MULTILINE,
    )
    if not self_contained_match:
        findings.append("core-runtime.md lacks the self-contained dispatch section")
    else:
        self_contained_owner = re.sub(r"\s+", " ", self_contained_match.group(1))
        for label, required in SENDABLE_PACKET_REQUIREMENTS.items():
            if required not in self_contained_owner:
                findings.append(f"sendable-packet gate missing {label}")
    message_identity_match = re.search(
        r"^## Ambiguous Tool Outcomes, Role Reconciliation, And Batch Deduplication[ \t]*\n([\s\S]*?)(?=^## |\Z)",
        core,
        re.MULTILINE,
    )
    if not message_identity_match:
        findings.append("core-runtime.md lacks the message-identity boundary section")
    else:
        message_identity_owner = re.sub(r"\s+", " ", message_identity_match.group(1))
        for index, required in enumerate(MESSAGE_ID_BOUNDARY_REQUIREMENTS):
            if required not in message_identity_owner:
                findings.append(f"message-identity boundary missing requirement_{index}")
        for label, forbidden in MESSAGE_ID_FORBIDDEN.items():
            if forbidden in message_identity_owner:
                findings.append(f"message-identity fixed contradiction present {label}")
    for index, required in enumerate(LIVING_BRIEF_REQUIREMENTS):
        if required not in core_normalized:
            findings.append(f"living-brief runtime missing requirement_{index}")
    for label, forbidden in LIVING_BRIEF_FORBIDDEN.items():
        if forbidden in core_normalized:
            findings.append(f"living-brief fixed contradiction present {label}")
    for label, forbidden in UNEXPECTED_FAILURE_FORBIDDEN.items():
        if forbidden in normalized_markdown:
            findings.append(f"unexpected-failure fixed contradiction present {label}")
    for label, required in DELIVERY_REQUIREMENTS.items():
        if required not in core_normalized:
            findings.append(f"delivery gate missing {label}")
    for label, required in DELIVERY_UAT_REQUIREMENTS.items():
        if required not in uat:
            findings.append(f"uat.md missing delivery counterexample {label}")
    for label, forbidden in SENDABLE_PACKET_FORBIDDEN.items():
        if forbidden in normalized_markdown:
            findings.append(f"sendable-packet fixed contradiction present {label}")
    for label, forbidden in TRUTH_SOURCE_INTAKE_FORBIDDEN.items():
        if forbidden in normalized_markdown:
            findings.append(f"truth-source intake fixed contradiction present {label}")
    for index, required in enumerate(OUTCOME_ANCHOR_REQUIREMENTS):
        if required not in core_normalized:
            findings.append(f"outcome-anchor runtime missing requirement_{index}")
    for label, forbidden in OUTCOME_ANCHOR_FORBIDDEN.items():
        if forbidden in normalized_markdown:
            findings.append(f"outcome-anchor fixed contradiction present {label}")
    for label, forbidden in DRIFT_CHECKPOINT_FORBIDDEN.items():
        if forbidden in normalized_markdown:
            findings.append(f"drift-checkpoint fixed contradiction present {label}")
    for label, forbidden in RESULT_DISPOSITION_FORBIDDEN.items():
        if forbidden in normalized_markdown:
            findings.append(f"result-disposition fixed contradiction present {label}")
    for label, forbidden in EXECUTION_PROFILE_FORBIDDEN.items():
        if forbidden in normalized_markdown:
            findings.append(f"execution-profile fixed contradiction present {label}")
    if "[parallel-producers.md](references/parallel-producers.md)" not in skill:
        findings.append("SKILL.md lacks direct progressive-disclosure route")
    if "The long-task drift checkpoint is owned only" not in skill:
        findings.append("SKILL.md lacks drift-checkpoint owner pointer")
    if "`/CER-auto` route selection, recheck, and safe transition are owned only by" not in skill:
        findings.append("SKILL.md lacks execution-profile owner pointer")
    if "that owner's single bounded-read requirement" not in re.sub(r"\s+", " ", skill):
        findings.append("SKILL.md lacks the selector single-read owner pointer")
    if "[Parallel Candidate Producers](parallel-producers.md)" not in core:
        findings.append("core-runtime role summary lacks owner pointer")
    if "CER has only the formal roles C, E1, R, and E2" not in core:
        findings.append("core-runtime formal role boundary is incomplete")
    fifth_role_patterns = (
        r"CER\s+has\s+only\s+the\s+formal\s+roles\s+C,\s*E1,\s*R,\s*E2,\s*P",
        r"(?:producer|candidate producer|P)\s+is\s+(?:a\s+)?formal\s+(?:CER\s+)?role",
        r"(?:fifth|5th)\s+(?:CER\s+)?formal\s+role",
    )
    for pattern in fifth_role_patterns:
        if re.search(pattern, all_markdown, flags=re.IGNORECASE):
            findings.append("a fifth formal CER role must not be declared")
            break
    if "## Parallel Candidate Producer Counterexamples" not in uat:
        findings.append("uat.md lacks bounded producer counterexamples")
    for label, required in UAT_REQUIREMENTS.items():
        if required not in uat:
            findings.append(f"uat.md missing producer counterexample {label}")
    for label, required in SENDABLE_PACKET_UAT_REQUIREMENTS.items():
        if required not in uat:
            findings.append(f"uat.md missing sendable-packet counterexample {label}")
    for label, required in MESSAGE_ID_UAT_REQUIREMENTS.items():
        if required not in uat:
            findings.append(f"uat.md missing message-identity counterexample {label}")
    for label, required in LIVING_BRIEF_UAT_REQUIREMENTS.items():
        if required not in uat:
            findings.append(f"uat.md missing living-brief counterexample {label}")
    for label, required in TRUTH_SOURCE_INTAKE_UAT_REQUIREMENTS.items():
        if required not in uat:
            findings.append(f"uat.md missing truth-source intake counterexample {label}")
    for label, required in CONTROLLER_CHALLENGE_UAT_REQUIREMENTS.items():
        if required not in texts["references/uat.md"]:
            findings.append(f"uat.md missing Controller long-task challenge {label}")
    if "## Outcome Anchor And Progress Scenarios" not in texts["references/uat.md"]:
        findings.append("uat.md lacks outcome-anchor progress scenarios")
    for label, required in OUTCOME_ANCHOR_UAT_REQUIREMENTS.items():
        if required not in uat:
            findings.append(f"uat.md missing outcome-anchor counterexample {label}")
    for label, required in DRIFT_CHECKPOINT_UAT_REQUIREMENTS.items():
        if required not in uat:
            findings.append(f"uat.md missing drift-checkpoint counterexample {label}")
    for label, required in RESULT_DISPOSITION_UAT_REQUIREMENTS.items():
        if required not in uat:
            findings.append(f"uat.md missing result-disposition counterexample {label}")
    if "## Adaptive Execution Profile Scenarios" not in texts["references/uat.md"]:
        findings.append("uat.md lacks adaptive execution profile scenarios")
    for label, required in EXECUTION_PROFILE_UAT_REQUIREMENTS.items():
        if required not in uat:
            findings.append(f"uat.md missing execution-profile scenario {label}")
    unexpected_failure_uat_match = re.search(
        r"^## Unexpected Failure And Scope-Exception Scenarios[ \t]*\n([\s\S]*?)(?=^## |\Z)",
        texts["references/uat.md"],
        re.MULTILINE,
    )
    if not unexpected_failure_uat_match:
        findings.append("uat.md lacks unexpected-failure scope-exception scenarios")
    else:
        unexpected_failure_uat = unexpected_failure_uat_match.group(1)
        for label, marker in UNEXPECTED_FAILURE_UAT_MARKERS.items():
            if all_markdown.count(marker) != 1 or marker not in unexpected_failure_uat:
                findings.append(f"unexpected-failure UAT marker invalid {label}")
    if "Parallel candidate producers are C's internal on-demand capability. They do not enter role columns" not in roadmap:
        findings.append("roadmap.md lacks display-only producer boundary")
    for index, required in enumerate(LIVING_BRIEF_ROADMAP_REQUIREMENTS):
        if required not in roadmap:
            findings.append(f"roadmap.md missing living-brief display requirement_{index}")
    for index, required in enumerate(OUTCOME_ANCHOR_ROADMAP_REQUIREMENTS):
        if required not in roadmap:
            findings.append(f"roadmap.md missing outcome-anchor display requirement_{index}")
    for relative in (
        "references/core-runtime.md",
        "references/roadmap.md",
        "references/uat.md",
        "references/parallel-producers.md",
    ):
        if "## Contents" not in texts[relative]:
            findings.append(f"long reference lacks concise table of contents: {relative}")
    if "{package_version}" not in roadmap or "{package_version}" not in uat:
        findings.append("card/UAT templates lack package_version placeholder")
    if "never display the placeholder itself" not in roadmap:
        findings.append("roadmap lacks mandatory package_version substitution boundary")
    if re.search(r"(?:formal roles|role columns).{0,40}(?:producer).{0,20}(?:enter|add|include)", roadmap, re.IGNORECASE):
        findings.append("roadmap adds producer to formal role display")
    return findings


def validate(root: Path) -> list[str]:
    root = root.resolve()
    actual_files = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }
    unexpected = sorted(actual_files - EXPECTED_FILES)
    if unexpected:
        return [f"unexpected package files: {unexpected}"]
    findings = validate_texts(root, read_texts(root))
    router_bytes = len((root / "SKILL.md").read_bytes())
    if router_bytes > MAX_ROUTER_BYTES:
        findings.append(
            f"SKILL.md concise-router budget exceeded: {router_bytes} > {MAX_ROUTER_BYTES} bytes"
        )
    return findings


def mutation_matrix(root: Path) -> tuple[int, list[str]]:
    baseline = read_texts(root)
    failures: list[str] = []
    cases: list[tuple[str, dict[str, str]]] = []

    def mutated(relative: str, old: str, new: str = "") -> dict[str, str]:
        candidate = copy.deepcopy(baseline)
        if old not in candidate[relative]:
            raise RuntimeError(f"self-test anchor missing: {relative}: {old}")
        candidate[relative] = candidate[relative].replace(old, new, 1)
        return candidate

    def mutated_all(relative: str, old: str, new: str = "") -> dict[str, str]:
        candidate = copy.deepcopy(baseline)
        if old not in candidate[relative]:
            raise RuntimeError(f"self-test anchor missing: {relative}: {old}")
        candidate[relative] = candidate[relative].replace(old, new)
        return candidate

    def mutated_fragment(relative: str, fragment: str) -> dict[str, str]:
        candidate = copy.deepcopy(baseline)
        pattern = re.escape(fragment).replace(r"\ ", r"\s+")
        changed, count = re.subn(pattern, "", candidate[relative])
        if count < 1:
            raise RuntimeError(f"self-test normalized anchor missing: {relative}: {fragment}")
        candidate[relative] = changed
        return candidate

    cases.append(("version_invalid", mutated("VERSION", baseline["VERSION"], "version\n")))
    cases.append(
        (
            "semver_outside_version",
            mutated(
                "references/roadmap.md",
                "# User Checkpoints And Roadmap",
                "# User Checkpoints And Roadmap " + ".".join(("9", "9", "9")),
            ),
        )
    )
    cases.append(("frontmatter_extra", mutated("SKILL.md", "name: cer-workflow-en", "name: cer-workflow-en\nmetadata: bad")))
    cases.append(
        (
            "extra_slash_command",
            mutated(
                "SKILL.md",
                "| `/CER-help`",
                "| `/CER-producer` | `producer` | forbidden |\n| `/CER-help`",
            ),
        )
    )
    cases.append(("owner_marker_duplicate", mutated("SKILL.md", "# CER Workflow", f"# CER Workflow\n{OWNER_MARKER}")))
    cases.append(("owner_marker_missing", mutated("references/parallel-producers.md", OWNER_MARKER)))
    cases.append(
        (
            "unexpected_failure_owner_marker_duplicate",
            mutated(
                "SKILL.md",
                "# CER Workflow",
                f"# CER Workflow\n{UNEXPECTED_FAILURE_OWNER_MARKER}",
            ),
        )
    )
    cases.append(
        (
            "unexpected_failure_owner_marker_missing",
            mutated("references/core-runtime.md", UNEXPECTED_FAILURE_OWNER_MARKER),
        )
    )
    wrong_section_marker = mutated(
        "references/core-runtime.md", UNEXPECTED_FAILURE_OWNER_MARKER
    )
    wrong_section_marker["references/core-runtime.md"] = wrong_section_marker[
        "references/core-runtime.md"
    ].replace(
        "## YAGNI And Stop",
        f"{UNEXPECTED_FAILURE_OWNER_MARKER}\n## YAGNI And Stop",
        1,
    )
    cases.append(("unexpected_failure_owner_marker_wrong_section", wrong_section_marker))
    cases.append(
        (
            "drift_checkpoint_owner_marker_duplicate",
            mutated(
                "SKILL.md",
                "# CER Workflow",
                f"# CER Workflow\n{DRIFT_CHECKPOINT_OWNER_MARKER}",
            ),
        )
    )
    cases.append(
        (
            "drift_checkpoint_owner_marker_missing",
            mutated("references/core-runtime.md", DRIFT_CHECKPOINT_OWNER_MARKER),
        )
    )
    drift_wrong_section = mutated(
        "references/core-runtime.md", DRIFT_CHECKPOINT_OWNER_MARKER
    )
    drift_wrong_section["references/core-runtime.md"] = drift_wrong_section[
        "references/core-runtime.md"
    ].replace(
        "## YAGNI And Stop",
        f"{DRIFT_CHECKPOINT_OWNER_MARKER}\n## YAGNI And Stop",
        1,
    )
    cases.append(("drift_checkpoint_owner_marker_wrong_section", drift_wrong_section))
    cases.append(
        (
            "result_disposition_owner_marker_duplicate",
            mutated(
                "SKILL.md",
                "# CER Workflow",
                f"# CER Workflow\n{RESULT_DISPOSITION_OWNER_MARKER}",
            ),
        )
    )
    cases.append(
        (
            "result_disposition_owner_marker_missing",
            mutated("references/core-runtime.md", RESULT_DISPOSITION_OWNER_MARKER),
        )
    )
    result_disposition_wrong_section = mutated(
        "references/core-runtime.md", RESULT_DISPOSITION_OWNER_MARKER
    )
    result_disposition_wrong_section["references/core-runtime.md"] = result_disposition_wrong_section[
        "references/core-runtime.md"
    ].replace(
        "## Self-Contained Dispatch",
        f"{RESULT_DISPOSITION_OWNER_MARKER}\n## Self-Contained Dispatch",
        1,
    )
    cases.append(("result_disposition_owner_marker_wrong_section", result_disposition_wrong_section))
    cases.append(
        (
            "execution_profile_owner_marker_duplicate",
            mutated(
                "SKILL.md",
                "# CER Workflow",
                f"# CER Workflow\n{EXECUTION_PROFILE_OWNER_MARKER}",
            ),
        )
    )
    cases.append(
        (
            "execution_profile_owner_marker_missing",
            mutated("references/core-runtime.md", EXECUTION_PROFILE_OWNER_MARKER),
        )
    )
    execution_profile_wrong_section = mutated(
        "references/core-runtime.md", EXECUTION_PROFILE_OWNER_MARKER
    )
    execution_profile_wrong_section["references/core-runtime.md"] = execution_profile_wrong_section[
        "references/core-runtime.md"
    ].replace(
        "## YAGNI And Stop",
        f"{EXECUTION_PROFILE_OWNER_MARKER}\n## YAGNI And Stop",
        1,
    )
    cases.append(("execution_profile_owner_marker_wrong_section", execution_profile_wrong_section))
    cases.append(
        (
            "implicit_invocation_true",
            mutated("agents/openai.yaml", "allow_implicit_invocation: false", "allow_implicit_invocation: true"),
        )
    )
    cases.append(("default_prompt_missing_skill", mutated("agents/openai.yaml", "$cer-workflow-en", "CER")))
    cases.append(
        (
            "default_prompt_unconditional_reviewer",
            mutated(
                "agents/openai.yaml",
                "with one writer for this work; create a fresh Reviewer in proportion to risk",
                "with one writer and a fresh Reviewer for this work",
            ),
        )
    )
    for label, counterexample in REVIEWER_PROPORTIONALITY_COUNTEREXAMPLES.items():
        cases.append(
            (
                f"default_prompt_{label}",
                mutated(
                    "agents/openai.yaml",
                    "without extra setup",
                    f"without extra setup; {counterexample}",
                ),
            )
        )
    cases.append(
        (
            "user_prompt_exposes_setup",
            mutated(
                "agents/openai.yaml",
                "without extra setup",
                "after configuring producer lanes, scratch roots, and hashes",
            ),
        )
    )
    cases.append(
        (
            "trigger_frontmatter_plain_close_reversed",
            mutated(
                "SKILL.md",
                "Plain start/work or close/finish messages are not CER triggers",
                "Plain close/finish messages are CER close triggers",
            ),
        )
    )
    cases.append(
        (
            "trigger_skill_auto_row_reversed",
            mutated(
                "SKILL.md",
                "no C exists before the route decision",
                "C exists before the route decision",
            ),
        )
    )
    cases.append(
        (
            "trigger_core_auto_row_reversed",
            mutated(
                "references/core-runtime.md",
                "no C exists before the route decision",
                "C exists before the route decision",
            ),
        )
    )
    cases.append(
        (
            "trigger_uat_install_auto_reversed",
            mutated(
                "references/uat.md",
                "no C exists before the route decision",
                "C exists before the route decision",
            ),
        )
    )
    cases.append(
        (
            "trigger_skill_start_row_reversed",
            mutated(
                "SKILL.md",
                "Plain start/work messages do not start CER",
                "Plain start/work messages start CER",
            ),
        )
    )
    cases.append(
        (
            "trigger_skill_close_row_reversed",
            mutated(
                "SKILL.md",
                "Plain close/finish messages do not close CER",
                "Plain close/finish messages close CER",
            ),
        )
    )
    cases.append(
        (
            "trigger_core_start_row_reversed",
            mutated(
                "references/core-runtime.md",
                "Plain start/work messages do not start CER",
                "Plain start/work messages start CER",
            ),
        )
    )
    cases.append(
        (
            "trigger_core_close_row_reversed",
            mutated(
                "references/core-runtime.md",
                "Plain close/finish messages do not close CER",
                "Plain close/finish messages close CER",
            ),
        )
    )
    cases.append(
        (
            "trigger_core_startup_owner_reversed",
            mutated(
                "references/core-runtime.md",
                "Plain start/work messages belong to the target workspace's existing governance and are not CER triggers",
                "Plain start/work messages are CER triggers",
            ),
        )
    )
    cases.append(
        (
            "trigger_core_stop_owner_reversed",
            mutated(
                "references/core-runtime.md",
                "Plain close/finish messages belong to the target workspace's existing governance and do not map to CER stop or close",
                "Plain close/finish messages belong to CER and map to CER stop or close",
            ),
        )
    )
    cases.append(
        (
            "trigger_uat_install_start_reversed",
            mutated(
                "references/uat.md",
                "a plain start/work message does not",
                "a plain start/work message does",
            ),
        )
    )
    cases.append(
        (
            "trigger_uat_install_close_reversed",
            mutated(
                "references/uat.md",
                "a plain close/finish message does not close CER and does not map to `/CER-stop`",
                "a plain close/finish message closes CER and maps to `/CER-stop`",
            ),
        )
    )
    cases.append(
        (
            "trigger_uat_failure_condition_lost",
            mutated(
                "references/uat.md",
                "A plain start/work message starts CER, or a plain close/finish message triggers CER close/stop",
                "A plain start/work message does not start CER, and a plain close/finish message does not trigger CER close/stop",
            ),
        )
    )
    cases.append(
        (
            "unprovided_dependency",
            mutated("agents/openai.yaml", "policy:", "dependencies:\n  tools: []\npolicy:"),
        )
    )
    cases.append(
        (
            "missing_progressive_link",
            mutated_all(
                "SKILL.md",
                "[parallel-producers.md](references/parallel-producers.md)",
                "parallel producers",
            ),
        )
    )
    for label, fragment in OWNER_REQUIREMENTS.items():
        cases.append(
            (
                f"owner_missing_{label}",
                mutated_fragment("references/parallel-producers.md", fragment),
            )
        )
    for label, fragment in UAT_REQUIREMENTS.items():
        cases.append(
            (f"uat_missing_{label}", mutated_fragment("references/uat.md", fragment))
        )
    for label, fragment in UNEXPECTED_FAILURE_REQUIREMENTS.items():
        cases.append(
            (
                f"unexpected_failure_owner_missing_{label}",
                mutated_fragment("references/core-runtime.md", fragment),
            )
        )
    for label, fragment in DELIVERY_REQUIREMENTS.items():
        cases.append(
            (
                f"delivery_gate_missing_{label}",
                mutated_fragment("references/core-runtime.md", fragment),
            )
        )
    for label, fragment in DELIVERY_UAT_REQUIREMENTS.items():
        cases.append(
            (
                f"delivery_uat_missing_{label}",
                mutated_fragment("references/uat.md", fragment),
            )
        )
    for label, fragment in TRUTH_SOURCE_INTAKE_REQUIREMENTS.items():
        cases.append(
            (
                f"truth_source_intake_owner_missing_{label}",
                mutated_fragment("references/core-runtime.md", fragment),
            )
        )
    for label, fragment in DRIFT_CHECKPOINT_REQUIREMENTS.items():
        cases.append(
            (
                f"drift_checkpoint_owner_missing_{label}",
                mutated_fragment("references/core-runtime.md", fragment),
            )
        )
    for label, fragment in RESULT_DISPOSITION_REQUIREMENTS.items():
        cases.append(
            (
                f"result_disposition_owner_missing_{label}",
                mutated_fragment("references/core-runtime.md", fragment),
            )
        )
    for label, fragment in EXECUTION_PROFILE_REQUIREMENTS.items():
        cases.append(
            (
                f"execution_profile_owner_missing_{label}",
                mutated_fragment("references/core-runtime.md", fragment),
            )
        )
    for label, fragment in SENDABLE_PACKET_REQUIREMENTS.items():
        cases.append(
            (
                f"sendable_packet_owner_missing_{label}",
                mutated_fragment("references/core-runtime.md", fragment),
            )
        )
    for index, fragment in enumerate(MESSAGE_ID_BOUNDARY_REQUIREMENTS):
        cases.append(
            (
                f"message_id_owner_missing_{index}",
                mutated_fragment("references/core-runtime.md", fragment),
            )
        )
    for index, fragment in enumerate(LIVING_BRIEF_REQUIREMENTS):
        cases.append(
            (
                f"living_brief_runtime_missing_{index}",
                mutated_fragment("references/core-runtime.md", fragment),
            )
        )
    for index, fragment in enumerate(LIVING_BRIEF_ROADMAP_REQUIREMENTS):
        cases.append(
            (
                f"living_brief_roadmap_missing_{index}",
                mutated_fragment("references/roadmap.md", fragment),
            )
        )
    for index, fragment in enumerate(OUTCOME_ANCHOR_REQUIREMENTS):
        cases.append(
            (
                f"outcome_anchor_runtime_missing_{index}",
                mutated_fragment("references/core-runtime.md", fragment),
            )
        )
    for index, fragment in enumerate(OUTCOME_ANCHOR_ROADMAP_REQUIREMENTS):
        cases.append(
            (
                f"outcome_anchor_roadmap_missing_{index}",
                mutated_fragment("references/roadmap.md", fragment),
            )
        )
    for label, fragment in SENDABLE_PACKET_UAT_REQUIREMENTS.items():
        cases.append(
            (
                f"sendable_packet_uat_missing_{label}",
                mutated_fragment("references/uat.md", fragment),
            )
        )
    for label, fragment in MESSAGE_ID_UAT_REQUIREMENTS.items():
        cases.append(
            (
                f"message_id_uat_missing_{label}",
                mutated_fragment("references/uat.md", fragment),
            )
        )
    for label, fragment in LIVING_BRIEF_UAT_REQUIREMENTS.items():
        cases.append(
            (
                f"living_brief_uat_missing_{label}",
                mutated_fragment("references/uat.md", fragment),
            )
        )
    for label, fragment in TRUTH_SOURCE_INTAKE_UAT_REQUIREMENTS.items():
        cases.append(
            (
                f"truth_source_intake_uat_missing_{label}",
                mutated_fragment("references/uat.md", fragment),
            )
        )
    for label, fragment in CONTROLLER_CHALLENGE_UAT_REQUIREMENTS.items():
        cases.append(
            (
                f"controller_challenge_uat_missing_{label}",
                mutated_fragment("references/uat.md", fragment),
            )
        )
    for label, fragment in OUTCOME_ANCHOR_UAT_REQUIREMENTS.items():
        cases.append(
            (
                f"outcome_anchor_uat_missing_{label}",
                mutated_fragment("references/uat.md", fragment),
            )
        )
    for label, fragment in DRIFT_CHECKPOINT_UAT_REQUIREMENTS.items():
        cases.append(
            (
                f"drift_checkpoint_uat_missing_{label}",
                mutated_fragment("references/uat.md", fragment),
            )
        )
    for label, fragment in RESULT_DISPOSITION_UAT_REQUIREMENTS.items():
        cases.append(
            (
                f"result_disposition_uat_missing_{label}",
                mutated_fragment("references/uat.md", fragment),
            )
        )
    for label, fragment in EXECUTION_PROFILE_UAT_REQUIREMENTS.items():
        cases.append(
            (
                f"execution_profile_uat_missing_{label}",
                mutated_fragment("references/uat.md", fragment),
            )
        )
    for label, marker in UNEXPECTED_FAILURE_UAT_MARKERS.items():
        cases.append(
            (
                f"unexpected_failure_uat_marker_missing_{label}",
                mutated("references/uat.md", marker),
            )
        )
    for label, contradiction in UNEXPECTED_FAILURE_FORBIDDEN.items():
        cases.append(
            (
                f"unexpected_failure_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## Execution Loop",
                    f"## Execution Loop\n\n{contradiction}.",
                ),
            )
        )
    for label, contradiction in SENDABLE_PACKET_FORBIDDEN.items():
        cases.append(
            (
                f"sendable_packet_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## Self-Contained Dispatch",
                    f"## Self-Contained Dispatch\n\n{contradiction}.",
                ),
            )
        )
    for label, contradiction in MESSAGE_ID_FORBIDDEN.items():
        cases.append(
            (
                f"message_id_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## Ambiguous Tool Outcomes, Role Reconciliation, And Batch Deduplication",
                    f"## Ambiguous Tool Outcomes, Role Reconciliation, And Batch Deduplication\n\n{contradiction}.",
                ),
            )
        )
    for label, contradiction in LIVING_BRIEF_FORBIDDEN.items():
        cases.append(
            (
                f"living_brief_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## Controller Preflight",
                    f"## Controller Preflight\n\n{contradiction}.",
                ),
            )
        )
    for label, contradiction in TRUTH_SOURCE_INTAKE_FORBIDDEN.items():
        cases.append(
            (
                f"truth_source_intake_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## Controller Preflight",
                    f"## Controller Preflight\n\n{contradiction}.",
                ),
            )
        )
    for label, contradiction in OUTCOME_ANCHOR_FORBIDDEN.items():
        cases.append(
            (
                f"outcome_anchor_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## Outcome Anchor And Progress Gate",
                    f"## Outcome Anchor And Progress Gate\n\n{contradiction}.",
                ),
            )
        )
    for label, contradiction in DRIFT_CHECKPOINT_FORBIDDEN.items():
        cases.append(
            (
                f"drift_checkpoint_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## Outcome Anchor And Progress Gate",
                    f"## Outcome Anchor And Progress Gate\n\n{contradiction}.",
                ),
            )
        )
    for label, contradiction in RESULT_DISPOSITION_FORBIDDEN.items():
        cases.append(
            (
                f"result_disposition_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## Outcome Anchor And Progress Gate",
                    f"## Outcome Anchor And Progress Gate\n\n{contradiction}.",
                ),
            )
        )
    for label, contradiction in EXECUTION_PROFILE_FORBIDDEN.items():
        cases.append(
            (
                f"execution_profile_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## Execution Profile Gate",
                    f"## Execution Profile Gate\n\n{contradiction}.",
                ),
            )
        )
    cases.append(
        (
            "roadmap_adds_producer_role",
            mutated(
                "references/roadmap.md",
                "do not enter role columns,",
                "enter role columns,",
            ),
        )
    )
    cases.append(
        (
            "fifth_formal_role",
            mutated(
                "references/core-runtime.md",
                "CER has only the formal roles C, E1, R, and E2",
                "CER has only the formal roles C, E1, R, E2, and P",
            ),
        )
    )

    for name, candidate in cases:
        if not validate_texts(root, candidate):
            failures.append(name)
    return len(cases), failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the CER skill package")
    parser.add_argument("root", nargs="?", default=".", help="CER skill root")
    parser.add_argument("--self-test", action="store_true", help="run in-memory mutation matrix")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings = validate(root)
    if findings:
        for finding in findings:
            print(f"FAIL: {finding}")
        print(f"status: failed ({len(findings)} findings)")
        return 1
    print("status: passed")
    print(f"version: {(root / 'VERSION').read_text(encoding='utf-8-sig').strip()}")
    print(f"files: {len(EXPECTED_FILES)}")
    if args.self_test:
        count, failures = mutation_matrix(root)
        print(f"mutation_cases: {count}")
        if failures:
            print(f"FAIL: mutation false-green: {failures}")
            return 1
        print("mutation_status: passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
