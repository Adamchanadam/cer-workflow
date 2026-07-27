# CER 工作法

[English](README.en.md)

CER = Controller、Executor、Reviewer。

CER 把統籌、寫檔、驗收分到獨立 Codex task，再由 Controller 串成閉環。它適合長期、多批、容易中斷，或需要獨立檢查的重要工作。小任務可以繼續用普通單一對話。

使用者主要留在 Controller。只有方向、權限、成本、發布、重大問題或最終驗收需要你決定時，Controller 才回到你面前。

![CER 工作法示意圖：Controller、Executor 和 Reviewer 分別負責統籌、寫檔及驗收](assets/cer-workflow-infographic.png)

## 三個角色

**Controller（C）：統籌與裁決**
理解目標、限制和完成條件，安排工作，判斷結果；不修改專案檔案。

**Executor（E1）：執行與寫檔**
唯一修改檔案；按批次實作、測試、回傳候選成果與證據。同一輪持續使用同一 E1，避免多人同時寫檔。

**Reviewer（R1）：獨立驗收**
獨立 Codex task，只讀檢查、提出結論、不寫檔；只在重要、高風險或需要獨立驗證時啟用。

側欄裡的 `C:01`、`E1:01`、`R1:01` 代表同一輪 CER 的不同角色。

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

## 普通單一對話與 CER

| 普通單一對話 | CER |
|---|---|
| 同一個對話完成理解、修改和檢查。 | 統籌、寫檔和驗收分到獨立 Codex task。 |
| 適合一次性小修改。 | 適合長期、多批、容易中斷或重要工作。 |
| 對話變長後，容易失去主線。 | Controller 保持主線，分批收斂結果。 |
| 使用者常要追問、整理和接續上下文。 | 各角色主動把成果和問題回到 Controller。 |
| 檢查容易受同一段執行脈絡影響。 | Reviewer 可在獨立脈絡做只讀驗收。 |

CER 的價值不是增加角色，而是減少上下文污染、角色混亂和確認偏誤；使用者不必管理每一步。

## 停用和收尾有甚麼分別

`/CER-stop` 是停用 CER，回到普通單一對話。它表示 Controller 不再安排新的 Executor 或 Reviewer 工作，不代表任務已完成。

`/CER-close` 是正式結束本輪 CER。Controller 會整理成果、風險和未完成事項，並確認 Executor 停止寫檔。收尾後，舊 C／E／R 只保留作歷史；下一輪會使用新的角色 task。

## 包含內容

- [`skills/cer-workflow/`](skills/cer-workflow/)：繁中 CER Skill
- [`skills/cer-workflow-en/`](skills/cer-workflow-en/)：英文 CER Skill
- [`RELEASE_NOTES.md`](RELEASE_NOTES.md)：繁中發布說明
- [`RELEASE_NOTES.en.md`](RELEASE_NOTES.en.md)：英文發布說明

本 repo 只提供公開、可安裝的 CER Skill 內容。
