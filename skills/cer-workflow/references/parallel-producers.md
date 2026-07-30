# 平行候選生產者

<!-- cer-parallel-producers-owner -->

本檔是 CER 平行候選生產者的唯一完整規則 owner。它規定 C 如何按需使用
inline、非正式能力，同時保持正式角色、唯一 writer、fresh Reviewer、來源裁決
及停止邊界不變。

## 目錄

- [定位與角色邊界](#定位與角色邊界)
- [使用者操作保持簡單](#使用者操作保持簡單)
- [啟動資格](#啟動資格)
- [Lane 凍結契約](#lane-凍結契約)
- [模式與寫入邊界](#模式與寫入邊界)
- [Scratch root 機械邊界](#scratch-root-機械邊界)
- [候選回傳](#候選回傳)
- [C 的讀回、裁決與合流](#c-的讀回裁決與合流)
- [失敗、漂移與生命週期](#失敗漂移與生命週期)
- [禁止事項](#禁止事項)

## 定位與角色邊界

- CER 正式角色只有 C、E1、R、E2。平行候選生產者不是第五角色，不使用正式
  title、cycle、ready、result、batch lifecycle 或 Reviewer 身份。
- 生產者是 C 的 inline、非正式、按需候選能力。不得新增 slash command、
  lock、registry、run id、常駐模式或背景服務。
- 生產者不代替 E1 寫入正式 project，不代替 R 獨立反證，也不直接與 E1、E2
  或 R 通訊。
- 正式 project writer 仍只有 E1。只有既有接管條件成立後，才可改由 E2；
  任何 producer、C 或 R 都不得成為平行 project writer。

## 使用者操作保持簡單

正常 CER 使用只保留既有明示觸發與五個操作指令。使用者無須設定 producer、
lane、scratch root、hash、角色或額外審閱程序，也無須學習「平行候選生產者」
詞彙。C 在內部判斷是否值得平行、分配及驗證隔離位置；不值得或不可證明安全時
自動使用零名 producer 並回到串行分析。對使用者只報告會影響結果的成果、未知、
阻礙或風險，不展示內部 lane 儀式。

## 啟動資格

C 只有在以下條件全部成立時，才可啟動兩條或以上的平行 lane：

1. 至少兩條工作線互不依賴，不需要彼此結果、共享可變狀態或固定執行次序。
2. 每條 lane 的輸入及來源身份已凍結。
3. C 同期有不重複的關鍵分析、守門或裁決工作，不退化為候選整理員。
4. 每條候選可由 C 按權威來源獨立驗證。
5. 預期淨省時明顯高於啟動、讀回、hash、去重及裁決成本。
6. 所需平行槽可用，且不會壓縮正式 E1 或 fresh R 的必要能力。

任一條不成立、不可判定，或一次有界讀取已足夠時，`producer_count=0`，C 串行
完成分析。這是正常 auto-idle，不是降級、錯誤或需要使用者設定的模式。

## Lane 凍結契約

C 在每條 lane 啟動前凍結以下完整內容：

- `lane_label`：只供本次候選辨識，不是正式角色或 run id。
- `mode`：只能是 `read_only` 或 `isolated_artifact`。
- 單一目標。
- 輸入身份與版本、來源身份及可核實座標。
- 允許範圍與禁止範圍。
- 預期候選輸出。
- 驗收方式。
- 停止條件。
- `isolated_artifact` 另須有 C 明確提供並已通過機械邊界檢查的 lane 專屬
  `scratch_root`。

未凍結、互相矛盾或中途被 producer 改寫的 lane 不啟動或立即失效。生產者不得
自行擴張目標、來源、權限、輸出或驗收。

## 模式與寫入邊界

### `read_only`

- 在任何位置都必須零寫入，包括 project、scratch、暫存、外部系統及 producer
  自己可見的 workspace。
- 只可讀取 C 指定的輸入與來源，並回傳文字候選。

### `isolated_artifact`

- 只可寫入 C 明確提供、lane 專屬、task-owned 的 `scratch_root`。
- 不得寫 target project、正式真源、另一 lane、使用者根目錄、系統位置、
  外部服務或任何未列目標。
- artifact 是候選，不是正式 project 成果。它只能由 C 讀回、重算 hash 及合流；
  不得由 producer 直接交給 E1 或 R 採用。

## Scratch root 機械邊界

C 必須在啟動 artifact lane 前解析實際絕對路徑，並逐項證明：

1. `scratch_root` 與 target project 互不包含，兩者都不是另一方的祖先。
2. `scratch_root` 不是磁碟根、使用者根、系統根或其等價高風險根。
3. 現存路徑鏈不含 symlink、junction、Windows reparse point、mount 或其他會把
   寫入導向未核實位置的連結。
4. 每條 lane root 彼此不相等、互不為祖先，且不與正式真源、其他 lane 或外部
   系統重疊。
5. 實際工具權限只容許該 lane 的明示 root；不能以相對路徑、萬用字元、環境
   fallback 或 producer 自選位置擴張。

任一項不能證明即不啟動該 lane。不得退回 project 內 staging、共享 scratch、
使用者根或其他較危險位置。

## 候選回傳

每條自然到達的候選至少包含：

- `lane_label`。
- 凍結的輸入身份。
- 實際來源座標。
- `claims`：可由來源逐項核實的候選主張。
- `unknowns`：缺失、矛盾、未核實或受限制部分。

`isolated_artifact` 另須列每個 artifact 的實際絕對路徑與 SHA-256。回傳不是正式
CER ready/result，不使用正式 batch 身份，也不構成接納、進度或 Reviewer 證據。

## C 的讀回、裁決與合流

- C 親自讀回支撐關鍵主張的來源與 artifact，不以 producer 摘要代替。
- C 對每個 artifact 重算 SHA-256，並核對路徑仍在已驗 scratch root、輸入身份
  未漂移、來源座標可重播。
- 來源或候選衝突時，C 按使用者裁決、專案真源及任務所需權威來源判斷；不得
  投票、按數量、完成先後或相同答案接納。
- C 只合流仍在本次 intake 邊界內、來源與 hash 未漂移、可獨立驗證的部分。
- 只有 C 完成讀回、去重、衝突裁決及合流後，才可形成給 E1 的正式自足 batch。
  E1 只接收該 C 合流批次，不得直接使用 producer 原始通訊、lane 摘要或未合流
  scratch artifact。
- R 仍從凍結原始證據獨立反證；producer 候選不能冒充 fresh R 證據。

## 失敗、漂移與生命週期

- C 不 wait、poll 或背景監察 producer，只採用自然到達且仍在 intake 邊界內的
  候選。
- 遲到候選在 intake 已關閉、正式 batch 已凍結、`CER-stop` 或 `CER-close`
  開始後失效；不得重開已裁決批次。
- 輸入或來源漂移時，只淘汰依賴該身份的 lane；未受影響 lane 不重跑。
- artifact 路徑越界、hash drift、tamper、來源不可重播或 lane 合約漂移時，該
  候選 fail closed 並不得合流。
- producer 建立失敗、沒有 subagent 能力、逾時、自然沒有回傳或候選不可驗證時，
  C 回到一般串行分析，不重複相同失敗。只有缺失證據本身是任務 blocker 時，
  CER 才因證據缺口受阻。
- `/CER-stop` 與 `/CER-close` 不等待 producer。C 停止採用新候選，讓遲到內容
  失效，並依正式 E1／R 生命週期完成停用或收尾。

## 禁止事項

- producer 冒充 C、E1、R、E2 或 fresh Reviewer。
- producer 使用正式 title、cycle、ready、result、slash、lock、registry 或
  run id。
- C、R 或 producer 寫入 target project；E1 以外出現共享 workspace writer。
- `read_only` 產生任何寫入。
- `isolated_artifact` 寫出已驗 lane root，或使用 project 內／祖先、磁碟根、
  使用者根、系統根、link、junction、reparse point、mount 或重疊 lane。
- producer 直接向 E1／E2／R 傳送候選，或 E1 採用未經 C 合流的 scratch。
- 以 producer 數量、票數、速度或一致答案代替 C 的權威來源裁決。
- 為了 producer 要求使用者設定 lane、scratch、hash、角色、審閱程序或新增指令。
- 為等候 producer 而輪詢、背景監察、延遲 stop／close，或採用已遲到、漂移、
  tamper、越界的候選。
