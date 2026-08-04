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
EXPECTED_DEFAULT_PROMPT = (
    "Use $cer-workflow-en with one writer for this work; create a fresh Reviewer in "
    "proportion to risk, and accelerate internally when useful without extra setup."
)
FORMAL_COMMANDS = {
    "/CER-start",
    "/CER-stop",
    "/CER-close",
    "/CER-status",
    "/CER-help",
}

EN_TRIGGER_MATRIX_EXPECTATIONS = {
    "frontmatter": (
        "Use only for explicit CER-qualified commands or equivalent meaning",
        "Plain start/work or close/finish messages are not CER triggers",
    ),
    "start_row": ("Plain start/work messages do not start CER",),
    "close_row": ("Plain close/finish messages do not close CER",),
    "startup_owner": ("Plain start/work messages belong to the target workspace's existing governance and are not CER triggers",),
    "stop_owner": ("Plain close/finish messages belong to the target workspace's existing governance and do not map to CER stop or close",),
    "uat_install_start": (
        "`/CER-start` and `Start CER` trigger CER",
        "a plain start/work message does not",
    ),
    "uat_install_close": (
        "`/CER-close` and `Close CER` trigger CER close",
        "a plain close/finish message does not close CER and does not map to `/CER-stop`",
    ),
    "uat_failure": ("A plain start/work message starts CER, or a plain close/finish message triggers CER close/stop",),
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
    "relative_identity": "A formal dispatch uses relative wording such as `same E1`, `the E1 above`, or `next sequence`",
    "hostid_hard_required": "Controller still hard-requires `hostId`",
    "hostid_inferred": "derives hostId from `local`, title, sessionId, threadId shape, or an error message",
    "sessionid_replaces_threadid": "A formal dispatch uses sessionId instead of threadId as the formal dispatch coordinate",
    "review_manifest_missing": "R dispatch lacks actual `candidateIdentity`, `candidateManifest`, or candidate delivery evidence",
}

SENDABLE_PACKET_FORBIDDEN = {
    "placeholder_allowed": "A sendable dispatch may retain `<...>` placeholders",
    "relative_identity_allowed": "`same E1`, `the E1 above`, or `next sequence` may be used as formal dispatch identity",
    "hostid_always_required": "Every real dispatch must include `hostId` even when the active tool schema requires only `threadId`",
    "sessionid_infers_hostid": "hostId may be derived from sessionId, title, `local`, or an error message before continuing",
    "sessionid_replaces_threadid": "sessionId may replace threadId as formal dispatch coordinate",
    "review_manifest_optional": "R dispatch may omit `candidateManifest`",
    "draft_pass": "`draft_packet` may self-rate as sendable",
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
        findings.append(f"slash commands must remain exactly five: {sorted(skill_commands)}")

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
    for label, forbidden in SENDABLE_PACKET_FORBIDDEN.items():
        if forbidden in normalized_markdown:
            findings.append(f"sendable-packet fixed contradiction present {label}")
    if "[parallel-producers.md](references/parallel-producers.md)" not in skill:
        findings.append("SKILL.md lacks direct progressive-disclosure route")
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
    return validate_texts(root, read_texts(root))


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
