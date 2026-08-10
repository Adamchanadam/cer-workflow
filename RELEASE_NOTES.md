# 發布說明

範圍說明：本檔各版本區段記錄對應版本的 release history；未進入已授權 release
flow 的未發布內容會明確標示為候選。若 release 中止，對應內容必須改回候選或移除。
實際執行規則以使用者已安裝版本隨附的 Skill references 為準。

## v0.3.12

本版把 `/CER-auto` 的新手入口和 README 視覺說明整理成可公開版本。重點是讓新用戶
先知道「直接提出任務」即可，由 Skill 選最低足夠路線；完整 CER 仍保留給明確需要
full CER 的工作。

- README 首屏改用 `/CER-auto` 四路線選擇圖，說明 ordinary execution、Goal、
  CER-gated Goal/E1 和 blocked
- README 補上 `/CER-auto <任務>` 的任務寫法：目標、限制／不可做、成功驗收、
  權威來源／授權邊界
- `cer-workflow-infographic.png` 和 `cer-exploration-helper-architecture.png`
  已更新為 CER-auto 對齊版本；舊圖以 `.legacy-20260810*` 檔名保留
- `/CER-help` 的 task-template 說明與 README 對齊，例子按用戶背景生成，不固定行業
- 本版不擴張 runtime owner、不新增平行規則、不取代明示 `/CER-start`
- 中英文 Skill packages 均為 VERSION `0.3.12`，各 8 files，411 mutation cases 通過
- 發布後使用者手動 UAT 仍需另行回報

## v0.3.11

本版加入本地 `/CER-auto` 入口，讓使用者只提出任務，由 Skill 先選最低足夠執行
強度；清楚小任務不啟動 CER，清楚長任務交給 Goal，只有權威升格、公開聲稱、
release/readiness、交接真源或外部／不可逆後果才進入 CER gate。

- `/CER-auto <任務、限制、優先序>` 會先回一行路線：ordinary execution、Goal、
  CER-gated Goal/E1 或 blocked
- `ordinary execution` 不建立 C／E／R 身份、不顯示小熊卡，也不載入其他 CER
  references
- `Goal` 承擔清楚長任務的閉環推進與驗證 loop，但不擁有 CER 的唯一 writer、角色
  身份或 authority owner
- `CER-gated Goal/E1` 只在成果準備升格為正式資料、模型輸入、報告段落、decision
  gate、handoff truth、release/readiness claim 或 public/external claim 時啟動
- 權威來源、安全邊界、驗收條件、root／permission、Goal 能力或外部操作授權不足時，
  路線必須是 blocked，不能以 hash、receipt、source count、schema 或 AI confidence
  代替權威證據
- `/CER-start` 沒有被取代；它仍是使用者已確定需要完整 CER 流程時的直接入口
- 公開 README 補上 `/CER-auto <任務>` 的新手用法；`/CER-help` 的指令表會隨本版
  Skill 顯示 `/CER-auto`
- 中英文 runtime、UAT 與 Skill validators 加入 Goal-aware routing、authority
  promotion、blocked route 及 illegal shortcut 的固定反例；套件各有 411 個 mutation cases
- Release-readiness 已完成全文靜態審核及兩輪 AI 真實流程 UAT；發布後使用者手動 UAT
  仍需另行回報

## v0.3.10

本版補上結果回來後的處置閉環，避免候選、診斷、衍生輸出或 Reviewer PASS 被錯誤
升格成權威輸入、主線進度或下一批決策來源。

- C 接納結果時必須明示 `accepted_as`、`authority_effect`、`progress_effect`、
  `permitted_next_use`、`forbidden_next_use`，以及是否需要目標專案既有持久化
- 裸 `RESULT_ACCEPTED` 只代表該批次已裁決及通訊去重，不代表權威升格、主線進度，
  也不代表下一批可把結果當權威輸入
- 候選、草稿、診斷、衍生輸出及純審閱結果預設只可作 `working_material`；要升格為
  `authoritative_input`，必須有使用者明示或目標專案既有 owner 讀回、升格依據及
  讀回證據
- 下一批使用上一批結果時，派工包必須標明 `prior_result_use:
  working_material | authority_input`；若是 `authority_input`，必須列出
  `promotion_evidence` 與 `project_owner_anchor`
- Reviewer verdict 分成 `content_verdict`、`implementation_verdict`、
  `outcome_verdict`、`authority_promotion_verdict`；內容或技術 PASS 不會自動變成
  outcome PASS、authority promotion PASS 或主線進度，`out_of_scope` 也不是 PASS
