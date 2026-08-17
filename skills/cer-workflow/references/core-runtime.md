# CER Core v1 執行核心

## 目錄

- [角色](#角色)
- [知識底座](#知識底座)
- [公開 runtime 語言邊界](#公開-runtime-語言邊界)
- [小熊卡 package 版本](#小熊卡-package-版本)
- [操作指令](#操作指令)
- [執行強度閘門](#執行強度閘門)
- [Controller preflight](#controller-preflight)
- [成果錨定與進展閘](#成果錨定與進展閘)
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

## 公開 runtime 語言邊界

<!-- cer-public-runtime-language-boundary-owner -->
`PUBLIC_SKILL_BOUNDARY_V1` 是後續公開分發遷移邊界，不自動改變目前已安裝或已發布的
package。未來公開 runtime 行為改動先以英文 `cer-workflow-en` package 作 canonical
authoring／validation source；若保留繁中 package，它只能作相容入口與用戶語言鏡像，
不得另定或覆蓋 CER 行為。

英文 canonical runtime 不等於英文-only 操作。`/CER-auto`、`/CER-start`、
`/CER-stop`、`/CER-close`、`/CER-status`、`/CER-help` 保持穩定 ASCII 指令；中文
自然語意觸發仍須有效；面向使用者的回覆跟隨使用者或目標專案語言。不得只因 runtime
正文是英文，就把中文輸入預設改成英文回答。

`README.md`／`README.en.md` 只屬用戶展示與安裝說明，不能覆蓋 runtime owner。
`RELEASE_NOTES.md` 維持現行先繁中後英文的 repository notes 方向。`uat.md` 中
Full Audit、release-readiness、post-release manual UAT 或「本 Codex 專案」語境只屬
maintainer release-QA，不是 ordinary execution、Goal、CER 工作法或 `/CER-help` 的一般
runtime 步驟。刪除、退役或合併繁中 package，以及 public/global sync、install、commit、
tag、release、npm publish 或 deploy，仍須另行授權、遷移驗收與讀回。

## 小熊卡 package 版本

每次顯示任何 lifecycle 或 checkpoint 小熊卡前，先讀本 Skill 根目錄、與
`SKILL.md` 同層的 `VERSION`。只接受完整內容符合穩定 semver
`X.Y.Z`；有效時在卡頭渲染為 `vX.Y.Z`。`VERSION` 缺失、不可讀或格式錯誤時，
卡頭顯示 `version unverified`。

卡片形狀只使用 [roadmap.md](roadmap.md) 的 Handoff Kit 排板風格 ASCII 小熊模板，並
作為獨立 fenced `text` code block 輸出；不得把卡片放入 bullet、引用或普通段落。

不得回退為 `v1`，也不得用網路、Git tag、GitHub Release、`skills` CLI lock
metadata 或其他外部狀態猜版本。`CER Core v1` 只表示工作流世代。每次 release
或 upgrade 必須先更新 `VERSION`；更新整個 Skill 後，下一張卡自然讀到新版本。

## 操作指令

CER v1 接受自然語言和 slash command 兩種入口。slash command 是穩定文字別名，
方便在 AI terminal、snippet、Snap 或可搜尋指令面板中保存；平台不支援時，直
接貼上同一句仍有效。

| 指令 | 自然語言 | 效果 |
|---|---|---|
| `/CER-auto <任務、限制、優先序>` | `CER 自適應：...` | 只在本地使用者 task 先選 ordinary execution、Goal、CER 工作法或 blocked；路線裁決前不成立 C；選到 CER 工作法才進完整 C／E／R，R 按風險決定。Remote 首版不支援。 |
| `/CER-start <任務、限制、優先序>` | `CER 啟動：...`／`CER 開始：...`／`CER 開工：...` | 啟動 CER v1；由本地使用者 task 成為 C，或由明確指定的 Remote 接收 task 在 `C_READY` 閉環成立後成為該 target_root 的唯一 C。單獨 `開工` 不啟動 CER。 |
| `/CER-stop` | `停止 CER，改用單 thread 繼續。` | 停用 CER mode，不再派新 E1／R；若 E1 已在寫入，先要求 E1 停止或回傳可判定狀態。 |
| `/CER-close` | `CER 收工。`／`CER 關閉。`／`關閉 CER。` | 完成 CER 收尾；同一 E1 只按既有真源回寫必要狀態並標 writer closed。單獨 `收工` 不觸發 CER close。 |
| `/CER-status` | `顯示 CER 狀態。` | 報告 C 已知的目標、C／E1／R 座標、下一停點和阻礙；不得為狀態而輪詢。 |
| `/CER-help` | `顯示 CER 指令。` | 顯示可用指令、自然語言等價句與 `/CER-auto` 任務寫法。 |

## 執行強度閘門

<!-- cer-execution-profile-gate-owner -->
本節是 `/CER-auto` 的唯一 runtime owner；不得另建 profile 文件、角色、registry 或固定表格。首版只支援本地使用者 task；Remote `/CER-auto` 未支援，必須停止而不能猜測接收 C。入口 task 在路線裁決前不是 C。`CER 工作法` 是進入現行 CER startup 的完整協作路線，不代表繞過 C 或變成只派 E1 的捷徑；C／E1 在 CER 啟動成功後成立，R 仍由既有 Reviewer owner 按風險決定。明示 `/CER-start` 的語義保持不變，仍直接進入完整 CER，直至使用者 stop、close 或依既有規則交接。

收到 `/CER-auto` 時，先只讀本節及裁決所需的使用者要求與目標專案真源，以最低足夠協作強度選 ordinary execution、Goal、CER 工作法或 blocked，並只輸出一行：`路線：ordinary execution — <理由>`、`路線：Goal — <清楚終點與驗證 loop>`、`路線：CER 工作法 — <需要 CER 的原因與停點>` 或 `路線：blocked — <缺少的權威／安全／驗收條件>`。本節與裁決真源路徑已知、同一讀取邊界安全且沒有權限或範圍差異時，必須在同一次有界讀取中取得，不得只為 selector 另開讀取往返；安全或邊界不同時仍分開，不能為省時越權或擴讀。ordinary execution 不啟動 CER、不自稱 C／E／R、不顯示小熊卡，並停止載入其他 CER references；它依目標專案既有單 thread 或普通 subagent 規則執行，普通 subagent 不得冒充正式 E／R。Goal 路線使用目前 runtime 可用的 Goal 能力承擔長任務推進和驗證 loop，但 Goal 不提供 CER 的唯一 writer、C／E／R 身份或 authority owner，也不載入其他 CER references。選 CER 工作法時才在需要 CER 的停點完整讀取本檔及 `roadmap.md`，通過現行 `/CER-start` 的唯一 C、startup 及 preflight 閘門；成功後照常顯示啟動卡。blocked 路線只報缺口與下一個可解除條件，不用流程完成冒充成果完成。

路線按下一步的後果、不確定性、可回復性及 owner 清晰度裁決，不按字數、檔案數、長任務標籤、source count、schema、hash、receipt 或 token 壓力單獨升降；source count、schema、hash 或 receipt 都不能代替 authority evidence。權威清楚、單一 writer、改動可回復、沒有外部副作用且既有驗收足以裁決時，可選 ordinary execution。任務較長、多步或需要閉環推進，但終點、驗證 loop、可停止條件和已知權威來源清楚，而且本步尚未要求把成果採納為正式資料、模型輸入、報告、decision gate、handoff truth、release／readiness claim 或 public／external claim 時，可選 Goal；若終點或來源仍模糊，先 ordinary diagnostic／收窄或 blocked，不直接進 Goal。當 Goal 或 E1 產物準備被接受為 formal data、model input、report paragraph、decision gate、handoff truth、release／readiness claim、public／external claim，或造成外部／不可逆／權限／付費後果時，選 CER 工作法，只在該採用停點由既有 CER runtime owner 承擔正式採用裁決。缺少權威來源、安全邊界、驗收條件、root／permission、Goal 能力且無安全 fallback、可回復性，或外部／不可逆操作未獲授權時，選 blocked。若既有 owner 已明確裁定目標狀態，剩下只是在同一 workspace 由單一 writer 作本地、可回復的 metadata 對帳，沒有正式採用裁決、模型重算或外部後果，而且直接讀回足以反證，則不因觸及持久狀態而自動選 CER 工作法；owner、artifact 角色、accepted outcome 或外部後果仍有爭議時，仍選 CER 工作法或 blocked。成本永遠不能繞過安全、權威、持久化、外部授權、Reviewer 或目標 release owner。

只在四個實質邊界重判：使用者要求、權威或後果改變；階段邊界；result disposition 改變承接、進度或權威效力；外部、公開、不可逆或其他高後果操作前。不得在每個小步重判；token 壓力本身不是升降理由。R 是否建立仍由既有 Reviewer owner 按風險決定，release assurance 仍由目標專案既有 release owner 決定；本路由不得固定建立、固定省略或取代兩者，也不得把 Goal 當成 Reviewer、release owner 或正式採用 owner。

只有由 `/CER-auto` 進入的執行可自動在 ordinary execution、Goal 與 CER 工作法之間轉換。從已啟動的 CER 降回 ordinary execution 或 Goal 前，必須證明沒有 active batch，E1 已停止寫入，結果已讀回並完成 result disposition，必要持久化已回寫讀回，而且沒有 truth conflict；這是路線轉換，不是 `/CER-stop` 或 `/CER-close`，不顯示停用或收尾卡。ordinary execution 或 Goal 升到 CER 工作法前，ordinary／Goal writer 必須先停止並讀回；其草稿、診斷、Goal 輸出或普通 subagent 輸出預設只作 working material，除非目標專案既有 owner 已明確接納為權威。CER startup 成立後，E1 在首次寫入前重讀 workspace baseline。

只有轉換會跨 task、session 或 context，或會承接實質 artifact、裁決或風險時，才保存一個短、非權威的 route-transition checkpoint；同一 task 且沒有實質承接可省略。它寫入目標專案既有 handoff／current-state owner 或下一個自足派工，不建新檔、schema、YAML 或 registry，只保留轉換方向與原因、目前目標和 outcome owner、未完成條件與下一個可觀察差異、最新 result disposition、accepted facts 與 working material／禁止承接、writer／持久化／baseline 讀回，以及 open risk 與下一個允許動作。檢查點不得改寫任何 owner；必要讀回缺失或互相矛盾時，下一次寫入或派工保持 blocked。

## Controller preflight

在建立本輪 E1、復用同輪既有 E1，或派任何實際 E1／R 批次前，C 先完成適應式任務契約。它不是表格儀式；簡單低風險且終點唯一的任務可只在內部完成並以短摘要直接工作。長期、多批，或新產品、流程、設計、內容、體驗型成果，C 維護一份活的任務簡報，並把必要答案濃縮進首次公開對齊的初始路線圖與自足派工。活的任務簡報不是新 workflow，也不建立固定項目文件；它只是 C 在本輪 CER 內用來承載目前已裁決任務狀態的工作面。

通用任務前檢／層級對焦的唯一全域 owner 不在 CER Skill；本節只作 CER-specific mapping，不重定義該八項。C 將通用 `對準`／`失焦`／`受阻` 判斷映射到本節的 `已確認`、`可安全推定`、`關鍵缺失` 與 blocked 停點。複雜 ordinary／Goal／CER 工作法任務不得只因 route label 跳過必要層級對焦；簡單、單步、低風險且終點唯一的任務仍可內部通過，不強制顯示對焦卡。可見對焦卡、preflight、活的任務簡報或路線圖更新不計作成果進度、驗收證據或產品品質證明，也不改變 `/CER-auto` 四路線、不新增 CER role、schema、enum 或 slash command。

C 只判斷五項，每項標成 `已確認`、`可安全推定` 或 `關鍵缺失`：

- 終點：可觀察終點是甚麼，哪些明確不做。
- 真源：完成判斷前必讀甚麼，已讀甚麼，仍有哪些關鍵未知。
- 根因與邊界：為何需要 CER；最小可驗收 E1 批次是甚麼。
- 權限與停點：哪些由 AI 自行處理，是否需要首次公開對齊，以及哪些真正需要使用者裁決或停止。
- 驗收與比例：甚麼證據可推翻方案；驗收是否剛好足夠，是否已變成防禦性擴建。

三態判定必須有證據邊界。`已確認` 只可來自使用者明示或已讀權威真源，C 必須能指出來源錨點；沒有來源的推測不得標成 `已確認`。`可安全推定` 必須通過反事實測試：若相反假設成立，仍不會實質改變交付物、使用流程、協作方式、資料處理、權限／風險或驗收，也不會造成重大重做，才可通過；若多個合理答案會導致實質不同成果，該項就是 `關鍵缺失`。

<!-- cer-truth-source-intake-gate-owner -->
真源攝取門檻屬於 Controller preflight 的唯一 owner，不另建文件、角色或固定表格。對任何會實質影響本批成果、權限、驗收、owner 或受保護語意的完成條件，C 在派正式實作批次前必須能回答四項：誰擁有；誰實際使用；如何生效；甚麼反例能推翻。`誰擁有` 指使用者裁決、專案真源、規則、檔案或外部權威的來源錨點。`誰實際使用` 指 E1、R、交付物、安裝面、公開面、後續批次或使用者流程如何消費該條件。`如何生效` 指它如何改變本批派工、交付內容、權限、驗收或成果判定。`甚麼反例能推翻` 指哪個讀回、測試、Reviewer 問題或反例會令本批不能算成功。任一項答不到，或答案依賴未讀的必要真源，該條件就是 `關鍵缺失`；C 不得派正式實作批次，只能做必要唯讀診斷、收窄驗收範圍，或用 `🟡 使用者裁決` 停問。簡單、單步、低風險且終點唯一的任務可在 C 內部輕量通過，但前提是缺省答案不會實質改變結果；不得把此門檻擴成預設全文讀取、全 repo 審查或固定 Full Audit。

對需要首次公開對齊或中途收斂的任務，活的任務簡報至少列明：已確認要求／排除、可安全推定、關鍵缺口、最新使用者回饋、本批凍結、下一個可觀察預覽或裁決點、與上一版相比改變了甚麼。C 只凍結下一個可安全執行批次；後續方向可保持暫定，待使用者看到中間成果、補資料或 R 提出反證後再更新。使用者回饋、真源讀回或 R 證據改變方向／範圍／交付形狀／驗收時，C 先更新活的任務簡報和路線圖差異，再派下一批；若已派出的批次受影響，按批次去重規則用新的 `batchId`／`payloadDigest` 重凍結或先 supersede 舊批次。

派工前，C 做一次短 QC：逐項核對 `已確認` 是否有來源、`可安全推定` 的反事實結果是否成立，以及本批凍結沒有把推測升格為 `已確認`。QC 失敗時，C 不得建立／復用 E1，也不得派實際批次；只能先做必要唯讀調查，或用 `🟡 使用者裁決` 最多問三個會實質改變結果的問題。

`關鍵缺失` 代表 C 不能安全判斷或派工。此時 C 只可先做必要唯讀調查；若仍缺少會實質改變結果的資訊，用 `🟡 使用者裁決` 最多問三個問題。preflight 通過後，C 才做通訊座標與 ready 驗證。E1／R 派工使用最新活的任務簡報與本批凍結，只能回報矛盾、阻礙或候選修正，不能自行擴大目標、真源、權限或驗收。

驗收有效性與比例原則在 C 每次作成或沿用驗收、修補或發布結論前都再次套用，不是預設重跑驗證。
C 先指出具體結論、支撐該結論的證據及其前提。既有證據只在被驗對象、需求、
直接支撐結論的依賴與環境前提、交付物與驗證方法仍適用或已驗證等效，且沒有可信反證時可保留；
全新脈絡不能假定不可讀的舊證據仍有效。任一前提失效時，只為受影響結論重建最小充分證據；
只有可追溯的前提到結論因果鏈、跨表面耦合、累積互動、
source／package mismatch 或發布／安裝產物不一致，或可信理由顯示舊驗證假綠，才擴大
範圍。廣度跟因果覆蓋走，深度跟失敗後果與證據不確定性走；任務標籤、檔案數、改動
大小或 `high risk` 字眼本身，都不能擴大或縮小驗收。此規則只在證據已知後界定範圍；
不取代用針對性檢查發現不穩定外部聲稱，或驗證真實發布／安裝產物。

## 成果錨定與進展閘

長期、多批或容易返工的 CER 任務，C 在首次實際派工前固定一個不可由後續批次自行改寫的 `outcome_anchor`。它只保存使用者要求與已讀專案真源的座標，不解釋或重寫專業內容，至少包含：使用者最終要取得的可驗收成果、完成條件的權威來源指向、不可接受的替代成果，以及明示排除範圍。使用者明確改目標、權威真源改變，或 C 用停點取得必要裁決後，才可建立新的錨；新錨必須列明與前一錨的差異。E1、R 或相鄰機制工作不得自行改寫 `outcome_anchor`。

C 將本輪工作線分類為 `mainline_outcome`、`diagnostic`、`mechanism_improvement` 或 `governance_self_improvement`。只有 `mainline_outcome` 可以增加主線進度；診斷可為下一批提供必要條件，但不計作成果；通用機制或治理自我改善必須證明是解除原成果阻礙的最小必要手段，否則另列，不阻塞主線。

每個非純探索的正式批次在派出前，C 必須能回答：本批改善哪一項未完成條件；成功後可讀回的前後差異是甚麼；依賴、權威來源與承接路徑是否存在；若成功仍不改善 `outcome_anchor`，為何仍是解除阻礙的必要條件。預期成果改善為零且不是必要條件的實作批次不得派出；只產生診斷、證據、候選、設計或審閱的批次必須標為非主線進度。

活動不等於成果。候選建立、審閱完成、格式或結構通過、檔案一致、問題已記錄、設計已完成、版本改名或包裝更新，都不自動增加主線進度。只有 C 讀回並裁決某項使用者完成條件取得已接納差異時，才可回報為成果進展；最終回報優先列已接納成果，而不是批次、任務或審閱數量。

<!-- cer-result-disposition-gate-owner -->
結果處置門檻屬於本節唯一 owner。C 在接納候選、報告進度、更新目標專案真源，或把上一批結果交給下一批使用前，必須明示本次裁決的效果；低風險小批可用一句短摘要，高風險或多批承接須可讀回：`accepted_as` 為 `evidence_only`、`working_candidate`、`terminal_deliverable` 或 `authoritative_input`；`authority_effect` 為 `none` 或 `existing_authority_updated`；`progress_effect` 為 `none` 或 `accepted_outcome_delta`；以及 `permitted_next_use`、`forbidden_next_use`、`unmet_conditions`、`persistence_readback`、是否需要目標專案既有持久化。`permitted_next_use` 是唯一下一步允許用途欄位，不另建 `next_allowed_use` 平行詞。上一批承接另須把 `prior_result_use` 明確標為 `working_material` 或 `authority_input`；若標為 `authority_input`，必須列出 `promotion_evidence` 與 `project_owner_anchor`。裸 `RESULT_ACCEPTED` 只表示 C 已完成該批次裁決及通訊去重，不代表全域正式採用、主線成果進度或下一批可作權威輸入。

上述 `accepted_as`、`authority_effect`、`progress_effect` 及 `prior_result_use` 均為封閉詞彙。階段、用途或承接範圍只寫入目標專案既有 `phase`／`status`、`permitted_next_use` 或 `forbidden_next_use`，不得合成近義詞或加後綴的新值；適當 writer 持久化前必須按本節合法值驗證，任何規格外值均保持 persistence、next dispatch 及 progress claim blocked。

候選、草稿、診斷、衍生輸出及純審閱結果預設只可作 `working_material`。要採納為 `authoritative_input`，C 必須有使用者明示或已讀目標專案既有 owner 的來源錨點、採納依據及讀回證據；找不到時，下一批停在 `dispatch_blocked`。Reviewer verdict 被 C 用作裁決依據時，須按 `content_verdict`、`implementation_verdict`、`outcome_verdict`、`authority_promotion_verdict` 分層；內容或技術 PASS 不會自動形成 outcome PASS、authority promotion PASS 或主線進度；R 未審的維度只能標為 `not_reviewed`／`out_of_scope`，`out_of_scope` 不是 PASS，C 不得擴大 R 原本審閱範圍。只有 `outcome_anchor` 本身要求草稿、候選或樣稿作終點時，`working_candidate` 才可成為合法 `terminal_deliverable`；這仍不等於更新權威來源。

若結果會改變當前階段、artifact 角色、下一產品路線、權威來源、progress claim 或後續批次輸入，C 必須先按目標專案既有持久化規則由適當 writer 完成回寫並讀回。`persistence_readback` 缺失、只說已保存但無 owner 讀回，或 `unmet_conditions` 尚未清零時，下一批只能消費為 `working_material`、診斷證據或保持 blocked，不得轉成 `authority_input`。持久真源互相矛盾、尚未同步或 artifact 角色未能判定時，`next_dispatch` 必須是 `blocked`；即使沒有下一批，C 亦不得把結果接納為 `terminal_deliverable`、報告進度或宣稱完成。同一終點集合包含多個 artifact 時，C 還須讀回每個被列為 `terminal_deliverable` 的最終狀態聲稱；若其中任何 artifact 仍寫着未接納、持久化待完成、舊階段或舊下一步，整組仍屬矛盾，該 artifact 必須降為 `evidence_only`／排除，或按原驗收修正並重驗，之後才可終端接納。CER 不指定固定 handoff、docs、registry 或資料庫，只要求目標專案 owner 的同步終態可讀回。

長期、多批、高風險或非簡單正式 CER 批次在關閉、接納為終端成果或交給下一批前，C 必須在本結果處置門檻內讀回一個 compact delegation close bundle；這不是新 runtime owner、新 public command、KDL dependency 或平行 result-disposition schema，普通 ordinary execution、Goal 草稿和低風險小批不強制使用。bundle 可用短摘要或結構化摘要，但必須把既有 `messageId`、`batchId`、`batchSeq`、`payloadDigest`、assignee／return target、工具 schema／receipt 明示需要或提供的 hostId、`pre_dispatch_evidence`／`outcome_anchor` 指向、本批未完成條件、成功後可讀回成果差異、已凍結驗收、明示排除的非主線項、有限 repair budget、`delivery_state`、結果候選狀態、`acceptance_blockers`、`worker_regressions`、`adjacent_backlog`、`scope_change_requests`、本節 result disposition 效果及下一步裁決放在同一收口讀回。dispatch、result、ack 身份或 digest 不一致，或 `delivery_state` 仍是 `delivery_unknown`／`not_delivered` 時，不得接納結果、報告成果進度或派下一批。`acceptance_blockers` 和 `worker_regressions` 才可在 repair budget 未耗盡時導致有界修補；ack 不得重置 attempt 或調高 max_attempts。`adjacent_backlog` 只可另列，不能單獨造成主線修補；`scope_change_requests` 只能 blocked 或停問使用者重定終點，不能包裝成 bounded repair。`next_dispatch=close` 時不得殘留 acceptance blocker、worker regression、必需持久化缺失或未清零 `unmet_conditions`；validator 或 closure PASS 只證明協調閉環一致，不等於 outcome PASS、authority PASS、release-readiness、npm readiness 或 token-saving claim。

<!-- cer-controller-drift-checkpoint-owner -->
長期任務防失焦檢查點屬於本節唯一 owner，不另建監察角色、背景程序或固定表格。長期、多批或容易受上下文污染的任務，在 resume／上下文轉換、連續兩批沒有已接納成果差異、同類失敗第二次、E1／R 提出相鄰改向或替代交付、使用者改方向或補限制，以及 close／release／重大交付前，C 做一次有界 drift checkpoint：下一批是否仍改善 `outcome_anchor` 的未完成條件；成功後有甚麼可讀回成果差異；E1／R 或相鄰改善是否正在取代主線成果。任一項答不到，C 不得派正式實作批次，只可改做診斷、收窄驗收、停問使用者、終止路線，或在 C 不能可靠反證且風險足夠時建立 fresh R。checkpoint、活的任務簡報或路線圖更新不計作成果進度；不得觸發背景 monitoring、polling、自動 `wait_threads`、固定 R、固定 Full Audit，或套用到簡單、單步、低風險且終點唯一的任務。

同一失敗類別按共同根因、使用者後果、受影響完成條件和方法判定；改名、換版本、換包裝、調整措辭或重派相同修法，不會變成新類別。同一類別連續兩次未解決後，C 不得派第三個同類修正版或同方法重試。C 必須回到根因分析，改用實質不同方法、縮窄 validator 聲稱、停問使用者，或終止該路線。

## 工具結果不明、角色對帳與批次去重

本節適用於有副作用的 task/thread 建立，以及 ready、accept、stop、正式派工、
批次狀態、結果與接納等控制訊息。C 對每次操作只使用
`confirmed`、`pending`、`outcome_unknown`、`duplicate`、`blocked` 五種狀態；
工具回報失敗、逾時、部分結果或非權威別名時，不得直接判定操作沒有發生。
每條控制訊息另以 `delivery_state` 記錄送達狀態，只用 `confirmed_delivered`、`not_delivered`、`delivery_unknown` 三值；它不取代操作狀態，只回答該訊息是否到達指定目標。`confirmed_delivered` 需要 target direct-push ack、target 開始新 turn、target 成為該 `batchId`／`payloadDigest` 的 active assignee，或工具提供綁定 exact `messageId`／`batchId`／`payloadDigest` 的權威 delivery receipt。send 返回 success、title 變化、thread id 存在或 sender 自稱已送出都不足夠；官方 failure、錯目標或 batchId／payloadDigest 不匹配才可標 `not_delivered`，其餘不明一律 `delivery_unknown`。

- 建立角色前，C 先對本輪實際參與 host、project、target root、cycle 與 role
  做一次有界建立前快照。快照只供本次對帳，不得演變成 lock、central registry
  或 CER run ID。
- 只有官方 receipt 或權威讀回給出當前工具 schema 所需的實際座標、project
  與 target root，建立才是 `confirmed`。這通常至少包括 threadId；hostId 只在
  當前工具 schema 或 receipt 明示需要／提供時使用。只有 `clientThreadId`、逾時、錯誤或
  部分結果時，操作是 `pending` 或 `outcome_unknown`，不是確定失敗。
- `outcome_unknown` 禁止自動重試。C 只做一次有界控制面對帳：比較建立前快照，
  在全部實際參與 host 的官方 task/thread 列表中，以 project、target root、
  cycle、role 及建立意圖匹配候選。一次對帳可包含平台已知 settle interval
  前後兩次權威快照；這是故障恢復，不是輪詢工作結果。
- 穩定期後零個候選仍只可把建立操作標成 `blocked`，不得自動再建立；其
  pending operation 必須在任何後續 resume、startup 或新建同 role 前先重做
  一次權威對帳，以捕捉延遲出現的孤立 task。一個候選須再以官方 metadata
  及零寫入 `ready` 確認；多於一個候選即 `duplicate`。
- 路由座標以 C 按當前工具 schema 讀回的官方 threadId 及 receipt 明示必需座標
  為準。不得硬性要求 hostId；不得由 task 自報的 `local`、顯示別名、title、
  sessionId、threadId 形狀或錯誤訊息推導 hostId。`ready` 仍須自報角色、target root
  及回傳目標；與官方 metadata 不一致時先對帳，不派正式工作。
- 發現重複角色時，所有候選保持零寫入。只有全部候選都證明未收到正式工作且
  零寫入，C 才可選定一個；其餘候選收到 `STOP_ZERO_WRITE` 後，須以 direct-push
  停止確認或官方可讀的不可工作終態證明停止。封存狀態、標題或發出停止訊息
  本身都不是停止證據；無法取得任一停止證據即 `blocked`，不得以可用性理由放寬。
- 任一重複 E1／E2 可能已收到正式工作或寫入時，C 停止所有新派工，讀回 writer
  與 workspace 狀態。先以穩定 `messageId` 向全部可能 writer 發停止指令，再以
  direct-push 或官方終態讀回證明全部已停止；接着判定已寫表面、候選成果及
  workspace 一致性。只有狀態可判定後，C 才可選定其中一名恢復，或在全部舊 writer
  已停止後依既有接管規則建立 E2；不得自動回滾或簡單選一個繼續。
- 每個正式批次使用本輪唯一且穩定的 `batchId`，綁定 cycle、角色、C 選定的
  threadId 或平台等價座標、當前工具 schema／receipt 明示必需的路由座標、
  target root、該接收者本輪單調遞增的 `batchSeq`
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
- `messageId` 只是 CER 訊息層的識別、去重及追蹤欄位，不是 Codex 執行指令、App Server
  `method`、JSON-RPC request `id`、`threadId`、`sessionId`、idempotency key 或授權。
  未經實際工具呼叫及工具結果／可核實送達證據，單獨把它寫入 prompt、派工包、摘要、
  自稱回執或一般 workspace 文字，不會建立 thread、開始 turn、呼叫工具、觸發寫入或
  授予角色權限；只有 `messageId` 不算訊息已送達或工作已執行。
- 任一控制或結果 send 為 `outcome_unknown` 時禁止盲目重發。先以 operation receipt、
  已收到的對應確認，或一次有界目的地／thread 讀回尋找相同 `messageId`；仍無法
  證明時，只有接收者身份仍唯一且具訊息去重，才可用相同 `messageId` 及完全相同
  內容受控重送一次，否則 `blocked`。故障恢復讀回是「不監察」規則的有界例外。
  此例外同時覆蓋送達段的「收到 push 後才讀回」及啟動段禁止以事後 read 冒充
  通訊驗證的限制，但只可證明該 `messageId` 的送達；它不能單獨證明整條 ready／
  accept 通訊鏈成立。
- `delivery_unknown` 只可按本節做一次有界讀回和同 `messageId` 受控重送；仍未知時保持 `pending`／`blocked`，不得當成已收到、已開始、已接納或可派下一批。
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
5. Remote 接收 task 收到明確 Remote CER 啟動語意後，先 direct-push candidate `C_READY`，必含自身 threadId 或平台等價座標、target_root、return target／path，以及當前工具 schema／receipt 明示必需的回傳或路由座標；不得猜 hostId。發送方完成唯一性核實並實際讀回 `C_READY` 後，必須以同一可用回傳路徑向接收者發 `C_ACCEPTED`；接收者收到 `C_ACCEPTED` 後才成為 active C 並做 Controller preflight。只發送 `C_READY`、未讀回 `C_READY` 或未收到 `C_ACCEPTED`，Remote C 身份及通訊路徑都不成立。若發送方原本是 active C，須先完成 handoff／close 才可發 `C_ACCEPTED`。
6. 不得為唯一 C 新增 lock file、central registry、run ID、conflict engine、新角色或測試例外；唯一性只靠已存在真源、官方枚舉、明示座標與本輪實際回傳／讀回證據判定。
7. C 為每輪 CER-start 分配 project 內側欄辨識用短 cycle 編號。規則生效後的新 cycle 不得使用 `00`，必須用官方 project task/title 枚舉讀回既有數字 cycle 標籤，選下一個未使用正整數，至少兩位顯示為 `01`、`02`；超過 99 可自然擴展。不得新增 central registry、lock 或 run ID。`00` 只表示 cycle numbering 規則生效前已開始、無法可靠回推原 cycle number 的 legacy/migration cycle；它和其他 cycle 編號一樣只供顯示，不是 lock、run ID、唯一 C 證據或 thread 身份，完整 threadId 仍是權威。Codex title 工具可用時，不得用初始 prompt、模型自動生成 title 或首行 label 代替側欄 rename；`create_thread` receipt 後立即呼叫官方 title 工具（目前 Codex schema 為 `set_thread_title`）設定／改名，並用 `list_threads`、`read_thread` 或平台等價讀回確認。讀回前，C 不得把該角色的 `ready` 判為合格，也不得送正式批次。若新 cycle 無法可靠枚舉或設定 title，保留最短 role title 並報真實 `title sync warning`；不得顯示問號 cycle 標籤、不得猜測數字，也不得因顯示標籤失敗冒充 lifecycle 或 identity failure。C 命名或識別自身可見 task／thread 為 `🚀 C:01｜<極短任務名>`；平台不能改 title 時，在首則可見訊息或停點卡首行標示同等角色標籤。單獨 `C:` 不是合格 Controller title／label。
8. C 完成 Controller preflight，建立或更新活的任務簡報，並只凍結下一個可安全執行批次；若有 `關鍵缺失`，只做必要唯讀調查或停問，不建立／復用 E1，也不派實際批次。
9. Controller preflight 通過後，C 完成通訊 preflight：以可用工具證明本次實際採用的路徑可用，包括身份來源、目標 root、必要參數、發送路徑、接收者、可見標題或角色標籤、assignee 可取得的回傳來源、可核實 threadId 或平台等價座標，以及 C 的裁決點。sessionId 只在當前工具 schema／receipt 明示需要／提供時附帶記錄，不可代替 threadId 或推導 hostId。
10. 若官方 `create_thread` 新建 task 工具不可用，或無法讀回側欄可見 title、可核實 thread id 與正式回傳路徑，E／R 委派即阻塞；不得降級用 inline sub-agent、fork、delegate 或既有 task 冒充正式 E／R。
11. 新建 E1／R／E2 時，標題或首行標籤必須分別以 `E1:01｜<極短任務名>`、`R1:01｜<極短審閱名>`／`R2:01｜...`、`E2:01｜...` 格式開首，不加 `🚀`；角色序號在冒號前，cycle 編號在冒號後，避免把第二輪 E1 誤作 E2。同輪所有 C／E／R 使用相同 cycle 編號，下一輪使用新 cycle 編號；legacy/migration cycle 可用 `00`。每個派工包和 ready／結果回執都要包含發送者角色、接收者、回傳目標、threadId 或平台等價座標。
12. C 透過官方 `create_thread` 建立本輪全新持久 E1。E1 先零寫入 direct-push `ready`；C 必須實際收到含正確角色、cycle 編號、側欄可見標題／標籤、thread 座標和回傳目標的合格零寫入 `ready`。同一輪後續批次持續復用該同一 E1 且 E1 threadId 保持相同；完成上一輪 `/CER-close` 後的新一輪必須建立全新 E1、使用新 cycle 編號，所有 R 也必須 fresh；不得復用上一輪 closed C 的任何 E／R task 或座標。
13. 任一通訊 preflight 環節缺失，或 assignee 沒有實際 direct-push 合格零寫入 `ready`，C 只顯示開眼 `🔴 重大阻礙` 卡並停止；不得顯示成功啟動卡，也不得用 wait snapshot、完成狀態、commentary、輪詢、事後 read、文件審閱、fork 建立成功或單向 send 成功冒充通訊驗證。若平台不會自動喚醒 idle C，C 仍不得自行等待；狀態保持 `POST_DISPATCH_PARKED`／`delivery_incomplete`，直到 direct-push 成為主線輸入，或使用者明示要求一次性查證。
14. 到此才算成功接受 `CER-start`。C 的第一個使用者可見成功回執必須是 [roadmap.md](roadmap.md) 的固定開眼 `🔵 CER 已啟動` 卡；保留完整三行 ASCII 小熊，版本在第一行，狀態在第二行，第三行只保留小熊底線，並作為獨立 fenced `text` code block 輸出。單批與多批都相同；不得用閉眼卡或猜測版本。
15. 同一輪、同一 C、同一 E1、同一回傳目標、同一可核實座標的後續批次不重做握手；座標或回傳目標改變即重做 ready。
16. C 判定為長期、多階段、多批次，或需要首次公開對齊的任務時，在固定啟動卡後、第一批前依 [roadmap.md](roadmap.md) 顯示初始進度面。簡單單批且終點唯一的任務只顯示短摘要，不強制建立路線圖。
17. 只有固定啟動卡已顯示，且所需的初始路線圖或短摘要已補上後，C 才可派第一個實際批次。

若使用者沒有明示 CER，而工作只是低風險單一步驟，可按普通工作處理；一旦明示 CER，不能以「任務簡單」靜默取消角色拓撲。單獨 `開工` 屬於目標 workspace 既有治理，不是 CER trigger。

## 自足派工

每個 E1／R 實際批次只包含必要內容：

- 角色與單一目標；
- 目標 root；
- 必讀真源與已裁決背景；
- Controller preflight 已通過的真源攝取四問摘要：誰擁有、誰實際使用、如何生效、甚麼反例能推翻；
- `outcome_anchor`、本批工作線分類、目標完成條件及預期成果差異；
- 若本批使用上一批 E／R 結果，列明結果處置門檻已裁決的 `prior_result_use: working_material | authority_input`、可否只作工作材料；若是 `authority_input`，列出 `promotion_evidence`、`project_owner_anchor`、讀回證據及禁止用途；
- 允許及禁止範圍；
- 驗收與能推翻方案的反例；
- 停止條件；
- 本批穩定 `batchId`、單調遞增 `batchSeq`、不可變 `payloadDigest`，以及所綁定的 cycle、接收者 threadId 或平台等價座標、當前工具 schema／receipt 明示必需的路由座標與 target root；
- 活的任務簡報與本批凍結，以及任何 `已確認`、`可安全推定`、`關鍵缺失` 的處置、必要來源錨點和反事實結果；
- 回傳 C 的 direct-push 目標、threadId 或平台等價座標；sessionId 只在當前工具 schema／receipt 明示需要／提供時附帶記錄，不可代替 threadId 或推導 hostId；
- 本批需要的知識底座、來源座標、未知與禁止越界範圍；
- 短回報要求。

新建 E1／R 的 `create_thread` 初始 prompt 不等於正式批次。它只可承載零寫入
ready handshake：角色、cycle／title、target root、C 回傳目標、允許使用正式
task 訊息工具對該回傳目標 direct-push ready／blocker／結果、禁止
project／source-root 寫入及外部副作用、禁止開始實作，以及需要回報自身座標與來源
可用性。正式 direct-push 回傳通道是 CER 內部通訊，不屬於被禁止的
project／source-root 寫入或外部副作用；禁止的仍是未授權 project／source-root
寫入、public／global sync、commit、release、install、deploy、email、權限／付費
action 或其他對外狀態改變。若使用者或平台明示連這條內部回傳通道也不可用，或
派工包同時要求 direct-push 又禁止所有可執行該回傳的工具訊息，C 只能修正派工包
一次或停在 `delivery_unavailable`／`dispatch_blocked`，不得用 child final、
passive read 或使用者轉述補成 ready／result。不得在 create prompt 放入完整
source corpus、候選工作內容或正式批次 payload，也不得要求 E1／R 在 ready 前
處理內容；若已發生，C 必須把它視為 pre-batch payload leak／batch lifecycle
violation，停止或重凍結，不得把後續相同 digest 的 duplicate ack 當作正常高效
通訊。若 assignee 無法從已授權真源自行讀取大型輸入，C 只在正式
`sendable_packet` 發送一次；過長或跨風險邊界的輸入按語義／風險切成多個正式批次。若 assignee 可從已授權真源讀取，派工包優先給來源座標、digest、必要摘錄
與禁止越界範圍，不重貼整份 corpus。

長期、多批、高風險或非簡單正式實作批次的 `sendable_packet` 必須包含短小 `pre_dispatch_evidence`。它不是新真源、固定表格、背景監察或 Full Audit，只是把既有 Controller preflight、`outcome_anchor`／drift 判斷濃縮成 assignee 可讀回的派工前證據。內容至少列明：`outcome_anchor` 指向或摘要；本批改善的未完成條件與成功後可讀回成果差異；真源攝取四問摘要及來源錨點；已讀必要真源與仍缺真源的處置；本批工作線分類；若觸發 drift checkpoint，列其結論，否則說明未觸發理由。缺失、互相矛盾、依賴未讀必要真源，或只有「已判斷」但沒有可讀回摘要時，`sendable_packet` 不可送出，C 停在 `dispatch_blocked`。E1／R 收到缺少必要 `pre_dispatch_evidence` 的正式批次時，只可 direct-push 零寫入 blocker（例如 `BATCH_BLOCKED_MISSING_PRE_DISPATCH_EVIDENCE`）並停止，不得開始寫入、審閱或沿錯誤方向補完 C 的判斷。簡單、單步、低風險且終點唯一的任務可用短摘要通過，不強制大表格。

不得寫「見上文」或要求 assignee 自行重建 C 的上下文。高風險批次補足背景與反例；低風險小修改保持短，不套巨型表格。E1 只獲授權執行本批凍結內容，不得把暫定後續意向當成完整規格或自行補成後續批次。E1／R 發現活的任務簡報、本批凍結、`outcome_anchor` 與真源矛盾時，先回報 blocker 或候選修正，不自行改寫契約後繼續。R 依最新任務簡報、本批凍結、候選 identity 及 delivery evidence 驗收，並同時對照不可被批次改寫的 `outcome_anchor`；不按最初 prompt 或過期假設驗收。R 必須同時回答本批是否仍服務原始成果、是否產生可接納的成果差異、是否只是活動或返工，以及是否用另一種交付形式代替使用者原本要求；技術合格但沒有成果改善時，不得回報為一般成功進度。

派工包可在 C 內部暫為 `draft_packet`；但正式可送出的 `sendable_packet` 不得保留 `<...>` 佔位符。正式派工必須填入實際 `threadId` 或平台等價座標、`returnTarget`、`messageId`、`batchId`、`batchSeq`、`payloadDigest`，以及當前工具 schema／receipt 明示必需的路由座標。sessionId 不可代替 threadId 作正式派工座標。hostId 只在當前工具 schema 或 receipt 明示需要／提供時使用；不得把 hostId 寫成跨平台硬性必填，不得由 `local`、title、sessionId、threadId 形狀或錯誤訊息推導 hostId。`同一 E1`／`上述 E1`／`下一個序號` 等相對說法只可作草稿，正式派工必須換成可核實實值。R 派工必須填入實際 `candidateIdentity`、`candidateManifest` 及候選 delivery evidence；缺任一項即停在 `dispatch_blocked` 或 `decision_blocked`，不得自評為可送出或要求 E1／R 盲猜。

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
- `ready` 必須回傳自身角色、可見標題或首行標籤、threadId 或平台等價座標、收到的目標 root、回傳目標及是否具備必要來源。sessionId 只在當前工具 schema／receipt 明示需要／提供時附帶記錄，不可代替 threadId，也不可用來推導 hostId。所有訊息都帶穩定 `messageId`；`BATCH_RECEIVED` 還須回傳當前工具 schema／receipt 明示必需的路由座標及綁定核對結果。
- 完成、受阻或未完成時，先 direct-push 短結果給 C，再停止；結果回執帶 `messageId`、`batchId`、`payloadDigest` 及 threadId 或平台等價座標，避免 C 將另一個 task、另一批或另一修訂的結果誤接納。C 裁決後回 `RESULT_ACCEPTED`。
- 派下一批前，上一批結果必須同時有必要控制訊息的 `confirmed_delivered`、已解決 result disposition、以及明示下一批輸入是 `authority_input`、`working_material`、診斷證據或 clean baseline；缺任一項時不得派下一批，也不得建立平行 writer／reviewer 補償不明通訊。
- 相同 `batchId` 重複送達時，接收者依 `RECEIVED_ZERO_WRITE`、`IN_PROGRESS`、`RESULT_READY`、`RESULT_ACCEPTED` 或 `STATE_UNKNOWN` 恢復，不得盲目重做；相同身份但不同 digest 立即阻塞。
- 除非某參與者已觀察到明確 `outcome_unknown` 並依本節故障恢復規則讀取精確
  `messageId`，C 只有收到 push 後才做一次有界讀回及裁決。故障讀回只可核對
  該控制訊息是否送達或目標是否錯誤，不可擴成 waiting、polling、背景監聽或
  進度追蹤。
- C 派工、建 task 或送訊後立即進入 `POST_DISPATCH_PARKED`。在此狀態下，
  C 不得自動使用 `wait_threads`、`read_thread` 或平台等價工具作等待、喚醒、
  進度追蹤、commentary 讀取、final 讀取、狀態探測或結果發現。唯一可推進狀態
  的一般路線，是 assignee 的 direct-push 成為 C／主線的實際輸入，或工具回傳
  權威 delivery receipt。
- `POST_DISPATCH_PARKED` 只有兩個讀取例外：使用者在同一輪明示要求的一次性
  thread 查證；或 C 已收到 direct-push 後，為驗證或裁決作一次有界讀回。前者是
  使用者指示的診斷，不是自動協調或正式交付證據；後者不得擴成下一輪等待、
  polling 或 commentary 追蹤。
- 沒有 direct-push 時，wait snapshot、完成狀態、commentary、摘要、child final、
  task title、使用者轉述或被動讀取都不能把 `pending`／`delivery_incomplete`
  推進為 ready、done、PASS、RESULT_READY 或 RESULT_ACCEPTED，也不能觸發下一批。
- 同一邏輯訊息的受控重送不算新的正式 send；對帳後只可依本節允許的唯一一次同
  `messageId`、同內容重送。重送後 C 仍回到 `POST_DISPATCH_PARKED`，不得以
  額外控制訊息、改名、改 cycle label 或改包裝重開等待額度。
- 「不監察」禁止自動 waiting、反覆 waiting、polling、背景監聽、反覆狀態探測、
  把 wait snapshot 當成果，以及未收到 push 的被動 thread read；使用者明示的
  一次性查證或 push 後的一次核對 read 不在禁止範圍。
- 送達不可用只阻止委派；C 仍可做獲授權的唯讀研究、分析與裁決，但不能代替 E1 寫入。

## 執行閉環

1. C 依使用者任務、`outcome_anchor`、活的任務簡報、目前本批凍結，以及目標專案已確認的計劃／真源，給本輪同一 E1 一個批次。
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

3. C 讀回實際成果，先判定它是否改善 `outcome_anchor` 的未完成條件，再按風險自行裁決或用官方 `create_thread` 建立 fresh R。
4. R 只驗指定風險、整體成果仍然對齊原始成果及成品邏輯，不只驗格式。
<!-- cer-review-convergence -->
5. R 首次指出缺陷後，C 先按共同根因和使用者後果合併同類發現；只做一次有界唯讀影響檢查，找齊承載本輪合約的現行真源、交付面與檢查位置。
6. C 凍結本輪 `owner／affected surfaces／acceptance／counterexample family`，給同一 E1 一個批次修完整個受影響邊界。
7. 修後 R 只重驗凍結範圍。若出現不同根因、不同使用者後果或最新修補造成的新回歸，只有 C 可在歸因後重凍結並另派新批次；E1 不得自行擴大。
8. 換字、換句序或同義改寫仍屬同一問題；不得逐句追加規則或 validator pattern。若同一反例家族持續避過機械檢查，C 改變檢查方法或收窄 validator 聲稱能力。
9. 凍結反例通過、沒有實質新缺陷，且成果差異已讀回後，C 依結果處置門檻接納；只有此時才由 E1 更新目標專案既有的權威進度來源，沒有進度來源便不自行創造。
10. 必要狀態收斂後 C 停止；相鄰改善另列，不增加 Reviewer、治理層或全 repo 重審。每批終態只可為已接納成果、明確承接的必要條件、誠實阻塞並返回重新選路，或終止該路線；不得把「再做一個同類修正版」當成預設下一步。
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

- 角色、批次、R、停點、測試及同步動作只按本次風險和交付需要增加。同一目標下，C 只在新增 E／R 或任務支線是完成原始目標或處理已核實阻礙的最小必要手段時才派發；否則合併、停止或自行裁決。
- 能由 C 讀回和相稱測試可靠驗收的，不建立 R；能窄修的，不重審所有已接納部分。
- 已達需求、核心反例通過、必要風險清零後停止；相鄰改善另列，不自動擴張。
- 相鄰機制改善、治理自我改善或診斷失敗，不會自動阻塞原任務；只有它是 `outcome_anchor` 未完成條件的必要依賴，且缺失會令主線成果不可安全接納時，才成為主線 blocker。
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
- 本輪 R 的封存只屬成功收尾後的介面收納。只有已完成、已讀回、已由 C 裁決的
  R 任務可用官方封存工具收起；C 與 E1 預設保留可見。仍在工作、受阻、未回傳
  或未裁決的 R 不可封存。封存不是刪除，不改 threadId、內容或歷史，也不是停止、
  審閱或收尾證據。

使用者向 C 明示 `CER 收工`、`CER 關閉`、`關閉 CER` 或 `/CER-close` 時：

1. C 停止新派工，裁決可安全裁決的候選，整理已接納、未完成、風險、證據和下一步。
2. C 給同一 E1 一個自足收工批次。
3. E1 只按目標專案既有規則回寫必要進度／決策真源，標示 E1 已停止寫入，讀回後 direct-push；若沒有持久真源，只回報實際交付與 writer closed。
4. C 讀回實際交付、必要真源及 `writer closed` 後，先用官方 title 工具自動把本輪所有可核實 C／E／R title 的 cycle 編號後加 `✓`，例如 `🚀 C:01✓｜...`、`E1:01✓｜...`、`R1:01✓｜...`；legacy/migration `00` 同樣可改為 `00✓`。C 必須讀回 title。這是 CER-close 內建 display-only rename，不另問使用者；不改 threadId、內容或歷史。rename 部分或全部失敗不推翻已證明的 writer close，但必須如實報 `title sync warning` 與失敗座標，不得宣稱已改名。
5. 完成 writer close、必要讀回及可完成的 title sync／warning 後，若官方封存工具可用，C 封存本輪已完成、已讀回、已裁決的 R 任務；不得封存 C、E1、仍在工作、受阻、未回傳或未裁決的 R。封存失敗不推翻 writer close，但必須如實報封存提示與失敗座標。
6. 完成可做的 R 封存或封存提示後，才顯示 [roadmap.md](roadmap.md) 的固定閉眼 `🟢 CER 已收尾` 卡，使用本次讀到的 package 版本並保留 `writer closed`，再告知使用者結果、title sync warning 如有、R 封存結果，以及延續限制。若有 R 被封存，摘要必須用當前輸出語言明講「已封存本輪 <數量> 個審閱任務；這只是封存，不是刪除，仍可在已封存任務中找回。」閉眼卡只代表 writer close／必要讀回完成，不代表 title sync 或 R 封存全綠。沒有 writer closed 或必要讀回未完成時，只顯示開眼 `🔴 重大阻礙` 卡，不得顯示閉眼收尾卡，也不得封存 R 來製造乾淨狀態。
7. 成功收尾後，該輪 C／E／R task 整組轉為只讀歷史座標，不可接收同一 workspace 下一輪工作。下一輪須由新 task 重走唯一 C 閘門、建立全新 E1，且所有 R 都 fresh。

新 session 只可從實際存在的目標專案真源恢復；證據不足便標示 continuity limited。若無可核實 E1 座標，先證明原 writer 停止，再建立 E2。

## 停用 CER

使用者明示「停止 CER，改用單 thread 繼續」或 `/CER-stop` 時：

1. C 停止派發新 E1／R 批次。
2. 若沒有 active writer，C 以普通單 thread 繼續。
3. 若 E1 已開始寫入，C 先要求 E1 停止、回傳目前成果或 blocker，並標示是否 writer closed。
4. C 讀回沒有 active writer 或 writer 已停止的可判定狀態後，顯示 [roadmap.md](roadmap.md) 的固定閉眼 `⚪ CER 已停用` 卡，使用本次讀到的 package 版本並保留 `CER inactive`，才回到單 thread。
5. 不能證明 writer 停止或必要讀回未完成時，只顯示開眼 `🔴 重大阻礙` 卡，不得顯示閉眼停用卡，也不假設工作區安全。

`/CER-stop` 不等同 `/CER-close`。前者是停用 CER 協作拓撲；後者是完成 CER 收尾與必要持久化。單獨 `收工` 屬於目標 workspace 既有治理，不映射為 CER stop 或 close。
