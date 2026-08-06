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

ZH_TRIGGER_MATRIX_EXPECTATIONS = {
    "frontmatter": (
        "只在使用者明確帶 CER 的指令或同等語意時使用",
        "單獨「開工／收工」不是 CER 觸發",
    ),
    "start_row": ("單獨 `開工` 不啟動 CER",),
    "close_row": ("單獨 `收工` 不觸發 CER close",),
    "startup_owner": ("單獨 `開工` 屬於目標 workspace 既有治理，不是 CER trigger",),
    "stop_owner": ("單獨 `收工` 屬於目標 workspace 既有治理，不映射為 CER stop 或 close",),
    "uat_install_start": (
        "`/CER-start`、`CER 啟動`、`CER 開始`、`CER 開工` 正常觸發 CER",
        "單獨 `開工` 不觸發 CER",
    ),
    "uat_install_close": (
        "`/CER-close`、`CER 收工`、`CER 關閉`、`關閉 CER` 正常觸發 CER close",
        "單獨 `收工` 不觸發 CER close，也不映射為 `/CER-stop`",
    ),
    "uat_failure": ("單獨 `開工` 啟動 CER，或單獨 `收工` 觸發 CER close／stop",),
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
    "auto_wait_threads_forbidden": "派工後自動使用 `wait_threads`／`read_thread` 當接收機制",
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

DELIVERY_REQUIREMENTS = {
    "no_auto_wait": "不得在派工、建 task 或送訊後自動使用 `wait_threads`／`read_thread` 當接收機制",
    "wait_preconditions": "只有已聲明某個 direct-push 狀態轉移、該次唯一 threadId／平台等價座標及目前 cursor 已知",
    "no_automatic_waiting": "禁止自動 waiting、反覆 waiting",
}

TRUTH_SOURCE_INTAKE_REQUIREMENTS = {
    "sole_owner": "真源攝取門檻屬於 Controller preflight 的唯一 owner",
    "four_questions": "誰擁有；誰實際使用；如何生效；甚麼反例能推翻",
    "owner_definition": "`誰擁有` 指使用者裁決、專案真源、規則、檔案或外部權威的來源錨點",
    "consumer_definition": "`誰實際使用` 指 E1、R、交付物、安裝面、公開面、後續批次或使用者流程如何消費該條件",
    "effect_definition": "`如何生效` 指它如何改變本批派工、交付內容、權限、驗收或成果判定",
    "disproof_definition": "`甚麼反例能推翻` 指哪個讀回、測試、Reviewer 問題或反例會令本批不能算成功",
    "missing_is_critical": "任一項答不到，或答案依賴未讀的必要真源，該條件就是 `關鍵缺失`",
    "no_dispatch": "C 不得派正式實作批次，只能做必要唯讀診斷、收窄驗收範圍，或用 `🟡 使用者裁決` 停問",
    "not_full_audit": "不得把此門檻擴成預設全文讀取、全 repo 審查或固定 Full Audit",
}

TRUTH_SOURCE_INTAKE_UAT_REQUIREMENTS = {
    "four_questions_pass": "非簡單正式實作批次在派工前，C 能逐項回答真源攝取四問",
    "missing_blocks": "C 答不到真源攝取四問任一項",
    "missing_still_dispatches": "非簡單正式實作批次未回答誰擁有、誰實際使用、如何生效、甚麼反例能推翻，C 仍建立／復用 E1 或派實作批次",
    "overwide_gate": "C 把真源攝取門檻擴成預設全文讀取、全 repo 審查、固定 Full Audit、第二份規則 owner 或固定表格流程",
}

TRUTH_SOURCE_INTAKE_FORBIDDEN = {
    "missing_four_questions_dispatch": "未回答誰擁有、誰實際使用、如何生效、甚麼反例能推翻時，C 仍可派正式實作批次",
    "full_ingestion_required": "真源攝取門檻要求預設全文讀取、全 repo 審查或固定 Full Audit",
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

SENDABLE_PACKET_REQUIREMENTS = {
    "draft_sendable_split": "`draft_packet`",
    "no_placeholders": "`sendable_packet` 不得保留 `<...>` 佔位符",
    "truth_intake_summary": "Controller preflight 已通過的真源攝取四問摘要：誰擁有、誰實際使用、如何生效、甚麼反例能推翻",
    "concrete_bindings": "正式派工必須填入實際 `threadId` 或平台等價座標、`returnTarget`、`messageId`、`batchId`、`batchSeq`、`payloadDigest`，以及當前工具 schema／receipt 明示必需的路由座標",
    "sessionid_not_threadid": "sessionId 不可代替 threadId 作正式派工座標",
    "hostid_not_hard_required": "hostId 只在當前工具 schema 或 receipt 明示需要／提供時使用",
    "no_hostid_inference": "不得由 `local`、title、sessionId、threadId 形狀或錯誤訊息推導 hostId",
    "relative_identity_draft_only": "`同一 E1`／`上述 E1`／`下一個序號` 等相對說法只可作草稿",
    "review_manifest": "R 派工必須填入實際 `candidateIdentity`、`candidateManifest` 及候選 delivery evidence",
    "missing_blocks": "缺任一項即停在 `dispatch_blocked` 或 `decision_blocked`",
}

SENDABLE_PACKET_UAT_REQUIREMENTS = {
    "placeholder_self_pass": "正式 `sendable_packet` 仍保留 `<...>` 佔位符",
    "relative_identity": "正式派工用 `同一 E1`／`上述 E1`／`下一個序號` 等相對說法",
    "hostid_hard_required": "Controller 仍硬性要求 `hostId`",
    "hostid_inferred": "由 `local`、title、sessionId、threadId 形狀或錯誤訊息推導 hostId",
    "sessionid_replaces_threadid": "正式派工以 sessionId 代替 threadId 作正式派工座標",
    "review_manifest_missing": "R 派工缺實際 `candidateIdentity`、`candidateManifest` 或候選 delivery evidence",
}

SENDABLE_PACKET_FORBIDDEN = {
    "placeholder_allowed": "正式可送出的派工包可以保留 `<...>` 佔位符",
    "relative_identity_allowed": "`同一 E1`／`上述 E1`／`下一個序號` 可作為正式派工身份",
    "hostid_always_required": "正式派工一律必須填入 `hostId`，即使當前工具 schema 只要求 `threadId`",
    "sessionid_infers_hostid": "可由 sessionId、title、`local` 或錯誤訊息推導 hostId 後繼續",
    "sessionid_replaces_threadid": "sessionId 可代替 threadId 作正式派工座標",
    "review_manifest_optional": "R 派工可以省略 `candidateManifest`",
    "draft_pass": "`draft_packet` 可自評為可送出",
}

MESSAGE_ID_BOUNDARY_REQUIREMENTS = (
    "`messageId` 只是 CER 訊息層的識別、去重及追蹤欄位",
    "不是 Codex 執行指令、App Server `method`、JSON-RPC request `id`、`threadId`、`sessionId`、idempotency key 或授權",
    "未經實際工具呼叫及工具結果／可核實送達證據",
    "只有 `messageId` 不算訊息已送達或工作已執行",
)

MESSAGE_ID_UAT_REQUIREMENTS = {
    "identity_not_command": "只在 prompt、派工包、摘要或自稱回執中放入 `messageId`，就把它當成已建立 thread、開始 turn、呼叫工具、觸發寫入或授權",
}

MESSAGE_ID_FORBIDDEN = {
    "messageid_starts_operation": "單獨 `messageId` 可以建立 thread、開始 turn 或呼叫工具",
    "messageid_is_authority": "`messageId` 本身就是授權或 idempotency key",
}

LIVING_BRIEF_REQUIREMENTS = (
    "C 維護一份活的任務簡報",
    "活的任務簡報不是新 workflow，也不建立固定項目文件",
    "已確認要求／排除、可安全推定、關鍵缺口、最新使用者回饋、本批凍結、下一個可觀察預覽或裁決點、與上一版相比改變了甚麼",
    "C 只凍結下一個可安全執行批次",
    "E1／R 派工使用最新活的任務簡報與本批凍結",
    "E1 只獲授權執行本批凍結內容",
    "R 依最新任務簡報、本批凍結、候選 identity 及 delivery evidence 驗收",
)

LIVING_BRIEF_ROADMAP_REQUIREMENTS = (
    "顯示活的任務簡報、本批凍結和下一個可觀察停點",
    "任何用戶可見的活的任務簡報都必須明示 `CER`",
    "不得以「Codex 任務簡報」",
    "CER 路線圖｜活簡報",
    "CER 活簡報：已確認=<...>｜安全推定=<...>｜待裁決=<...>",
    "CER 本批凍結：<只本批會做>",
    "CER 上次回饋／變更：<...／無>",
    "活的任務簡報也只由最高可用權威來源",
)

LIVING_BRIEF_UAT_REQUIREMENTS = {
    "fuzzy_start": "模糊但可開始的多批任務，C 建立活的任務簡報",
    "no_full_spec_first": "不要求使用者先寫完整規格",
    "not_project_context_prereq": "不把 `$project-context-workflow` 當成前置",
    "feedback_delta": "使用者看過中間成果後改方向或補限制時，C 先更新活的任務簡報和路線圖差異",
    "review_latest_brief": "R 驗收依最新任務簡報、本批凍結、候選 identity 及 delivery evidence",
}

LIVING_BRIEF_FORBIDDEN = {
    "new_workflow": "活的任務簡報是一個獨立新 workflow",
    "initial_prompt_full_freeze": "整輪初始 prompt 永遠是完整凍結規格",
    "e1_unfrozen_future": "E1 可自行實作未凍結後續批次",
    "r_initial_prompt_only": "R 只按最初 prompt 驗收",
}

OUTCOME_ANCHOR_REQUIREMENTS = (
    "不可由後續批次自行改寫的 `outcome_anchor`",
    "不可接受的替代成果",
    "`mainline_outcome`、`diagnostic`、`mechanism_improvement` 或 `governance_self_improvement`",
    "預期成果改善為零且不是必要條件的實作批次不得派出",
    "活動不等於成果",
    "只有 C 讀回並裁決某項使用者完成條件取得已接納差異",
    "同一失敗類別按共同根因、使用者後果、受影響完成條件和方法判定",
    "改名、換版本、換包裝",
    "連續兩次未解決後，C 不得派第三個同類修正版",
    "每批終態只可為已接納成果",
)

OUTCOME_ANCHOR_ROADMAP_REQUIREMENTS = (
    "`outcome_anchor` 的已接納成果差異",
    "不得以批次、task 或審閱",
    "CER 成果錨：未完成=<完成條件>｜已接納差異=<成果差異／無>",
    "CER 工作線：<mainline_outcome／diagnostic／mechanism_improvement／governance_self_improvement>",
)

OUTCOME_ANCHOR_UAT_REQUIREMENTS = {
    "anchor_fixed": "長期多批任務在首批前固定 `outcome_anchor`",
    "zero_delta_rejected": "預期成果改善為零且不是必要條件的實作批次被拒絕",
    "diagnostic_not_progress": "診斷批次可以執行並產生承接條件，但標為 `diagnostic`，不增加主線進度",
    "technical_pass_not_progress": "技術檢查、格式、檔案一致或審閱通過，但 `outcome_anchor` 沒有已接納成果差異時，不標記為成功進度",
    "third_retry_intercepted": "同一失敗類別連續兩次未解決後，第三次同類修正版被攔截",
    "rename_same_retry": "改名、換版本、換包裝或同方法重派仍被識別為同類重試",
    "reviewer_rejects_drift": "R 必須拒絕偏離原始成果、只有技術活動、反覆返工或用另一種交付形式代替使用者原要求的批次",
    "mechanism_not_mainline": "`mechanism_improvement` 或 `governance_self_improvement` 不污染主線進度",
    "adjacent_not_blocker": "相鄰改善失敗不會自動阻塞原任務",
    "simple_lightweight": "簡單、單步、低風險且終點唯一的任務仍可用短摘要和 C 讀回驗收",
    "completion_outcomes": "任務完成回報列已接納成果差異和未完成條件",
}

OUTCOME_ANCHOR_FORBIDDEN = {
    "zero_delta_dispatch": "預期成果改善為零的實作批次可以派出",
    "diagnostic_mainline": "診斷批次增加主線進度",
    "third_retry_allowed": "第三個同類修正版可以繼續派出",
    "activity_completion": "批次、task、Reviewer 或候選數量就是完成證據",
}

DRIFT_CHECKPOINT_REQUIREMENTS = {
    "sole_owner": "長期任務防失焦檢查點屬於本節唯一 owner",
    "no_new_monitor": "不另建監察角色、背景程序或固定表格",
    "resume_trigger": "resume／上下文轉換",
    "two_no_delta_trigger": "連續兩批沒有已接納成果差異",
    "same_failure_trigger": "同類失敗第二次",
    "adjacent_trigger": "E1／R 提出相鄰改向或替代交付",
    "user_change_trigger": "使用者改方向或補限制",
    "close_release_trigger": "close／release／重大交付前",
    "next_condition": "下一批是否仍改善 `outcome_anchor` 的未完成條件",
    "readable_delta": "成功後有甚麼可讀回成果差異",
    "mainline_replacement": "是否正在取代主線成果",
    "no_dispatch": "C 不得派正式實作批次",
    "allowed_exits": "只可改做診斷、收窄驗收、停問使用者、終止路線",
    "fresh_r_bounded": "風險足夠時建立 fresh R",
    "not_progress": "checkpoint、活的任務簡報或路線圖更新不計作成果進度",
    "no_monitoring": "不得觸發背景 monitoring、polling、自動 `wait_threads`、固定 R、固定 Full Audit",
    "simple_exempt": "簡單、單步、低風險且終點唯一的任務",
}

DRIFT_CHECKPOINT_UAT_REQUIREMENTS = {
    "generic_trigger": "長期、多批或容易受上下文污染的任務",
    "two_no_delta": "連續兩批沒有已接納成果差異",
    "same_failure": "同類失敗第二次",
    "adjacent_change": "E1／R 提出相鄰改向或替代交付",
    "next_condition": "下一批改善哪個 `outcome_anchor` 未完成條件",
    "not_progress": "drift checkpoint、活的任務簡報或路線圖更新不計作成果進度",
    "no_monitoring": "不觸發背景 monitoring、polling、自動 `wait_threads`、固定 R 或固定 Full Audit",
    "missing_checkpoint_dispatch": "連續兩批沒有已接納成果差異，C 未做 drift checkpoint 仍派主線實作批次",
    "adjacent_rewrites_mainline": "E1／R 提出相鄰改向、替代交付或範圍外 blocker 後，C 未分類是否取代主線成果便改寫下一批主線",
    "checkpoint_as_progress": "drift checkpoint、活的任務簡報或路線圖更新被計作成果進度",
    "checkpoint_triggers_monitoring": "drift checkpoint 觸發背景 monitoring、polling、自動 `wait_threads`、固定 R 或固定 Full Audit",
    "simple_forced": "簡單、單步、低風險且終點唯一的任務被迫執行 drift checkpoint",
}

DRIFT_CHECKPOINT_FORBIDDEN = {
    "background_monitor": "drift checkpoint 會啟動背景 monitoring",
    "automatic_wait": "drift checkpoint 可自動使用 `wait_threads`",
    "fixed_reviewer": "每次 drift checkpoint 都必須建立 R",
    "fixed_full_audit": "每次 drift checkpoint 都觸發 Full Audit",
    "progress_credit": "drift checkpoint 本身增加主線成果進度",
    "simple_required": "簡單單步任務必須執行 drift checkpoint",
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
        ZH_TRIGGER_MATRIX_EXPECTATIONS["frontmatter"],
        "SKILL.md frontmatter trigger boundary",
        findings,
    )
    for label, source in (
        ("SKILL.md /CER-start row", command_table_row(skill, "/CER-start")),
        ("core-runtime.md /CER-start row", command_table_row(core, "/CER-start")),
    ):
        assert_snippets_present(
            source,
            ZH_TRIGGER_MATRIX_EXPECTATIONS["start_row"],
            label,
            findings,
        )
    for label, source in (
        ("SKILL.md /CER-close row", command_table_row(skill, "/CER-close")),
        ("core-runtime.md /CER-close row", command_table_row(core, "/CER-close")),
    ):
        assert_snippets_present(
            source,
            ZH_TRIGGER_MATRIX_EXPECTATIONS["close_row"],
            label,
            findings,
        )
    assert_snippets_present(
        markdown_section(core, "## 啟動"),
        ZH_TRIGGER_MATRIX_EXPECTATIONS["startup_owner"],
        "core-runtime.md startup owner",
        findings,
    )
    assert_snippets_present(
        markdown_section(core, "## 停用 CER"),
        ZH_TRIGGER_MATRIX_EXPECTATIONS["stop_owner"],
        "core-runtime.md stop owner",
        findings,
    )
    install = markdown_section(uat, "## 安裝情景")
    assert_snippets_present(
        install,
        ZH_TRIGGER_MATRIX_EXPECTATIONS["uat_install_start"],
        "uat.md installation start matrix",
        findings,
    )
    assert_snippets_present(
        install,
        ZH_TRIGGER_MATRIX_EXPECTATIONS["uat_install_close"],
        "uat.md installation close matrix",
        findings,
    )
    assert_snippets_present(
        markdown_section(uat, "## 失敗條件"),
        ZH_TRIGGER_MATRIX_EXPECTATIONS["uat_failure"],
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
    if all_markdown.count(TRUTH_SOURCE_INTAKE_OWNER_MARKER) != 1:
        findings.append("truth-source intake owner marker must occur exactly once")
    if TRUTH_SOURCE_INTAKE_OWNER_MARKER not in texts["references/core-runtime.md"]:
        findings.append("truth-source intake owner marker is not in core-runtime.md")
    if all_markdown.count(DRIFT_CHECKPOINT_OWNER_MARKER) != 1:
        findings.append("drift checkpoint owner marker must occur exactly once")
    if DRIFT_CHECKPOINT_OWNER_MARKER not in texts["references/core-runtime.md"]:
        findings.append("drift checkpoint owner marker is not in core-runtime.md")

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
    core_normalized = re.sub(r"\s+", " ", core)
    preflight_match = re.search(
        r"^## Controller preflight[ \t]*\n([\s\S]*?)(?=^## 啟動|\Z)",
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
    outcome_anchor_match = re.search(
        r"^## 成果錨定與進展閘[ \t]*\n([\s\S]*?)(?=^## |\Z)",
        core,
        re.MULTILINE,
    )
    if not outcome_anchor_match:
        findings.append("core-runtime.md lacks the outcome-anchor progress owner section")
    else:
        outcome_anchor_owner = re.sub(r"\s+", " ", outcome_anchor_match.group(1))
        if DRIFT_CHECKPOINT_OWNER_MARKER not in outcome_anchor_owner:
            findings.append("drift checkpoint marker is outside outcome-anchor progress section")
        for label, required in DRIFT_CHECKPOINT_REQUIREMENTS.items():
            if required not in outcome_anchor_owner:
                findings.append(f"drift checkpoint owner missing {label}")
    self_contained_match = re.search(
        r"^## 自足派工[ \t]*\n([\s\S]*?)(?=^## |\Z)", core, re.MULTILINE
    )
    if not self_contained_match:
        findings.append("core-runtime.md lacks the self-contained dispatch section")
    else:
        self_contained_owner = re.sub(r"\s+", " ", self_contained_match.group(1))
    for label, required in SENDABLE_PACKET_REQUIREMENTS.items():
        if required not in self_contained_owner:
            findings.append(f"sendable-packet gate missing {label}")
    message_identity_match = re.search(
        r"^## 工具結果不明、角色對帳與批次去重[ \t]*\n([\s\S]*?)(?=^## |\Z)",
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
    if "[parallel-producers.md](references/parallel-producers.md)" not in skill:
        findings.append("SKILL.md lacks direct progressive-disclosure route")
    if "長任務防失焦檢查點只由" not in skill:
        findings.append("SKILL.md lacks drift-checkpoint owner pointer")
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
    if "## 成果錨定與進展情景" not in texts["references/uat.md"]:
        findings.append("uat.md lacks outcome-anchor progress scenarios")
    for label, required in OUTCOME_ANCHOR_UAT_REQUIREMENTS.items():
        if required not in uat:
            findings.append(f"uat.md missing outcome-anchor counterexample {label}")
    for label, required in DRIFT_CHECKPOINT_UAT_REQUIREMENTS.items():
        if required not in uat:
            findings.append(f"uat.md missing drift-checkpoint counterexample {label}")
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
            "drift_checkpoint_owner_marker_duplicate",
            mutated(
                "SKILL.md",
                "# CER 工作法",
                f"# CER 工作法\n{DRIFT_CHECKPOINT_OWNER_MARKER}",
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
        "## YAGNI 與停止",
        f"{DRIFT_CHECKPOINT_OWNER_MARKER}\n## YAGNI 與停止",
        1,
    )
    cases.append(("drift_checkpoint_owner_marker_wrong_section", drift_wrong_section))
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
            "trigger_frontmatter_plain_close_reversed",
            mutated(
                "SKILL.md",
                "單獨「開工／收工」不是 CER 觸發",
                "單獨「開工／收工」會觸發 CER close",
            ),
        )
    )
    cases.append(
        (
            "trigger_skill_start_row_reversed",
            mutated(
                "SKILL.md",
                "單獨 `開工` 不啟動 CER",
                "單獨 `開工` 啟動 CER",
            ),
        )
    )
    cases.append(
        (
            "trigger_skill_close_row_reversed",
            mutated(
                "SKILL.md",
                "單獨 `收工` 不觸發 CER close",
                "單獨 `收工` 觸發 CER close",
            ),
        )
    )
    cases.append(
        (
            "trigger_core_start_row_reversed",
            mutated(
                "references/core-runtime.md",
                "單獨 `開工` 不啟動 CER",
                "單獨 `開工` 啟動 CER",
            ),
        )
    )
    cases.append(
        (
            "trigger_core_close_row_reversed",
            mutated(
                "references/core-runtime.md",
                "單獨 `收工` 不觸發 CER close",
                "單獨 `收工` 觸發 CER close",
            ),
        )
    )
    cases.append(
        (
            "trigger_core_startup_owner_reversed",
            mutated(
                "references/core-runtime.md",
                "單獨 `開工` 屬於目標 workspace 既有治理，不是 CER trigger",
                "單獨 `開工` 屬於 CER trigger",
            ),
        )
    )
    cases.append(
        (
            "trigger_core_stop_owner_reversed",
            mutated(
                "references/core-runtime.md",
                "單獨 `收工` 屬於目標 workspace 既有治理，不映射為 CER stop 或 close",
                "單獨 `收工` 屬於 CER 指令，映射為 CER stop 或 close",
            ),
        )
    )
    cases.append(
        (
            "trigger_uat_install_start_reversed",
            mutated(
                "references/uat.md",
                "單獨 `開工` 不觸發 CER",
                "單獨 `開工` 觸發 CER",
            ),
        )
    )
    cases.append(
        (
            "trigger_uat_install_close_reversed",
            mutated(
                "references/uat.md",
                "單獨 `收工` 不觸發 CER close，也不映射為 `/CER-stop`",
                "單獨 `收工` 觸發 CER close，並映射為 `/CER-stop`",
            ),
        )
    )
    cases.append(
        (
            "trigger_uat_failure_condition_lost",
            mutated(
                "references/uat.md",
                "單獨 `開工` 啟動 CER，或單獨 `收工` 觸發 CER close／stop",
                "單獨 `開工` 不啟動 CER，且單獨 `收工` 不觸發 CER close／stop",
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
    for label, contradiction in SENDABLE_PACKET_FORBIDDEN.items():
        cases.append(
            (
                f"sendable_packet_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## 自足派工",
                    f"## 自足派工\n\n{contradiction}。",
                ),
            )
        )
    for label, contradiction in MESSAGE_ID_FORBIDDEN.items():
        cases.append(
            (
                f"message_id_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## 工具結果不明、角色對帳與批次去重",
                    f"## 工具結果不明、角色對帳與批次去重\n\n{contradiction}。",
                ),
            )
        )
    for label, contradiction in LIVING_BRIEF_FORBIDDEN.items():
        cases.append(
            (
                f"living_brief_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## Controller preflight",
                    f"## Controller preflight\n\n{contradiction}。",
                ),
            )
        )
    for label, contradiction in TRUTH_SOURCE_INTAKE_FORBIDDEN.items():
        cases.append(
            (
                f"truth_source_intake_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## Controller preflight",
                    f"## Controller preflight\n\n{contradiction}。",
                ),
            )
        )
    for label, contradiction in OUTCOME_ANCHOR_FORBIDDEN.items():
        cases.append(
            (
                f"outcome_anchor_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## 成果錨定與進展閘",
                    f"## 成果錨定與進展閘\n\n{contradiction}。",
                ),
            )
        )
    for label, contradiction in DRIFT_CHECKPOINT_FORBIDDEN.items():
        cases.append(
            (
                f"drift_checkpoint_contradiction_{label}",
                mutated(
                    "references/core-runtime.md",
                    "## 成果錨定與進展閘",
                    f"## 成果錨定與進展閘\n\n{contradiction}。",
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