- 如果結果會改變當前階段、artifact 角色、下一產品路線、權威來源、progress claim
  或後續批次輸入，C 必須先按目標專案既有持久化規則回寫並讀回；未同步或互相矛盾
  時，下一批停在 `dispatch_blocked`
- 中英文 runtime、UAT 與 Skill validators 加入 result-disposition、authority
  promotion、prior-result consumption 及 persistence-before-next-dispatch 的固定反例；
  套件各有 316 個 mutation cases
- Release-readiness 已完成全文靜態審核及兩輪 AI 真實流程 UAT；發布後使用者手動 UAT
  仍需另行回報

## v0.3.9

本版把 A/B/C true dry-run 證明的 create-prompt lifecycle weakness 收斂進 runtime。
重點是把「開新 E1／R task」和「正式派工」分開，避免一開始就把完整 corpus 或
formal batch payload 塞進新 task，令 READY、處理結果、重送去重和驗收證據混在一起。

- 新 E1／R `create_thread` 初始 prompt 只可作 zero-write ready handshake：說明角色、
  cycle／title、target root、C return target、不得寫入／不得開始工作，並要求回報自身
  座標或 source availability
- `create_thread` 初始 prompt 不得包含 complete source corpus、candidate work content
  或 formal batch payload，也不得要求 E1／R 在 READY 前處理內容
- 若已發生 pre-ready 內容處理，C 必須視為 `pre-batch payload leak`／batch lifecycle
  violation，停下或 refreeze；後續同 digest duplicate ack 不可當作正常高效通訊
- assignee 不能自行讀取已授權 source 時，C 在 READY 後只送一次 formal
  `sendable_packet`；如內容太長或跨風險邊界，按語義／風險單元分拆
- assignee 可以讀取已授權 source 時，正式派工優先給 coordinates、digest、必要 excerpts
  與 no-go boundaries，不重貼整份 corpus
- A/B/C dry-run 未證明本 CER Skill 有過度 microbatch、harmful over-coarse batching、
  過度保留、長 prompt send failure 或不合理慢推進的缺陷；本版只修證據成立的
  create-prompt／formal dispatch 分界
- 中英文 runtime、UAT 與 Skill validator 加入 create-prompt payload leakage 的固定反例；
  套件各有 283 個 mutation cases
- 本版 release-readiness 記錄為 `Full Audit 通過（只限全文靜態審核；AI 真實流程 UAT 不可用）`
- 發布後使用者手動 UAT 仍需另行回報

## v0.3.8

本版發布 v0.3.7 後完成的兩項 runtime 收斂：派工前可讀回證據，以及派工後
`POST_DISPATCH_PARKED` no-wait 狀態。重點是把 C 的判斷和收件路徑變成可驗收邊界，
防止長期 CER 因等待、口頭承諾或錯方向承接而失焦。

- 長期、多批、高風險或非簡單正式實作批次的派工包，必須包含短小
  `pre_dispatch_evidence`；它把既有 Controller preflight、`outcome_anchor` 和 drift
  判斷濃縮成 E1／R 可讀回的派工前證據，而不是新增真源、表格、監察程序或 Full
  Audit
- `pre_dispatch_evidence` 至少列明成果錨、本批改善的未完成條件、成功後可讀回成果
  差異、真源攝取四問摘要及來源錨點、必要真源已讀／缺失處置、工作線分類，以及
  drift checkpoint 結論或未觸發理由
- 缺少必要派工前證據、證據互相矛盾、依賴未讀必要真源，或只稱「已判斷」但沒有
  可讀回摘要時，C 停在 `dispatch_blocked`；E1／R 只可回傳零寫入 blocker，不得開始
  寫入、審閱或替 C 補完判斷
- C 派工、建立 task 或送訊後立即進入 `POST_DISPATCH_PARKED`。在此狀態下，C 不得
  自動使用 `wait_threads`、`read_thread`、等待、輪詢、讀 commentary、讀 child final
  或狀態探測來發現 ready、進度、checkpoint 或結果
- 只有使用者同一輪明示要求的一次性診斷讀取，或已收到 direct-push 後的一次有界讀回
  ／裁決，才可讀取相關 task。沒有 direct-push 時，wait snapshot、完成狀態、
  commentary、child final 或被動讀取都不能推進 lifecycle、觸發下一批或成為正式交付
  證據
