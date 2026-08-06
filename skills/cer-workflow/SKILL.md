---
name: cer-workflow
description: "執行獨立的 CER 多代理工作法，適用於長期、多批、容易中斷，或需要 Controller、同一持久 Executor、按風險建立 fresh Reviewer、自足跨 task 派工、主動回傳、停點、分階段交付及按需平行候選分析的工作。只在使用者明確帶 CER 的指令或同等語意時使用，例如 /CER-start、CER 啟動、CER 開始、CER 開工、/CER-stop、/CER-close、CER 收工、CER 關閉、關閉 CER，或明示需要 CER 角色及閉環執行。單獨「開工／收工」不是 CER 觸發。本 Skill 不規定項目文件。"
---

# CER 工作法

CER Core v1 是只供 Codex 使用、可獨立運行的工作法。Claude Code 需要另一個
尚未提供的 Skill；不得把本 Skill 或本 repo 說成目前支援 Claude Code。

## 啟動

使用者明示 `/CER-start <總任務、限制、優先序>`、`CER 啟動：...`、`CER 開始：...`、`CER 開工：...` 或同等帶 CER 的語意時：

1. 接受 `/CER-start` 前，完整讀取 [core-runtime.md](references/core-runtime.md) 及
   [roadmap.md](references/roadmap.md)。
2. 處理 `/CER-close` 時，只讀取 `core-runtime.md` 的「角色」、「小熊卡 package
   版本」及「獨立持久化與收工」，以及 `roadmap.md` 的「固定生命週期卡」。
3. 處理 `/CER-stop` 時，只讀取 `core-runtime.md` 的「角色」、「小熊卡 package
   版本」及「停用 CER」，以及 `roadmap.md` 的「固定生命週期卡」。其他小熊停點
   只讀取 `roadmap.md` 的相關段落。
4. 只有角色座標或終態證據不完整、互相矛盾，或目標專案另有要求時，才擴大
   讀取範圍；不得只因指令是 stop／close 而完整重讀全部 references。
5. CER 已啟動後，目標 `AGENTS.md` 明確路由的 Kit full closeout 或 governance
   bridge 語意，只讀取 `core-runtime.md` 的「自足派工」相應規則，不另行設計
   Kit 程序。
6. 只有執行安裝驗收或 fresh UAT 時，完整讀取 [uat.md](references/uat.md)。
7. C 要評估或使用平行候選生產者時，先完整讀取
   [parallel-producers.md](references/parallel-producers.md)；該檔是此能力的
   唯一完整規則 owner。

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
- 每次成功接受 `CER-start` 都先顯示 [roadmap.md](references/roadmap.md) 的固定開眼
  啟動卡；簡單單批任務也不例外。每次顯示任何小熊卡前，先讀本 Skill 根目錄
  `VERSION`；卡片必須按 roadmap 的獨立 fenced `text` code block 輸出。啟動
  受阻時顯示開眼紅色 blocker 卡，不得顯示閉眼成功卡。
- 正式 E／R 都必須是同一 Codex project 側欄可見、由官方 `create_thread`
  建立的獨立新 task/thread；不得用 inline sub-agent、fork 或 delegate 降級代替。
- 每輪 `CER-start` 建立全新 E1；同一輪後續批次持續復用該同一 E1 作唯一
  writer。E2 只在接管條件成立後另建新 task。
- Reviewer（R）只在高風險或 C 不能可靠反證時建立；每個 R 都必須是 fresh
  新 task、唯讀、有界，不可沿用舊 R。
- C 可依 [parallel-producers.md](references/parallel-producers.md) 按需使用
  inline 平行候選生產者。它不是正式角色，不得成為共享 workspace writer、
  代替 E／R、直接與 E1／R 通訊或產生正式 ready/result；不適合平行時生產者
  數量為零，由 C 串行分析。
