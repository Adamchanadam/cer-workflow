# CER 工作法

[English](README.en.md)

CER = Controller、Executor、Reviewer。

CER 把統籌、寫檔、驗收分到獨立 Codex task，再由 Controller 串成閉環。它適合長期、多批、容易中斷，或需要獨立檢查的重要工作。小任務可以繼續用普通單一對話。

使用者主要留在 Controller。只有方向、權限、成本、發布、重大問題或最終驗收需要你決定時，Controller 才回到你面前。

![CER 工作法示意圖：Controller、Executor 和 Reviewer 分別負責統籌、寫檔及驗收](assets/cer-workflow-infographic.png)

## Goal 與 CER：10 個實際分別

Goal 和 CER 都可以從簡短要求開始，也都容許你在途中補資料、改限制和查看進度。終點已清楚，希望 Codex 自主推進至完成，通常先用 Goal。若成品要看過中間版本才逐步收斂，或你想由 Controller 管理執行、停點和驗收，CER 會較合適。

CER 的工作方式較接近「人機共同開發」：Codex 負責做事，你在會改變成品的決定點參與。最初的要求不必寫成完整規格；Controller 會分清已確認內容、安全假設和關鍵缺口，重要缺口問清楚後才派工。

| # | 比較點 | Goal | CER |
|---:|---|---|---|
| 1 | 最初的要求 | `/goal` 的文字同時是首個要求和完成條件；方向仍模糊時，可先用 `/plan` 釐清。 | Controller 先分清已確認內容、安全假設和關鍵缺口；缺口會明顯改變成品時，先問清楚再派工。 |
| 2 | 推進方式 | Codex 持續朝同一 Goal 推進，適合較少介入的長任務。 | Controller 把工作拆成可驗收批次，讀回一批後再決定下一批。 |
| 3 | 中途回饋 | 可在同一對話用 `Steer` 改變當前工作、用 `Queue` 留待下一輪，亦可暫停或修改 Goal。 | 你把回饋留給 Controller；Controller 判斷受影響範圍、更新路線圖，再把新批次交回同一 Executor。 |
| 4 | 進度顯示 | ChatGPT 桌面版會顯示 Goal 進度列；你也可要求 Codex 整理目前進度。 | 長期或多階段任務使用頁內路線圖（inline roadmap），顯示目前階段、已接納成果、阻礙和下一個使用者停點。 |
| 5 | 預覽與停點 | 可隨時要求查看、解釋或調整；何時預覽通常由最初的要求或當下需要決定。 | 路線圖預先標出需要預覽或裁決的停點；方向、交付形狀或驗收改變時會顯示差異。 |
| 6 | 使用者在流程中的位置 | 你設定 Goal 並可隨時介入，Codex 自主選擇下一步；需要決定或批准時會停下來。 | 你主要留在 Controller 對話，按中間成果補需求或改方向；Controller 負責把決定傳到執行線。 |
| 7 | 對話與角色 | 主對話可自行工作，也可使用側欄可見的原生子代理；角色和交接方式按任務而定。 | 每輪固定由 C 統籌、同一 E1 寫檔；風險需要時才建立全新 Reviewer 做只讀驗收。 |
| 8 | 寫檔權責 | 主代理或獲授權的子代理都可能修改；平行工作須避免寫入同一來源。 | 同一輪只有 E1 寫檔，C 和 R 不寫，避免不同角色同時修改。 |
| 9 | 獨立驗收 | 可另行要求 review（例如 `/review`）或安排子代理檢查，但不是每個 Goal 的固定流程。 | 只有重要、高風險或需要獨立證據時才啟用全新 Reviewer；問題由 C 合併後交同一 E1 修正。 |
| 10 | 最合適的任務 | 終點穩定、完成條件可寫清楚，而且希望 Codex 連續完成。 | 成品要經過數次預覽才收斂，或你希望保留較強的人手控制、清楚分工和獨立驗收。 |

