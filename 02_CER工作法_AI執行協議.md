# CER 工作法：AI 執行協議

本文件是 Markdown 交付面，不是 `skills/cer-workflow/` 本身。v1 執行章節由
`skills/cer-workflow/` references 產生；v2 設計章節由
`dev/references/CER_KIT_ADAPTER_V2.md` 產生。不可單獨手改本文件。

CER Core v1 只支援獨立模式，不依賴或操作 Agent Handoff Kit。目標 workspace
既有的安全、使用者規則與權威真源仍然有效；若目標規則明示必須使用 Kit，
本 v1 應停止並說明未支援，不得繞過。

## CER v1 Runtime

## CER Core v1 執行核心

### 角色

- Controller（C）：使用者主 task 的主控者。負責全局判斷、真源映射、批次裁決、候選讀回及使用者溝通。C 不寫 workspace。
- Executor（E1）：同一任務持續重用、使用者可見、可再次派工的獨立 task，也是唯一 writer。E1 只執行 C 的自足批次，驗證後回報候選。
- Reviewer（R）：只在高風險、核心承諾、資料完整性、安全、外部能力不確定，或 C 不能可靠反證時建立。R fresh、唯讀、有界，不改檔、不指揮 E1。
- E2：只有原 E1 已確認停止寫入、工作區可判定且 C 發出接管批次後才可建立。不得存在平行 writer。

### 知識底座

CER 不限於工程任務。凡任務依賴醫療、法律、金融、投資、政策、學術、商業、
設計、營運、內容或其他專業知識，C 必須先按風險界定知識底座：領域範圍、
權威來源、術語、資料年度或版本、品質標準、不可由 AI 代選的取捨，以及需要
揭露的不確定性。已有專案真源或使用者提供來源時優先沿用；缺關鍵來源時停下
標示未知，不用一般常識補成專業結論。

E1 的派工包只包含本批所需的知識底座摘要、來源座標與禁止越界範圍。R 的工作
是依同一知識底座獨立反證高風險主張、來源使用、推論和結論，不只檢查格式。
簡單低風險任務不為知識底座建立文件；必要內容直接放入自足派工或停點說明。

### 操作指令

CER v1 接受自然語言和 slash command 兩種入口。slash command 是穩定文字別名，
方便在 AI terminal、snippet、Snap 或可搜尋指令面板中保存；平台不支援時，直
接貼上同一句仍有效。

| 指令 | 自然語言 | 效果 |
|---|---|---|
| `/CER-start <任務、限制、優先序>` | `CER 工作法啟動：...` | 啟動 CER v1，由目前使用者 task 成為 C。 |
| `/CER-stop` | `停止 CER，改用單 thread 繼續。` | 停用 CER mode，不再派新 E1／R；若 E1 已在寫入，先要求 E1 停止或回傳可判定狀態。 |
| `/CER-close` | `CER 收工。`／`收工。` | 完成 CER 收尾；同一 E1 只按既有真源回寫必要狀態並標 writer closed。 |
| `/CER-status` | `顯示 CER 狀態。` | 報告 C 已知的目標、C／E1／R 座標、下一停點和阻礙；不得為狀態而輪詢。 |
| `/CER-help` | `顯示 CER 指令。` | 顯示可用指令與自然語言等價句。 |

### 啟動

1. C 讀目前安裝的 CER runtime、使用者總任務、明示限制及目標 workspace 實際存在的權威規則。
2. 若目標規則明示必須使用 Agent Handoff Kit，停止並說明 CER Core v1 尚不支援；不得繞過。
3. C 確認目前 task 是使用者手動建立的 C，而不是被委派的 assignee。
4. C 命名或識別自身可見 task／thread 為 `C: <任務短名>`；平台不能改 title 時，在首則可見訊息或停點卡首行標示同等角色標籤。
5. C 在建立或復用 E1 前完成通訊 preflight：以可用工具證明本次實際採用的路徑可用，包括身份來源、目標 root、必要參數、發送路徑、接收者、可見標題或角色標籤、assignee 可取得的回傳來源、可核實 session／thread id 或平台等價座標，以及 C 的裁決點。
6. 若正式新建 task 工具不可用，只可停止，或改用同平台已證明可收發且上下文邊界清楚的既有 task。fork／delegate 帶有來源上下文時，不可冒充 fresh E1／R UAT。
7. 新建或復用 E1／R／E2 時，標題或首行標籤必須分別以 `E1:`、`R1:`／`R2:`、`E2:` 開首；每個派工包和 ready／結果回執都要包含發送者角色、接收者、回傳目標、session／thread id 或平台等價座標。
8. 任一通訊環節缺失，或 assignee 沒有實際 direct-push ready，C 發 `🔴 重大阻礙`；不得用 wait、輪詢、事後 read、文件審閱、fork 建立成功或單向 send 成功冒充通訊驗證。
9. C 建立或復用一個持久 E1。E1 先零寫入 direct-push `ready`；C 收到含正確角色、標題／標籤、session／thread 座標和回傳目標的 ready 後才派實際批次。
10. 同一 C、同一 E1、同一回傳目標、同一可核實座標的後續批次不重做握手；座標或回傳目標改變即重做 ready。
11. C 顯示初始路線圖，說明目標、現有計劃／進度真源、知識底座狀態、角色狀態與下一停點，再開始派工。

