# CER 工作法

[English](README.en.md)

CER 工作法讓長期、多批或高風險的 AI 工作有清楚分工、唯一 writer 和可核實的回傳閉環。

你把目標、限制和優先順序交給 `🚀 C:` Controller。C 先釐清任務和驗收，再把實際工作交給同一個持久 `E1:` Executor；只有風險需要時，才建立 fresh `R1:` Reviewer 獨立反證。真正需要方向裁決、補資料、處理阻礙或驗收時，C 才回到你面前。

![CER 工作法原理圖](assets/cer-workflow-infographic.png)

## 一句 prompt 安裝或升級

把這句交給 Codex：

```text
請為 Codex 安裝或升級繁中 CER Skill；只處理 skills/cer-workflow，不要安裝其他語言或其他 agent 版本。使用 `skills` CLI，並以其上游文件為準：
1. 先執行 `npx skills ls -g -a codex`，並讀回實際全域安裝路徑、來源及可用的 `skills` CLI metadata。
2. 如 `cer-workflow` 已被 `skills` CLI 辨識，執行：npx skills update cer-workflow --global --yes
3. 如 `cer-workflow` 未被辨識且沒有目標檔案衝突，執行：npx skills add Adamchanadam/cer-workflow --skill cer-workflow --agent codex --global --yes
4. 如目標路徑已有檔案但 `skills` CLI 不辨識或不能管理，禁止自動覆寫、刪除或以 --yes 靜默遷移；先報告實際路徑、來源證據、現況及遷移影響，等我明確確認。
5. 完成後讀回來源 URL、skill path、已安裝 `VERSION` 及安裝狀態。
6. 不要自動啟動 CER；等我輸入明確 CER 指令。
```

以上流程依據 Vercel Labs [`skills` CLI 上游 README](https://github.com/vercel-labs/skills/blob/main/README.md)。Codex 全域安裝位置以 `skills` CLI 回報的 canonical/global location、實際路徑與來源讀回為準；目前 CLI 實證可回報 `~/.agents/skills/`，而 Codex 也可能已有 agent-native `~/.codex/skills/` copy。是否由 `skills` CLI 管理，必須依 `skills ls`／`skills update` 辨識結果及可讀回的來源／metadata 判斷，不能只靠路徑判定。

本 repo 的繁中和英文 Skill 都是供 Codex 使用、可各自獨立安裝的 package。Claude Code 版是另一個尚未提供的 Skill；本 repo 目前不聲稱支援 Claude Code。詳細操作規程只在各自的 `references/`。

小熊卡的 package 版本只讀自已安裝 Skill 內的 `VERSION`，目前為 `0.2.1`；每次升級整個 Skill 後會自然讀到新值。缺失、不可讀或格式錯誤時，卡片顯示 `version unverified`，不以工作流世代或網路資料猜測。

## 開始使用

安裝後，以明確帶 CER 的語句啟動：

```text
CER 啟動：<你想完成的事、限制、優先順序>
```

或：

```text
/CER-start <你想完成的事、限制、優先順序>
```

單獨 `開工` 不會啟動 CER；它保留給目前 workspace 的既有工作方式。

## 操作指令

| 指令 | 自然語言 | 用途 |
|---|---|---|
| `/CER-start <任務、限制、優先順序>` | `CER 啟動：...`／`CER 開始：...`／`CER 開工：...` | 啟動 CER。 |
| `/CER-stop` | `停止 CER，改用單 thread 繼續。` | 退出 CER 工作模式；不再派新 E1／R，但不代表任務已完成。 |
| `/CER-close` | `CER 收工。`／`CER 關閉。`／`關閉 CER。` | 正式完成 CER 收尾；確認成果、未完成事項和同一 E1 的 `writer closed` 狀態。 |
| `/CER-status` | `顯示 CER 狀態。` | 顯示已知狀態、角色座標、下一停點與阻礙，不輪詢。 |
| `/CER-help` | `顯示 CER 指令。` | 顯示可用指令。 |

單獨 `收工` 不會觸發 CER close，也不會被當成 `/CER-stop`。

## CER 怎樣工作

1. C 在實際派工前，用最短方式確認終點、真源、邊界、權限／停點和驗收；沒有來源的推測不能冒充已確認。
2. 本地或明確指定的 Remote task 可以成為唯一 C。Remote 接收者先回 candidate `C_READY`；啟動方核實沒有另一個 active C、讀回收據並回送 `C_ACCEPTED` 後，接收者才正式成為 C。
3. C 證明 task/thread 身份、發送路徑、回傳座標和裁決點，再取得 E1 的零寫入 `ready`。
4. 同一個持久 E1 是唯一 writer。每個批次都自足，不依賴「見上文」。
5. E1 主動 direct-push 候選給 C；C 讀回、測試和裁決，不靠輪詢找成果。
6. R 找到多項問題時，C 先按共同成因和對使用者的影響合併同類問題，一次修完整個受影響邊界。只有成因、使用者影響不同，或最新修補造成新回歸時，才另開範圍。

長期或多批任務會用 inline roadmap 顯示終點、目前位置、下一停點和角色狀態。方向抉擇、重大阻礙、階段成果和最終驗收才打斷使用者；普通小步不展示流程儀式。

## 和單 thread 有甚麼分別

單 thread 適合一次性小修改或你想逐步帶著 AI 做的工作。CER 適合長期、多批、容易中斷、需要唯一 writer 或按風險獨立反證的工作。

CER 的代價是啟動前要先證明通訊閉環。只建立 task、改 title 或單向 send 都不算完成；缺少 `ready/result` 回傳時，CER 會誠實停在 blocker。

## 停用和收尾有甚麼分別

`/CER-stop` 是退出 CER 工作模式。用在你想中途改回普通單 thread 時；C 會停止新派工，如果 E1 正在寫入，先把 writer 收斂到可判定狀態。它不宣稱任務完成，也不產生正式 CER 收尾證明。

`/CER-close` 是正式結束這次 CER。用在任務已完成或要交最終結果時；C 會收斂成果、風險和未完成事項，讓同一 E1 只更新 workspace 已有的必要真源並標示 `writer closed`。CER 不會自行建立固定專案文件或平行進度來源。

## 包含內容

- [`skills/cer-workflow/`](skills/cer-workflow/)：繁中 CER Core v1 Skill
- [`skills/cer-workflow-en/`](skills/cer-workflow-en/)：完整英文鏡像 Skill
- [`RELEASE_NOTES.md`](RELEASE_NOTES.md)：繁中發布說明
- [`RELEASE_NOTES.en.md`](RELEASE_NOTES.en.md)：英文發布說明

本 repo 只提供 CER Core v1 的公開、可安裝內容。
