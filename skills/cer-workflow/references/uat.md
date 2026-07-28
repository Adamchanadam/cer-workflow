# CER Core v1 Fresh UAT

Fresh UAT 必須在獨立乾淨 project 以側欄可見官方新 task 執行。來源專案的 C 建立、
fork 或 delegate 出來的 task 帶有來源上下文，不算 fresh。

只有標題、fork、delegate、單向送訊或工具參數成功，不等於閉環通過。必須有 E1 direct-push ready/result。

在本 Codex 專案的 Full Audit／全面檢中，若官方 `create_thread` task 工具與乾淨
UAT workspace 可用，AI 真實流程 UAT 是必要組成，不能用 sub-agent、fork 或文字
模擬。若工具或乾淨 workspace 經實證不可用，才可精確降級為
`Full Audit 通過（只限全文靜態審核；AI 真實流程 UAT 不可用）`，不得說 AI UAT
通過。發布後使用者手動 UAT 是公開安裝與使用者體驗的另一層，結果另報
`未執行／通過／失敗`；AI UAT 不可冒充人工 UAT。

AI 真實流程 UAT 證據必須列出兩輪實際 thread ids 並做機械比較：同一輪多批次 E1
threadId 相同；C2 threadId 不同於 C1；第二輪 E1 threadId 不同於第一輪 E1；第二輪
每個 R 都是新 threadId，不得等於第一輪任何 R，也不得沿用同輪較早 R。只用文字說
fresh 不足夠。

同一輪所有 C／E／R title 必須使用相同短 cycle 編號，例如 `🚀 C:01｜...`、
`E1:01｜...`、`R1:01｜...`；下一輪使用新編號。規則生效後的新 cycle 必須用
`01` 以上，不能用 `00`。`00` 只可用於明確 legacy/migration fixture，表示 cycle
numbering 規則生效前已開始且無法可靠回推原 cycle number。cycle 編號只供側欄
辨識，不是 lock、run ID、唯一 C 證據或 thread 身份。若新 cycle 無法可靠枚舉或
設定 title，保留最短 role title 並報真實 `title sync warning`；不得顯示問號 cycle
標籤，不得猜測數字。

## 安裝情景

- 目標只有本 Skill，沒有來源 handoff 或來源專案背景。
- 本 Skill 只供 Codex；不得聲稱目前 repo 已提供 Claude Code 版 Skill。
- Skill 根目錄 `VERSION` 只有一行穩定 semver，現值為 `0.2.4`；每張小熊卡顯示
  前都重新讀取，格式無效時顯示 `version unverified`。
- 新 C 能只靠 Skill 和使用者總任務啟動。
- `/CER-start`、`CER 啟動`、`CER 開始`、`CER 開工` 正常觸發 CER；單獨 `開工` 不觸發 CER。
- `/CER-close`、`CER 收工`、`CER 關閉`、`關閉 CER` 正常觸發 CER close；單獨 `收工` 不觸發 CER close，也不映射為 `/CER-stop`。

## 完整流程

1. 使用者輸入已有清晰目標／計劃的多批總任務，可用 `CER 工作法啟動：...` 或 `/CER-start ...`。
2. C 以 `🚀 C:01｜<極短任務名>` 標題或首行標籤識別主 task，完成 Controller preflight；完整任務直接通過，有來源的 `已確認` 和通過反事實測試的 `可安全推定` 不阻塞，關鍵終點／權限／驗收缺失時用黃色停點最多問三題。
3. C 完成通訊 preflight，用官方 `create_thread` 建立同一 Codex project 側欄可見
   的全新 `E1:01｜...` 持久 task，讀回 title、thread id 與正式回傳路徑，取得含
   session／thread 座標的 ready direct-push。
4. C 映射目標專案既有真源與本任務知識底座，不建立固定 CER 文件。
5. 每次成功接受 `CER-start`，C 的第一個使用者可見成功回執都是固定開眼
   `CER 工作法 v0.2.4`／`🔵 CER 已啟動` 卡；保留完整三行小熊，版本與狀態接在第三行
   小熊腳後，以固定 `·` 分隔而不另起一行；單批也必須顯示。
   多階段／多批或需要首次公開對齊的任務再用真正 inline visualization 顯示初始路線圖，並確認不是
   只用 Mermaid。
6. C 只在啟動、重大裁決、重大阻礙、階段交付、成功停用和成功收尾時使用相應
   小熊卡；普通 E1 子步驟不發卡。
7. 同一 E1 完成至少兩個實作批次；低風險批次不建立 R；同輪後續批次復用
   第 3 步的同一 E1，不重建也不換人。E1 使用 C 的凍結任務契約，不自行擴大
   範圍或驗收。
