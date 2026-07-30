# CER Core v1 執行核心

## 目錄

- [角色](#角色)
- [知識底座](#知識底座)
- [小熊卡 package 版本](#小熊卡-package-版本)
- [操作指令](#操作指令)
- [Controller preflight](#controller-preflight)
- [工具結果不明、角色對帳與批次去重](#工具結果不明角色對帳與批次去重)
- [啟動](#啟動)
- [自足派工](#自足派工)
- [送達](#送達)
- [執行閉環](#執行閉環)
- [自適應批次加速](#自適應批次加速)
- [YAGNI 與停止](#yagni-與停止)
- [獨立持久化與收工](#獨立持久化與收工)
- [停用 CER](#停用-cer)

## 角色

- Controller（C）：經本地或 Remote 啟動閘門接納的唯一主控者。負責全局判斷、真源映射、批次裁決、候選讀回及使用者溝通。C 不寫 workspace。
- Executor（E1）：每輪 `CER-start` 由官方 `create_thread` 在同一 Codex project
  建立的側欄可見獨立新 task/thread，也是本輪唯一 writer。同一輪後續批次持續
  復用該同一 E1；E1 只執行 C 的自足批次，驗證後回報候選。
- Reviewer（R）：只在高風險、核心承諾、資料完整性、安全、外部能力不確定，或
  C 不能可靠反證時建立。每個 R 都必須由官方 `create_thread` 建立為 fresh
  新 task/thread，唯讀、有界，不改檔、不指揮 E1，不可沿用舊 R。
- E2：只有原 E1 已確認停止寫入、工作區可判定且 C 發出接管批次後，才可由官方
  `create_thread` 另建新 task/thread。不得存在平行 writer。

CER 正式角色只有 C、E1、R、E2。C 可按
[平行候選生產者](parallel-producers.md) 使用 inline、非正式、按需能力，但它
不是第五角色，不改變唯一 E1 writer、fresh R 或 E2 接管邊界。完整啟動、
隔離、候選合流及 fail-closed 規則只由該 reference 擁有。

## 知識底座

CER 不限於工程任務。凡任務依賴醫療、法律、金融、投資、政策、學術、商業、
設計、營運、內容或其他專業知識，C 必須先按風險界定知識底座：領域範圍、
權威來源、術語、資料年度或版本、品質標準、不可由 AI 代選的取捨，以及需要
揭露的不確定性。已有專案真源或使用者提供來源時優先沿用；缺關鍵來源時停下
標示未知，不用一般常識補成專業結論。

E1 的派工包只包含本批所需的知識底座摘要、來源座標與禁止越界範圍。R 的工作
是依同一知識底座獨立反證高風險主張、來源使用、推論和結論，不只檢查格式。
簡單低風險任務不為知識底座建立文件；必要內容直接放入自足派工或停點說明。

## 小熊卡 package 版本

每次顯示任何 lifecycle 或 checkpoint 小熊卡前，先讀本 Skill 根目錄、與
`SKILL.md` 同層的 `VERSION`。只接受完整內容符合穩定 semver
`X.Y.Z`；有效時在卡頭渲染為 `vX.Y.Z`。`VERSION` 缺失、不可讀或格式錯誤時，
卡頭顯示 `version unverified`。

不得回退為 `v1`，也不得用網路、Git tag、GitHub Release、`skills` CLI lock
metadata 或其他外部狀態猜版本。`CER Core v1` 只表示工作流世代。每次 release
或 upgrade 必須先更新 `VERSION`；更新整個 Skill 後，下一張卡自然讀到新版本。

## 操作指令

CER v1 接受自然語言和 slash command 兩種入口。slash command 是穩定文字別名，
方便在 AI terminal、snippet、Snap 或可搜尋指令面板中保存；平台不支援時，直
接貼上同一句仍有效。

| 指令 | 自然語言 | 效果 |
|---|---|---|
| `/CER-start <任務、限制、優先序>` | `CER 啟動：...`／`CER 開始：...`／`CER 開工：...` | 啟動 CER v1；由本地使用者 task 成為 C，或由明確指定的 Remote 接收 task 在 `C_READY` 閉環成立後成為該 target_root 的唯一 C。單獨 `開工` 不啟動 CER。 |
| `/CER-stop` | `停止 CER，改用單 thread 繼續。` | 停用 CER mode，不再派新 E1／R；若 E1 已在寫入，先要求 E1 停止或回傳可判定狀態。 |
| `/CER-close` | `CER 收工。`／`CER 關閉。`／`關閉 CER。` | 完成 CER 收尾；同一 E1 只按既有真源回寫必要狀態並標 writer closed。單獨 `收工` 不觸發 CER close。 |
| `/CER-status` | `顯示 CER 狀態。` | 報告 C 已知的目標、C／E1／R 座標、下一停點和阻礙；不得為狀態而輪詢。 |
| `/CER-help` | `顯示 CER 指令。` | 顯示可用指令與自然語言等價句。 |

## Controller preflight

在建立本輪 E1、復用同輪既有 E1，或派任何實際 E1／R 批次前，C 先完成適應式任務契約。它不是表格儀式；簡單低風險且終點唯一的任務可只在內部完成並以短摘要直接工作。長期、多批，或新產品、流程、設計、內容、體驗型成果，則把必要答案濃縮進首次公開對齊的初始路線圖與自足派工。

C 只判斷五項，每項標成 `已確認`、`可安全推定` 或 `關鍵缺失`：

- 終點：可觀察終點是甚麼，哪些明確不做。
- 真源：完成判斷前必讀甚麼，已讀甚麼，仍有哪些關鍵未知。
- 根因與邊界：為何需要 CER；最小可驗收 E1 批次是甚麼。
- 權限與停點：哪些由 AI 自行處理，是否需要首次公開對齊，以及哪些真正需要使用者裁決或停止。
- 驗收與比例：甚麼證據可推翻方案；驗收是否剛好足夠，是否已變成防禦性擴建。

三態判定必須有證據邊界。`已確認` 只可來自使用者明示或已讀權威真源，C 必須能指出來源錨點；沒有來源的推測不得標成 `已確認`。`可安全推定` 必須通過反事實測試：若相反假設成立，仍不會實質改變交付物、使用流程、協作方式、資料處理、權限／風險或驗收，也不會造成重大重做，才可通過；若多個合理答案會導致實質不同成果，該項就是 `關鍵缺失`。

派工前，C 做一次短 QC：逐項核對 `已確認` 是否有來源、`可安全推定` 的反事實結果是否成立，以及凍結任務契約沒有把推測升格為 `已確認`。QC 失敗時，C 不得建立／復用 E1，也不得派實際批次；只能先做必要唯讀調查，或用 `🟡 使用者裁決` 最多問三個會實質改變結果的問題。

`關鍵缺失` 代表 C 不能安全判斷或派工。此時 C 只可先做必要唯讀調查；若仍缺少會實質改變結果的資訊，用 `🟡 使用者裁決` 最多問三個問題。preflight 通過後，C 才做通訊座標與 ready 驗證。E1／R 派工使用同一份凍結任務契約，只能回報矛盾、阻礙或候選修正，不能自行擴大目標、真源、權限或驗收。

驗收有效性與比例原則在 C 每次作成或沿用驗收、修補或發布結論前都再次套用，不是預設重跑驗證。
C 先指出具體結論、支撐該結論的證據及其前提。既有證據只在被驗對象、需求、
直接支撐結論的依賴與環境前提、交付物與驗證方法仍適用或已驗證等效，且沒有可信反證時可保留；
全新脈絡不能假定不可讀的舊證據仍有效。任一前提失效時，只為受影響結論重建最小充分證據；
只有可追溯的前提到結論因果鏈、跨表面耦合、累積互動、
source／package mismatch 或發布／安裝產物不一致，或可信理由顯示舊驗證假綠，才擴大
範圍。廣度跟因果覆蓋走，深度跟失敗後果與證據不確定性走；任務標籤、檔案數、改動
大小或 `high risk` 字眼本身，都不能擴大或縮小驗收。此規則只在證據已知後界定範圍；
不取代用針對性檢查發現不穩定外部聲稱，或驗證真實發布／安裝產物。

## 工具結果不明、角色對帳與批次去重

本節適用於有副作用的 task/thread 建立，以及 ready、accept、stop、正式派工、
批次狀態、結果與接納等控制訊息。C 對每次操作只使用
`confirmed`、`pending`、`outcome_unknown`、`duplicate`、`blocked` 五種狀態；
工具回報失敗、逾時、部分結果或非權威別名時，不得直接判定操作沒有發生。

- 建立角色前，C 先對本輪實際參與 host、project、target root、cycle 與 role
  做一次有界建立前快照。快照只供本次對帳，不得演變成 lock、central registry
  或 CER run ID。
- 只有官方 receipt 或權威讀回同時給出 threadId、目前實際 hostId、project
  與 target root，建立才是 `confirmed`。只有 `clientThreadId`、逾時、錯誤或
  部分結果時，操作是 `pending` 或 `outcome_unknown`，不是確定失敗。
- `outcome_unknown` 禁止自動重試。C 只做一次有界控制面對帳：比較建立前快照，
  在全部實際參與 host 的官方 task/thread 列表中，以 project、target root、
  cycle、role 及建立意圖匹配候選。一次對帳可包含平台已知 settle interval
  前後兩次權威快照；這是故障恢復，不是輪詢工作結果。
- 穩定期後零個候選仍只可把建立操作標成 `blocked`，不得自動再建立；其
  pending operation 必須在任何後續 resume、startup 或新建同 role 前先重做
  一次權威對帳，以捕捉延遲出現的孤立 task。一個候選須再以官方 metadata
  及零寫入 `ready` 確認；多於一個候選即 `duplicate`。
- 路由座標以 C 讀回的官方 threadId 與目前實際 hostId 為準，不信任 task
  自報的 `local` 或顯示別名。`ready` 仍須自報角色、target root 及回傳目標；
  與官方 metadata 不一致時先對帳，不派正式工作。
- 發現重複角色時，所有候選保持零寫入。只有全部候選都證明未收到正式工作且
  零寫入，C 才可選定一個；其餘候選收到 `STOP_ZERO_WRITE` 後，須以 direct-push
  停止確認或官方可讀的不可工作終態證明停止。archive、title 或發出停止訊息
  本身都不是停止證據；無法取得任一停止證據即 `blocked`，不得以可用性理由放寬。
- 任一重複 E1／E2 可能已收到正式工作或寫入時，C 停止所有新派工，讀回 writer
  與 workspace 狀態。先以穩定 `messageId` 向全部可能 writer 發停止指令，再以
  direct-push 或官方終態讀回證明全部已停止；接着判定已寫表面、候選成果及
  workspace 一致性。只有狀態可判定後，C 才可選定其中一名恢復，或在全部舊 writer
  已停止後依既有接管規則建立 E2；不得自動回滾或簡單選一個繼續。
- 每個正式批次使用本輪唯一且穩定的 `batchId`，綁定 cycle、角色、C 選定的
  threadId、目前實際 hostId、target root、該接收者本輪單調遞增的 `batchSeq`
  及不可變 `payloadDigest`。digest 覆蓋完整自足派工內容；內容或任務契約有任何
  改變便使用新 `batchId` 及較高 `batchSeq`。受控重送只能重送完全相同的
  `batchId`、`batchSeq`、`payloadDigest` 及內容。
- 接收者為每個 `batchId` 判定 `RECEIVED_ZERO_WRITE`、`IN_PROGRESS`、
  `RESULT_READY`、`RESULT_ACCEPTED` 或 `STATE_UNKNOWN`，並以 task/thread 歷史及
  workspace 讀回作恢復證據。首次核對綁定後 direct-push `BATCH_RECEIVED`，
  再開始實質工作；開始寫入前標成 `IN_PROGRESS`，結果固定後標成 `RESULT_READY`，
  收到 C 的 `RESULT_ACCEPTED` 後才標成 `RESULT_ACCEPTED`。
- 相同 `batchId` 再次送達時，`RECEIVED_ZERO_WRITE` 可繼續原批一次；
  `IN_PROGRESS` 只回 `BATCH_IN_PROGRESS` 而不重啟；`RESULT_READY` 重播同一結果；
  `RESULT_ACCEPTED` 才回 `DUPLICATE_IGNORED`。中斷後無法證明狀態時標成
  `STATE_UNKNOWN`，停止寫入並先做 writer／workspace 恢復；相同 `batchId`
  但 `payloadDigest` 不同一律 `blocked`。
- 若新批次取代尚未終結的舊批次，C 先以穩定 `messageId` 發
  `BATCH_SUPERSEDE`，列明舊／新 `batchId` 與 `batchSeq`。接收者先記錄舊批次
  `SUPERSEDED`，使其任何延遲送達都被拒絕；若舊批次已開始或可能寫入，先停止
  並完成 writer／workspace 恢復。C 只有收到 `BATCH_SUPERSEDED`，且舊批次已證明
  零寫入取消、已終結，或恢復完成後，才可派發／開始新修訂。接收者拒絕任何低於
  已接受最高 `batchSeq` 的未授權批次。
- 所有 ready、accept、stop、批次回執、狀態、結果及結果接納訊息都使用穩定
  `messageId`，綁定訊息種類、sender、recipient、相關 `batchId` 如有，以及
  不可變訊息內容。接收者按 `messageId` 去重；重複訊息重播既有確認，不重做副作用。
- 任一控制或結果 send 為 `outcome_unknown` 時禁止盲目重發。先以 operation receipt、
  已收到的對應確認，或一次有界目的地／thread 讀回尋找相同 `messageId`；仍無法
  證明時，只有接收者身份仍唯一且具訊息去重，才可用相同 `messageId` 及完全相同
  內容受控重送一次，否則 `blocked`。故障恢復讀回是「不監察」規則的有界例外。
  此例外同時覆蓋送達段的「收到 push 後才讀回」及啟動段禁止以事後 read 冒充
  通訊驗證的限制，但只可證明該 `messageId` 的送達；它不能單獨證明整條 ready／
  accept 通訊鏈成立。
- C 收到並裁決結果後，以穩定 `messageId` 回 `RESULT_ACCEPTED`。結果送達或
  `RESULT_ACCEPTED` 結果不明時，重送與接收端均按相同訊息身份去重，避免結果遺失
  或接納兩次；不得建立無限 receipt-of-receipt 鏈。
- 平台日後提供 idempotency key 或權威 operation receipt 時，以其為優先證據；
  CER 不假裝平台已有此能力，也不把該 key／receipt 變成 CER lock 或 run ID。

## 啟動

1. C 讀目前安裝的 CER 執行規則、使用者總任務、明示限制及目標 workspace 實際存在的權威規則。
2. 啟動閘門由 Remote 發送方或本地啟動 task 負責；接收 task 只能回 candidate `C_READY`，不得只因訊息來自另一 task 而全面拒絕 Remote C，也不得用沉默、沒有回應或自己看不到其他 task 來證明唯一 C。
3. 啟動閘門只在本次實際協作域判定唯一 C：用官方 task／thread 列表或平台等價工具，枚舉此啟動會使用的每個參與 host；對可讀候選核實 resolved target_root／cwd、`🚀 C:` 身份及 active／idle／closed／handed-off 狀態；再加上發送方明示自己沒有把同一 root 交給另一 C。所有參與 host 都可枚舉且沒有 active C，才可判 no active C；不掃描平台外或未參與 host，也不得把不可見 task 當不存在。
4. 同一輪已知 active C 只可沿用；轉移須有舊 C 明確 handoff／close 的實際訊息或狀態讀回。完成 `/CER-close` 的舊 C 及其 E／R task 整組只可保留作歷史，不可接收同一 workspace 新一輪工作。新一輪只能由新 task 成為 C；閘門必須讀回舊 C 已 `closed`／`handed-off`、沒有 active C，且所有參與 host 可核實。任一參與 host 不可枚舉、舊 C 狀態或候選 root／身份／狀態不可讀回、座標不完整或證據衝突，即為 unknown 並停止，不建立第二 C。
5. Remote 接收 task 收到明確 Remote CER 啟動語意後，先 direct-push candidate `C_READY`，必含自身 threadId、hostId、target_root、return target／path。發送方完成唯一性核實並實際讀回 `C_READY` 後，必須以同一可用回傳路徑向接收者發 `C_ACCEPTED`；接收者收到 `C_ACCEPTED` 後才成為 active C 並做 Controller preflight。只發送 `C_READY`、未讀回 `C_READY` 或未收到 `C_ACCEPTED`，Remote C 身份及通訊路徑都不成立。若發送方原本是 active C，須先完成 handoff／close 才可發 `C_ACCEPTED`。
6. 不得為唯一 C 新增 lock file、central registry、run ID、conflict engine、新角色或測試例外；唯一性只靠已存在真源、官方枚舉、明示座標與本輪實際回傳／讀回證據判定。
7. C 為每輪 CER-start 分配 project 內側欄辨識用短 cycle 編號。規則生效後的新 cycle 不得使用 `00`，必須用官方 project task/title 枚舉讀回既有數字 cycle 標籤，選下一個未使用正整數，至少兩位顯示為 `01`、`02`；超過 99 可自然擴展。不得新增 central registry、lock 或 run ID。`00` 只表示 cycle numbering 規則生效前已開始、無法可靠回推原 cycle number 的 legacy/migration cycle；它和其他 cycle 編號一樣只供顯示，不是 lock、run ID、唯一 C 證據或 thread 身份，完整 threadId 仍是權威。若新 cycle 無法可靠枚舉或設定 title，保留最短 role title 並報真實 `title sync warning`；不得顯示問號 cycle 標籤、不得猜測數字，也不得因顯示標籤失敗冒充 lifecycle 或 identity failure。C 命名或識別自身可見 task／thread 為 `🚀 C:01｜<極短任務名>`；平台不能改 title 時，在首則可見訊息或停點卡首行標示同等角色標籤。單獨 `C:` 不是合格 Controller title／label。
8. C 完成 Controller preflight，凍結本次任務契約；若有 `關鍵缺失`，只做必要唯讀調查或停問，不建立／復用 E1，也不派實際批次。
9. Controller preflight 通過後，C 完成通訊 preflight：以可用工具證明本次實際採用的路徑可用，包括身份來源、目標 root、必要參數、發送路徑、接收者、可見標題或角色標籤、assignee 可取得的回傳來源、可核實 session／thread id 或平台等價座標，以及 C 的裁決點。
10. 若官方 `create_thread` 新建 task 工具不可用，或無法讀回側欄可見 title、可核實 thread id 與正式回傳路徑，E／R 委派即阻塞；不得降級用 inline sub-agent、fork、delegate 或既有 task 冒充正式 E／R。
11. 新建 E1／R／E2 時，標題或首行標籤必須分別以 `E1:01｜<極短任務名>`、`R1:01｜<極短審閱名>`／`R2:01｜...`、`E2:01｜...` 格式開首，不加 `🚀`；角色序號在冒號前，cycle 編號在冒號後，避免把第二輪 E1 誤作 E2。同輪所有 C／E／R 使用相同 cycle 編號，下一輪使用新 cycle 編號；legacy/migration cycle 可用 `00`。每個派工包和 ready／結果回執都要包含發送者角色、接收者、回傳目標、session／thread id 或平台等價座標。
12. C 透過官方 `create_thread` 建立本輪全新持久 E1。E1 先零寫入 direct-push `ready`；C 必須實際收到含正確角色、cycle 編號、側欄可見標題／標籤、thread 座標和回傳目標的合格零寫入 `ready`。同一輪後續批次持續復用該同一 E1 且 E1 threadId 保持相同；完成上一輪 `/CER-close` 後的新一輪必須建立全新 E1、使用新 cycle 編號，所有 R 也必須 fresh；不得復用上一輪 closed C 的任何 E／R task 或座標。
13. 任一通訊 preflight 環節缺失，或 assignee 沒有實際 direct-push 合格零寫入 `ready`，C 只顯示開眼 `🔴 重大阻礙` 卡並停止；不得顯示成功啟動卡，也不得用 wait snapshot、完成狀態、commentary、輪詢、事後 read、文件審閱、fork 建立成功或單向 send 成功冒充通訊驗證。平台需要事件等待才會喚醒 idle C 時，只可依「送達」使用一次有界 event wait，真正 `ready` 仍須以 direct-push 到達。
14. 到此才算成功接受 `CER-start`。C 的第一個使用者可見成功回執必須是 [roadmap.md](roadmap.md) 的固定開眼 `🔵 CER 已啟動` 卡；保留完整三行小熊，版本與狀態在第三行小熊腳後以固定 `·` 分隔，不另起一行。單批與多批都相同；不得用閉眼卡或猜測版本。
15. 同一輪、同一 C、同一 E1、同一回傳目標、同一可核實座標的後續批次不重做握手；座標或回傳目標改變即重做 ready。
16. C 判定為長期、多階段、多批次，或需要首次公開對齊的任務時，在固定啟動卡後、第一批前依 [roadmap.md](roadmap.md) 顯示初始進度面。簡單單批且終點唯一的任務只顯示短摘要，不強制建立路線圖。
17. 只有固定啟動卡已顯示，且所需的初始路線圖或短摘要已補上後，C 才可派第一個實際批次。

若使用者沒有明示 CER，而工作只是低風險單一步驟，可按普通工作處理；一旦明示 CER，不能以「任務簡單」靜默取消角色拓撲。單獨 `開工` 屬於目標 workspace 既有治理，不是 CER trigger。

## 自足派工

每個 E1／R 實際批次只包含必要內容：

- 角色與單一目標；
- 目標 root；
- 必讀真源與已裁決背景；
- 允許及禁止範圍；
- 驗收與能推翻方案的反例；
- 停止條件；
- 本批穩定 `batchId`、單調遞增 `batchSeq`、不可變 `payloadDigest`，以及所綁定的 cycle、接收者 threadId、目前實際 hostId 與 target root；
- 凍結任務契約，以及任何 `已確認`、`可安全推定`、`關鍵缺失` 的處置、必要來源錨點和反事實結果；
- 回傳 C 的 direct-push 目標、session／thread id 或平台等價座標；
- 本批需要的知識底座、來源座標、未知與禁止越界範圍；
- 短回報要求。

不得寫「見上文」或要求 assignee 自行重建 C 的上下文。高風險批次補足背景與反例；低風險小修改保持短，不套巨型表格。E1／R 發現凍結契約與真源矛盾時，先回報 blocker 或候選修正，不自行改寫契約後繼續。

CER 已啟動時，若目標 workspace 的 `AGENTS.md` 把使用者語意明確路由為
Agent Handoff Kit full closeout（例如 `收工`、`Wrap up Agent Handoff` 或同等
session closeout 意圖），或把指定文件明確路由為 governance bridge，C 只把
使用者原始指令、目標 root、同一 E1 與回傳座標、指定文件如有，以及尚未
持久化而該工作流必須知道的已裁決狀態交給同一 E1。C 不得重述、拆解、擴張、
預判、預先執行或另建該工作流的程序、checklist、檔案清單、maintenance 判斷、
測試或完成聲稱；E1 自行依目標 `AGENTS.md` 路由出的現行權威執行，完成或受阻後
direct-push 實際終態。

Kit full closeout 只有在其權威終態證據成立後，C 才處理 CER title `✓` 與收尾卡；
受阻時不得聲稱 `writer closed`。同一 E1 已回傳可核實的 Kit 權威終態後，C 只作
必要成果讀回，不重跑 Kit 程序或檢查；證據缺失或矛盾時才回同一 E1 補證。
Governance bridge 完成後只作一般成果讀回與裁決，CER 保持啟動。
`/CER-close` 仍只是 CER 指令，不反向觸發 Kit full closeout。

## 送達

- E1／R 工作前以正式送訊工具 direct-push 零寫入 `ready`；收到正式批次後，再以該批 `batchId` 及 `payloadDigest` direct-push `BATCH_RECEIVED`，依批次生命週期開始或恢復工作。
- `ready` 必須回傳自身角色、可見標題或首行標籤、session／thread id 或平台等價座標、收到的目標 root、回傳目標及是否具備必要來源。所有訊息都帶穩定 `messageId`；`BATCH_RECEIVED` 還須回傳目前實際 hostId 與綁定核對結果。
- 完成、受阻或未完成時，先 direct-push 短結果給 C，再停止；結果回執帶 `messageId`、`batchId`、`payloadDigest` 及 session／thread 座標，避免 C 將另一個 task、另一批或另一修訂的結果誤接納。C 裁決後回 `RESULT_ACCEPTED`。
- 相同 `batchId` 重複送達時，接收者依 `RECEIVED_ZERO_WRITE`、`IN_PROGRESS`、`RESULT_READY`、`RESULT_ACCEPTED` 或 `STATE_UNKNOWN` 恢復，不得盲目重做；相同身份但不同 digest 立即阻塞。
- 除非某參與者已觀察到明確 `outcome_unknown` 並依本節故障恢復規則讀取精確
  `messageId`，C 只有收到 push 後才做一次有界讀回及裁決。故障讀回不可擴成
  waiting、polling 或背景監聽。
- 若平台不會自動以跨 task 輸入喚醒 idle C，C 可對每個已聲明的預期
  direct-push 狀態轉移，以該次已知唯一 threadId／hostId、目前 cursor、因果
  `messageId` 及預期訊息種類形成 `eventWaitKey`，啟動一次有界 `wait_threads`
  或平台等價 event wait。建立後的 `ready`、正式批次後的 `BATCH_RECEIVED`、
  `BATCH_RECEIVED` 後的最終結果、stop 後的停止確認各是不同狀態轉移，可各有
  一次初始等待。等待只保持接收端可被 direct-push 喚醒；
  wait snapshot 內的完成狀態、commentary、摘要或檔案聲稱都不是 ready/result
  證據。真正 direct-push 必須成為接收端的實際輸入或有權威 receipt。
- event wait 被符合 `eventWaitKey` 的 direct-push 中斷後，該狀態轉移完成；下一個
  已聲明轉移可用新的 key 及最新 cursor 建立自己的等待。逾時而沒有相符 push 時，
  該 key 改標 `pending` 或 `outcome_unknown` 並先做有界對帳；不得只因 commentary、
  task 完成或不相干輸入而把轉移當完成。
- 同一邏輯訊息的受控重送不算新的正式 send。只有對帳後依本節允許的唯一一次同
  `messageId`、同內容重送，才可為同一 `eventWaitKey` 建立一次 `recovery` 等待；
  recovery 再逾時即 `blocked`。新的邏輯操作或下一個合法批次生命週期轉移才使用
  新 key，不得以額外控制訊息或改名重開等待額度。
- 「不監察」禁止反覆 waiting、polling、背景監聽、反覆狀態探測、把 wait snapshot
  當成果，以及未收到 push 的被動 thread read；上述單次有界 event wait、使用者
  明示的一次有界 read，或 push 後的核對 read，不在禁止範圍。
- 送達不可用只阻止委派；C 仍可做獲授權的唯讀研究、分析與裁決，但不能代替 E1 寫入。

## 執行閉環

1. C 依使用者任務及目標專案已確認的計劃／真源，給本輪同一 E1 一個批次。
2. E1 只完成本批，讀回、測試並 direct-push 候選。

<!-- cer-unexpected-failure-gate-owner -->
未預期失敗不會改變本批授權：測試只產生證據，不增加修改權；檔案在允許範圍內，
也不代表 E1 可改變該檔案內其他 owner、權威來源或受保護語意。
普通批次沒有未預期失敗，或失敗不會促使新增／擴大寫入時，不啟動本閘門。

任何因未預期失敗而新增或擴大寫入前，E1 先做有界唯讀歸因：

- 有可重現證據證明失敗由本批直接造成，而且修正不改變凍結的 owner、語意、來源、
  權限或驗收：可在本批修正；
- 可比較、可核實的批次前 baseline 證明問題已存在：只回報，不修；
- 無法證明因果，失敗來自不穩定測試、環境或依賴，驗收本身可能錯誤，或修正需要
  改變另一 owner、權威來源、准入條件、fallback、產品／專業語意或跨 subsystem
  行為：立即停止進一步寫入，向 C 回傳目前成果、已跑檢查、未知與 blocker。

直接驗收判定本批候選是否可接納；完整回歸只用來發現整合風險，失敗不自動授權
相鄰修補。即使完整回歸已列入凍結驗收，它也只會阻塞候選，不會擴大 E1 的修補權。
只有 C 可重凍結契約，並用新的 `batchId`／`payloadDigest` 派發新批次來擴大範圍；C 凍結結果與語意邊界，不指定逐行實作。

3. C 讀回實際成果，按風險自行裁決或用官方 `create_thread` 建立 fresh R。
4. R 只驗指定風險及成品邏輯，不只驗格式。
<!-- cer-review-convergence -->
5. R 首次指出缺陷後，C 先按共同根因和使用者後果合併同類發現；只做一次有界唯讀影響檢查，找齊承載本輪合約的現行真源、交付面與檢查位置。
6. C 凍結本輪 `owner／affected surfaces／acceptance／counterexample family`，給同一 E1 一個批次修完整個受影響邊界。
7. 修後 R 只重驗凍結範圍。若出現不同根因、不同使用者後果或最新修補造成的新回歸，只有 C 可在歸因後重凍結並另派新批次；E1 不得自行擴大。
8. 換字、換句序或同義改寫仍屬同一問題；不得逐句追加規則或 validator pattern。若同一反例家族持續避過機械檢查，C 改變檢查方法或收窄 validator 聲稱能力。
9. 凍結反例通過且沒有實質新缺陷後，C 接納；只有此時才由 E1 更新目標專案既有的權威進度來源，沒有進度來源便不自行創造。
10. 必要狀態收斂後 C 停止；相鄰改善另列，不增加 Reviewer、治理層或全 repo 重審。
11. 長期、多階段或多批次任務的進度更新與小熊停點分工一律依 [roadmap.md](roadmap.md)；只用 direct-push 後已讀回及已裁決事實，不輪詢 E1。

普通小修改由 C 讀回加相稱測試即可。高風險修補只重審受影響邊界；不得用更多 R 代替清楚驗收條件。

## 自適應批次加速

自適應批次加速是 C 的預設內部排程，不是使用者模式、Turbo 設置或 slash command。
它不改變 C／E／R 角色、唯一 writer、安全門檻、獨立審閱或驗收標準：

- C 以 checkpoint 建立證據有效期。只有被驗對象、需求、直接依賴與環境前提、
  交付物、驗證方法仍相同或已證明等效，而且沒有可信矛盾時，才可跨相依工作
  共用一次讀取與定位。fresh R 必須從凍結的原始證據自行讀取，C／E 摘要不可
  代替 R 的獨立證據。
- `no_material_delta` 只可在目前權威讀回已證明驗收成立時，停止原定寫入批次。
  證據收集、審閱、稽核或故障恢復批次，不得只因沒有檔案寫入而略過。
- 同一 checkpoint 的新事實可集中收集，C 最多統一推進一次有效期；任何需求、
  來源、依賴、環境、交付物、驗證方法或可信反證改變，都立即令受影響結論失效
  並重開最小充分證據。
- 相容的驗收命令與反例可合併排程，但每項檢查仍保留獨立輸出、exit status、
  來源與裁決。依賴執行次序、共享可變狀態、互斥資源或會互相污染的檢查必須分開。
- 每個穩定風險邊界只建立一名 fresh R，讓其審閱完整候選；不可逆或高後果行動
  必須在行動前完成相應 R，不能為了批次合併延後。凍結邊界修補後可由該輪 R
  重驗，不逐小步建立新 R。
- 通訊或批次生命週期為 `pending`／`outcome_unknown`／`duplicate`／`STATE_UNKNOWN`、唯一 writer 不明、來源新鮮度
  或證據身份不明、需要使用者裁決，或出現可信矛盾時，加速自動停用並回到一般
  CER 規則。`/CER-status` 可報 `active`、`partial` 或 `off` 及原因，但不得為此輪詢。

## YAGNI 與停止

- 角色、批次、R、停點、測試及同步動作只按本次風險和交付需要增加。
- 能由 C 讀回和相稱測試可靠驗收的，不建立 R；能窄修的，不重審所有已接納部分。
- 已達需求、核心反例通過、必要風險清零後停止；相鄰改善另列，不自動擴張。
- 若代理與治理成本壓過任務價值，縮減協作結構，不以更多程序補償不清晰驗收。

## 獨立持久化與收工

CER Core v1 不規定項目文件。它沿用目標專案既有的權威計劃、進度及決策真源；
沒有持久真源時，不假稱新 session 可恢復完整狀態。

CER-close 的完成條件固定，取證方式按實際情況調節：

- 已知本輪 C／E／R 的完整 threadId 或平台等價座標時，直接向這些角色讀回終態；
  不先枚舉整個 project 的 task。只有座標不完整或互相矛盾、writer 狀態不明，
  或目標專案另有明文要求時，才在相關 project 範圍枚舉並擴大讀回。
- E1 只更新目標專案既有且本次收尾確有需要的真源；不固定要求 handoff、log、
  進度表或任何文件組合。沒有需要更新的持久真源時，只讀回實際交付與
  `writer closed`。
- 純狀態收尾預設只做可證明終態的針對性結構與內容讀回。只有本輪改動了治理、
  schema 或核心流程，出現可信矛盾／假綠、source 與交付物不一致，或專案規則
  明定時，才執行相應完整 validator／doctor。
- 不因指令名稱是 close 而建立 Reviewer。只有收尾結論本身涉及需要獨立反證的
  高後果風險時才建立 fresh R；檢查廣度按因果覆蓋，深度按失敗後果與證據
  不確定性調節。

使用者向 C 明示 `CER 收工`、`CER 關閉`、`關閉 CER` 或 `/CER-close` 時：

1. C 停止新派工，裁決可安全裁決的候選，整理已接納、未完成、風險、證據和下一步。
2. C 給同一 E1 一個自足收工批次。
3. E1 只按目標專案既有規則回寫必要進度／決策真源，標示 E1 已停止寫入，讀回後 direct-push；若沒有持久真源，只回報實際交付與 writer closed。
4. C 讀回實際交付、必要真源及 `writer closed` 後，先用官方 title 工具自動把本輪所有可核實 C／E／R title 的 cycle 編號後加 `✓`，例如 `🚀 C:01✓｜...`、`E1:01✓｜...`、`R1:01✓｜...`；legacy/migration `00` 同樣可改為 `00✓`。C 必須讀回 title。這是 CER-close 內建 display-only rename，不另問使用者；不改 threadId、內容或歷史。rename 部分或全部失敗不推翻已證明的 writer close，但必須如實報 `title sync warning` 與失敗座標，不得宣稱已改名。
5. 完成 writer close、必要讀回及可完成的 title sync／warning 後，才顯示 [roadmap.md](roadmap.md) 的固定閉眼 `🟢 CER 已收尾` 卡，卡頭使用本次讀到的 package 版本並保留 `writer closed`，再告知使用者結果、title sync warning 如有，以及延續限制。閉眼卡只代表 writer close／必要讀回完成，不代表 title sync 全綠。沒有 writer closed 或必要讀回未完成時，只顯示開眼 `🔴 重大阻礙` 卡，不得顯示閉眼收尾卡。
6. 成功收尾後，該輪 C／E／R task 整組轉為只讀歷史座標，不可接收同一 workspace 下一輪工作。下一輪須由新 task 重走唯一 C 閘門、建立全新 E1，且所有 R 都 fresh。

新 session 只可從實際存在的目標專案真源恢復；證據不足便標示 continuity limited。若無可核實 E1 座標，先證明原 writer 停止，再建立 E2。

## 停用 CER

使用者明示「停止 CER，改用單 thread 繼續」或 `/CER-stop` 時：

1. C 停止派發新 E1／R 批次。
2. 若沒有 active writer，C 以普通單 thread 繼續。
3. 若 E1 已開始寫入，C 先要求 E1 停止、回傳目前成果或 blocker，並標示是否 writer closed。
4. C 讀回沒有 active writer 或 writer 已停止的可判定狀態後，顯示 [roadmap.md](roadmap.md) 的固定閉眼 `⚪ CER 已停用` 卡，卡頭使用本次讀到的 package 版本並保留 `CER inactive`，才回到單 thread。
5. 不能證明 writer 停止或必要讀回未完成時，只顯示開眼 `🔴 重大阻礙` 卡，不得顯示閉眼停用卡，也不假設工作區安全。

`/CER-stop` 不等同 `/CER-close`。前者是停用 CER 協作拓撲；後者是完成 CER 收尾與必要持久化。單獨 `收工` 屬於目標 workspace 既有治理，不映射為 CER stop 或 close。
