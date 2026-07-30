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
    "使用 $cer-workflow 以唯一 writer 執行這項工作；按風險建立 fresh Reviewer，"
    "必要時在內部自動加速，無需額外設定。"
)
FORMAL_COMMANDS = {
    "/CER-start",
    "/CER-stop",
    "/CER-close",
    "/CER-status",
    "/CER-help",
}

REVIEWER_PROPORTIONALITY_COUNTEREXAMPLES = {
    "simple_fixed_fresh_reviewer": "簡單任務也固定建立 fresh Reviewer",
    "every_simple_task_reviewer": "每個簡單任務均安排 Reviewer",
    "simple_task_fixed_r": "簡單任務亦固定建立 R",
    "reverse_low_risk_fresh_reviewer": "fresh Reviewer 預設用於所有低風險任務",
    "passive_simple_task_reviewer": "Reviewer 皆會被安排給簡單工作",
    "low_risk_independent_reviewer": "低風險任務總是由獨立審閱者覆核",
}

OWNER_REQUIREMENTS = {
    "formal_roles": "CER 正式角色只有 C、E1、R、E2",
    "not_fifth_role": "不是第五角色",
    "no_new_lifecycle": "不使用正式 title、cycle、ready、result、batch lifecycle 或 Reviewer 身份",
    "no_new_commands": "不得新增 slash command",
    "two_independent_lanes": "至少兩條工作線互不依賴，不需要彼此結果、共享可變狀態或固定執行次序",
    "frozen_input_version": "每條 lane 的輸入及來源身份已凍結",
    "concurrent_controller_work": "C 同期有不重複的關鍵分析、守門或裁決工作，不退化為候選整理員",
    "independently_verifiable_candidates": "每條候選可由 C 按權威來源獨立驗證",
    "material_time_saving": "預期淨省時明顯高於啟動、讀回、hash、去重及裁決成本",
    "available_execution_slots": "所需平行槽可用，且不會壓縮正式 E1 或 fresh R 的必要能力",
    "read_only": "`read_only`",
    "isolated_artifact": "`isolated_artifact`",
    "read_only_zero_write": "在任何位置都必須零寫入",
    "project_noncontainment": "與 target project 互不包含",
    "dangerous_roots": "不是磁碟根、使用者根、系統根",
    "link_boundary": "symlink、junction、Windows reparse point、mount",
    "lane_nonoverlap": "彼此不相等、互不為祖先",
    "actual_tool_permission_boundary": "實際工具權限只容許該 lane 的明示 root；不能以相對路徑、萬用字元、環境 fallback 或 producer 自選位置擴張",
    "lane_contract_label": "`lane_label`",
    "lane_contract_goal": "單一目標",
    "lane_contract_input": "輸入身份與版本、來源身份及可核實座標",
    "lane_contract_scope": "允許範圍與禁止範圍",
    "lane_contract_output": "預期候選輸出",
    "lane_contract_acceptance": "驗收方式",
    "lane_contract_stop": "停止條件",
    "scratch_root": "`scratch_root`",
    "candidate_claims": "`claims`",
    "candidate_unknowns": "`unknowns`",
    "verifiable_source_coordinates": "實際來源座標",
    "candidate_hash": "實際絕對路徑與 SHA-256",
    "controller_readback": "C 親自讀回",
    "rehash": "重算 SHA-256",
    "no_vote": "不得 投票",
    "merged_batch": "E1 只接收該 C 合流批次",
    "no_direct_e1": "不得直接使用 producer 原始通訊",
    "no_wait_poll": "C 不 wait、poll 或背景監察 producer",
    "late": "遲到候選",
    "input_drift": "輸入或來源漂移",
    "tamper": "hash drift、tamper",
    "out_of_bounds": "路徑越界",
    "producer_failure": "producer 建立失敗",
    "stop_close": "`/CER-stop` 與 `/CER-close` 不等待 producer",
    "serial_fallback": "`producer_count=0`",
    "user_simplicity": "使用者無須設定 producer",
    "material_only_report": "只報告會影響結果的成果、未知、 阻礙或風險",
}