若使用者沒有明示 CER，而工作只是低風險單一步驟，可按普通工作處理；一旦明示 CER，不能以「任務簡單」靜默取消角色拓撲。

### 自足派工

每個 E1／R 實際批次只包含必要內容：

- 角色與單一目標；
- 目標 root；
- 必讀真源與已裁決背景；
- 允許及禁止範圍；
- 驗收與能推翻方案的反例；
- 停止條件；
- 回傳 C 的 direct-push 目標、session／thread id 或平台等價座標；
- 本批需要的知識底座、來源座標、未知與禁止越界範圍；
- 短回報要求。

不得寫「見上文」或要求 assignee 自行重建 C 的上下文。高風險批次補足背景與反例；低風險小修改保持短，不套巨型表格。

### 送達

- E1／R 工作前以正式送訊工具 direct-push `ready`。
- `ready` 必須回傳自身角色、可見標題或首行標籤、session／thread id 或平台等價座標、收到的目標 root、回傳目標及是否具備必要來源。
- 完成、受阻或未完成時，先 direct-push 短結果給 C，再停止；結果回執同樣要帶 session／thread 座標，避免 C 將另一個 task 的結果誤接納。
- C 只有收到 push 後才做一次有界讀回及裁決。
- 「不監察」只禁止 waiting、polling、背景監聽、反覆狀態探測及未收到 push 的被動 thread read。使用者明示要求的一次有界 read，或 push 後的核對 read，仍可使用。
- 送達不可用只阻止委派；C 仍可做獲授權的唯讀研究、分析與裁決，但不能代替 E1 寫入。

### 執行閉環

1. C 依使用者任務及目標專案已確認的計劃／真源，給同一 E1 一個批次。
2. E1 只完成本批，讀回、測試並 direct-push 候選。
3. C 讀回實際成果，按風險自行裁決或建立 fresh R。
4. R 只驗指定風險及成品邏輯，不只驗格式。
5. C 接納後，才由 E1 更新目標專案既有的權威進度來源；沒有進度來源便不自行創造。
6. C 在方向、交付形狀、重大阻礙、可觀察階段成果及最終驗收時向使用者交付停點。

普通小修改由 C 讀回加相稱測試即可。高風險修補只重審受影響邊界；不得用更多 R 代替清楚驗收條件。

### YAGNI 與停止

- 角色、批次、R、停點、測試及同步動作只按本次風險和交付需要增加。
- 能由 C 讀回和相稱測試可靠驗收的，不建立 R；能窄修的，不重審所有已接納部分。
- 已達需求、核心反例通過、必要風險清零後停止；相鄰改善另列，不自動擴張。
- 若代理與治理成本壓過任務價值，縮減協作結構，不以更多程序補償不清晰驗收。

### 獨立持久化與收工

CER Core v1 不規定項目文件。它沿用目標專案既有的權威計劃、進度及決策真源；
沒有持久真源時，不假稱新 session 可恢復完整狀態。

使用者向 C 明示「收工」、「CER 收工」或 `/CER-close` 時：

1. C 停止新派工，裁決可安全裁決的候選，整理已接納、未完成、風險、證據和下一步。
2. C 給同一 E1 一個自足收工批次。
3. E1 只按目標專案既有規則回寫必要進度／決策真源，標示 E1 已停止寫入，讀回後 direct-push；若沒有持久真源，只回報實際交付與 writer closed。
4. C 讀回實際交付和必要真源，以 `🟢 階段性交付／最終驗收` 告知使用者結果及延續限制。