8. 一個高風險核心承諾由官方 `create_thread` 建立的側欄可見 `R1:01｜...` fresh
   新 task 依同一知識底座和凍結任務契約唯讀反證，且只重審受影響邊界。
9. C 在重大方向或交付形狀改變時停點，分階段交付可觀察成果，區分技術驗收與用途校正，最後取得適用的使用者驗收。
10. 使用者明示 `CER 收工`、`CER 關閉`、`關閉 CER` 或 `/CER-close`；同一 E1 更新既有必要真源並標 writer closed。C 完成必要讀回後，用官方 title 工具把本輪可核實 C／E／R title 改成 `🚀 C:01✓｜...`、`E1:01✓｜...`、`R1:01✓｜...` 並讀回；失敗則如實報 `title sync warning` 與失敗座標。最後才顯示固定閉眼 `🟢 CER 已收尾`／`writer closed` 卡；沒有持久真源時不假稱可跨 session 完整恢復。
11. 另做組合情景：與 `$project-context-workflow` 同用時不重建文件、不搶共識關卡，也不由後者建立 C／E1／R。
12. 另做停用情景：使用者輸入 `/CER-stop`；C 不再派新 E1/R，若 E1 正在寫入先收斂到 writer closed 或重大阻礙。只有證明沒有 active writer 並完成必要讀回，才顯示固定閉眼 `⚪ CER 已停用`／`CER inactive` 卡並回到單 thread。

## Remote Controller 情景

- 明確 Remote `/CER-start` 或同等 CER 啟動語意指定接收 task 時，接收者先 direct-push candidate `C_READY`，內容包含 threadId、hostId、target_root、return target／path。
- 發送方／本地啟動閘門以官方 task／thread 列表或平台等價工具完整枚舉本次參與 host，讀回候選 root／`🚀 C:` 身份／active 狀態，且明示自己沒有把同一 root 交給另一 C；完成後用同一路徑發 `C_ACCEPTED`，接收者收到後才成為 active `🚀 C:`。
- 參與 host 枚舉不完整、候選 root／身份／狀態不可讀回、座標不完整或證據衝突時必須停止。
- 已有 active C 時只可沿用，或在舊 C 明確 handoff／close 並讀回後轉移；若發送方原是 active C，必須先完成 handoff／close 才可發 `C_ACCEPTED`。
- benign 跨 task E1／R 敘述若仍是自足派工和 direct-push 回傳，不得被誤判為 Remote C 衝突。

## 跨輪隔離情景

- 同一 workspace 成功 `/CER-close` 後，舊 C／E／R task 可保留作歷史，但整組
  不可再接收下一輪工作。
- 新 task 的新 `CER-start` 只有在唯一 C 閘門讀回舊 C 已
  `closed`／`handed-off`、沒有 active C，且所有參與 host 可核實後才成立。
- 新一輪建立全新 E1，所有 R 都 fresh；不得復用上一輪 closed C 的任何 E1
  或 R task／座標。證據必須比較 cycle 編號與 threadId：同輪 E1 threadId 相同，
  第二輪 cycle 編號不同，C／E1／R threadId 均不同，且舊輪 title 前段已有 `✓` 或
  有真實 `title sync warning`。
- 乾淨 project 的 AI 真實流程 UAT 新 cycle 必須使用 numeric `01` 以上；`00` 只可
  出現在明確 legacy migration fixture。任何可見問號 cycle title 都判失敗。
- 舊 C 狀態或任一參與 host 不可核實時，啟動受阻並顯示開眼紅色 blocker 卡。

## Codex task 拓撲情景

- E1、E2 及每個 R 都由官方 `create_thread` 在同一 Codex project 建立為側欄
  可見獨立新 task/thread；ready/result 讀回 title、thread id 與正式回傳路徑。
- 同一輪後續批次持續復用本輪同一 E1；只有 E1 停止寫入、workspace 可判定且
  C 發出接管批次後，才可用 `create_thread` 另建 E2。
- 每個 R 都是 fresh 新 task；同一輪或跨輪都不得沿用舊 R。
- C 可用 inline sub-agent 作唯讀探索、證據整理或候選分析；它不得寫 workspace，
  不得代替 E 或 R，不得產生正式 ready/result，也不得作 CER Reviewer 通過證據。
- 缺少 `create_thread`、側欄可見 title、可核實 thread id 或正式回傳路徑時，
  E／R 委派受阻；不得降級使用 inline sub-agent、fork、delegate 或既有 task。

## 審閱收斂情景

