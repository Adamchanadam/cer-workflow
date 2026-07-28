# 發布說明

範圍說明：本檔各版本區段記錄對應版本的 release history；實際執行規則以使用者已安裝版本隨附的 Skill references 為準。

## v0.2.2

本版修正 v0.2.1 後確認的兩項 CER 使用問題：

- 小熊卡腳部改用 `╰ ^ ╯`，避免行首 `>` 在 Markdown 內被呈現為引用
- `/CER-close` 保留 `writer closed`、必要讀回、title sync／warning 與 history-only 等收尾條件
- 已知本輪 C／E／R task 時，直接讀回相關角色，不預設掃描整個 project
- 純狀態收尾採用針對性讀回；只有證據缺失、狀態矛盾、核心流程受影響或專案規則要求時才擴大檢查
- v0.2.2 CER-close UAT 已通過；發布後使用者手動 UAT 仍獨立回報

## v0.2.1

本版收斂已通過 Full Audit 的 release-ready 候選：

- 小熊生命週期卡改由 Skill `VERSION` 動態顯示 package 版本，並修正啟動、停用、收尾卡時機
- 正式 C／E／R 使用官方側欄可見 task 拓撲，保留同輪 E1 復用、fresh R 與跨輪隔離
- 短 numeric cycle title、CER-close `✓` rename 與 `title sync warning` 邊界完整寫入執行面
- C 在作成或沿用驗收、修補、發布結論前，會再次套用驗收有效性與比例規則；未受影響證據可保留，前提失效才重開對應結論，範圍按可追溯因果擴大，深度按後果與不確定性調整，不因任務標籤或檔案數加重
- Codex-only 安裝／升級 prompt 依語言拆分，避免混裝其他語言或其他 agent 版本
- release-readiness 證據包含全文靜態審核與兩輪 AI 真實流程 UAT；發布後使用者手動 UAT 仍獨立回報

## v0.2.0

本版收斂為完整雙語公開版本：

- 完整、可獨立安裝的繁中與英文 Skill package
- 實際派工前的 Controller preflight；沒有來源的推測不得當作已確認
- 本地或 Remote 啟動唯一 Controller，使用 `C_READY`／`C_ACCEPTED` 完成核實
- 明確限定 `/CER-start`、`/CER-stop`、`/CER-close`；`/CER-stop` 回到普通單一對話工作，普通 `開工`／`收工` 不觸發 CER
- `🚀 C:` 作為 Controller 可見命名；E1／R／E2 標籤不變
- 同成因、同使用者影響的審閱發現收斂為一次受影響邊界修正；真正的新缺陷分開處理
- 長期工作使用 inline roadmap 和相稱 checkpoint
- 分離的繁中／英文資訊圖與公開文件

## v0.1.1

文件與指令更新：

- 繁中 README 作為入口頁
- 英文 README 頁
- CER 工作法資訊圖
- `/CER-start`、`/CER-stop`、`/CER-close`、`/CER-status` 和 `/CER-help`
- 在專案內啟動、停止和收尾 CER 的說明
- 與單一對話工作的白話比較

## v0.1.0

初始公開預覽：

- CER Core v1 作為可安裝 Skill
- 持久 Executor 與按風險建立的 Reviewer 角色
- 跨 task 工作的 session/thread 回傳規則
- 四色 checkpoint 時機
- 專家任務的知識底座範圍
