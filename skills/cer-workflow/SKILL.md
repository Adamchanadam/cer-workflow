---
name: cer-workflow
description: "Run the standalone CER multi-agent workflow for long-running, multi-batch, or interruption-prone work that needs a Controller, one persistent Executor, risk-based fresh Reviewers, self-contained cross-task delegation, direct return, checkpoints, and staged delivery. Use when the user says CER 工作法啟動, asks to install or use CER, or explicitly requests CER roles and closed-loop execution. It does not prescribe project documents or integrate with Agent Handoff Kit."
---

# CER 工作法

CER Core v1 是獨立運行的工作法。它不需要、也不操作 Agent Handoff Kit。

## 啟動

使用者明示 `CER 工作法啟動：<總任務、限制、優先序>` 時：

1. 完整讀取 [core-runtime.md](references/core-runtime.md)。
2. 顯示初始路線圖或四色停點時，完整讀取 [roadmap.md](references/roadmap.md)。
3. 只有執行安裝驗收或 fresh UAT 時，完整讀取 [uat.md](references/uat.md)。

## 不可破壞規則

- 由使用者手動開啟並輸入 CER 啟動訊息的 task 才是 Controller（C）。
- 同一任務只用一個持久、可見、可再次派工的 Executor（E1）作唯一 writer；不可用一次性臨時 subagent 代替。
- Reviewer（R）只在高風險或 C 不能可靠反證時 fresh、唯讀、有界建立。
- 每個跨 task 批次必須 self-contained；E1／R 不會自動繼承 C 的對話。
- 新建或識別 task／thread 時，使用 `C:`、`E1:`、`R1:`、`R2:` 或 `E2:` 開首的可見標題或等價首行標籤；回傳目標必須包含可核實 session／thread id 或平台等價座標。
- 建立 task 或開始驗證前，先以實際工具證明身份來源、必要參數、發送路徑、接收者、session／thread 座標與裁決點。任一環缺失即停止該委派架構；不得以文件審閱、事後 thread read 或猜測代替通訊驗證。
- create／fork／send／title 只部分成功但沒有 E1 direct-push ready/result 時，視為通訊鏈未成立；C 只可發重大阻礙，不得派實際批次或宣稱閉環成立。
- E1／R 以 direct-push 主動交付結果；C 不以 waiting、polling 或背景監聽發現成果。
- C 不寫 workspace；E1 的成果只是候選，只有 C 可按實際讀回裁決接納。
- 尊重目標專案已有真源、計劃與進度；CER 不建立固定項目文件，也不把自己的角色狀態冒充專案計劃。
- 面對醫療、法律、金融、投資、政策、學術、商業、設計、營運等知識性複雜任務時，C 必須先界定任務所需的知識底座；E1 只在該範圍內執行，R 依同一範圍做獨立反證。
- 重大方向、交付形狀或成本未裁決時必須在使用者主 task 停點；執行後在合理階段交付可觀察成果。
- 角色、批次、Reviewer、停點與驗收按風險比例化；不得以更多代理、文件、審閱或治理儀式代替清晰目標及可驗收條件。
- 模型與力度是能力、成本和使用者限制的選擇，不是 CER 固定版本 blocker。

## 版本邊界

本 Skill 只包含 CER Core v1。本 v1 不讀寫 Kit handoff、log、mirror 或 closeout，也不聲稱 Kit 開工／收工。若目標 workspace 的權威規則明示必須使用 Agent Handoff Kit，停止並說明 v1 不支援該整合；不得靜默繞過。

`02_CER工作法_AI執行協議.md` 是另一套 Markdown 交付面；其 v1 章節由本 Skill 核心 references 產生。不得把 Markdown 的 v1 規則與 Skill v1 規則手動改成互相打架。

需要把模糊構思收斂成藍圖、需求、R&D、計劃及進度時，可另用
`$project-context-workflow`。它不是 CER 前置；CER 只讀取其已確認真源，不建立
第二套文件或重複共識關卡。
