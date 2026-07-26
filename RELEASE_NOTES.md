# 發布說明

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