Goal 部分依 OpenAI 官方的 [Long-running work](https://learn.chatgpt.com/docs/long-running-work)、[Prompting](https://learn.chatgpt.com/docs/prompting) 和 [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) 整理。CER 部分以本儲存庫的 [Controller 前置檢查](skills/cer-workflow/references/core-runtime.md#controller-preflight)、[執行閉環](skills/cer-workflow/references/core-runtime.md#執行閉環) 和 [頁內路線圖](skills/cer-workflow/references/roadmap.md#兩種介面) 為準。

## 三個角色

**Controller（C）：統籌與裁決**
理解目標、限制和完成條件，安排工作，判斷結果；不修改專案檔案。

**Executor（E1）：執行與寫檔**
唯一修改檔案；按批次實作、測試、回傳候選成果與證據。同一輪持續使用同一 E1，避免多人同時寫檔。

**Reviewer（R1）：獨立驗收**
獨立 Codex task，只讀檢查、提出結論、不寫檔；只在重要、高風險或需要獨立驗證時啟用。

側欄裡的 `C:01`、`E1:01`、`R1:01` 代表同一輪 CER 的不同角色。

## 探索助手：加快 Controller 前期分析

CER 的正式角色仍然只有 C／E／R。中大型任務往往需要同時搜尋資料、比較方案、
整理介面構想或預先找出可能出錯的地方；若全部由 Controller 逐項處理，前期
準備便可能拖慢整個流程。

因此，Controller 可按需要啟動少量「探索助手」，讓它們同時查看和整理不同方向
的資料。探索助手屬於 C 的輔助能力，而不是第四個正式角色：它不修改專案、不
代替 Executor 或 Reviewer，也不能自行宣布工作完成。Controller 仍會親自核對
資料、處理不同答案及作最終決定，所以原有的寫檔和獨立驗收安排不會改變。

![CER 探索助手決策樹：C 先判斷，小任務由 C 自己分析，中大型任務才啟動探索助手；候選回到 C，由 E1 寫檔，需要時才由 R 只讀驗收](assets/cer-exploration-helper-architecture.png)

探索助手預設閒置。適合的是資料來源清楚、可以分頭核對，而且同時處理確實較省
時間的中大型任務；是否啟動由 Controller 自動判斷。完整判斷條件只在
[探索助手完整規則](skills/cer-workflow/references/parallel-producers.md#啟動資格)
定義，避免不同文件各自維護而出現差異。

簡單任務不使用探索助手。如果資料途中改變，只重做受影響的部分；如果助手無法
啟動、逾時或找不到所需資料，Controller 會自己繼續分析，不會令整個 CER 流程
無故停下。

在一次中型任務的實際測試中，兩項資料整理工作如果逐項完成，需要約 71 秒；
同時處理則只需約 43 秒，等待時間少約四成。期間 Controller 亦同時完成資料核對
和規則檢查。這顯示探索助手在合適的任務中確實能節省時間，但這只是一個測試
例子，不代表每個項目都會有相同提升。

## 一句 prompt 安裝或升級

把這句交給 Codex：

```text
請使用 skills CLI，為 Codex 安裝或升級繁體中文版 CER Skill：https://github.com/Adamchanadam/cer-workflow 中的 skills/cer-workflow。若既有安裝可由 CLI 管理，請升級；若尚未安裝，請安裝；若目標位置已有檔案但 CLI 無法確認可管理，請先停止並報告，不要覆寫或刪除。完成後請讀回安裝路徑、來源及 VERSION；安裝或升級只到此為止，不要啟動 CER，等我另行輸入 CER 指令。
```

## 開始使用

安裝後，以明確帶 CER 的語句啟動：

```text
CER 啟動：<你想完成的事、限制、優先順序>
```

或：

```text
/CER-start <你想完成的事、限制、優先順序>
```

單獨 `開工` 不會啟動 CER；它保留給你目前的工作方式。

## 操作指令

| 指令 | 自然語言 | 用途 |
|---|---|---|
| `/CER-start <任務、限制、優先順序>` | `CER 啟動：...`／`CER 開始：...`／`CER 開工：...` | 啟動 CER，由 Controller 統籌後續工作。 |
| `/CER-stop` | `停止 CER，改用普通單一對話繼續。` | 停用 CER，不再安排新的 Executor 或 Reviewer 工作；這不代表任務已完成。 |
| `/CER-close` | `CER 收工。`／`CER 關閉。`／`關閉 CER。` | 正式結束本輪 CER；整理成果、風險和未完成事項。 |
| `/CER-status` | `顯示 CER 狀態。` | 顯示目前進度、下一個停點和已知問題。 |
| `/CER-help` | `顯示 CER 指令。` | 顯示可用指令。 |

單獨 `收工` 不會觸發 CER close，也不會被當成 `/CER-stop`。

## CER 怎樣工作

1. 你把完整任務交給 Controller，包括目標、限制和優先順序。
2. Controller 確認完成條件、資料來源和停點，然後把實作交給 Executor。
3. Executor 修改檔案、測試，並把候選成果和證據回給 Controller。
4. 重要或高風險工作，Controller 會交給 Reviewer 做獨立只讀檢查。
5. Controller 合併問題、決定是否修正，最後把成果、風險和需要你決定的事交回來。

同一成因的問題會合併成一批交回同一個 Executor 修正；只有不同問題、新影響或新風險，才會擴大處理範圍。

CER 啟動時會先確認各個工作 task 能互相回傳訊息；若未能確認，會停止並告知，不會假裝已開始。

## 停用和收尾有甚麼分別

`/CER-stop` 是停用 CER，回到普通單一對話。它表示 Controller 不再安排新的 Executor 或 Reviewer 工作，不代表任務已完成。

`/CER-close` 是正式結束本輪 CER。Controller 會整理成果、風險和未完成事項，並確認 Executor 停止寫檔。收尾後，舊 C／E／R 只保留作歷史；下一輪會使用新的角色 task。

## 包含內容

- [`skills/cer-workflow/`](skills/cer-workflow/)：繁中 CER Skill
- [`skills/cer-workflow-en/`](skills/cer-workflow-en/)：英文 CER Skill
- [`RELEASE_NOTES.md`](RELEASE_NOTES.md)：繁中發布說明
- [`RELEASE_NOTES.en.md`](RELEASE_NOTES.en.md)：英文發布說明

本 repo 只提供公開、可安裝的 CER Skill 內容。