- R 首次指出缺陷後，同類發現按共同根因和使用者後果合併；C 只做一次有界影響檢查，找齊本輪 current owners、affected surfaces 與檢查位置。
- 同一組發現包含兩項只有換字或詞序不同、但根因和使用者後果相同的問題，以及一項具不同根因、不同使用者後果或由最新修補造成的新回歸時，C 把前兩項合併成一個收斂範圍及批次，並把第三項保留為有效擴大。
- C 凍結 acceptance 與 counterexample family，由同一 E1 一批修完整個 affected boundary；R 修後只重驗凍結範圍。
- 同義改寫不展開新一輪逐句修補；frozen counterexample family 通過且沒有實質新缺陷後，C 接納並停止。

## Controller preflight QC 情景

- 使用者以自然語言給出足以開始的小批任務，但漏填不會實質改變成果的可逆細節時，C 可標為 `可安全推定` 並繼續。
- 若漏填資訊存在多個合理答案，且答案不同會實質改變交付物、權限／風險、驗收或造成重大重做，C 必須標為 `關鍵缺失` 並停問。
- C 的凍結任務契約和 E1／R 派工都保留三態、必要來源錨點和反事實結果；不得虛構使用者確認。

## 驗收有效性情景

- 只有版本或發布文件改動時，可保留未受影響的執行流程 UAT；但必須驗證
  版本、文件、連結與交付物讀回。
- 目前外部權威反駁安裝聲稱時，即使本地執行流程沒改，也只重開受影響的公開安裝
  聲稱與其依賴交付面。
- source／package 或安裝產物不一致時，發布或安裝結論必須先做產物讀回。
- 只有 `high risk`／發布任務標籤、檔案數或改動大小，沒有前提到結論因果鏈時，不
  授權全專案重審。
- 有可信證據顯示舊驗證假綠時，重開受影響結論並重建最小充分證據。
- 全新脈絡無法讀取先前證據時，不能靜默沿用舊結論；必須讀回證據、標示
  continuity limited，或重建受影響證據。

## 比例化收尾情景

- 本輪 C／E／R threadId 完整且 writer 狀態可直接讀回時，C 只向已知角色讀回
  終態、必要真源及 title sync；不先枚舉整個 project，也不因 close 而建立 R。
- 純狀態收尾只更新本次確有需要的既有真源並作針對性結構／內容讀回；沒有持久
  真源需要更新時，只驗實際交付與 `writer closed`，不固定更新任何文件組合。
- 角色座標不完整或互相矛盾、writer 狀態不明時，C 在相關 project 範圍枚舉並
  擴大讀回；不得以比例原則略過未知終態。
- 本輪改動治理、schema 或核心流程，出現可信矛盾／假綠、source 與交付物不一致，
  或專案明定完整檢查時，執行相應完整 validator／doctor；否則不因 close 名稱
  自動執行。
- 每張 CER 小熊卡使用 `╰ ^ ╯` 作腳部；不得使用會在 Markdown 行首形成引用的
  `>` 符號。
- 每張小熊卡保留完整三行；版本與狀態只可接在第三行小熊腳後，以固定 `·` 分隔，不另起一行。

## Kit 權威轉交情景

- 目標 workspace 的 `AGENTS.md` 把 `收工`、`Wrap up Agent Handoff` 或同等
  session closeout 語意路由為 Kit full closeout 時，C 給同一 E1 的批次保留
  使用者原始指令、正確 root、角色／回傳座標及必要未持久化狀態，不重述 Kit
  closeout 程序、檔案清單、maintenance 判斷或額外測試。
- Kit 權威終態未成立或回報 blocked 時，C 不得宣稱 `writer closed`、同步 title
  `✓` 或顯示 CER 收尾卡；終態成立後才依 CER 自身生命週期收尾。
- 同一 E1 已回傳可核實的 Kit 權威終態時，C 只作必要成果讀回，不再尋找另一
  CLI、重跑 `closeout-status` 或複製其他 Kit 檢查；證據缺失或矛盾才回同一 E1 補證。
- `/CER-close` 只執行 CER close，不反向觸發 Kit full closeout。
- 目標 `AGENTS.md` 把 `治理打通`、`把文件接入 Agent Handoff Kit` 或同等文件
  governance bridge 語意路由至既有治理工作流時，C 只把原始指令、指定文件及
  必要座標交給同一 E1；完成後 CER 保持啟動。
- Kit 權威入口不可讀、同一 E1 不可核實或存在另一 writer 時，轉交受阻；不得
  猜測、模擬或另建 Kit 程序。

## 失敗條件

