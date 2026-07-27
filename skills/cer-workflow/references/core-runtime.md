# CER Core v1 執行核心

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

C 可以使用 inline sub-agent 作唯讀探索、證據整理或候選分析；它不是 CER 的正式
C／E／R 角色，不得寫 workspace、不得代替 E 或 R、不得產生正式 ready/result，
也不得作為 CER Reviewer 通過證據。

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

在建立本輪 E1、復用同輪既有 E1，或派任何實際 E1／R 批次前，C 先完成適應式任務契約。它不是表格儀式；簡單低風險任務可只在內部完成並直接工作，長期或多批任務則把必要答案濃縮進初始路線圖或自足派工。

C 只判斷五項，每項標成 `已確認`、`可安全推定` 或 `關鍵缺失`：

- 終點：可觀察終點是甚麼，哪些明確不做。
- 真源：完成判斷前必讀甚麼，已讀甚麼，仍有哪些關鍵未知。
- 根因與邊界：為何需要 CER；最小可驗收 E1 批次是甚麼。
- 權限與停點：哪些由 AI 自行處理，哪些真正需要使用者裁決或停止。
- 驗收與比例：甚麼證據可推翻方案；驗收是否剛好足夠，是否已變成防禦性擴建。

三態判定必須有證據邊界。`已確認` 只可來自使用者明示或已讀權威真源，C 必須能指出來源錨點；沒有來源的推測不得標成 `已確認`。`可安全推定` 必須通過反事實測試：若相反假設成立，仍不會實質改變交付物、權限／風險或驗收，也不會造成重大重做，才可通過；若多個合理答案會導致實質不同成果，該項就是 `關鍵缺失`。

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
13. 任一通訊 preflight 環節缺失，或 assignee 沒有實際 direct-push 合格零寫入 `ready`，C 只顯示開眼 `🔴 重大阻礙` 卡並停止；不得顯示成功啟動卡，也不得用 wait、輪詢、事後 read、文件審閱、fork 建立成功或單向 send 成功冒充通訊驗證。
14. 到此才算成功接受 `CER-start`。C 的第一個使用者可見成功回執必須是 [roadmap.md](roadmap.md) 的固定開眼 `🔵 CER 已啟動` 卡；卡頭使用本次讀到的 package 版本，腳部 `> ^ <` 右側留白。單批與多批都相同；不得用閉眼卡或猜測版本。
15. 同一輪、同一 C、同一 E1、同一回傳目標、同一可核實座標的後續批次不重做握手；座標或回傳目標改變即重做 ready。
16. C 判定為長期、多階段或多批次任務時，在固定啟動卡後、第一批前依 [roadmap.md](roadmap.md) 顯示初始進度面；簡單單批任務不強制建立路線圖。
17. 只有固定啟動卡已顯示，且長期／多批任務的初始路線圖已按需要補上後，C 才可派第一個實際批次。

若使用者沒有明示 CER，而工作只是低風險單一步驟，可按普通工作處理；一旦明示 CER，不能以「任務簡單」靜默取消角色拓撲。單獨 `開工` 屬於目標 workspace 既有治理，不是 CER trigger。

## 自足派工

每個 E1／R 實際批次只包含必要內容：

- 角色與單一目標；
- 目標 root；
- 必讀真源與已裁決背景；
- 允許及禁止範圍；
- 驗收與能推翻方案的反例；
- 停止條件；
- 凍結任務契約，以及任何 `已確認`、`可安全推定`、`關鍵缺失` 的處置、必要來源錨點和反事實結果；
- 回傳 C 的 direct-push 目標、session／thread id 或平台等價座標；
- 本批需要的知識底座、來源座標、未知與禁止越界範圍；
- 短回報要求。

不得寫「見上文」或要求 assignee 自行重建 C 的上下文。高風險批次補足背景與反例；低風險小修改保持短，不套巨型表格。E1／R 發現凍結契約與真源矛盾時，先回報 blocker 或候選修正，不自行改寫契約後繼續。

## 送達

- E1／R 工作前以正式送訊工具 direct-push `ready`。
- `ready` 必須回傳自身角色、可見標題或首行標籤、session／thread id 或平台等價座標、收到的目標 root、回傳目標及是否具備必要來源。
- 完成、受阻或未完成時，先 direct-push 短結果給 C，再停止；結果回執同樣要帶 session／thread 座標，避免 C 將另一個 task 的結果誤接納。
- C 只有收到 push 後才做一次有界讀回及裁決。
- 「不監察」只禁止 waiting、polling、背景監聽、反覆狀態探測及未收到 push 的被動 thread read。使用者明示要求的一次有界 read，或 push 後的核對 read，仍可使用。
- 送達不可用只阻止委派；C 仍可做獲授權的唯讀研究、分析與裁決，但不能代替 E1 寫入。

## 執行閉環

1. C 依使用者任務及目標專案已確認的計劃／真源，給本輪同一 E1 一個批次。
2. E1 只完成本批，讀回、測試並 direct-push 候選。
3. C 讀回實際成果，按風險自行裁決或用官方 `create_thread` 建立 fresh R。
4. R 只驗指定風險及成品邏輯，不只驗格式。
<!-- cer-review-convergence -->
5. R 首次指出缺陷後，C 先按共同根因和使用者後果合併同類發現；只做一次有界唯讀影響檢查，找齊承載本輪合約的現行真源、交付面與檢查位置。
6. C 凍結本輪 `owner／affected surfaces／acceptance／counterexample family`，給同一 E1 一個批次修完整個受影響邊界。
7. 修後 R 只重驗凍結範圍。只有不同根因、不同使用者後果或最新修補造成的新回歸才可擴大。
8. 換字、換句序或同義改寫仍屬同一問題；不得逐句追加規則或 validator pattern。若同一反例家族持續避過機械檢查，C 改變檢查方法或收窄 validator 聲稱能力。
9. 凍結反例通過且沒有實質新缺陷後，C 接納；只有此時才由 E1 更新目標專案既有的權威進度來源，沒有進度來源便不自行創造。
10. 必要狀態收斂後 C 停止；相鄰改善另列，不增加 Reviewer、治理層或全 repo 重審。
11. 長期、多階段或多批次任務的進度更新與小熊停點分工一律依 [roadmap.md](roadmap.md)；只用 direct-push 後已讀回及已裁決事實，不輪詢 E1。

普通小修改由 C 讀回加相稱測試即可。高風險修補只重審受影響邊界；不得用更多 R 代替清楚驗收條件。

## YAGNI 與停止

- 角色、批次、R、停點、測試及同步動作只按本次風險和交付需要增加。
- 能由 C 讀回和相稱測試可靠驗收的，不建立 R；能窄修的，不重審所有已接納部分。
- 已達需求、核心反例通過、必要風險清零後停止；相鄰改善另列，不自動擴張。
- 若代理與治理成本壓過任務價值，縮減協作結構，不以更多程序補償不清晰驗收。

## 獨立持久化與收工

CER Core v1 不規定項目文件。它沿用目標專案既有的權威計劃、進度及決策真源；
沒有持久真源時，不假稱新 session 可恢復完整狀態。

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
