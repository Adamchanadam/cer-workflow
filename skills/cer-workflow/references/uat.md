# CER Core v1 Fresh UAT

## 目錄

- [安裝情景](#安裝情景)
- [完整流程](#完整流程)
- [Remote Controller 情景](#remote-controller-情景)
- [跨輪隔離情景](#跨輪隔離情景)
- [Codex task 拓撲情景](#codex-task-拓撲情景)
- [工具結果不明與批次去重情景](#工具結果不明與批次去重情景)
- [自適應批次加速情景](#自適應批次加速情景)
- [平行候選生產者反證情景](#平行候選生產者反證情景)
- [審閱收斂情景](#審閱收斂情景)
- [Controller preflight QC 情景](#controller-preflight-qc-情景)
- [成果錨定與進展情景](#成果錨定與進展情景)
- [未預期失敗與範圍例外情景](#未預期失敗與範圍例外情景)
- [驗收有效性情景](#驗收有效性情景)
- [比例化收尾情景](#比例化收尾情景)
- [Kit 權威轉交情景](#kit-權威轉交情景)
- [失敗條件](#失敗條件)

Fresh UAT 必須在獨立乾淨 project 以側欄可見官方新 task 執行。來源專案的 C 建立、
fork 或 delegate 出來的 task 帶有來源上下文，不算 fresh。

只有標題、fork、delegate、單向送訊或工具參數成功，不等於閉環通過。必須有 E1 direct-push ready/result。

AI 真實流程 UAT 的 PASS 資格是上述閉環證據，不是等待義務。完成本檔允許的一次
有界等待、對帳或受控重送後，若 assignee 仍未 direct-push 零寫入 ready 或
result，C 必須按證據裁決該 UAT attempt 為 FAIL 或 `delivery_unavailable`，並停止該
嘗試；不得反覆建立同型 task、輪詢、背景等待，或用 sub-agent、fork、文字模擬
補成 PASS。只有證明必需 task／delivery 工具鏈或乾淨 workspace 對本輪不可用時，
才可使用下述 static-only downgrade；普通未完成或無證據不是 downgrade。

在本 Codex 專案的 Full Audit／全面檢中，若官方 `create_thread` task 工具與乾淨
UAT workspace 可用，AI 真實流程 UAT 是必要組成，不能用 sub-agent、fork 或文字
模擬。若必需 task／delivery 工具鏈或乾淨 workspace 經實證不可用，才可精確降級為
`Full Audit 通過（只限全文靜態審核；AI 真實流程 UAT 不可用）`，不得說 AI UAT
通過。發布後使用者手動 UAT 是公開安裝與使用者體驗的另一層，結果另報
`未執行／通過／失敗`；AI UAT 不可冒充人工 UAT。

AI 真實流程 UAT 證據必須列出兩輪實際 thread ids 並做機械比較：同一輪多批次 E1
threadId 相同；C2 threadId 不同於 C1；第二輪 E1 threadId 不同於第一輪 E1；第二輪
每個 R 都是新 threadId，不得等於第一輪任何 R，也不得沿用同輪較早 R。只用文字說
fresh 不足夠。

每輪外層 UAT cycle C 也是發布派工者的受託 assignee：cycle 工作開始前必須
direct-push 零寫入 `ready` 回主線 return target；完成、受阻或 checkpoint 時，必須
先 direct-push 結構化 `AI_UAT_CYCLE_N: PASS/FAIL` 回同一主線 target 才可結束。派工者
不得自動用 `wait_threads`／`read_thread` 等待外層 UAT；只能在已預期 direct-push
且平台不自動喚醒時，於該 direct-push 後使用一次有界 `wait_threads`／`read_thread`
作喚醒、核實或裁決。
子 C final、wait snapshot、被動讀取、task title 或使用者轉述「UAT task 已完工」本身
不是正式交付證據，不能滿足 AI 真實流程 UAT 或發布就緒。若外層回傳協議缺失，派工者
可要求同一 cycle C 以既有 final 證據作一次有界 delivery-repair push；收到前該 cycle 是
`delivery_incomplete`，不是已通過 UAT cycle。

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
- Skill 根目錄 `VERSION` 只有一行穩定 semver；每張小熊卡顯示前都重新讀取，
  把模板 `{package_version}` 完整替換，格式無效時顯示
  `version unverified`；不得原樣顯示佔位文字。
- 新 C 能只靠 Skill 和使用者總任務啟動。
- 預設提示使用「按風險建立 fresh Reviewer」；簡單任務不會因預設提示而強制建立 Reviewer。
- `/CER-start`、`CER 啟動`、`CER 開始`、`CER 開工` 正常觸發 CER；單獨 `開工` 不觸發 CER。
- `/CER-close`、`CER 收工`、`CER 關閉`、`關閉 CER` 正常觸發 CER close；單獨 `收工` 不觸發 CER close，也不映射為 `/CER-stop`。

## 完整流程

1. 使用者輸入已有清晰目標／計劃的多批總任務，可用 `CER 工作法啟動：...` 或 `/CER-start ...`。
2. C 以 `🚀 C:01｜<極短任務名>` 標題或首行標籤識別主 task，完成 Controller preflight；完整任務直接通過，有來源的 `已確認` 和通過反事實測試的 `可安全推定` 不阻塞，關鍵終點／權限／驗收缺失時用黃色停點最多問三題。
3. C 完成通訊 preflight，用官方 `create_thread` 建立同一 Codex project 側欄可見
   的全新 `E1:01｜...` 持久 task；`create_thread` receipt 後立即用官方 title
   工具（Codex 目前為 `set_thread_title`）設定／改名並讀回 title，不以初始
   prompt、模型自動 title 或首行 label 代替；再讀回 thread id 與正式回傳路徑，取得含
   threadId 或平台等價座標的 ready direct-push；sessionId 只在當前工具 schema／receipt
   明示需要／提供時附帶記錄，不可代替 threadId 或推導 hostId。若實際平台不會自動喚醒 idle C，
   C 可對該 E1 使用一次有界 event wait；wait snapshot 不算 ready 證據。
4. C 映射目標專案既有真源與本任務知識底座，不建立固定 CER 文件。
5. 每次成功接受 `CER-start`，C 的第一個使用者可見成功回執都是固定開眼
   `CER 工作法 v{package_version}`／`🔵 CER 已啟動` 卡；實際輸出前先以
   `VERSION` 替換佔位，保留完整三行 ASCII 小熊，版本在第一行、狀態在第二行、
   第三行只保留小熊底線，並作為獨立 fenced `text` code block 輸出；單批也必須顯示。
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
10. 使用者明示 `CER 收工`、`CER 關閉`、`關閉 CER` 或 `/CER-close`；同一 E1 更新既有必要真源並標 writer closed。C 完成必要讀回後，用官方 title 工具把本輪可核實 C／E／R title 改成 `🚀 C:01✓｜...`、`E1:01✓｜...`、`R1:01✓｜...` 並讀回；失敗則如實報 `title sync warning` 與失敗座標。若本輪有已完成、已讀回、已裁決的 R，C 可封存這些 R 並保留 C／E1 可見；收尾摘要明講封存不是刪除，仍可在已封存任務中找回。最後才顯示固定閉眼 `🟢 CER 已收尾`／`writer closed` 卡；沒有持久真源時不假稱可跨 session 完整恢復。
11. 另做組合情景：與 `$project-context-workflow` 同用時不重建文件、不搶共識關卡，也不由後者建立 C／E1／R。
12. 另做停用情景：使用者輸入 `/CER-stop`；C 不再派新 E1/R，若 E1 正在寫入先收斂到 writer closed 或重大阻礙。只有證明沒有 active writer 並完成必要讀回，才顯示固定閉眼 `⚪ CER 已停用`／`CER inactive` 卡並回到單 thread。

## Remote Controller 情景

- 明確 Remote `/CER-start` 或同等 CER 啟動語意指定接收 task 時，接收者先 direct-push candidate `C_READY`，內容包含 threadId 或平台等價座標、target_root、return target／path，以及當前工具 schema／receipt 明示必需的回傳或路由座標；不得猜 hostId。
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
- C 可依 [parallel-producers.md](parallel-producers.md) 使用 inline 平行候選
  生產者；它不是正式角色，不加入角色 title／cycle／lifecycle 卡，也不能代替
  E 或 R。
- 缺少 `create_thread`、`create_thread` 後官方 title 工具設定／讀回證據、
  側欄可見 title、可核實 thread id 或正式回傳路徑時，
  E／R 委派受阻；不得降級使用 inline sub-agent、fork、delegate 或既有 task。

## 工具結果不明與批次去重情景

- `create_thread` 回報錯誤或逾時，但一次有界官方枚舉找到一個符合建立前快照的
  新 task 時，C 不重試建立；以官方 metadata 及該 task 的零寫入 `ready` 完成確認。
- `create_thread` 回報不明後，一次有界對帳找不到候選時，狀態是 `blocked`；
  不把立即枚舉的零候選當成可自動重試授權。稍後 resume、startup 或建立同 role
  前會再次對帳，延遲出現的 task 不會被當成不存在。
- 同一 role／cycle／root 出現三個候選時，三者先保持零寫入；C 只選定一個，
  其餘兩個各自收到 `STOP_ZERO_WRITE` 並 direct-push 停止確認後，才派正式工作。
- 三個零寫入候選中有一個無法 direct-push 停止確認時，只有官方不可工作終態
  讀回可代替；兩種證據都沒有便 `blocked`，不得讓其餘候選先工作。
- task 自報 host 為 `local`，官方 metadata 顯示目前實際 hostId 為另一座標時，
  路由採用官方 metadata；差異先對帳，不能把顯示別名當權威身份。
- 重複 E1 中任何一個可能已收到正式批次或寫入時，C 停止新派工並讀回 writer
  及 workspace 狀態；全部 writer 停止且 workspace 可判定後，才選定一名恢復，
  或依接管規則建立 E2。不能只指定一個、取消其餘便繼續。
- E1 回 `BATCH_RECEIVED` 後、開始工作前中斷時，批次保持
  `RECEIVED_ZERO_WRITE`；相同 `batchId` 只續行原批一次，不另開第二次執行。
- E1 在部分寫入後中斷且無法證明批次狀態時，標成 `STATE_UNKNOWN`，停止寫入並
  先恢復唯一 writer 及 workspace；不得因重複送達而重跑整批。
- `RESULT_READY` 的批次重複送達時，E1 重播相同結果；C 已回
  `RESULT_ACCEPTED` 後再重複送達，才只回 `DUPLICATE_IGNORED`。
- 首次 send 結果不明後，sender 對完全相同內容作受控重送時，`batchId`、
  `batchSeq`、`payloadDigest` 與內容全部不變。驗收或任務契約有改動便使用新
  `batchId` 及較高 `batchSeq`。
- 相同 `batchId` 帶不同 `payloadDigest` 時，接收者立即 `blocked`；C 不可把舊
  批次結果接納為新修訂。
- 舊批次 B1 送達結果不明，而新契約需要 B2 時，C 先送
  `BATCH_SUPERSEDE B1 -> B2`。接收者記錄 B1 為 `SUPERSEDED` 並回確認；B1
  若其後延遲送達即被拒絕。B1 已開始或可能寫入時，完成停止及 workspace 恢復後
  才開始較高 `batchSeq` 的 B2。
- ready、`C_ACCEPTED`、stop、批次狀態、結果或 `RESULT_ACCEPTED` 任一 send
  回報不明時，sender 先以相同 `messageId` 作一次有界 receipt／目的地讀回；
  必要時只可受控重送同一訊息一次，receiver 去重並重播既有確認。
- E1 已完成但結果 push 回報不明時，C 可由同一 `messageId` 的目的地讀回或
  重複結果取得候選，裁決後回同一 `RESULT_ACCEPTED`；不永久等待，也不接納兩次。
- 對精確 `messageId` 的故障讀回可在未收到 push 時執行，但只證明該訊息送達；
  不會被當成整條 ready／accept 通訊鏈成立，也不會擴成輪詢。
- 平台不會自動喚醒 idle C 時，C 對已知唯一 E1 使用一次有界 event wait；
  E1 direct-push READY 以新輸入中斷等待後才繼續。只得 wait snapshot、完成狀態
  或 commentary 而沒有 direct-push 時，仍未通過。
- 同一批次先後預期 `BATCH_RECEIVED` 與最終結果時，兩者使用不同
  `eventWaitKey` 及最新 cursor，各有一次初始等待；第一個回執不會消耗最終結果
  的等待額度。
- 同一預期訊息逾時後，只有完成對帳及唯一一次同 `messageId` 受控重送，才可
  使用一次 recovery wait；再次逾時即阻塞。額外控制訊息或改名不能重開額度。
- 平台沒有 idempotency key 或權威 operation receipt 時，CER 使用有界對帳與
  `batchId` 去重，不虛構平台 receipt；批次識別只作重複送達防護。

## 自適應批次加速情景

- 同一 checkpoint 內，被驗對象、需求、直接依賴／環境、交付物及驗證方法均未
  改變且無可信反證時，同源證據可一次讀取、一次定位並跨相依工作共用。
- 需求、來源、直接依賴、環境前提、交付物或驗證方法任何一項改變時，受影響
  證據立即失效，只重建該結論的最小充分證據。
- 寫入前權威讀回已證明驗收成立時，`no_material_delta` 可停止該寫入批次；
  審閱、證據、稽核或故障恢復批次不能只因零寫入而略過。
- 同一 checkpoint 的新事實集中收集並最多統一推進一次有效期；出現可信矛盾時，
  即使已集中處理仍須重開受影響結論。
- 相容驗收命令與反例可同批執行，但每項保留獨立輸出、exit status、來源與
  裁決；依賴次序或共享可變狀態的檢查分開執行。
- 完整高風險候選才建立一名 fresh R；不可逆或高後果行動則在行動前先完成
  相應 R，不得把必要審閱延後到行動後。
- 通訊結果、批次生命週期、角色重複、唯一 writer、證據身份／新鮮度任一不明，
  或需要使用者裁決時，自適應加速為 `off`，回到一般 CER 規則。
- fresh R 從凍結原始證據自行讀取並反證；C／E 的摘要只可定位，不可代替獨立證據。

## 平行候選生產者反證情景

- 兩條互不依賴 lane、凍結輸入、C 有同期不重複工作、候選可獨立驗證、淨省時
  明顯且槽位可用時，兩條候選可自然到達並由 C 合流。
- 簡單一次讀取、沒有 subagent 能力、平行成本不划算或任一資格不可判定時，
  `producer_count=0`，C 串行完成，使用者不需設定 lane、scratch、hash 或角色。
- `read_only` lane 嘗試任何寫入時，候選失效。
- artifact scratch 位於 project 內或其祖先、磁碟根、使用者根、系統根、
  symlink、junction、reparse point、mount、與另一 lane 相等／互為祖先或越界
  寫入時，該 lane 不啟動或 fail closed。
- 凍結輸入只在一條 lane 漂移時，只淘汰相依候選；未受影響候選不重跑。
- 來源衝突時，C 按權威來源裁決，不按票數、完成先後或多數相同答案接納。
- 候選遲到、producer 失敗、來源不可重播或 artifact hash tamper 時，候選失效；
  producer 失敗本身不阻塞 CER，除非缺失證據就是任務 blocker。
- producer 冒充 E／R、直接送 E1、E1 採用未合流 scratch，或 C／R／producer
  寫 target project 時，整個相依候選 fail closed。
- `/CER-stop` 或 `/CER-close` 不等待 producer；遲到候選不重開已關閉 intake。
- 生產者不取得正式 title、cycle、ready、result、slash、lock、registry 或 run id；
  roadmap 的角色欄和 lifecycle 卡仍只有正式角色。

## 審閱收斂情景

- R 首次指出缺陷後，同類發現按共同根因和使用者後果合併；C 只做一次有界影響檢查，找齊本輪 current owners、affected surfaces 與檢查位置。
- 同一凍結目標已有實質 E／R 結果後，C 若為同根因另建 E／R 或任務支線，卻不能指出新的可推翻問題，以及它對原始目標或已核實阻礙的最小必要性，則該派發不成立；C 應合併、停止或自行裁決。
- 同一組發現包含兩項只有換字或詞序不同、但根因和使用者後果相同的問題，以及一項具不同根因、不同使用者後果或由最新修補造成的新回歸時，C 把前兩項合併成一個收斂範圍及批次，並把第三項保留為有效擴大。
- C 凍結 acceptance 與 counterexample family，由同一 E1 一批修完整個 affected boundary；R 修後只重驗凍結範圍。
- 同義改寫不展開新一輪逐句修補；frozen counterexample family 通過且沒有實質新缺陷後，C 接納並停止。

## Controller preflight QC 情景

- 使用者以自然語言給出足以開始的小批任務，但漏填不會實質改變成果的可逆細節時，C 可標為 `可安全推定` 並繼續。
- 若漏填資訊存在多個合理答案，且答案不同會實質改變交付物、權限／風險、驗收或造成重大重做，C 必須標為 `關鍵缺失` 並停問。
- 模糊但可開始的多批任務，C 建立活的任務簡報，保留已確認要求／排除、可安全推定、關鍵缺口、最新使用者回饋、本批凍結、下一個可觀察預覽或裁決點；只凍結下一個可安全執行批次，不要求使用者先寫完整規格，不把 `$project-context-workflow` 當成前置，也不另建固定項目文件。
- 使用者看過中間成果後改方向或補限制時，C 先更新活的任務簡報和路線圖差異；若已派批次受影響，使用新的 `batchId`／`payloadDigest` 或先 supersede 舊批次，再交回同一 E1，不沿用過期假設。
- R 驗收依最新任務簡報、本批凍結、候選 identity 及 delivery evidence；不得只按最初 prompt 或過期假設驗收。
- C 的本批凍結和 E1／R 派工都保留三態、必要來源錨點和反事實結果；不得虛構使用者確認。
- 非簡單正式實作批次在派工前，C 能逐項回答真源攝取四問：誰擁有、誰實際使用、如何生效、甚麼反例能推翻；答案只作 Controller preflight 與自足派工摘要，不建立第二個規則 owner。
- C 答不到真源攝取四問任一項，或答案依賴未讀必要真源時，該完成條件是 `關鍵缺失`；C 不派正式實作批次，只做必要唯讀診斷、收窄驗收範圍或停問使用者。

## 成果錨定與進展情景

- 長期多批任務在首批前固定 `outcome_anchor`，保留使用者最終成果、完成條件真源指向、不可接受替代成果及排除範圍；E1 或 R 在後續批次不能自行改寫它。
- 預期成果改善為零且不是必要條件的實作批次被拒絕；C 只可改成診斷、停問或另選能改善完成條件的批次。
- 診斷批次可以執行並產生承接條件，但標為 `diagnostic`，不增加主線進度。
- 技術檢查、格式、檔案一致或審閱通過，但 `outcome_anchor` 沒有已接納成果差異時，不標記為成功進度。
- 同一失敗類別連續兩次未解決後，第三次同類修正版被攔截；改名、換版本、換包裝或同方法重派仍被識別為同類重試。
- R 必須拒絕偏離原始成果、只有技術活動、反覆返工或用另一種交付形式代替使用者原要求的批次。
- `mechanism_improvement` 或 `governance_self_improvement` 不污染主線進度；只有被證明是完成 `outcome_anchor` 的必要依賴時才可成為主線 blocker。
- 相鄰改善失敗不會自動阻塞原任務；C 只能把它另列，或證明其缺失令主線成果不可安全接納。
- 長期、多批或容易受上下文污染的任務，在 resume／上下文轉換、連續兩批沒有已接納成果差異、同類失敗第二次、E1／R 提出相鄰改向或替代交付、使用者改方向或補限制，以及 close／release／重大交付前，C 做一次有界 drift checkpoint；若不能指出下一批改善哪個 `outcome_anchor` 未完成條件、成功後的可讀回成果差異，或 E1／R 相鄰方案是否正在取代主線，C 不派正式實作批次，只可診斷、收窄、停問、終止路線或按風險建立 fresh R。
- drift checkpoint、活的任務簡報或路線圖更新不計作成果進度，不觸發背景 monitoring、polling、自動 `wait_threads`、固定 R 或固定 Full Audit。
- 簡單、單步、低風險且終點唯一的任務仍可用短摘要和 C 讀回驗收，不強制建立成果錨表格、R 或路線圖。
- 任務完成回報列已接納成果差異和未完成條件，不以批次、task、審閱或候選數量作完成證據。

## 未預期失敗與範圍例外情景

以下情景只驗收 [core-runtime.md](core-runtime.md) 的未預期失敗閘門，不另定規則：

<!-- cer-uat-unexpected-failure:gate-off -->
- 普通批次沒有未預期失敗時，閘門完全不啟動；不得增加 baseline、表格或回報程序。
<!-- cer-uat-unexpected-failure:caused -->
- 本批直接造成回歸，而且修正保留凍結語意、owner、來源及權限時，E1 可在本批
  修正；輸出、來源及 owner 不變的純技術重構也可繼續。
<!-- cer-uat-unexpected-failure:preexisting -->
- 可比較的批次前 baseline 證明失敗原已存在時，E1 只回報，不修復。
<!-- cer-uat-unexpected-failure:unknown -->
- 無法取得可比較 baseline，或失敗屬不穩定測試、環境或依賴而因果不明時，E1
  停止進一步寫入，不猜測修復。
<!-- cer-uat-unexpected-failure:semantic-boundary -->
- 檔案雖在允許範圍內，但修正會改變另一 owner、權威來源、fallback、准入條件或
  跨 subsystem 行為時，E1 停止。測試或 allowlist／diff check 只因這些擴張而變綠，
  仍屬假綠。
<!-- cer-uat-unexpected-failure:acceptance-boundary -->
- 直接驗收本身可能錯誤，或完整回歸在直接驗收外失敗時，E1 只歸因及回報，不改
  產品語意迎合測試，也不自動修補相鄰行為；完整回歸屬凍結驗收時可阻塞候選，
  但仍不擴大修補權。

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
- 成功收尾後，已完成、已讀回、已由 C 裁決的 R 可封存，以減少側欄雜亂；
  C／E1 預設保留可見。仍在工作、受阻、未回傳或未裁決的 R 不封存。封存不是刪除，
  不可當作停止、審閱或收尾證據；有封存時，收尾摘要用同一輸出語言說明可在
  已封存任務中找回。
- 每張 CER 小熊卡使用 Handoff Kit 排板風格 ASCII 三行卡；卡片必須作為獨立
  fenced `text` code block 輸出，不得被 Markdown 容器改變排版。
- 每張小熊卡保留完整三行；版本只在第一行，狀態只在第二行，第三行只保留小熊底線。

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
- 平行候選生產者寫 target project、產生正式 ready/result、代替 E／R，或被列為
  CER Reviewer 通過證據。
- E1／R 缺少官方 `create_thread` 建立證據、`create_thread` 後官方 title 工具設定／讀回證據、側欄可見 title、可核實 thread id 或正式回傳路徑，仍開始工作。
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
- 初始 prompt 被當成整輪不可改的完整規格；或使用者已改方向後，C 未更新活的任務簡報和路線圖差異便派下一批。
- E1 把暫定後續意向當成完整規格，自行補做未凍結批次；或 R 只按最初 prompt／過期假設推翻候選。
- 活的任務簡報被寫成另一套流程、固定文件組或新角色，而不是既有 Controller preflight 和路線圖的一部分。
- 本批凍結或派工把無來源推測寫成 `已確認`。
- 非簡單正式實作批次未回答誰擁有、誰實際使用、如何生效、甚麼反例能推翻，C 仍建立／復用 E1 或派實作批次。
- C 把真源攝取門檻擴成預設全文讀取、全 repo 審查、固定 Full Audit、第二份規則 owner 或固定表格流程。
- 關鍵終點、權限或驗收缺失時，C 不停問而直接派工。
- 長期多批任務未固定 `outcome_anchor`，或後續 E1／R 自行改寫最終成果、完成條件、替代成果或排除範圍。
- 預期成果改善為零且不是必要條件的實作批次仍被派出。
- 診斷、候選、審閱、格式通過、檔案一致、問題記錄、設計完成、改名或換版本被自動計作主線成果進度。
- 技術檢查通過但沒有 `outcome_anchor` 成果差異時，C 回報為成功進度。
- 同一失敗類別連續兩次未解決後，C 仍派第三個同類修正版；或用改名、換版本、換包裝掩飾同方法重試。
- R 只檢查本批技術合格，未檢查是否服務原始成果、是否只有活動或返工、是否替代了使用者原要求。
- 通用機制改善或治理自我改善污染主線進度，或其失敗在未證明必要依賴前阻塞原任務。
- 連續兩批沒有已接納成果差異，C 未做 drift checkpoint 仍派主線實作批次。
- E1／R 提出相鄰改向、替代交付或範圍外 blocker 後，C 未分類是否取代主線成果便改寫下一批主線。
- drift checkpoint、活的任務簡報或路線圖更新被計作成果進度。
- drift checkpoint 觸發背景 monitoring、polling、自動 `wait_threads`、固定 R 或固定 Full Audit。
- 簡單、單步、低風險且終點唯一的任務被迫執行 drift checkpoint。
- 完成回報只列批次、task、Reviewer 或候選數量，沒有列已接納成果差異。
- E1 把測試失敗當成新增修改權，或把允許檔案當成可改該檔案所有語意。
- 未預期失敗因果不明，或修正需要擴大 owner、權威來源、fallback、准入條件時，
  E1 仍繼續寫入或以測試變綠冒充正確。
- 完整回歸失敗自動觸發相鄰修補，或 E1 未經 C 重凍結及新批次便擴大範圍。
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
- 正式 `sendable_packet` 仍保留 `<...>` 佔位符，或缺實際 `threadId`／平台等價座標、
  `returnTarget`、`messageId`、`batchId`、`batchSeq`、`payloadDigest` 或當前工具
  schema／receipt 明示必需的路由座標，仍自評 PASS。
- 當前工具 schema 只要求 `threadId` 時，Controller 仍硬性要求 `hostId`，或由
  `local`、title、sessionId、threadId 形狀或錯誤訊息推導 hostId 後自評 PASS。
- 正式派工以 sessionId 代替 threadId 作正式派工座標，或要求接收者由 sessionId
  推導 threadId／hostId 後繼續。
- 正式派工用 `同一 E1`／`上述 E1`／`下一個序號` 等相對說法代替可核實實值。
- R 派工缺實際 `candidateIdentity`、`candidateManifest` 或候選 delivery evidence，
  仍要求 Reviewer 審閱。
- 未證明送達鏈便開始工作。
- 只證明 title、fork 或單向 send，沒有 E1 direct-push ready/result。
- create 結果為逾時、錯誤或部分結果時，在有界權威對帳前立即重試。
- create 結果不明後，立即枚舉為零候選便當成確定失敗並自動再建立。
- pending create 在後續 resume、startup 或建立同 role 前沒有再次權威對帳，
  因而漏掉延遲出現的孤立 task。
- 官方 metadata 與 task 自報 `local` 不一致時，仍以自報別名作權威路由。
- 發現重複角色後，在未證明全部零寫入及未收到正式工作、未收到其餘候選停止
  確認前，已向選定 task 派正式工作。
- 以封存狀態、標題或發出停止訊息代替 task 的 direct-push 停止確認。
- 重複候選既無 direct-push 停止確認亦無官方不可工作終態，仍讓另一候選開始工作。
- 重複 E1 可能已寫入時，沒有恢復唯一 writer 及讀回 workspace 狀態便繼續。
- 正式批次沒有穩定 `batchId`，或未綁定選定 threadId／平台等價座標、當前工具
  schema／receipt 明示必需的路由座標、cycle、target root、單調遞增 `batchSeq`
  與不可變 `payloadDigest`。
- 相同 `batchId` 搭配不同內容或 `payloadDigest`；內容改動後仍沿用舊 `batchId`。
- `BATCH_RECEIVED` 後中斷便把批次當成完成；或不看批次生命週期，一律忽略或
  一律重跑相同 `batchId`。
- `IN_PROGRESS` 中斷或部分寫入後沒有標 `STATE_UNKNOWN` 及恢復 writer／workspace，
  便重跑整批。
- `RESULT_READY` 重複送達時不重播既有結果；或未收到 `RESULT_ACCEPTED` 已永久
  忽略同一批次。
- ready、accept、stop、狀態、結果或結果接納訊息沒有穩定 `messageId`，或
  outcome 不明時盲目重發／永久等待。
- send 結果不明時改用新 `messageId` 或新 `batchId` 規避去重。
- 只在 prompt、派工包、摘要或自稱回執中放入 `messageId`，就把它當成已建立
  thread、開始 turn、呼叫工具、觸發寫入或授權；或沒有實際工具呼叫及可核實工具
  結果／送達證據，仍宣稱訊息已送達或工作已執行。
- 舊批次尚未零寫入取消、終結或完成 writer／workspace 恢復，已派發或開始較高
  `batchSeq` 的新修訂；或延遲送達的 `SUPERSEDED`／較低次序批次仍被執行。
- 以「只有收到 push 後才可讀回」拒絕精確 `messageId` 的有界故障恢復，導致
  outcome 不明永久等待；或反過來以故障讀回冒充完整通訊 preflight。
- 通訊、批次生命週期、唯一 writer、來源新鮮度或證據身份不明時仍啟用自適應加速。
- 被驗對象、需求、直接依賴／環境、交付物、驗證方法或可信反證已改變，仍沿用
  舊證據。
- 只因 `no_material_delta` 或零檔案寫入而略過審閱、證據、稽核或故障恢復。
- 不可逆或高後果行動把本應行動前完成的 fresh R 延後到行動後。
- 合併驗收命令後遺失個別輸出、exit status、來源或裁決，或把依賴次序／共享
  可變狀態的檢查混跑。
- fork 帶入來源上下文卻被當成 fresh UAT。
- assignee 沒有回傳 ready/result 仍宣稱閉環成立。
- 新 task 沒有可見 `E1:`／`R1:` 標題或首行標籤，或 ready／結果回執缺 threadId 或平台等價座標。
- C 派工後自動使用 `wait_threads`／`read_thread` 當接收機制、反覆 event wait、在逾時後再次等待、以輪詢發現成果，或把 wait snapshot、
  task 完成狀態、commentary／摘要當成 ready/result 證據。
- `BATCH_RECEIVED` 的等待錯誤消耗最終結果的等待額度，令已 direct-push 結果
  無法推進。
- 相同 `messageId` 受控重送被當作全新邏輯 send，因而可無限重開 event wait。
- 平台需要 event wait 才能喚醒 idle C，但 C 絕對禁止單次有界 event wait，
  導致已 direct-push 的 READY／結果無法推進。
- 知識性複雜任務沒有界定知識底座，或 R 只查格式、不反證專業主張。
- 每個內部小步都發卡，或重大裁決／阻礙／階段交付時沒有發卡。
- 小熊卡沒有先讀本 Skill 的 `VERSION`，把 `v1` 當 package 版本，或從網路、
  Git tag、GitHub Release／lock metadata 猜版本。
- `VERSION` 缺失、不可讀或格式錯誤時沒有顯示 `version unverified`。
- 啟動卡不保留完整三行 ASCII 小熊、沒有把版本放第一行、沒有把狀態放第二行，或第三行不是只保留小熊底線。
- 任何 CER 小熊卡不是獨立 fenced `text` code block，或因 Markdown 容器而走位。
- release／upgrade 沒有先更新 `VERSION`。
- 單批 `CER-start` 沒有固定啟動卡，或啟動卡錯用閉眼小熊。
- stop／close 尚未證明 writer 停止或必要讀回完成，卻顯示閉眼成功卡；close 在
  title sync 或 `title sync warning` 讀回前顯示閉眼卡；title rename 失敗卻宣稱已
  改名；受阻時沒有使用開眼紅色 blocker 卡。
- C 把仍在工作、受阻、未回傳或未裁決的 R 封存，或預設封存 C／E1。
- C 封存 R 後沒有明講封存不是刪除，或把封存狀態當成停止、審閱或收尾證據。
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
- 預設提示把 fresh Reviewer 寫成每次、每項或所有任務都必須建立。
- CER 自行建立固定五份項目文件或平行進度。
- 把 `$project-context-workflow` 當作 CER 安裝前置。
- `/CER-stop` 後仍繼續派新 E1/R，或未證明 active writer 停止便當作已回到單 thread。
- `/CER-status` 觸發輪詢或背景監察。
- 只做到文件或局部技術成功，沒有真實成品。