- 每個跨 task 批次必須 self-contained；E1／R 不會自動繼承 C 的對話。
- 新建或識別 task／thread 時，Controller 使用 `🚀 C:01｜...` 形式的可見標題或等價首行標籤；E1／R／E2 仍使用 `E1:01｜...`、`R1:01｜...`、`R2:01｜...` 或 `E2:01｜...`，不加 rocket；同輪共用同一短 cycle 編號，下一輪用新編號。`00` 只可標示 cycle numbering 規則生效前已開始且無法可靠回推原編號的 legacy/migration cycle；新 cycle 必須用 `01` 以上，不顯示問號 cycle label。cycle 編號只供側欄辨識，不是唯一性證據；完整 threadId 仍是權威。回傳目標必須包含可核實 threadId 或平台等價座標；sessionId 只在當前工具 schema／receipt 明示需要／提供時記錄，不可代替 threadId 或推導 hostId。
- 建立 task 或開始驗證前，先以實際工具證明身份來源、必要參數、發送路徑、接收者、threadId 或平台等價座標與裁決點。任一環缺失即停止該委派架構；不得以文件審閱、事後 thread read 或猜測代替通訊驗證。
- create／send 回報失敗、逾時或部分結果時，先標成 `outcome_unknown`，不得當成確定失敗而立即重試。C 只做一次有界權威對帳；重複角色在選定唯一 task 並證明其餘已零寫入停止前，不得接收正式工作。若任何重複 writer 可能已工作或寫入，先阻塞並恢復唯一 writer 狀態。
- 每個正式批次使用穩定 `batchId`、單調 `batchSeq` 及不可變 `payloadDigest`；所有控制、回執與結果訊息使用穩定 `messageId`。接收者按已登記、執行中、結果已備妥、結果已接納或狀態不明去重與恢復；相同身份但不同內容一律阻塞，舊批次未取消、終結或恢復前不得開始新修訂。
- 自適應批次加速是預設排程策略，不是 Turbo 模式或額外 slash command；它只在通訊、批次生命週期、唯一 writer、證據有效性及任務契約均可判定時運作，任一狀態不明即自行停用，不降低安全、獨立審閱或驗收要求。
- E1／R 以 direct-push 主動交付結果；C 不得在派工後自動使用 `wait_threads`／`read_thread` 當接收機制。只有已聲明某個 direct-push 狀態轉移、已知唯一 thread 與目前 cursor，且平台不會自動喚醒 idle C 時，C 才可對該轉移啟動一次有界事件等待作喚醒；`BATCH_RECEIVED` 與最終結果是兩個不同轉移。不得把 wait snapshot、完成狀態或 commentary 當 ready/result 證據；同一轉移逾時後，只有完成對帳及唯一一次同 `messageId` 受控重送，才可再用一次恢復等待，之後必須阻塞，不得輪詢或背景監察。
- C 不寫 workspace；E1 的成果只是候選，只有 C 可按實際讀回裁決接納。
- 尊重目標專案已有真源、計劃與進度；CER 不建立固定項目文件，也不把自己的角色狀態冒充專案計劃。
- 真源攝取門檻只由 [core-runtime.md](references/core-runtime.md) 的 Controller preflight 擁有；入口摘要不重寫該規則。
- 長任務防失焦檢查點只由 [core-runtime.md](references/core-runtime.md) 的成果錨定與進展閘擁有；入口摘要不重寫該規則。
- 面對醫療、法律、金融、投資、政策、學術、商業、設計、營運等知識性複雜任務時，C 必須先界定任務所需的知識底座；E1 只在該範圍內執行，R 依同一範圍做獨立反證。
- 重大方向、交付形狀或成本未裁決時必須在使用者主 task 停點；執行後在合理階段交付可觀察成果。
- 角色、批次、Reviewer、停點與驗收按風險比例化；不得以更多代理、文件、審閱或治理儀式代替清晰目標及可驗收條件。E／R 或任務支線的新增必要性與收斂判斷只由 [core-runtime.md](references/core-runtime.md) 的「YAGNI 與停止」定義。
- 模型與力度是能力、成本和使用者限制的選擇，不是 CER 固定版本 blocker。
- 同一 workspace 的一輪 `/CER-close` 完成後，該輪 C／E／R task 只可保留作
  歷史，整組不可接收下一輪工作。下一輪必須由新 task 通過唯一 C 閘門，建立
  全新 E1，且所有 R 都 fresh；不得復用上一輪任何 E／R 座標。
- `/CER-close` 成功時，先證明 `writer closed` 與必要讀回，再用官方 title 工具自動
  把該輪可核實 C／E／R title 的 cycle 編號加 `✓` 並讀回；rename 失敗只報
  `title sync warning`，不得冒充已改名，最後才顯示閉眼收尾卡。

## 版本邊界

本 Skill 只包含供 Codex 使用的 CER Core v1；`v1` 是工作流世代，不是目前安裝
package 版本。小熊卡的 package 版本只來自本 Skill 的 `VERSION`。每次 release
或 upgrade 必須先更新 `VERSION`；`skills` CLI 更新整個 Skill 後，卡片自然讀到
新版本。

根目錄 `01_CER工作法_人類概覽.md` 與 `02_CER工作法_AI執行協議.md` 是本來源專案的內部需求與驗收藍圖，和本 Skill 的執行面分開維護。Skill references 是實際操作規程；兩者以需求和驗收對齊，但互不擁有對方。

需要把模糊構思收斂成藍圖、需求、R&D、計劃及進度時，可另用
`$project-context-workflow`。它不是 CER 前置；CER 只讀取其已確認真源，不建立
第二套文件或重複共識關卡。