UAT_REQUIREMENTS = {
    "default_prompt_risk_proportionate": "預設提示使用「按風險建立 fresh Reviewer」",
    "default_prompt_simple_task": "簡單任務不會因預設提示而強制建立 Reviewer",
    "normal_two_lanes": "兩條互不依賴 lane",
    "auto_idle": "`producer_count=0`",
    "no_subagent": "沒有 subagent 能力",
    "cost_fallback": "平行成本不划算",
    "read_only_write": "`read_only` lane 嘗試任何寫入",
    "root_boundary": "project 內或其祖先、磁碟根、使用者根、系統根",
    "link_boundary": "symlink、junction、reparse point、mount",
    "lane_overlap": "與另一 lane 相等／互為祖先",
    "partial_drift": "只淘汰相依候選",
    "source_conflict": "不按票數",
    "late_candidate": "候選遲到",
    "producer_failure": "producer 失敗",
    "artifact_tamper": "artifact hash tamper",
    "role_impersonation": "producer 冒充 E／R",
    "direct_to_e1": "直接送 E1",
    "unmerged_scratch": "E1 採用未合流 scratch",
    "project_write": "C／R／producer 寫 target project",
    "stop_close": "`/CER-stop` 或 `/CER-close` 不等待 producer",
    "no_lifecycle_identity": "不取得正式 title、cycle、ready、result、slash、lock、registry 或 run id",
    "roadmap_boundary": "roadmap 的角色欄和 lifecycle 卡仍只有正式角色",
}