不得跑 Kit closeout、重建 Kit mirror 或聲稱 `handoff saved`。新 session 只可從實際存在的目標專案真源恢復；證據不足便標示 continuity limited。若無可核實 E1 座標，先證明原 writer 停止，再建立 E2。

### 停用 CER

使用者明示「停止 CER，改用單 thread 繼續」或 `/CER-stop` 時：

1. C 停止派發新 E1／R 批次。
2. 若沒有 active writer，C 以普通單 thread 繼續。
3. 若 E1 已開始寫入，C 先要求 E1 停止、回傳目前成果或 blocker，並標示是否 writer closed。
4. C 讀回可判定狀態後，才回到單 thread；不能證明 writer 停止時，以 `🔴 重大阻礙` 告知使用者，不假設工作區安全。

`/CER-stop` 不等同 `/CER-close`。前者是停用 CER 協作拓撲；後者是完成 CER 收尾與必要持久化。

## 使用者停點與路線圖

### 固定停點卡

```text
   ()_()     CER 工作法
 ( ◕ᴥ◕ )    🔵 計劃預覽
   > ^ <     checkpoint ready
```

第二行按場景替換：

- `🔵 計劃預覽`
- `🟡 方向抉擇`
- `🔴 重大阻礙`
- `🟢 階段性交付／最終驗收`

### 真實使用時機

CER 是連續閉環，不代表每個小步都發卡。小熊卡和 inline visualization 只在
使用者需要重新看全局、裁決、知道阻礙或驗收成果時使用：

1. 啟動 CER 或重啟一個可接續階段時，用 `🔵 計劃預覽` 顯示目標、既有
   plan／progress、知識底座狀態、角色座標與下一停點。
2. 派第一個實際批次前，若任務跨多批或需要 E1/R，顯示 `🔵 計劃預覽`，證明
   本批從哪個權威進度位置開始。
3. 重大方向、範圍、交付形狀、成本、知識來源或驗收標準需要使用者取捨時，
   用 `🟡 方向抉擇`。
4. 通訊鏈、session／thread 座標、權限、真源、知識底座、平台能力或安全條件
   不足，不能可靠繼續時，用 `🔴 重大阻礙`。
5. E1 完成可觀察階段、C 已讀回裁決，或 R 完成高風險反證後，用
   `🟢 階段性交付`。
6. 使用者收工或最終驗收時，用 `🟢 最終驗收` 顯示成果、writer closed、持久
   真源更新與下一 session 延續限制。

普通內部讀檔、低風險小修、E1 子步驟、已清楚不需使用者介入的下一步不發卡。

### 顯示優先序

每張 C 主 task 的停點卡都要在同一訊息附上使用者視角路線圖，顯示終點、階段、
目前位置、下一停點、知識底座狀態及 C／E1／R 狀態。停點卡是對使用者有用的
介入層：把既有 project plan／progress 翻譯成「現在要預覽、裁決、停下或驗收」
的狀態，不是第二套計劃或進度。優先沿用目標專案已有的權威 Roadmap／進度
來源；CER 不另建平行進度。

1. Codex 有可調用的 in-conversation visualization 能力時，預設建立 inline HTML visualization，並使用該能力要求的正式呈現指令，例如 `::codex-inline-vis{file="..."}`。
2. Mermaid 不算完成第一層要求。只有 inline visualization 能力不存在、不可調用、不可寫入其指定視覺目錄，或實際呈現失敗時，才使用 Mermaid。
3. Mermaid 也不可用時，才使用固定 Markdown／純文字。
4. 降級時用一句話明示原因；不可靜默降級，也不可因視覺能力缺失阻塞項目。

純文字 fallback：

```text
目標：<終點>
[✓] 已完成 → [● 現在] 當前階段 → [○] 後續階段 → [○] 最終交付／收工
目前：<一句>
下一停點：<一句>
知識底座：<已確認／缺來源／不適用>
角色：C=<狀態>｜E1=<狀態>｜R=<未建立／驗收中／完成>
```

### 路線圖真源

只用最高可用權威來源，不建立第二份進度：

1. 目標專案已有權威進度／Roadmap 時，由它派生。
2. 只有已確認計劃而未有進度來源時，由計劃加已核實執行狀態暫態派生。
3. 未有計劃時，由使用者本次需求與已核實角色／阻礙事實暫態派生，標示「初始／待收斂」。

若同時使用 `$project-context-workflow`，只讀取其已確認計劃與進度，不重做五步或
建立第二道相同共識關卡。

普通工程細節不發卡。方向或交付形狀取捨用 🟡；可靠性 blocker 用 🔴；可觀察階段成果與最終驗收用 🟢。