- 中英文 runtime、UAT 與 Skill validator 加入派工前證據與 `POST_DISPATCH_PARKED`
  no-wait 的固定反例；套件各有 275 個 mutation cases
- 發布後使用者手動 UAT 仍需另行回報

## v0.3.7

本版把 v0.3.6 公開後完成的三項通用 runtime 修補正式發布，重點是讓長期 CER
閉環工作更不容易因等待、相鄰方案、簡報或重複批次而失焦。

- 派工後，C 不得自動把 `wait_threads` 或 `read_thread` 當作接收結果的機制；
  正式結果必須由受派 task 主動 direct-push 回指定回傳目標。只有在已聲明的
  direct-push 狀態轉移中，或收到 direct-push 後需要喚醒、讀回或裁決時，才可做
  一次有界等待或讀回
- Controller preflight 新增真源攝取門檻：非簡單正式實作批次前，C 必須能回答
  完成條件由誰擁有、誰實際使用、如何生效，以及甚麼反例能推翻。若答案缺失或
  依賴未讀真源，C 不得派正式實作，只可做必要唯讀診斷、收窄驗收範圍或停下問
  使用者
- 長任務 drift checkpoint 由成果錨定與進展閘唯一擁有。遇到 resume／上下文轉換、
  連續兩批無已接納成果差異、同類失敗第二次、E1／R 提出相鄰或替代交付、使用者
  改方向或補限制、close／release／重大交付前，C 必須重新證明下一批仍改善
  `outcome_anchor`
- checkpoint、簡報和路線圖本身不計成果進度，也不會觸發背景監察、輪詢、自動
  `wait_threads`、固定 Reviewer 或固定 Full Audit；簡單、單步、低風險任務仍可
  使用輕量流程
- 中英文 runtime、UAT 與 Skill validator 加入 wait-auto delivery guard、真源攝取
  門檻及 drift checkpoint 的固定反例；套件各有 259 個 mutation cases
- 發布前 release-readiness 已完成全文靜態審核及 AI 真實流程 UAT；發布後使用者
  手動 UAT 仍需另行回報

## v0.3.6

本版修正長期多批 CER 任務可能把批次活動誤當成最終成果進度的問題。

新增的 `outcome_anchor` 會在長期、多批或容易返工的任務首次實際派工前固定使用者
最終要取得的成果、完成條件真源、不可接受的替代成果及排除範圍。後續 E1、R 或
相鄰機制改善不得自行改寫這個成果錨；若使用者或權威真源改變，C 必須明示新舊錨
差異。

- 非純探索批次派出前，C 必須指出本批改善哪項未完成條件、成功後有甚麼可讀回
  前後差異，以及依賴、權威來源和承接路徑是否存在；預期成果改善為零且不是必要
  前置條件的實作批次不得派出
- 候選建立、審閱完成、格式或結構通過、檔案一致、問題記錄、設計完成、版本改名
  或包裝更新，只屬活動；只有 C 讀回並接納某項使用者完成條件的成果差異，才可算
  主線進度
- 同一失敗類別按共同根因、使用者後果、受影響完成條件和方法判定；改名、換版本
  或換包裝不會變成新類別，連續兩次未解決後不得派第三個同類修正版
- Reviewer 必須同時檢查本批是否仍服務原始成果、是否有可接納成果差異、是否只是
  技術活動或返工，以及是否用另一種交付形式代替使用者原本要求
- CER 現在明確分開 `mainline_outcome`、`diagnostic`、`mechanism_improvement` 和
  `governance_self_improvement`；診斷及通用機制改善不會污染主線進度，也不會因自身
  失敗自動阻塞原任務
- 中英文 runtime、roadmap、UAT 與 Skill validator 加入成果錨、活動／成果分離、
  重試斷路器、Reviewer 成果檢查及工作線隔離的固定反例；套件各由 172 增至 201 個
  mutation cases
- AI 真實流程 UAT 的外層 cycle C 現在也必須 direct-push `AI_UAT_CYCLE_N: PASS/FAIL`
  回主線 release dispatcher；只靠 `wait_threads`、`read_thread`、子 task final、
  task title 或使用者轉述完工，不能標記 release-readiness 通過
- 發布後使用者手動 UAT 仍需另行回報

## v0.3.5

本版補上兩項 runtime 根修。

