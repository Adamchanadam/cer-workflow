---
name: cer-workflow
description: "執行獨立的 CER 多代理工作法，適用於長期、多批、容易中斷，或需要 Controller、同一持久 Executor、按風險建立 fresh Reviewer、自足跨 task 派工、主動回傳、停點及分階段交付的工作。只在使用者明確帶 CER 的指令或同等語意時使用，例如 /CER-start、CER 啟動、CER 開始、CER 開工、/CER-stop、/CER-close、CER 收工、CER 關閉、關閉 CER，或明示需要 CER 角色及閉環執行。單獨「開工／收工」不是 CER 觸發。本 Skill 不規定項目文件。"
---

# CER 工作法

CER Core v1 是獨立運行的工作法。

## 啟動

使用者明示 `/CER-start <總任務、限制、優先序>`、`CER 啟動：...`、`CER 開始：...`、`CER 開工：...` 或同等帶 CER 的語意時：

1. 完整讀取 [core-runtime.md](references/core-runtime.md)。
2. 顯示初始路線圖或四色停點時，完整讀取 [roadmap.md](references/roadmap.md)。
3. 只有執行安裝驗收或 fresh UAT 時，完整讀取 [uat.md](references/uat.md)。

## 操作指令

slash command 是文字別名。平台支援 slash、snippet 或 Snap 時，可登記成可搜尋指令；平台不支援時，使用者直接貼上同一句也有效。

| 指令 | 自然語言 | 效果 |
|---|---|---|
| `/CER-start <任務、限制、優先序>` | `CER 啟動：...`／`CER 開始：...`／`CER 開工：...` | 啟動 CER v1；本地或明確 Remote 接收 task 可成為唯一 C。單獨 `開工` 不啟動 CER。 |
| `/CER-stop` | `停止 CER，改用單 thread 繼續。` | 停用 CER，不再派新 E1/R；若 E1 正在寫入，先收斂到可判定狀態。 |
| `/CER-close` | `CER 收工。`／`CER 關閉。`／`關閉 CER。` | 完成 CER 收尾，讓同一 E1 回寫既有必要真源並標 writer closed。單獨 `收工` 不觸發 CER close。 |
| `/CER-status` | `顯示 CER 狀態。` | 只報告 C 已知狀態、角色座標、下一停點與阻礙；不輪詢。 |
| `/CER-help` | `顯示 CER 指令。` | 顯示本表。 |

## 不可破壞規則

- 本地 task 或明確 Remote 接收 task 必須通過 [core-runtime.md](references/core-runtime.md) 的完整唯一 C 啟動閘門。candidate `C_READY` 與發送方讀回仍不足夠；接收者實際收到 `C_ACCEPTED` 後才成為 active Controller（C）。
- 同一任務只用一個持久、可見、可再次派工的 Executor（E1）作唯一 writer；不可用一次性臨時 subagent 代替。
- Reviewer（R）只在高風險或 C 不能可靠反證時 fresh、唯讀、有界建立。
- 每個跨 task 批次必須 self-contained；E1／R 不會自動繼承 C 的對話。
- 新建或識別 task／thread 時，Controller 使用 `🚀 C:` 開首的可見標題或等價首行標籤；E1／R／E2 仍使用 `E1:`、`R1:`、`R2:` 或 `E2:`，不加 rocket；回傳目標必須包含可核實 session／thread id 或平台等價座標。
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

本 Skill 只包含 CER Core v1。

根目錄 `01_CER工作法_人類概覽.md` 與 `02_CER工作法_AI執行協議.md` 是本來源專案的內部需求與驗收藍圖，和本 Skill 的執行面分開維護。Skill references 是實際操作規程；兩者以需求和驗收對齊，但互不擁有對方。

需要把模糊構思收斂成藍圖、需求、R&D、計劃及進度時，可另用
`$project-context-workflow`。它不是 CER 前置；CER 只讀取其已確認真源，不建立
第二套文件或重複共識關卡。