## CER Core v1 Fresh UAT

UAT 必須由使用者在乾淨 project 手動建立新 task。來源專案的 C 建立、fork 或 delegate 出來的 task 帶有來源上下文，不算 fresh。

只有標題、fork、delegate、單向送訊或工具參數成功，不等於閉環通過。必須有 E1 direct-push ready/result。

### 安裝情景

- 目標只有本 Skill，沒有來源 handoff 或來源專案背景。
- 新 C 能只靠 Skill 和使用者總任務啟動。
- 目標權威規則若強制 Agent Handoff Kit，v1 應誠實停止，不繞過。

### 完整流程

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

### 失敗條件

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

## Markdown-only v2 Appendix

## CER v2：Agent Handoff Kit Adapter 設計真源

### 狀態與用途

狀態：已確認方向，延後到 CER Core v1 完成 fresh UAT 後才實作。

本文件保存 CER 與 Agent Handoff Kit 的整合背景、責任分工和未來驗收契約，避免下次 session 重新討論。它不是 CER Core v1 runtime，不得在 v1 啟動時載入或執行，也不授權修改 Agent Handoff Kit。

### 已確認架構

- Controller（C）全程保留，負責全局研究、範圍、語義裁決與使用者交付；C 不寫 workspace 或 Kit。
- 同一持久 E1 是 CER 與 Kit 的唯一 writer，負責產品寫入、checkpoint 及 Kit closeout。
- Reviewer 只在高風險治理、根修、契約、資料完整性、恢復機制、正式候選凍結或發布前使用；R 唯讀，不寫治理檔、不做 closeout。
- 普通小修由 C 讀回加機械測試；高風險修補只重審受影響邊界。
- 不以增加 Reviewer 數量代替明確驗收條件。

### Kit closeout 映射

1. C 停止派發新工作。
2. C 收齊必要 direct-push，裁決成立、失敗及待辦。
3. C 產生一份 self-contained 最終事實包。
4. 同一 E1 依目標 Kit 現行 closeout pack 寫入：
   - `dev/SESSION_HANDOFF.md`：目前狀態、下一步、風險和必要候選身份；
   - `dev/SESSION_LOG.md`：重要追溯證據；
   - `dev/PROJECT_DECISIONS.md`：只有重大決策；
   - `dev/PROJECT_INDEX.md`／`dev/DOC_SYNC_REGISTRY.md`：只在所擁有地圖或同步責任改變時；
   - `START_NEXT_SESSION_PROMPT.txt`：只從 handoff 的唯一 opening block 重生。
5. E1 執行機械驗收、實際讀回及 Kit `closeout-status`，再 direct-push 終態給 C。
6. 只有 Kit 回報 `status: complete`，C 才宣告 Kit 收工完成。

仍有 writer 寫入、必要 R 未裁決、候選身份不明、回執衝突或 closeout-status blocked 時，只能標受阻。

### v2 實作前置

- CER Core v1 已在使用者建立的 fresh project／task 完整通過。
- v1 的 C／E1／R、direct-push、五份項目真相、04 共識閘、inline 路線圖、階段性交付及獨立收工均穩定。
- 目標 Kit 版本與規則可讀，且整合不要求修改 Kit 核心。
- v2 Adapter 是按需 reference／adapter，不把 Kit 細節塞回 CER Core hot path。
- 標題更新、fork、delegate、單向送訊、文件審閱或事後 read 都不能取代
  E1 direct-push ready/result、Kit 寫入、closeout-status 及新 session
  恢復證據。

### v2 Fresh UAT

1. 在已安裝 Kit 的乾淨 project，由使用者手動建立 C task。
2. C 完成 Kit 最小唯讀 recovery 和跨 task 通訊 preflight。
3. 建立持久 E1；E1 自讀目標 Kit 規則後 ready direct-push。
4. E1 建立／更新 CER 01-05，並按 Kit Persistence Gate 保存必要 current state。
5. 完成至少兩個批次；普通批次無 R，高風險批次才有 fresh R。
6. 使用者向 C 說「收工」；C 發最終事實包，同一 E1 完成 Kit closeout。
7. 使用者在新 session 輸入 Kit「開工」，能從 handoff 找回 CER 目前位置、目標、風險、E1 續接資料和下一步。

若只證明文件可讀、模擬流程或 closeout 文案正確，而沒有真實 task 回傳、Kit 寫入、closeout-status 及新 session 恢復，v2 未通過。