第一，`messageId` 的身份邊界更清楚：它是 CER 訊息層的識別、去重及追蹤欄位，
不是 Codex 執行指令、App Server `method`、JSON-RPC request `id`、thread/session
身份、idempotency key 或授權。只有實際工具呼叫及可核實工具結果／送達證據，才可
推進訊息送達或工作執行判斷。

第二，Controller preflight 及路線圖正式整合「活的任務簡報」：模糊但可起步的
多批任務不要求使用者先寫完整規格；C 會分清已確認要求／排除、可安全推定、
關鍵缺口、最新回饋、本批凍結、下一個可觀察預覽或裁決點，且只凍結下一個可安全
執行批次。中途回饋改變方向時，C 先更新任務簡報和路線圖差異，再用新的批次身份
或 supersede 流程交回同一 E1；R 依最新任務簡報及本批凍結驗收，不按過期 prompt
驗收。用戶可見的簡報必須帶 CER 標識和 C／E1／R 語境，避免看起來像 Codex 原生
內部功能。

- 雙語 runtime owner 明確禁止只把 `messageId` 寫入 prompt、派工包、摘要或一般
  workspace 文字，就當成建立 thread、開始 turn、呼叫工具、觸發寫入或授權
- 雙語 runtime、roadmap、UAT 與 Skill validator 加入 living brief、CER 可見樣式的
  反例及固定回歸，套件各由 141 增至 172 個 mutation cases
- 已發布至 GitHub Release，並可用 skills CLI 安裝繁體中文版 Skill；發布後使用者
  手動 UAT 仍需另行回報

## v0.3.4

本版收斂四項已在實際 CER 使用中確認的通用 runtime 修正，不新增指令、角色或
任何單一專案專用規則：

- C 在 `create_thread` receipt 後，如當前 Codex title 工具可用，必須立即用官方
  工具設定／改名並讀回，才可接納 ready 或送出正式批次；title 工具不可用時保留
  如實的 `title sync warning`
- lifecycle 與 checkpoint 小熊卡統一為獨立 fenced `text` code block 的三行固定版式，
  版本只在第一行、狀態只在第二行，避免介面呈現時走位
- 同一凍結目標已有實質 E／R 結果後，C 只有在能指出新的可推翻問題，並證明新增
  E／R 或任務支線是完成原始目標或處理已核實阻礙的最小必要手段時才可派發；否則
  合併、停止或自行裁決
- `CER-close` 成功後，本輪已完成並已裁決的審閱任務可封存以減少側欄雜亂；
  C／E1 保留可見，摘要會明講封存不是刪除，仍可在已封存任務中找回
- 中英文 UAT 與專案治理驗證加入固定反例，防止遺漏 title set/readback、卡片版式或
  無必要的同根因任務支線，以及把封存誤當刪除或收尾證據；發布後使用者手動 UAT
  仍獨立回報

## v0.3.3

本版修正 v0.3.2 後確認的驗收弱點：文件文字已正確說明普通 `開工`／
`收工` 屬於 Agent Handoff Kit 語意，但 Skill validator 未能機械防止未來
把「單獨收工」誤改成 CER 收尾觸發：

- 中英文 Skill validator 新增 context-aware trigger matrix 檢查，分開驗證
  frontmatter、命令表、runtime 啟動／停止 owner，以及 UAT 安裝與失敗矩陣
- 合法的 CER 指令仍只限 `/CER-start`、`/CER-stop`、`/CER-close`、`/CER-status`
  和 `/CER-help`；普通 `開工`／`收工` 或 `start`／`close` 不會單獨觸發 CER
- UAT 內的 failure example 可保留「錯誤寫法」作反例；validator 不使用全域
  禁字，而是按章節語境檢查，避免假陽性與假綠燈
- 兩語套件各由 131 個 mutation cases 增至 141 個，新增反例會把
  SKILL、core runtime 或 UAT 中的單獨 close／start 語意漂移判為失敗
- 本版不改 CER runtime 觸發語意、不新增指令、不改 Keyring 或任何單一專案專用規則

## v0.3.2

本版修正正式派工封包可能仍保留佔位符、相對身份或缺少 Reviewer 候選證據，
但 Controller 仍自評為可送出的缺口：

- C 可在內部保留 `draft_packet`，但正式 `sendable_packet` 必須填入實際
  `threadId` 或平台等價座標、`returnTarget`、`messageId`、`batchId`、`batchSeq`
  、`payloadDigest`，以及當前工具 schema／receipt 明示必需的路由座標
