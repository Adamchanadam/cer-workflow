# CER Core v1 Fresh UAT

UAT 必須由使用者在乾淨 project 手動建立新 task。來源專案的 C 建立、fork 或 delegate 出來的 task 帶有來源上下文，不算 fresh。

只有標題、fork、delegate、單向送訊或工具參數成功，不等於閉環通過。必須有 E1 direct-push ready/result。

## 安裝情景

- 目標只有本 Skill，沒有來源 handoff 或來源專案背景。
- 新 C 能只靠 Skill 和使用者總任務啟動。
- `/CER-start`、`CER 啟動`、`CER 開始`、`CER 開工` 正常觸發 CER；單獨 `開工` 不觸發 CER。
- `/CER-close`、`CER 收工`、`CER 關閉`、`關閉 CER` 正常觸發 CER close；單獨 `收工` 不觸發 CER close，也不映射為 `/CER-stop`。

## 完整流程

1. 使用者輸入已有清晰目標／計劃的多批總任務，可用 `CER 工作法啟動：...` 或 `/CER-start ...`。
2. C 以 `🚀 C:` 標題或首行標籤識別主 task，完成 Controller preflight；完整任務直接通過，有來源的 `已確認` 和通過反事實測試的 `可安全推定` 不阻塞，關鍵終點／權限／驗收缺失時用黃色停點最多問三題。
3. C 完成通訊 preflight，建立或復用已證明可收發的 `E1:` 持久 task，取得含 session／thread 座標的 ready direct-push。
4. C 映射目標專案既有真源與本任務知識底座，不建立固定 CER 文件。
5. C 用真正 inline visualization 顯示初始路線圖；刻意確認不是只用 Mermaid。
6. C 只在啟動／首批前、重大裁決、重大阻礙、階段交付和收工時使用小熊卡與 inline visualization；普通 E1 子步驟不發卡。
7. 同一 E1 完成至少兩個實作批次；低風險批次不建立 R；E1 使用 C 的凍結任務契約，不自行擴大範圍或驗收。
8. 一個高風險核心承諾由 `R1:` fresh R 依同一知識底座和凍結任務契約唯讀反證，且只重審受影響邊界。
9. C 在重大方向或交付形狀改變時停點，分階段交付可觀察成果，最後取得使用者驗收。
10. 使用者明示 `CER 收工`、`CER 關閉`、`關閉 CER` 或 `/CER-close`；同一 E1 更新既有必要真源並標 writer closed；沒有持久真源時不假稱可跨 session 完整恢復。
11. 另做組合情景：與 `$project-context-workflow` 同用時不重建文件、不搶共識關卡，也不由後者建立 C／E1／R。
12. 另做停用情景：使用者輸入 `/CER-stop`；C 不再派新 E1/R，若 E1 正在寫入先收斂到 writer closed 或重大阻礙，再回到單 thread。

## Remote Controller 情景

- 明確 Remote `/CER-start` 或同等 CER 啟動語意指定接收 task 時，接收者先 direct-push candidate `C_READY`，內容包含 threadId、hostId、target_root、return target／path。
- 發送方／本地啟動閘門以官方 task／thread 列表或平台等價工具完整枚舉本次參與 host，讀回候選 root／`🚀 C:` 身份／active 狀態，且明示自己沒有把同一 root 交給另一 C；完成後用同一路徑發 `C_ACCEPTED`，接收者收到後才成為 active `🚀 C:`。
- 參與 host 枚舉不完整、候選 root／身份／狀態不可讀回、座標不完整或證據衝突時必須停止。
- 已有 active C 時只可沿用，或在舊 C 明確 handoff／close 並讀回後轉移；若發送方原是 active C，必須先完成 handoff／close 才可發 `C_ACCEPTED`。
- benign 跨 task E1／R 敘述若仍是自足派工和 direct-push 回傳，不得被誤判為 Remote C 衝突。

## 審閱收斂情景

- R 首次指出缺陷後，同類發現按共同根因和使用者後果合併；C 只做一次有界影響檢查，找齊本輪 current owners、affected surfaces 與檢查位置。
- 同一組發現包含兩項只有換字或詞序不同、但根因和使用者後果相同的問題，以及一項具不同根因、不同使用者後果或由最新修補造成的新回歸時，C 把前兩項合併成一個收斂範圍及批次，並把第三項保留為有效擴大。
- C 凍結 acceptance 與 counterexample family，由同一 E1 一批修完整個 affected boundary；R 修後只重驗凍結範圍。
- 同義改寫不展開新一輪逐句修補；frozen counterexample family 通過且沒有實質新缺陷後，C 接納並停止。

## Controller preflight QC 情景

- 使用者以自然語言給出足以開始的小批任務，但漏填不會實質改變成果的可逆細節時，C 可標為 `可安全推定` 並繼續。
- 若漏填資訊存在多個合理答案，且答案不同會實質改變交付物、權限／風險、驗收或造成重大重做，C 必須標為 `關鍵缺失` 並停問。
- C 的凍結任務契約和 E1／R 派工都保留三態、必要來源錨點和反事實結果；不得虛構使用者確認。

## 失敗條件

- 臨時 subagent 代替持久 E1。
- Controller 使用單獨 `C:` 而不是 `🚀 C:` 作可見標題或首行標籤。
- E1／R／E2 標題或首行標籤錯誤加上 `🚀`。
- 單獨 `開工` 啟動 CER，或單獨 `收工` 觸發 CER close／stop。
- 明確帶 CER 的啟動或 close 等價句沒有觸發相應 CER 行為。
- Controller preflight 未完成，或有 `關鍵缺失` 仍建立／復用 E1 或派實際批次。
- 可安全推定的細節被錯誤升級成阻塞表格；或簡單任務被迫展示治理儀式。
- 無使用者明示或已讀權威真源時，C 把推測標成 `已確認`。
- 反向假設會實質改變交付物、權限／風險、驗收或造成重大重做時，C 仍標成 `可安全推定` 並派工。
- 凍結任務契約或派工把無來源推測寫成 `已確認`。
- 關鍵終點、權限或驗收缺失時，C 不停問而直接派工。
- 缺根因仍 quick fix，或驗收反例膨脹成防禦性全專案檢查。
- E1／R 改寫 C 的凍結任務契約後繼續執行。
- 每種換字或詞序都新增 validator pattern、Reviewer 或 repair batch。
- 未找齊本輪 current owners 便逐洞修補。
- 沒有不同根因、不同使用者後果或最新修補造成的新回歸，仍擴大審閱或修補範圍。
- 不同根因、不同使用者後果或最新修補造成的新回歸被錯併入既有 counterexample family，因而漏驗實質新缺陷。
- 明確 Remote C 因訊息來自另一 task 被全面拒絕。
- 同一 target_root 已有 active C 時仍建立第二 C。
- active C 狀態不明時仍建立 C。
- 只送出 candidate `C_READY`，但未由發送方實際收到、讀回並回送 `C_ACCEPTED`，就宣稱 Remote C 身份或通訊路徑成立。
- 為唯一 C 新增 lock file、central registry、run ID、conflict engine、新角色或測試例外。
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
- CER 自行建立固定五份項目文件或平行進度。
- 把 `$project-context-workflow` 當作 CER 安裝前置。
- `/CER-stop` 後仍繼續派新 E1/R，或未證明 active writer 停止便當作已回到單 thread。
- `/CER-status` 觸發輪詢或背景監察。
- 只做到文件或局部技術成功，沒有真實成品。
