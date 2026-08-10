---
name: cer-workflow
description: "執行獨立 CER 工作法，或用本地 /CER-auto 選最低足夠的 ordinary／Goal／CER-gated／blocked 路線。只在使用者明確帶 CER 的指令或同等語意時使用；適合長期、多批、易中斷、需要唯一 writer、fresh Reviewer、自足派工、持久化及按需平行候選分析的工作。單獨「開工／收工」不是 CER 觸發。本 Skill 不規定項目文件。"
---

# CER 工作法

CER Core v1 只供 Codex 使用。Claude Code 需要另一個尚未提供的 Skill；不得聲稱本
Skill 或本 repo 目前支援 Claude Code。

## 入口路由

1. 處理本地 `/CER-auto` 時，在任何 CER 身份成立前，只讀取
   [core-runtime.md](references/core-runtime.md) 的「執行強度閘門」及裁決所需的使用者
   要求與目標專案真源；路徑已知時按該 owner 的單次有界讀取要求載入。選 ordinary execution 或 Goal 後停止載入其他 CER references；選 CER-gated Goal/E1
   時只在升格點完整讀取 `core-runtime.md` 及 [roadmap.md](references/roadmap.md)，按現行
   CER gate 啟動；blocked 則報缺口並停止。Remote `/CER-auto` 首版不支援。
2. 接受 `/CER-start` 前，完整讀取 [core-runtime.md](references/core-runtime.md) 及
   [roadmap.md](references/roadmap.md)。
3. 處理 `/CER-close` 時，只讀取 `core-runtime.md` 的「角色」、「小熊卡 package 版本」及
   「獨立持久化與收工」，以及 `roadmap.md` 的「固定生命週期卡」。
4. 處理 `/CER-stop` 時，只讀取 `core-runtime.md` 的「角色」、「小熊卡 package 版本」及
   「停用 CER」，以及 `roadmap.md` 的「固定生命週期卡」；其他停點只讀相關段落。
5. 只有角色座標或終態證據不完整、互相矛盾，或目標專案另有要求時才擴大讀取；不得只因指令是 stop／close 而完整重讀全部 references。
6. CER 啟動後，目標 `AGENTS.md` 明確路由 Kit full closeout 或 governance bridge 時，只讀取 `core-runtime.md` 的「自足派工」相應規則，不另行設計 Kit 程序。
7. 只有安裝驗收或 fresh UAT 才完整讀取 [uat.md](references/uat.md)。
8. C 評估或使用平行候選生產者前，完整讀取
   [parallel-producers.md](references/parallel-producers.md)；該檔是此能力的唯一完整 owner。

## 操作指令

slash command 是文字別名；平台不支援時，直接貼上同一句仍有效。

| 指令 | 自然語言 | 效果 |
|---|---|---|
| `/CER-auto <任務、限制、優先序>` | `CER 自適應：...` | 本地 task 先選 ordinary execution、Goal、CER-gated Goal/E1 或 blocked；路線裁決前不成立 C。Remote 首版不支援。 |
| `/CER-start <任務、限制、優先序>` | `CER 啟動：...` | 啟動 CER；本地或明確 Remote 接收 task 可成為唯一 C。單獨 `開工` 不啟動 CER。 |
| `/CER-stop` | `停止 CER，改用單 thread 繼續。` | 按 runtime 收斂 active writer 後停用 CER。 |
| `/CER-close` | `CER 收工。`／`CER 關閉。` | 按 runtime 收尾並證明 writer closed。單獨 `收工` 不觸發 CER close。 |
| `/CER-status` | `顯示 CER 狀態。` | 只報 C 已知狀態、座標、停點及阻礙；不輪詢。 |
| `/CER-help` | `顯示 CER 指令。` | 顯示本表。 |

`/CER-auto` 任務寫法：用 `目標＋限制／不可做＋成功驗收＋權威來源／授權邊界`。需要例子時，按使用者情境生成，不固定行業：`/CER-auto 幫我比較/整理/修補 <你的資料或問題>；不要 <不可做的事>；成功條件是 <可驗收成果>；如要作正式決策、付款、發布或外部承諾，先停下做 CER gate。`

## 入口邊界

- 完整唯一 C 啟動閘門由 `core-runtime.md` 擁有：candidate `C_READY` 與發送方讀回仍不足夠；
  接收者實際收到 `C_ACCEPTED` 後才成為 active Controller（C）。
- 正式 E／R 必須在同一 Codex project 側欄可見並由官方 `create_thread` 建立，不得用 inline sub-agent、fork 或 delegate 降級代替。每輪 `CER-start` 建立全新 E1，同一輪後續批次持續復用該同一 E1；每個 R 都必須是 fresh 新 task。完整拓撲、唯一 writer、Reviewer、批次、direct-push、result disposition、authority promotion、persistence 及 close 規則只在 `core-runtime.md` 定義。
- 顯示標籤只作辨識：`🚀 C:01｜...`、`E1:01｜...`、`R1:01｜...`、`R2:01｜...`、
  `E2:01｜...`。`00` 只可標示無法可靠回推的 legacy cycle；新 cycle 必須用 `01` 以上，
  不顯示問號 cycle label。cycle 編號只供側欄辨識，完整 threadId 仍是權威；收尾改名失敗只報
  `title sync warning`。卡片文字及 `VERSION` 讀法由 `roadmap.md`／`core-runtime.md` 擁有。
- 真源攝取門檻只由 `core-runtime.md` 的 Controller preflight 擁有；`/CER-auto` 的路線選擇、重判及安全切換只由其「執行強度閘門」擁有；長任務防失焦檢查點只由其成果錨定與進展閘擁有。入口不重寫 profile、Reviewer、YAGNI 或停止規則。

## 版本與藍圖邊界

`v1` 是工作流世代，不是 package 版本；package 版本只來自本 Skill 同層的 `VERSION`。
根目錄 `01_CER工作法_人類概覽.md` 與 `02_CER工作法_AI執行協議.md` 是來源專案的內部需求與驗收藍圖；Skill references 是實際操作規程。兩者對齊但互不擁有，不在入口複製 runtime。