- `hostId` 只在當前工具 schema 或 receipt 明示需要／提供時使用；不得把它寫成
  跨平台硬性必填，不得由 `local`、title、sessionId、threadId 形狀或錯誤訊息推導
- `sessionId` 不可代替 `threadId` 作正式派工座標，也不可用來推導 `hostId`
- `同一 E1`、`上述 E1`、`下一個序號` 等相對說法只可作草稿；正式交給 E1
  或 R 前必須換成可核實實值
- R 派工必須帶實際 `candidateIdentity`、`candidateManifest` 及候選 delivery
  evidence；缺任一項即停在 `dispatch_blocked` 或 `decision_blocked`
- 中英文 UAT 反例及 Skill validator 已加入同類 failure class 的固定情景；
  兩語套件各有 131 個 mutation cases，不以單次 prompt 字句 hard code 取代
  同類事件檢查
- AI 真實流程 UAT 已完成兩輪：第二輪使用全新 C／E1／R task，未重用第一輪
  C／E1／R；發布後使用者手動 UAT 仍獨立回報

## v0.3.1

本版修正 Executor 遇到未預期測試失敗時可能誤把測試結果或 allowlist 當成擴大
修改權的缺口。這是 CER Core 通用 runtime 修正，不加入 Keyring 專案語意，也不
新增角色、指令、模式或助手：

- `core-runtime.md` 的執行閉環現在明確規定：未預期失敗不會改變本批授權；測試
  只產生證據，不增加修改權；檔案在允許範圍內，也不代表 E1 可改變該檔案內
  其他 owner、權威來源或受保護語意
- E1 若因未預期失敗而想新增或擴大寫入，必須先做有界唯讀歸因。只有能證明是
  本批直接造成，且修正不改變凍結 owner、語意、來源、權限或驗收，才可在本批
  修正
- 若因果不明、失敗可能來自不穩定測試、環境或依賴，驗收本身可能錯誤，或修正
  需要改變另一 owner、權威來源、准入條件、fallback、產品／專業語意或跨
  subsystem 行為，E1 必須停止進一步寫入並回傳 blocker
- 直接驗收只判定本批候選是否可接納；完整回歸只用來發現整合風險。完整回歸
  失敗可阻塞候選，但不自動授權相鄰修補
- 只有 C 可重凍結契約，並用新的 `batchId`／`payloadDigest` 派發新批次來擴大
  範圍
- 中英文 UAT 反例及 Skill validator 已加入這個 gate 的固定情景；兩語套件各有
  109 個 mutation cases。發布後使用者手動 UAT 仍獨立回報

## v0.3.0

本版把 v0.2.6 已加入的「探索助手」整理成可在不同項目重用、可機械驗證的完整
能力，並修正兩個可能增加不必要工作或造成驗收假綠的問題：

- 使用者仍只需啟動 CER，無須設定助手或新增指令。完整規則集中在唯一的
  `parallel-producers.md`；README 保留一般介紹，不再成為第二份規則真源
- 簡單任務保持零名探索助手。只有至少兩條工作線互不依賴、輸入已凍結、C 同期
  有不同的重要工作、候選可分開核對、預期真正省時，而且有足夠執行位置時，
  C 才會自動並行探索
- 探索助手只交候選。唯讀工作保持零寫入；需要產生候選檔案時，只能使用已核實
  的獨立臨時區，並記錄來源位置及檔案雜湊，再由 C 親自讀回、去重和裁決
- 預設提示不再暗示每項工作都必須建立 Reviewer。簡單低風險工作由 C 作相稱
  檢查；只有風險或不能可靠反證時才建立 fresh Reviewer。驗證器要求整句與唯一
  核准版本完全一致，任何附加或替換的矛盾句都會失敗，不再靠追逐同義詞
- 驗證器由同一份規則要求清單產生逐項刪除反例。目前中英文套件各有 87 個
  mutation cases；八項平行安全及證據要求任何一項被刪除，以及以不同詞序、
  主動或被動句強制簡單／低風險任務建立 Reviewer，都必須被拒絕
- 中英文 Skill、README 及新節點資訊圖同步為同一架構；公開規則不含任何單一
  項目的名稱、路徑或專用判斷
- 繁中全域修正、兩語 Skill 結構檢查、兩語 87 項自我測試及公開雙語候選的
  最終獨立覆核均已通過。發布後使用者手動 UAT 尚未執行，會分開記錄

## v0.2.6

