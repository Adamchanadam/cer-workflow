# CER 工作法

[English](README.en.md)

CER 工作法給長任務一個更穩定的跑法。

你把目標、限制和優先順序交給 `C:` Controller。C 先理解任務，安排 `E1:` Executor 做實際工作；遇到高風險位置，再找 `R1:` Reviewer 做獨立檢查。中途能自行處理的問題，由 C 和 E1 閉環處理。真正需要你裁決、補資料或驗收時，C 才回到你面前。

![CER 工作法原理圖](assets/cer-workflow-infographic.png)

## 一句 prompt 安裝

把這句交給你的 agent：

```text
請從 https://github.com/Adamchanadam/cer-workflow 安裝 cer-workflow skill，安裝後用 $cer-workflow 啟動。
```

不用找檔案、不用懂 Git。你的 agent 應該會把 `skills/cer-workflow` 安裝到它的 skills 資料夾，完成後告訴你。

## 開始使用

安裝後，用自然語言或 slash command 開始：

```text
CER 工作法啟動：<你想完成的事、限制、優先順序>
```

```text
/CER-start <你想完成的事、限制、優先順序>
```

例子：

```text
CER 工作法啟動：檢查這個 repo 的發佈準備，修好文件和驗證問題。不要推送，除非我明確批准。
```

## 操作指令

這些 slash command 是穩定文字別名。你的 AI terminal 支援 slash command、snippet 或 Snap 時，可以把它們存起來；不支援時，直接貼上也可以。

| 指令 | 自然語言 | 用途 |
|---|---|---|
| `/CER-start <任務、限制、優先順序>` | `CER 工作法啟動：...` | 啟動 CER。 |
| `/CER-stop` | `停止 CER，改用單 thread 繼續。` | 停用 CER，不再派新 E1/R。 |
| `/CER-close` | `CER 收工。` / `收工。` | 完成 CER 收尾，讓同一 E1 標 writer closed。 |
| `/CER-status` | `顯示 CER 狀態。` | 顯示已知狀態和下一停點，不輪詢。 |
| `/CER-help` | `顯示 CER 指令。` | 顯示可用指令。 |

## 和一條 thread 加 sub-agent 有甚麼分別

傳統做法通常是你在同一條 thread 裡一路帶路。AI 做一步，你看一步；它卡住時問你；你再判斷要不要開 sub-agent、要問甚麼、回來後要不要信。這種方式簡單，短任務很好用。

CER 把這些中途協調交給 C。C 會先證明任務之間能收發訊息，然後把自足任務交給同一個 E1。E1 完成後主動回傳給 C。C 讀回、判斷、需要時找 R1 反證，再把真正可用的成果或停點交給你。

好處：

- 你不用每一步替 AI 拆任務。
- AI 中途遇到一般問題，先由 C 自行判斷和處理。
- 回到你面前的通常是方向裁決、阻礙、階段成果或最終驗收。
- 長任務較不容易因中斷、上下文散掉或 sub-agent 回傳不清而失控。
- 專業任務會先界定知識底座，避免用一般常識硬答。

代價：

- 啟動比單 thread 慢。
- 平台必須能證明 task/thread 的身份、發送路徑和回傳座標。
- 只成功建立 thread、改 title 或單向 send 不夠；沒有 E1 的 `ready/result` 回傳，CER 會停下。
- 小任務通常不值得用 CER。
- C 是 AI 主控，不等於你放棄裁決權。重大方向、權限、成本、發布和驗收仍會回到你手上。

## 這個賣點真實成立嗎

大方向成立，但有一個前提：平台要支援可驗證的跨 task 回傳。

CER v1 的規則要求 C 在派工前先證明：

- 誰是 C、E1、R1。
- 任務會送到哪裡。
- E1 怎樣把 `ready` 和結果回傳給 C。
- C 在哪裡裁決。

任一環缺失，C 會停在紅色 blocker。這樣做不夠自動，但比較誠實；它避免 AI 把「我已發出 prompt」當成「工作閉環成立」。

## 可以隨時啟用或停用嗎

可以。

在專案中，你可以用 `CER 工作法啟動：...` 或 `/CER-start ...` 開始 CER。適合長任務、多批修補、發布、治理、研究和高風險改動。

你也可以停用 CER，回到普通單 thread 工作。做法很簡單，直接說：

```text
停止 CER，改用單 thread 繼續。
```

也可以用：

```text
/CER-stop
```

停用後，C 不再派新的 E1/R1 批次。已經有 E1 在寫入時，C 需要先確認 writer 停止或交付到可判定狀態，再回到單 thread，避免同一個 workspace 同時有兩邊寫。

如果你想完成 CER 收尾，用 `/CER-close` 或 `CER 收工。`。這會讓同一 E1 回寫既有必要真源並標 `writer closed`。

## 何時不需要 CER

以下情況直接用單 thread 更快：

- 一次性小修改
- 你已經知道要改哪一行
- 沒有跨 task、驗收或發布風險
- 你想親自逐步帶著 AI 做

## 包含內容

- `skills/cer-workflow/`：CER Core v1 skill
- `01_CER工作法_人類概覽.md`：人類概覽
- `02_CER工作法_AI執行協議.md`：給沒有 skill 環境使用的 Markdown 協議

## 目前版本

這個 repo 發布 CER Core v1。

v1 是 standalone 工作法，不寫 Agent Handoff Kit 檔案，也不做 Kit closeout。`02_CER工作法_AI執行協議.md` 內有 v2 appendix，讓讀者知道 Kit Adapter 的邊界；可安裝 skill 只包含 v1。
