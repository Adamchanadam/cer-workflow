# 發布說明

範圍說明：本檔各版本區段記錄對應版本的 release history；未發布內容會明確標示
為候選。實際執行規則以使用者已安裝版本隨附的 Skill references 為準。

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