- 臨時 subagent 代替持久 E1。
- inline sub-agent、fork、delegate 或既有 task 被當作正式 E1、E2 或 R。
- C 的 inline sub-agent 寫 workspace、產生正式 ready/result、代替 E／R，或被列為 CER Reviewer 通過證據。
- E1／R 缺少官方 `create_thread` 建立證據、側欄可見 title、可核實 thread id 或正式回傳路徑，仍開始工作。
- Controller 使用單獨 `C:` 而不是 `🚀 C:01｜...` 作可見標題或首行標籤。
- E1／R／E2 標題或首行標籤錯誤加上 `🚀`。
- E1 第二輪被命名為 `E2:`，或把角色序號與 cycle 編號混在一起；同輪 C／E／R cycle 編號不一致；跨輪沿用同一 cycle 編號。
- cycle 編號被當作 lock、run ID、唯一 C 證據或 thread 身份；漏列 threadId 仍通過。
- 新 cycle 使用 `00`；任何可見問號 cycle title；無法可靠枚舉或設定 title 時顯示假標籤或猜測數字，而不是保留最短 role title 並報真實 `title sync warning`。
- 單獨 `開工` 啟動 CER，或單獨 `收工` 觸發 CER close／stop。
- C 把 Kit full closeout 或 governance bridge 的權威程序、檔案清單、
  maintenance 判斷或測試重寫進 E1 派工。
- Kit full closeout 尚未有權威成功終態，C 已宣稱 `writer closed`、同步 title
  `✓` 或顯示 CER 收尾卡。
- 同一 E1 已回傳可核實的 Kit 權威終態後，C 仍自行重跑 Kit 程序或檢查。
- 明確帶 CER 的啟動或 close 等價句沒有觸發相應 CER 行為。
- Controller preflight 未完成，或有 `關鍵缺失` 仍建立／復用 E1 或派實際批次。
- 可安全推定的細節被錯誤升級成阻塞表格；或簡單任務被迫展示治理儀式。
- 無使用者明示或已讀權威真源時，C 把推測標成 `已確認`。
- 反向假設會實質改變交付物、權限／風險、驗收或造成重大重做時，C 仍標成 `可安全推定` 並派工。
- 凍結任務契約或派工把無來源推測寫成 `已確認`。
- 關鍵終點、權限或驗收缺失時，C 不停問而直接派工。
- 缺根因仍 quick fix，或驗收反例膨脹成防禦性全專案檢查。
- 任務只因 `high risk`／發布任務標籤、檔案數或改動大小就擴成全專案重審。
- 目前外部權威、source／package 或發布／安裝產物不一致、可信假綠證據或不可讀舊證據已
  使前提失效，C 仍靜默沿用舊驗收、修補或發布結論。
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
- 小熊卡沒有先讀本 Skill 的 `VERSION`，把 `v1` 當 package 版本，或從網路、
  Git tag、GitHub Release／lock metadata 猜版本。
- `VERSION` 缺失、不可讀或格式錯誤時沒有顯示 `version unverified`。
- 啟動卡把版本或狀態另起一行，或不保留完整三行小熊／不用第三行小熊腳後的固定 `·` 分隔。
- 任何 CER 小熊卡仍使用 `>` 作腳部，因而被 Markdown 呈現為引用。
- release／upgrade 沒有先更新 `VERSION`。
- 單批 `CER-start` 沒有固定啟動卡，或啟動卡錯用閉眼小熊。
- stop／close 尚未證明 writer 停止或必要讀回完成，卻顯示閉眼成功卡；close 在
  title sync 或 `title sync warning` 讀回前顯示閉眼卡；title rename 失敗卻宣稱已
  改名；受阻時沒有使用開眼紅色 blocker 卡。
- close 後新一輪 C 復用上一輪的 E1 或 R task／座標。
- close 後舊輪 title 前段沒有 `✓`，也沒有真實 `title sync warning`，卻聲稱 close
  title 同步完成；只改 title 或只檢文字就算 lifecycle close。
- 已知完整角色座標且沒有矛盾時，仍只因 close 而廣泛枚舉 project task、固定更新
  一組狀態文件、執行完整 validator／doctor，或建立 Reviewer。
- 角色座標矛盾或 writer 狀態不明時，仍以比例原則為由拒絕擴大讀回。
- 同輪後續批次沒有復用同一 E1，卻在未達 E2 接管條件時另建 writer。
- 舊 C 狀態或參與 host 不可核實，仍啟動第二 C。
- 可用 inline visualization 時只顯示 Mermaid。
- 普通小修改都建立 fresh R 或全專案重審。
- CER 自行建立固定五份項目文件或平行進度。
- 把 `$project-context-workflow` 當作 CER 安裝前置。
- `/CER-stop` 後仍繼續派新 E1/R，或未證明 active writer 停止便當作已回到單 thread。
- `/CER-status` 觸發輪詢或背景監察。
- 只做到文件或局部技術成功，沒有真實成品。