本版在不改變 C／E／R、唯一 writer 或獨立 Reviewer 邊界的前提下，為 Controller
加入按需自動調度的「探索助手」：

- 探索助手可同時協助 C 搜尋資料、比較方案、整理介面構想及預先找出可能問題；
  它不是第四個正式角色，不修改專案、不代替 E1／R，也不新增操作指令
- 探索助手平常不會啟動。只有工作能安全分開、資料和目標已清楚、結果可以分開
  核對，而且預期真正省時時，C 才會自動使用
- 簡單任務不使用探索助手；C 仍會親自分析及作最終決定，不會因多數助手給出
  相同答案，便直接當作正確
- 如果資料途中改變，只重做受影響的部分；如果助手無法啟動、逾時或找不到資料，
  C 會自己繼續，不會令整個 CER 無故停下
- 一次中型任務的實際測試中，兩項工作逐項完成約需 71 秒，同時處理約需 43 秒，
  等待時間少約四成；這只是一個測試例子，不代表每個項目都有相同提升
- 本機檔案、Skill 結構、Kit 健康檢查、全文靜態發布審核及兩輪 AI 真實流程 UAT
  均已通過；發布後使用者手動 UAT 尚未執行，會分開記錄

## v0.2.5

本版加強長期、多批 CER 的送達可靠性，並把同源證據與風險分層加速收斂為預設自適應排程：

- 正式訊息及批次使用穩定 `messageId`、`batchId`、單調遞增 `batchSeq` 與不可變 `payloadDigest`；相同身份但不同內容立即阻塞
- `create_thread` 或 `send_message` 結果不明時禁止盲目重試；先做一次有界對帳，以實際 `threadId`、`hostId`、零寫入 `READY` 或權威 receipt 判定
- 舊批次修訂前先進入 `SUPERSEDED` 終態；延遲送達或重播的舊批次只能拒絕，不得重啟寫入
- 同源證據可在來源身份與新鮮度未變時跨相依工作共用；無實質狀態變化的批次在預檢停止，新事實集中收集，驗收命令與反例合併執行
- fresh Reviewer 只在完整高風險候選形成後建立；通訊、writer、證據、依賴或批次生命週期有任何不明時，自適應加速自行停用
- 平台不會自動喚醒 idle Controller 時，只為已聲明狀態轉移使用有界事件等待；snapshot、commentary 或 task 完成狀態不能代替 direct-push 結果
- 發布就緒已完成兩輪獨立 AI 真實流程 UAT，包括重複送達、批次取代、延遲舊批次拒絕、Reviewer 阻塞修正及 writer close；發布後使用者手動 UAT 仍未執行並須分開回報

## v0.2.4

本版把 CER 在已由 Agent Handoff Kit 治理的 workspace 內遇到 Kit 指令時的行為收斂為權威轉交：

- 目標 `AGENTS.md` 明確路由 `收工`、`Wrap up Agent Handoff` 或同等 session closeout 語意時，C 只把使用者原始指令、目標 root、同一 E1／回傳座標及必要未持久化狀態交給同一 E1
- C 不重述、拆解、擴張、預判、預先執行或另建 Kit full closeout／governance bridge 程序、checklist、檔案清單、maintenance 判斷、測試或完成聲稱
- Kit full closeout 權威終態未成立或回報 blocked 時，C 不宣稱 `writer closed`、不同步 title `✓`、不顯示 CER 收尾卡；終態成立後才處理 CER 自身收尾
- 同一 E1 已回傳可核實 Kit 終態後，C 只作必要成果讀回，不重跑 Kit 程序或檢查；證據缺失或矛盾才回同一 E1 補證
- governance bridge 完成後 CER 保持啟動；`/CER-close` 仍只是 CER 指令，不反向觸發 Kit full closeout

## v0.2.3

本版把 CER 進入實作前的公開對齊與生命週期提示收斂為可見停點：

- 長期、多批或新產品／流程／設計／內容／體驗型任務，在第一個實際 E1 批次前顯示 inline visualizer 路線圖；終點明確的簡單任務只顯示短摘要
- 可安全推定不再只看技術風險；若相反假設會改變使用流程、協作方式、資料處理、輸出內容或造成重大重做，C 必須先對齊或詢問關鍵問題
- 公開任務摘要顯示目標、範圍、假設、最小可觀察成果、技術驗收與用途校正，以及下一個使用者停點
- 小熊卡保留完整三行圖案，版本與狀態接在第三行小熊腳後，不另起一行

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
