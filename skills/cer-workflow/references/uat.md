# CER Core v1 Fresh UAT

UAT 必須由使用者在乾淨 project 手動建立新 task。來源專案的 C 建立、fork 或 delegate 出來的 task 帶有來源上下文，不算 fresh。

只有標題、fork、delegate、單向送訊或工具參數成功，不等於閉環通過。必須有 E1 direct-push ready/result。

## 安裝情景

- 目標只有本 Skill，沒有來源 handoff 或來源專案背景。
- 新 C 能只靠 Skill 和使用者總任務啟動。
- 目標權威規則若強制 Agent Handoff Kit，v1 應誠實停止，不繞過。

## 完整流程

1. 使用者輸入已有清晰目標／計劃的多批總任務，可用 `CER 工作法啟動：...` 或 `/CER-start ...`。
2. C 以 `C:` 標題或首行標籤識別主 task，完成通訊 preflight，建立或復用已證明可收發的 `E1:` 持久 task，取得含 session／thread 座標的 ready direct-push。
3. C 映射目標專案既有真源與本任務知識底座，不建立固定 CER 文件。
4. C 用真正 inline visualization 顯示初始路線圖；刻意確認不是只用 Mermaid。
5. C 只在啟動／首批前、重大裁決、重大阻礙、階段交付和收工時使用小熊卡與 inline visualization；普通 E1 子步驟不發卡。
6. 同一 E1 完成至少兩個實作批次；低風險批次不建立 R。
7. 一個高風險核心承諾由 `R1:` fresh R 依同一知識底座唯讀反證，且只重審受影響邊界。
8. C 在重大方向或交付形狀改變時停點，分階段交付可觀察成果，最後取得使用者驗收。
9. 使用者說收工或 `/CER-close`；同一 E1 更新既有必要真源並標 writer closed；沒有持久真源時不假稱可跨 session 完整恢復。
10. 另做組合情景：與 `$project-context-workflow` 同用時不重建文件、不搶共識關卡，也不由後者建立 C／E1／R。
11. 另做停用情景：使用者輸入 `/CER-stop`；C 不再派新 E1/R，若 E1 正在寫入先收斂到 writer closed 或重大阻礙，再回到單 thread。

## 失敗條件

- 臨時 subagent 代替持久 E1。
- 跨 task prompt 依賴既有對話。
- 未證明送達鏈便開始工作。
- 只證明 title、fork 或單向 send，沒有 E1 direct-push ready/result。
- fork 帶入來源上下文卻被當成 fresh UAT。
- assignee 沒有回傳 ready/result 仍宣稱閉環成立。
- 新 task 沒有可見 `E1:`／`R1:` 標題或首行標籤，或 ready／結果回執缺 session／thread 座標。
- C 以輪詢發現成果。
- 知識性複雜任務沒有界定知識底座，或 R 只查格式、不反證專業主張。
- 每個內部小步都發卡，或重大裁決／阻礙／階段交付時沒有發卡。
- 可用 inline visualization 時只顯示 Mermaid。
- 普通小修改都建立 fresh R 或全專案重審。
- 把 Kit 檔案或 Kit closeout 當作 v1 前置。
- CER 自行建立固定五份項目文件或平行進度。
- 把 `$project-context-workflow` 當作 CER 安裝前置。
- `/CER-stop` 後仍繼續派新 E1/R，或未證明 active writer 停止便當作已回到單 thread。
- `/CER-status` 觸發輪詢或背景監察。
- 只做到文件或局部技術成功，沒有真實成品。