UNEXPECTED_FAILURE_REQUIREMENTS = {
    "test_not_authority": "測試只產生證據，不增加修改權",
    "allowlist_not_semantics": "不代表 E1 可改變該檔案內其他 owner、權威來源或受保護語意",
    "gate_off": "不啟動本閘門",
    "caused": "可在本批修正",
    "preexisting": "只回報，不修",
    "unknown_or_boundary": "停止進一步寫入",
    "regression_boundary": "不會擴大 E1 的修補權",
    "controller_only": "只有 C 可重凍結契約，並用新的 `batchId`／`payloadDigest` 派發新批次來擴大範圍",
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
    "test_grants_authority": "測試失敗會增加 E1 的修改權",
    "allowlist_grants_semantics": "檔案在 allowlist 內即授權 E1 改變該檔案所有語意",
    "missing_baseline_guess": "沒有 baseline 時，E1 應猜測並修復",
    "executor_expands_scope": "E1 可自行擴大範圍，不需要 C 重凍結新批次",
    "controller_expands_without_new_identity": "C 可沿用舊 `batchId`／`payloadDigest` 擴大範圍",
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
    if not re.search(r'^name:\s*cer-workflow\s*$', match.group(1), re.MULTILINE):
        findings.append("SKILL.md name must be cer-workflow")
    if "明確帶 CER" not in match.group(1) or "按需平行候選" not in match.group(1):
        findings.append("SKILL.md description lacks explicit CER trigger or on-demand parallel capability")
    return findings


def openai_yaml_findings(text: str) -> list[str]:
    findings: list[str] = []
    required_lines = (
        'interface:',
        '  display_name: "CER 工作法"',
        '  short_description: "',
        '  default_prompt: "',
        'policy:',
        '  allow_implicit_invocation: false',
    )
    for required in required_lines:
        if required not in text:
            findings.append(f"agents/openai.yaml missing required shape: {required}")
    if "$cer-workflow" not in text:
        findings.append("agents/openai.yaml default_prompt must include $cer-workflow")
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
    if re.search(r"\b(?:producer|lane|scratch|hash)\b|平行候選生產者", text, re.IGNORECASE):
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
    if "## 探索助手自動調度" in all_markdown:
        findings.append("legacy exploration-helper owner section remains")

    skill = texts["SKILL.md"]
    core = texts["references/core-runtime.md"]
    uat = re.sub(r"\s+", " ", texts["references/uat.md"])
    roadmap = re.sub(r"\s+", " ", texts["references/roadmap.md"])
    unexpected_failure_match = re.search(
        r"^## 執行閉環[ \t]*\n([\s\S]*?)(?=^## |\Z)", core, re.MULTILINE
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
    for label, forbidden in UNEXPECTED_FAILURE_FORBIDDEN.items():
        if forbidden in normalized_markdown:
            findings.append(f"unexpected-failure fixed contradiction present {label}")
    if "[parallel-producers.md](references/parallel-producers.md)" not in skill:
        findings.append("SKILL.md lacks direct progressive-disclosure route")
    if "[平行候選生產者](parallel-producers.md)" not in core:
        findings.append("core-runtime role summary lacks owner pointer")
    if "CER 正式角色只有 C、E1、R、E2" not in core:
        findings.append("core-runtime formal role boundary is incomplete")
    fifth_role_patterns = (
        r"CER\s*正式角色只有\s*C、E1、R、E2、",
        r"(?:producer|生產者|候選生產者|P)\s*(?:是|為|屬於)\s*(?:CER\s*)?正式角色",
        r"(?:第五|第\s*5)\s*(?:個)?\s*(?:CER\s*)?正式角色",
    )
    for pattern in fifth_role_patterns:
        if re.search(pattern, all_markdown, flags=re.IGNORECASE):
            findings.append("a fifth formal CER role must not be declared")
            break
    if "## 平行候選生產者反證情景" not in uat:
        findings.append("uat.md lacks bounded producer counterexamples")
    for label, required in UAT_REQUIREMENTS.items():
        if required not in uat:
            findings.append(f"uat.md missing producer counterexample {label}")
    unexpected_failure_uat_match = re.search(
        r"^## 未預期失敗與範圍例外情景[ \t]*\n([\s\S]*?)(?=^## |\Z)",
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
    if "平行候選生產者是 C 的內部按需能力，不加入角色欄" not in roadmap:
        findings.append("roadmap.md lacks display-only producer boundary")
    for relative in (
        "references/core-runtime.md",
        "references/roadmap.md",
        "references/uat.md",
        "references/parallel-producers.md",
    ):
        if "## 目錄" not in texts[relative]:
            findings.append(f"long reference lacks concise table of contents: {relative}")
    if "{package_version}" not in roadmap or "{package_version}" not in uat:
        findings.append("card/UAT templates lack package_version placeholder")
    if "絕不可把佔位文字原樣顯示" not in roadmap:
        findings.append("roadmap lacks mandatory package_version substitution boundary")
    if re.search(r"(?:正式角色|角色欄).{0,40}(?:producer|生產者).{0,20}(?:加入|新增)", roadmap):
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
                "# 使用者停點與路線圖",
                "# 使用者停點與路線圖 " + ".".join(("9", "9", "9")),
            ),
        )
    )
    cases.append(("frontmatter_extra", mutated("SKILL.md", "name: cer-workflow", "name: cer-workflow\nmetadata: bad")))
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
    cases.append(("owner_marker_duplicate", mutated("SKILL.md", "# CER 工作法", f"# CER 工作法\n{OWNER_MARKER}")))
    cases.append(("owner_marker_missing", mutated("references/parallel-producers.md", OWNER_MARKER)))
    cases.append(
        (
            "unexpected_failure_owner_marker_duplicate",
            mutated(
                "SKILL.md",
                "# CER 工作法",
                f"# CER 工作法\n{UNEXPECTED_FAILURE_OWNER_MARKER}",
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
        "## YAGNI 與停止",
        f"{UNEXPECTED_FAILURE_OWNER_MARKER}\n## YAGNI 與停止",
        1,
    )
    cases.append(("unexpected_failure_owner_marker_wrong_section", wrong_section_marker))
    cases.append(
        (
            "implicit_invocation_true",
            mutated("agents/openai.yaml", "allow_implicit_invocation: false", "allow_implicit_invocation: true"),
        )
    )
    cases.append(("default_prompt_missing_skill", mutated("agents/openai.yaml", "$cer-workflow", "CER")))
    cases.append(
        (
            "default_prompt_unconditional_reviewer",
            mutated(
                "agents/openai.yaml",
                "以唯一 writer 執行這項工作；按風險建立 fresh Reviewer",
                "以唯一 writer 及 fresh Reviewer 執行這項工作",
            ),
        )
    )
    for label, counterexample in REVIEWER_PROPORTIONALITY_COUNTEREXAMPLES.items():
        cases.append(
            (
                f"default_prompt_{label}",
                mutated(
                    "agents/openai.yaml",
                    "無需額外設定",
                    f"無需額外設定；{counterexample}",
                ),
            )
        )
    cases.append(
        (
            "user_prompt_exposes_setup",
            mutated(
                "agents/openai.yaml",
                "無需額外設定",
                "請設定 producer lane、scratch root 及 hash",
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
                    "## 執行閉環",
                    f"## 執行閉環\n\n{contradiction}。",
                ),
            )
        )
    cases.append(
        (
            "roadmap_adds_producer_role",
            mutated(
                "references/roadmap.md",
                "不加入角色欄、生命週期卡",
                "加入角色欄、生命週期卡",
            ),
        )
    )
    cases.append(
        (
            "fifth_formal_role",
            mutated(
                "references/core-runtime.md",
                "CER 正式角色只有 C、E1、R、E2",
                "CER 正式角色只有 C、E1、R、E2、P",
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
